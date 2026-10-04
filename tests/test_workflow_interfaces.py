"""Regressions for the concrete Astra workflow-interface findings."""
import importlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.game-studio/runtime'))
sys.path.insert(0, str(ROOT / 'tools'))


class WorkflowInterfaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.checks = importlib.import_module('checks')

    def put(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def test_delivered_source_damage_fails_fixture_tests(self):
        self.put('src/counter.py', 'raise RuntimeError("damaged delivered source")\n')
        test = self.put('tests/test_counter.py', '')
        shutil.copyfile(ROOT / 'fixtures/minimal-counter/test_counter.py', test)
        # An old/local same-named copy must never shadow the delivered source.
        shutil.copyfile(ROOT / 'fixtures/minimal-counter/counter.py', self.root / 'tests/counter.py')
        result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests'],
                                cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('damaged delivered source', result.stderr)

    def test_story_formats_counts_priority_and_done_boundary(self):
        cases = [('Ready', 'Status: Ready'), ('In Review', '**Status:** In Review'),
                 ('Complete', '> **Status**: Complete'), ('Blocked', '- **Status**: Blocked'),
                 ('In Progress', '  **Status**: In Progress'), ('Done.', 'Status: Done.'),
                 ('Not Done', 'Status: Not Done'), ('UNKNOWN', '# no status')]
        for i, (_, text) in enumerate(cases):
            self.put(f'production/epics/e/story-{i:03}.md', text)
        result = self.checks.stories(self.root)
        self.assertEqual(result['complete'], 2)
        self.assertEqual(result['unfinished'][0]['status'], 'In Review')
        self.assertEqual(result['unfinished'][1]['status'], 'In Progress')
        self.assertEqual(result['next']['action'], 'story-done')
        actual = {Path(r['path']).stem: r['status'] for r in result['stories']}
        for i, (expected, _) in enumerate(cases):
            self.assertEqual(actual[f'story-{i:03}'], expected)

    def test_story_route_empty_complete_blocked(self):
        self.assertEqual(self.checks.stories(self.root)['next']['action'], 'NO STORIES')
        story = self.put('production/epics/e/story-001.md', 'Status: Done.')
        self.assertEqual(self.checks.stories(self.root)['next']['action'], 'COMPLETE')
        story.write_text('Status: Blocked', encoding='utf-8')
        self.assertEqual(self.checks.stories(self.root)['next']['action'], 'BLOCKED')

    def test_project_engine_records_override_packaged_version(self):
        engine = importlib.import_module('engine')
        self.put('project.yaml', 'engine: {name: Godot, version: "4.3"}\n')
        self.put('.game-studio/resources/engine-reference/godot/VERSION.md', '| **Engine Version** | Godot 4.6 |\n')
        self.put('docs/engine-reference/godot/VERSION.md', '| **Engine Version** | Godot 4.3 |\n| **Installed at pin time** | NOT DETERMINED |\n')
        result = engine.references(self.root)
        self.assertEqual(result['project']['version_record'], 'Godot 4.3')
        self.assertEqual(result['project']['documents']['VERSION.md'], 'docs/engine-reference/godot/VERSION.md')
        (self.root / 'docs/engine-reference/godot/VERSION.md').unlink()
        missing = engine.references(self.root)
        self.assertIsNone(missing['project']['version_record'])
        self.assertEqual(missing['project']['status'], 'NOT ASSESSED — NO PROJECT VERSION RECORD')

    def test_coherence_reports_local_contradictions_without_binary(self):
        self.put('project.yaml', 'engine: {name: Godot, version: "4.4", rendering: "Forward+", physics: Jolt}\ncommands:\n  test: [godot, --script, res://addons/missing.gd]\n  build: [godot, --export-release, Linux]\n')
        self.put('project.godot', '[application]\nconfig/features=PackedStringArray("4.3")\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n')
        self.put('src/player.gd', 'extends Node2D\n')
        result = self.checks.coherence(self.root)
        rows = {r['check']: r for r in result['observations']}
        for check in ['project-version', 'rendering', 'physics', 'test-entry:addons/missing.gd', 'export-presets']:
            self.assertEqual(rows[check]['status'], 'DIFFERS')
        self.assertEqual(rows['installed-binary']['status'], 'NOT ASSESSED')

    def test_coherence_explicit_probe_and_valid_runner_preset(self):
        self.put('project.yaml', 'engine: {name: Godot, version: "4.3"}\ncommands:\n  engine_probe: ' + json.dumps([sys.executable, '-c', 'print("fixture Godot 4.3")']) + '\n  test: [godot, --script, res://addons/runner.gd]\n  build: [godot, --export-release, "Linux Debug"]\n')
        self.put('addons/runner.gd', '# fixture entry')
        self.put('export_presets.cfg', '[preset.0]\nname="Linux Debug"\n')
        result = self.checks.coherence(self.root, probe=True)
        rows = {r['check']: r for r in result['observations']}
        self.assertEqual(rows['installed-binary']['status'], 'MATCH')
        self.assertEqual(rows['installed-binary']['execution']['exit_code'], 0)
        self.assertEqual(rows['test-entry:addons/runner.gd']['status'], 'MATCH')
        self.assertEqual(rows['export-presets']['status'], 'MATCH')

    def test_linked_review_receipt_cycle_and_dependency_changes(self):
        doc = self.put('design/gdd/shop.md', '# Shop\n## Dependencies\n- economy.md\n')
        economy = self.put('design/gdd/economy.md', '# Economy\n')
        report = self.put('reviews/review.md', '# Actual fixture review\nVerdict: CONCERNS\n')
        patterns = ['design/gdd/*.md']
        baseline = self.checks.receipts(self.root, 'hash', patterns, report='reviews/review.md')
        self.put('reviews/review.receipt.json', json.dumps(baseline))
        check = lambda: self.checks.receipts(self.root, 'check', patterns, 'reviews/review.receipt.json')
        self.assertTrue(check()['unchanged_inputs'])
        economy.write_text('# Economy\nChanged dependency rules', encoding='utf-8')
        self.assertFalse(check()['unchanged_inputs'])
        self.assertIn('design/gdd/economy.md', self.checks.review_scope(self.root, 'reviews/review.receipt.json')['changed'])
        self.assertIn('design/gdd/shop.md', self.checks.review_scope(self.root, 'reviews/review.receipt.json')['scope'])
        doc.unlink()
        self.assertIn('REMOVED', [r['status'] for r in check()['observations']])
        report.write_text('# Modified report', encoding='utf-8')
        self.assertEqual(check()['report_status'], 'CHANGED')
        self.assertEqual(self.checks.receipts(self.root, 'check', patterns, 'missing.receipt.json')['baseline_status'], 'MISSING')

    def test_review_scope_report_drift_and_context_changes_require_full_scope(self):
        self.put('design/gdd/a.md', '# A\n## Dependencies\nNone\n')
        self.put('design/gdd/b.md', '# B\n## Dependencies\nNone\n')
        context = self.put('design/registry/entities.yaml', 'entities: []\n')
        report = self.put('reviews/report.md', 'Verdict: CONCERNS\n')
        patterns = ['design/gdd/*.md', 'design/registry/entities.yaml']
        baseline = self.checks.receipts(self.root, 'hash', patterns, report='reviews/report.md')
        self.put('reviews/report.json', json.dumps(baseline))
        scope = lambda: self.checks.review_scope(self.root, 'reviews/report.json')['scope']
        self.assertEqual(scope(), [])
        context.write_text('entities: [{name: new}]\n', encoding='utf-8')
        self.assertEqual(len(scope()), 2)
        context.write_text('entities: []\n', encoding='utf-8')
        report.write_text('Changed verdict', encoding='utf-8')
        self.assertEqual(len(scope()), 2)
        baseline.pop('report')
        self.put('reviews/report.json', json.dumps(baseline))
        self.assertEqual(len(scope()), 2)

    def test_coherence_windows_relative_runner_path(self):
        self.put('project.yaml', 'engine: {name: Godot, version: "4.3"}\ncommands:\n  test: [godot, --script, "addons\\\\runner.gd"]\n')
        self.put('addons/runner.gd', '# fixture')
        result = self.checks.coherence(self.root)
        rows = {r['check']: r for r in result['observations']}
        self.assertEqual(rows['test-entry:addons/runner.gd']['status'], 'MATCH')

    def test_absent_rendering_is_unknown_and_patch_pin_is_compared(self):
        self.put('project.yaml', 'engine: {name: Godot, version: "4.3.1"}\n')
        self.put('docs/engine-reference/godot/VERSION.md', '| **Engine Version** | Godot 4.3.2 |\n')
        rows = {r['check']: r for r in self.checks.coherence(self.root)['observations']}
        self.assertEqual(rows['rendering']['status'], 'NOT ASSESSED')
        self.assertEqual(rows['pinned-reference']['status'], 'DIFFERS')

    def test_cli_emits_utf8_even_when_locale_encoding_cannot_encode_status(self):
        result = subprocess.run([sys.executable, str(ROOT / '.game-studio/runtime/studio.py'),
                                 'engine-reference', '--root', str(self.root)],
                                env={**os.environ, 'PYTHONIOENCODING': 'cp1252'}, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('NOT ASSESSED', json.loads(result.stdout.decode('utf-8'))['project']['status'])

    def test_dependency_order_and_missing_declaration_are_explicit(self):
        self.put('docs/architecture/adr-0001-base.md', '# Base\n## ADR Dependencies\nNone\n')
        self.put('docs/architecture/adr-0002-use.md', '# Use\n## ADR Dependencies\n| **Depends On** | ADR-0001-base |\n')
        self.put('docs/architecture/adr-0003-unknown.md', '# Unknown\n')
        result = self.checks.dependencies(self.root)
        self.assertEqual(result['missing_sections'], ['docs/architecture/adr-0003-unknown.md'])
        self.assertLess(result['order'].index('docs/architecture/adr-0001-base.md'), result['order'].index('docs/architecture/adr-0002-use.md'))


if __name__ == '__main__':
    unittest.main()
