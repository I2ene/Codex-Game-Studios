"""Execute an isolated, non-game consumer lifecycle and print bounded evidence."""
import json
import argparse
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.game-studio/runtime'))
import checks
import context
import installer


def execute(native_discovery=False):
    with tempfile.TemporaryDirectory(prefix='codex-studio-sample-') as temporary:
        root = Path(temporary) / 'existing consumer with spaces'
        root.mkdir()
        (root / 'AGENTS.md').write_text('Consumer-owned instruction: use the counter specification.\n', encoding='utf-8')
        config = {'schema_version': 1, 'project': {'name': 'Non-game counter fixture', 'stage': 'Production'},
                  'modes': {'rigor': 'minimal', 'automation': 'autonomous'},
                  'code_root': 'src', 'test_root': 'tests',
                  'commands': {'test': [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                               'build': [sys.executable, '-m', 'zipfile', '-c', 'delivery.zip', 'src/counter.py']}}
        import yaml
        (root / 'project.yaml').write_text(yaml.safe_dump(config, sort_keys=False), encoding='utf-8')
        dry = installer.install(ROOT, root, True)
        installed = installer.install(ROOT, root)
        discovery = {'status': 'NOT ASSESSED', 'reason': 'Native discovery probe not requested'}
        if native_discovery:
            from probe_codex import probe
            discovery = probe(root)
            expected = sorted(p.parent.name for p in (ROOT / '.agents/skills').glob('*/SKILL.md'))
            if discovery['status'] == 'EXECUTED' and (discovery['native_skills'] != expected or discovery['framework_errors'] or discovery['protocol_errors']):
                raise RuntimeError('Installed native discovery did not match release: ' + json.dumps(discovery))
        for folder in ['design', 'production/epics/counter', 'src', 'tests', 'production/session-state', 'reviews']:
            (root / folder).mkdir(parents=True, exist_ok=True)
        # Deterministic helper/artifact fixture, not a skill-execution claim.
        (root / 'design/game-brief.md').write_text('# Counter fixture brief\n\nNon-game framework smoke sample.\nGoal: increment an integer to a cap.\nMVP: one pure function.\nBuild order: implement counter, verify invalid inputs, package source.\nAcceptance: 0 <= value <= limit; clamp increment to limit; reject invalid types/ranges.\nNo engine, visuals, balancing or performance evaluation.\n', encoding='utf-8')
        story = root / 'production/epics/counter/story-001.md'
        story.write_text('# Counter function\nStatus: Ready\nType: Logic\nGDD: N/A — minimal one-page brief\nADR Governing Implementation: N/A — pure fixture function\n\n## Acceptance Criteria\n- Increment below cap\n- Clamp at cap including zero cap\n- Reject negative, over-cap and boolean inputs\n', encoding='utf-8')
        shutil.copyfile(ROOT / 'fixtures/minimal-counter/counter.py', root / 'src/counter.py')
        shutil.copyfile(ROOT / 'fixtures/minimal-counter/test_counter.py', root / 'tests/test_counter.py')
        tested = checks.run_command(root, 'test', 30)
        if tested['exit_code'] != 0:
            raise RuntimeError(tested)
        review = 'Parent review: acceptance criteria checked against pure function and executed tests.\nInteger type/range guards and cap behavior verified. No independent participant.\n'
        (root / 'reviews/code-review.md').write_text(review, encoding='utf-8')
        receipt = checks.receipts(root, 'hash', ['src/counter.py', 'tests/test_counter.py', 'design/game-brief.md'])
        (root / 'reviews/receipt.json').write_text(json.dumps(receipt), encoding='utf-8')
        unchanged = checks.receipts(root, 'check', ['src/counter.py', 'tests/test_counter.py', 'design/game-brief.md'], 'reviews/receipt.json')
        built = checks.run_command(root, 'build', 30)
        if built['exit_code'] != 0 or not (root / 'delivery.zip').is_file():
            raise RuntimeError(built)
        story.write_text(story.read_text(encoding='utf-8').replace('Status: Ready', 'Status: Complete') + '\n## Test Evidence\n2 executed fixture tests; actual packaging exit 0.\n', encoding='utf-8')
        (root / 'production/session-state/active.md').write_text('# Actual checkpoint\nObjective: non-game counter fixture.\nCompleted: brief, story, code, parent review, two tests, source archive.\nNext: none for fixture.\nNo game balance/performance/engine/release evaluation.\n', encoding='utf-8')
        recovered = context.recover(root)
        reinstall = installer.install(ROOT, root)
        for result in [tested, built]:
            result['cwd'] = '<sample-root>'
            result['argv'][0] = '<current-python>'
        return {'status': 'EXECUTED', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
                'scope': 'Deterministic non-game helper/artifact fixture; no model-driven skill execution or independent agents',
                'install_dry_run': dry['dry_run'], 'installed_version': installed['version'],
                'reinstall_writes': len(reinstall['write']), 'test_receipt': tested, 'package_receipt': built,
                'review_inputs_unchanged': all(o['status'] == 'UNCHANGED' for o in unchanged['observations']),
                'native_discovery': discovery,
                'checkpoint_recovered': recovered['checkpoint']['status'],
                'story_observation': checks.stories(root),
                'not_assessed': ['game balance', 'game performance', 'engine tests/build', 'playtest', 'platform certification', 'release deployment', 'trusted hook callback', 'custom-role launch']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--native-discovery', action='store_true', help='Read-only Codex CLI discovery in the installed fixture')
    result = execute(parser.parse_args().native_discovery)
    print(json.dumps(result, indent=2, ensure_ascii=False))
