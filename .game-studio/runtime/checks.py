"""Deterministic observations and actual command receipts; no game verdicts."""
from datetime import datetime, timezone
import glob
import json
from pathlib import Path
import re
import subprocess
import time
from config import load, resolve
from paths import confined, digest, plain, relative_parts

NO_DATA = 'NOT ASSESSED — NO DATA'


def files(root, pattern):
    root = plain(root)
    static = []
    for part in relative_parts(pattern):
        if glob.has_magic(part):
            break
        static.append(part)
    confined(root, '/'.join(static) or '.')
    return sorted(plain(p) for p in Path(root).glob(pattern) if p.is_file())


def regex(pattern):
    for old, new in [('[:space:]', r'\s'), ('[:digit:]', '0-9'), ('[:alpha:]', 'a-zA-Z'), ('[:alnum:]', 'a-zA-Z0-9')]:
        pattern = pattern.replace(old, new)
    if '[[:' in pattern:
        raise ValueError(f'Unsupported POSIX class: {pattern}')
    return re.compile(pattern, re.M)


def artifact(root, spec):
    root = plain(root)
    if not spec or 'glob' not in spec and 'any_of' not in spec:
        return {'status': 'NO_CHECK', 'note': (spec or {}).get('note', '')}
    if 'any_of' in spec:
        candidates = [artifact(root, row) for row in spec['any_of']]
        return {'status': 'PRESENT' if any(r['status'] == 'PRESENT' for r in candidates) else 'ABSENT', 'alternatives': candidates}
    matched = files(root, spec['glob'])
    status = 'ABSENT' if not matched else 'SHORT' if len(matched) < spec.get('min_count', 1) else 'PRESENT'
    if status == 'PRESENT' and spec.get('pattern'):
        expression = regex(spec['pattern'])
        if not any(expression.search(p.read_text(encoding='utf-8-sig')) for p in matched):
            status = 'PATTERN_MISS'
    return {'status': status, 'matched': [p.relative_to(root).as_posix() for p in matched], 'count': len(matched)}


def artifacts(root, phase=None, path=None):
    root = plain(root)
    if phase and path:
        raise ValueError('--phase and --path are exclusive')
    catalog = load(confined(root, '.game-studio/resources/docs/workflow-catalog.yaml'))
    groups = catalog.get('paths' if path else 'phases')
    if not isinstance(groups, dict) or not groups:
        raise ValueError('Workflow catalog missing or empty')
    selected = path or phase
    if selected and selected not in groups:
        raise ValueError(f'Unknown catalog selection: {selected}')
    rows = []
    for group, content in groups.items():
        if selected and group != selected:
            continue
        for step in content.get('steps', []):
            rows.append({'group': group, 'step': step['id'], 'required': step.get('required', False),
                         'command': step.get('command'), **artifact(root, step.get('artifact'))})
    return {'steps': len(rows), 'groups': len({r['group'] for r in rows}), 'observations': rows,
            'note': 'Presence checks only. Apply workflow tier and actual quality evidence separately.'}


