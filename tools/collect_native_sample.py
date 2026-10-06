"""Retain actual selected fixture outputs; never fabricate skill runs or verdicts."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]
DESTINATION = SOURCE / 'docs/migration/native-sample'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def collect(root):
    root = root.resolve()
    if not (root / 'evidence/minimal-native.md').is_file():
        raise ValueError('Actual parent evidence is required; run the workflow first')
    replacements = [(str(root), '<fixture-root>'),
                    (root.as_posix(), '<fixture-root>'),
                    (str(SOURCE / '.venv/Scripts/python.exe'), '<fixture-python>'),
                    ((SOURCE / '.venv/Scripts/python.exe').as_posix(), '<fixture-python>')]

    def normalized(value):
        if isinstance(value, dict):
            return {k: normalized(v) for k, v in value.items()}
        if isinstance(value, list):
            return [normalized(v) for v in value]
        if isinstance(value, str):
            for original, replacement in replacements:
                value = value.replace(original, replacement)
        return value

    selected = [p for folder in ['evidence', 'design', 'docs/architecture',
                                 'production', 'records', 'src', 'tests', 'inputs']
                for p in (root / folder).rglob('*')
                if p.is_file() and p.suffix in {'.md', '.json', '.yaml', '.py'}]
    # Earlier pre-repair helper output is not a final result; keep it only locally.
    selected = [p for p in selected if p != root / 'evidence/coherence.json']
    selected += [root / name for name in ['project.yaml', 'notes/current.md',
                                         'minimal-prompt.txt', 'minimal-final-network.txt']]
    manifest = []
    for path in sorted(selected):
        relative = path.relative_to(root).as_posix()
        original = path.read_bytes()
        content = original.decode('utf-8')
        if path.suffix == '.json':
            rewritten = normalized(json.loads(content))
            # Preserve original bytes when no path normalization is needed.
            if rewritten != json.loads(content):
                content = json.dumps(rewritten, indent=2, ensure_ascii=False) + '\n'
        else:
            content = normalized(content)
        content = content.replace('\r\n', '\n')
        retained = content.encode('utf-8')
        target = DESTINATION / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(retained)
        manifest.append({'path': relative, 'original_sha256': sha(original),
                         'retained_sha256': sha(retained), 'normalized': retained != original})

    # Only event types/status/exit codes are retained from the CLI transcript.
    event_counts = Counter()
    tool_results = []
    for line in (root / 'minimal-events-network.jsonl').read_text(encoding='utf-8').splitlines():
        event = json.loads(line)
        event_counts[event['type']] += 1
        item = event.get('item', {})
        if event['type'] == 'item.completed' and item.get('type') in {'command_execution', 'mcp_tool_call'}:
            tool_results.append({key: item[key] for key in ['type', 'status', 'exit_code'] if key in item})
    result = {
        'collected_at_utc': datetime.now(timezone.utc).isoformat(),
        'method': 'Actual current Codex parent manually loaded installed native entries/procedures and applied selected branches with tools',
        'scope': 'Synthetic nongame fixture; parent-only professional perspectives, not independent participants',
        'workflow_evidence': {
            'gs-help': 'evidence/before-stories.json',
            'gs-sprint-status': 'evidence/after-stories.json',
            'gs-story-done': 'evidence/minimal-native.md',
            'gs-design-review': 'design/gdd/reviews/counter-review-log.md',
            'gs-review-all-gdds': 'design/gdd/gdd-cross-review-2026-10-05.md',
            'gs-architecture-review': 'docs/architecture/architecture-review-2026-10-05.md',
            'gs-architecture-decision': 'docs/architecture/adr-0001-counter-utility-core.md',
            'gs-gate-check': 'production/gate-checks/pre-production-2026-10-05.md',
            'gs-release-checklist': 'production/releases/release-checklist-fixture.md',
            'gs-team-release': 'production/releases/release-report-fixture.md'},
        'role_profiles_read': ['gs-systems-designer', 'gs-qa-lead', 'gs-technical-director'],
        'independent_participants': [],
        'headless_cli': {'model_call': 'EXECUTED', 'requested_model': 'gpt-6.1-sol',
                         'requested_reasoning': 'xhigh', 'workflow': 'NOT ASSESSED',
                         'reason': 'Windows native sandbox setup failed before reads/commands',
                         'event_counts': dict(event_counts), 'tool_results': tool_results,
                         'final': 'minimal-final-network.txt',
                         'separate_restricted_network_attempt': 'No model connection; terminated its verified fixture process'},
        'not_assessed': ['autonomous headless workflow completion', 'all 74 full workflows',
                         'all 49 role behaviors/custom-role launch', 'trusted hook delivery',
                         'game balance/performance/visuals/playtests', 'engine tests/build',
                         'certification/deployment/live operations'],
        'normalization': 'Fixture/Python absolute paths replaced and CRLF normalized to LF. Original digests preserved; normalized config bytes cannot replay original input hashes. Linked report bytes and their report_hash remain unchanged.',
        'payload_release_sha256': sha((SOURCE / '.game-studio/release.json').read_bytes()),
        'artifacts': manifest}
    (DESTINATION / 'execution.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'artifacts': len(manifest), 'output': str(DESTINATION),
                      'headless_workflow': result['headless_cli']['workflow']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fixture', type=Path)
    collect(parser.parse_args().fixture)
