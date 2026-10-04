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
        status = re.search(r'(?im)^\s*\*{0,2}Status\*{0,2}:\*{0,2}\s*(.+)', text)
        rows.append({'path': p.relative_to(root).as_posix(), 'status': status.group(1).strip() if status else 'UNKNOWN'})
    return {'status': 'OBSERVED' if rows else NO_DATA, 'count': len(rows), 'stories': rows}


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


def receipts(root, action, patterns, receipt=None):
    root = plain(root)
    if action not in {'hash', 'check', 'sections-hash', 'sections-check'}:
        raise ValueError('Unknown receipt action')
    old, observations, unresolved = {}, [], []
    if action.endswith('check') and receipt:
        p = confined(root, receipt)
        if p.exists():
            data = json.loads(p.read_text(encoding='utf-8'))
            if not isinstance(data, dict) or data.get('algorithm') != 'sha256' or not isinstance(data.get('hashes'), dict):
                raise ValueError('Receipt must be native sha256 JSON; legacy stamps require a fresh review')
            old = data['hashes']
            for key, sha in old.items():
                confined(root, key.split('#', 1)[0] if action.startswith('sections-') else key)
                if not isinstance(sha, str) or len(sha) != 64:
                    raise ValueError('Invalid receipt hash')
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
    return {'algorithm': 'sha256', 'hashes': current, 'observations': observations,
            'unresolved': unresolved, 'status': 'OBSERVED' if current else NO_DATA}


def dependencies(root):
    root = plain(root)
    adrs = files(root, 'docs/architecture/adr-*.md')
    lookup = {p.stem.lower(): p.relative_to(root).as_posix() for p in adrs}
    graph, missing = {}, []
    for p in adrs:
        rel = p.relative_to(root).as_posix()
        text = p.read_text(encoding='utf-8-sig')
        match = re.search(r'(?ims)^## ADR Dependencies\s*\n(.*?)(?=^## |\Z)', text)
        dependency_text = match.group(1) if match else ''
        depends_row = re.search(r'(?im)^.*\*\*Depends On\*\*.*$', dependency_text)
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
    return {'status': 'OBSERVED' if adrs else NO_DATA, 'nodes': len(adrs), 'graph': graph, 'missing': missing, 'cycles': cycles}


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
    if receipt:
        observations = receipts(root, 'check', ['design/gdd/*.md'], receipt)
        changed = [r['path'] for r in observations['observations'] if r['status'] != 'UNCHANGED'
                   and Path(r['path']).stem not in excluded and not Path(r['path']).stem.startswith('gdd-cross-review-')]
    else:
        changed = names
    scoped = set(changed)
    queue = list(changed)
    missing, unresolved = [], []
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
        for dep in found - scoped:
            scoped.add(dep)
            queue.append(dep)
    if unresolved:
        scoped.update(names)  # Unknown declarations cannot safely narrow review.
    return {'status': 'OBSERVED' if names else NO_DATA, 'baseline': receipt,
            'changed': sorted(changed), 'scope': sorted(scoped), 'missing': missing,
            'unresolved_dependencies': unresolved,
            'note': 'Without a native receipt, conservative full scope. Confirm declared dependencies in the review.'}


def coherence(root):
    root = plain(root)
    result = resolve(root)
    engine = result['values'].get('engine.name')
    markers = {'Godot': list(Path(root).glob('project.godot')), 'Unity': list(Path(root).glob('ProjectSettings/ProjectVersion.txt')),
               'Unreal': list(Path(root).glob('*.uproject'))}
    return {'settings': result, 'engine_markers': {k: [p.relative_to(root).as_posix() for p in v] for k, v in markers.items()},
            'configured_engine': engine, 'status': 'OBSERVED' if engine else NO_DATA,
            'note': 'No engine setup or version inference performed.'}


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