def stories(root):
    root = plain(root)
    rows = []
    for p in files(root, 'production/epics/**/story-*.md'):
        text = p.read_text(encoding='utf-8-sig')
        status = None
        for line in text.splitlines():
            line = re.sub(r'^\s*(?:>\s*)?(?:[-+]\s+)?', '', line).replace('*', '')
            match = re.match(r'(?i)^Status:\s*(.*)$', line)
            if match:
                status = match.group(1).strip()
                break
        categories = [('COMPLETE', r'(complete|done)(?![a-z])'), ('IN_REVIEW', r'in review(?![a-z])'),
                      ('IN_PROGRESS', r'in progress(?![a-z])'), ('TODO', r'(ready|not started)(?![a-z])'),
                      ('BLOCKED', r'blocked(?![a-z])')]
        category = next((key for key, expr in categories if status and re.match(expr, status, re.I)),
                        'NO_STATUS' if status is None else 'OTHER')
        rows.append({'path': p.relative_to(root).as_posix(), 'status': status if status is not None else 'UNKNOWN', 'category': category})
    order = {'IN_REVIEW': 0, 'IN_PROGRESS': 1, 'TODO': 2, 'BLOCKED': 3, 'OTHER': 4, 'NO_STATUS': 4, 'COMPLETE': 5}
    rows.sort(key=lambda row: (order[row['category']], row['path']))
    unfinished = [row for row in rows if row['category'] != 'COMPLETE']
    counts = {key: sum(row['category'] == key for row in rows) for key in order}
    candidate = next((row for row in unfinished if row['category'] in {'IN_REVIEW', 'IN_PROGRESS', 'TODO'}), None)
    if candidate:
        action = 'story-done' if candidate['category'] == 'IN_REVIEW' else 'dev-story'
        routing = {'action': action, 'skill': '$gs-' + action, 'path': candidate['path']}
    else:
        action = 'NO STORIES' if not rows else 'COMPLETE' if not unfinished else 'BLOCKED' if all(row['category'] == 'BLOCKED' for row in unfinished) else 'REVIEW STATUS'
        routing = {'action': action, 'path': None}
    return {'status': 'OBSERVED' if rows else NO_DATA, 'count': len(rows), 'complete': counts['COMPLETE'],
            'counts': counts, 'stories': rows, 'unfinished': unfinished, 'next': routing,
            'note': 'Status/routing observations; closure still requires applicable actual acceptance/review evidence.'}


def sections(text):
    result, current, chunks, counts = {}, '__preamble__', [], {}
    for line in text.splitlines(keepends=True):
        if line.startswith('## '):
            result[current] = digest(''.join(chunks).encode())
            heading = line[3:].strip()
            counts[heading] = counts.get(heading, 0) + 1
            current = heading + (f' #{counts[heading]}' if counts[heading] > 1 else '')
            chunks = []
        chunks.append(line)
    result[current] = digest(''.join(chunks).encode())
    return result


def receipts(root, action, patterns, receipt=None, report=None, optional_patterns=None):
    root = plain(root)
    if action not in {'hash', 'check', 'sections-hash', 'sections-check'}:
        raise ValueError('Unknown receipt action')
    if action.endswith('check') and optional_patterns is not None:
        raise ValueError('Checks inherit saved optional classification; generate a fresh reviewed snapshot to change it')
    old, observations, unresolved, baseline = {}, [], [], {}
    if action.endswith('check') and receipt:
        p = confined(root, receipt)
        if p.exists():
            data = json.loads(p.read_text(encoding='utf-8'))
            if not isinstance(data, dict) or data.get('algorithm') != 'sha256' or not isinstance(data.get('hashes'), dict):
                raise ValueError('Receipt must be native sha256 JSON; legacy stamps require a fresh review')
            if data.get('kind') not in {None, 'sections' if action.startswith('sections-') else 'files'}:
                raise ValueError('Receipt kind differs from the requested comparison')
            old = data['hashes']
            baseline = data
            for key, sha in old.items():
                confined(root, key.split('#', 1)[0] if action.startswith('sections-') else key)
                if not isinstance(sha, str) or len(sha) != 64:
                    raise ValueError('Invalid receipt hash')
    optional_patterns = baseline.get('optional_patterns', []) if optional_patterns is None else optional_patterns
    if not isinstance(optional_patterns, list) or not all(isinstance(p, str) and p in patterns for p in optional_patterns):
        raise ValueError('Optional patterns must be an explicit subset of reviewed patterns')
    optional_patterns = list(dict.fromkeys(optional_patterns))
    current = {}
    for pattern in patterns:
        matched = files(root, pattern)
        if not matched:
            unresolved.append(pattern)
        for p in matched:
            rel = p.relative_to(root).as_posix()
            if action.startswith('sections-'):
                if '#' in rel:
                    raise ValueError('Section receipts require paths without #; use whole-file receipts for this filename')
                current.update({rel + '#' + h: sha for h, sha in sections(p.read_text(encoding='utf-8-sig')).items()})
            else:
                current[rel] = digest(p.read_bytes())
    for key, sha in current.items():
        observations.append({'path': key, 'hash': sha, 'status': 'UNCHANGED' if old.get(key) == sha else 'CHANGED' if key in old else 'NEW'})
    if action.endswith('check'):
        for key in old:
            relative = key.split('#', 1)[0] if action.startswith('sections-') else key
            if key not in current and any(Path(relative).match(p) for p in patterns):
                observations.append({'path': key, 'status': 'REMOVED'})
    linked_report = report if action.endswith('hash') else baseline.get('report')
    report_hash, report_status = None, 'UNLINKED'
    if linked_report:
        path = confined(root, linked_report)
        if not path.is_file():
            if action.endswith('hash'):
                raise ValueError('Write the actual review report before generating its companion receipt')
            report_status = 'ABSENT'
        else:
            report_hash = digest(path.read_bytes())
            report_status = 'RECORDED' if action.endswith('hash') else 'UNCHANGED' if report_hash == baseline.get('report_hash') else 'CHANGED'
    return {'algorithm': 'sha256', 'kind': 'sections' if action.startswith('sections-') else 'files',
            'hashes': current, 'observations': observations, 'patterns': list(patterns),
            'unresolved': unresolved, 'previous_unresolved': baseline.get('unresolved', []),
            'optional_patterns': optional_patterns,
            'required_unresolved': [p for p in unresolved if p not in optional_patterns],
            'optional_unresolved': [p for p in unresolved if p in optional_patterns],
            'baseline_status': 'PRESENT' if baseline else 'MISSING',
            'report': linked_report, 'report_hash': report_hash, 'report_status': report_status,
            'unchanged_inputs': bool(baseline and current and current == old and unresolved == baseline.get('unresolved', [])
                                     and list(patterns) == baseline.get('patterns') and report_status == 'UNCHANGED'),
            'status': 'OBSERVED' if current else NO_DATA}


def dependencies(root):
    root = plain(root)
    adrs = files(root, 'docs/architecture/adr-*.md')
    lookup = {p.stem.lower(): p.relative_to(root).as_posix() for p in adrs}
    graph, missing, missing_sections = {}, [], []
    for p in adrs:
        rel = p.relative_to(root).as_posix()
        text = p.read_text(encoding='utf-8-sig')
        match = re.search(r'(?ims)^## ADR Dependencies\s*\n(.*?)(?=^## |\Z)', text)
        dependency_text = match.group(1) if match else ''
        depends_row = re.search(r'(?im)^.*\*\*Depends On\*\*.*$', dependency_text)
        if not dependency_text.strip() or re.search(r'\bUNKNOWN\b', dependency_text, re.I) or '|' in dependency_text and not depends_row:
            missing_sections.append(rel)
        if depends_row:
            dependency_text = depends_row.group()
        elif '|' in dependency_text:
            dependency_text = ''  # A table without Depends On is unknown, not all ADR references.
        names = re.findall(r'(?i)\badr-[\w-]+(?:\.md)?', dependency_text)
        graph[rel] = []
        for name in names:
            key = name.removesuffix('.md').lower()
            if key in lookup:
                graph[rel].append(lookup[key])
            else:
                missing.append({'from': rel, 'target': name})
    cycles, visited = [], set()

    def visit(node, active):
        if node in active:
            cycles.append(active[active.index(node):] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        for other in graph[node]:
            visit(other, active + [node])

    for node in graph:
        visit(node, [])
    pending = {node: len(set(edges)) for node, edges in graph.items()}
    order, ready = [], sorted(node for node, count in pending.items() if not count)
    while ready:
        node = ready.pop(0)
        order.append(node)
        for other, edges in graph.items():
            if node in edges:
                pending[other] -= 1
                if pending[other] == 0:
                    ready.append(other)
                    ready.sort()
    return {'status': 'OBSERVED' if adrs else NO_DATA, 'nodes': len(adrs), 'graph': graph, 'missing': missing, 'cycles': cycles,
            'missing_sections': missing_sections, 'order': order,
            'note': 'Order covers declared edges only. Missing/unknown declarations and absent targets are gaps, not a clean dependency verdict.'}


def gdd_structure(root, patterns):
    root = plain(root)
    rows = []
    for pattern in patterns:
        for p in files(root, pattern):
            headings = re.findall(r'(?m)^#{1,3}\s+(.+)', p.read_text(encoding='utf-8-sig'))
            expected = {'Overview': r'Overview', 'Player Fantasy': r'Player Fantasy', 'Detailed Rules': r'Detailed (Rules|Design)',
                        'Formulas': r'Formulas', 'Edge Cases': r'Edge Cases', 'Dependencies': r'Dependencies',
                        'Tuning Knobs': r'Tuning Knobs', 'Acceptance Criteria': r'Acceptance Criteria'}
            present = [name for name, expr in expected.items() if any(re.match(r'(?i)^(?:[0-9]+[.)]?\s*)?' + expr, h) for h in headings)]
            rows.append({'path': p.relative_to(root).as_posix(), 'headings': headings,
                         'present': present, 'absent': [name for name in expected if name not in present]})
    return {'status': 'OBSERVED' if rows else NO_DATA, 'count': len(rows), 'documents': rows,
            'note': 'Headings are observations. The authoring/review skill applies its tier contract.'}


def review_scope(root, receipt=None):
    root = plain(root)
    excluded = {'game-concept', 'systems-index', 'game-pillars', 'gameplay-tags', 'fixture-swap-ledger', 'entity-registry', 'sound-bible'}
    names = [p.relative_to(root).as_posix() for p in files(root, 'design/gdd/*.md')
             if p.stem not in excluded and not p.stem.startswith('gdd-cross-review-')]
    baseline_reason, observations = 'No native baseline', None
    if receipt and confined(root, receipt).is_file():
        try:
            baseline = json.loads(confined(root, receipt).read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            baseline = {}
        if isinstance(baseline, dict) and baseline.get('algorithm') == 'sha256' and baseline.get('kind') == 'files':
            patterns = baseline.get('patterns', [])
            if not isinstance(patterns, list) or not all(isinstance(p, str) for p in patterns):
                raise ValueError('Receipt patterns must be a list of strings')
            observations = receipts(root, 'check', list(dict.fromkeys([*patterns, 'design/gdd/*.md'])), receipt)
            baseline_reason = 'Linked report and context compared'
        else:
            baseline_reason = 'Legacy/non-native baseline; full scope'
    if observations:
        changed = [r['path'] for r in observations['observations'] if r['status'] != 'UNCHANGED'
                   and r['path'].startswith('design/gdd/')
                   and Path(r['path']).stem not in excluded and not Path(r['path']).stem.startswith('gdd-cross-review-')]
        context_changed = any(not r['path'].startswith('design/gdd/') or Path(r['path']).stem in excluded
                              for r in observations['observations'] if r['status'] != 'UNCHANGED')
        absent_inputs_changed = set(observations['unresolved']) != set(observations['previous_unresolved'])
        required_missing = bool(observations['required_unresolved'])
        full_scope = observations['report_status'] != 'UNCHANGED' or context_changed or absent_inputs_changed or required_missing
        if required_missing:
            baseline_reason = 'Required input unavailable; conservative full scope without invented document changes'
        elif full_scope:
            baseline_reason = 'Report/context or absent-input set changed; full scope without invented document changes'
        elif observations['unresolved']:
            baseline_reason = 'Linked report/context compared; unchanged absent inputs remain unknown'
    else:
        changed = names
        full_scope = True
    scoped = set(names) | set(changed) if full_scope else set(changed)
    queue = list(names)
    missing = [rel for rel in changed if rel not in names and rel.startswith('design/gdd/')]
    unresolved, graph = [], {}
    while queue:
        rel = queue.pop()
        p = confined(root, rel)
        if not p.is_file():
            missing.append(rel)
            continue
        text = p.read_text(encoding='utf-8-sig')
        regions = re.findall(r'(?ims)^#{1,3}\s+(?:[0-9]+[.)]?\s*)?(?:System )?Dependencies[^\n]*\n(.*?)(?=^#{1,3} |\Z)', text)
        regions += re.findall(r'(?im)^.*Key deps:\s*(.*)$', text)
        declared = '\n'.join(regions)
        found = set()
        for dep in names:
            stem = Path(dep).stem
            # Bare system names in the shipped quick-reference template, bullets,
            # table cells and Markdown links all identify the same known document.
            if re.search(r'(?<![\w-])' + re.escape(stem) + r'(?:\.md)?(?![\w-])', declared, re.I) or dep in text or re.search(r'\]\(' + re.escape(stem) + r'\.md\)', text, re.I):
                found.add(dep)
        for name in re.findall(r'(?<![\w/])([\w-]+\.md)\b', declared):
            dep = 'design/gdd/' + name
            if not any(Path(known).name.lower() == name.lower() for known in names):
                unresolved.append({'from': rel, 'dependency': name})
        if declared.strip() and not found and not re.fullmatch(r'(?is)[\s*|`-]*(none|n/a)[\s*|`-]*', declared.strip()):
            unresolved.append({'from': rel, 'dependency': 'Unparsed dependency declaration'})
        graph[rel] = found
    # A changed dependency affects both its dependants and its own dependencies.
    while True:
        previous = set(scoped)
        for rel, edges in graph.items():
            if rel in scoped or edges & scoped:
                scoped.add(rel)
                scoped.update(edges)
        if scoped == previous:
            break
    if unresolved:
        scoped.update(names)  # Unknown declarations cannot safely narrow review.
    return {'status': 'OBSERVED' if names else NO_DATA, 'baseline': receipt,
            'baseline_reason': baseline_reason, 'freshness': observations,
            'changed': sorted(changed), 'scope': sorted(rel for rel in scoped if rel.startswith('design/gdd/')), 'missing': sorted(set(missing)),
            'unresolved_dependencies': unresolved,
            'note': 'Without a native receipt, conservative full scope. Confirm declared dependencies in the review.'}


def coherence(root, probe=False):
    from engine import coherence as compare
    return compare(root, probe)


def run_command(root, name, timeout=300):
    root = plain(root)
    argv = resolve(root)['values'].get('commands.' + name)
    if argv is None:
        return {'command': name, 'status': NO_DATA, 'reason': 'No configured argv command'}
    if not isinstance(argv, list) or not argv or not all(isinstance(p, str) and p for p in argv):
        raise ValueError(f'commands.{name} must be a nonempty argv list; no shell strings')
    start = time.monotonic()
    stamp = datetime.now(timezone.utc).isoformat()
    try:
        p = subprocess.run(argv, cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout, shell=False)
        return {'command': name, 'argv': argv, 'cwd': str(root), 'timestamp': stamp,
                'status': 'EXECUTED', 'exit_code': p.returncode, 'seconds': time.monotonic() - start,
                'stdout': p.stdout[-32000:], 'stderr': p.stderr[-32000:],
                'output_truncated': len(p.stdout) > 32000 or len(p.stderr) > 32000}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {'command': name, 'argv': argv, 'timestamp': stamp, 'status': 'EXECUTION FAILED',
                'exit_code': None, 'seconds': time.monotonic() - start, 'error': str(e)}
