from pathlib import Path
import sys
import tempfile
import unittest
import importlib
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.game-studio/runtime'))


class CheckTests(unittest.TestCase):
    def test_review_scope_accepts_bullets_and_template_system_names(self):
        checks = self.checks
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'design/gdd').mkdir(parents=True)
            (root / 'design/gdd/economy.md').write_text('# Economy', encoding='utf-8')
            shop = root / 'design/gdd/shop.md'
            for declared in ['## Dependencies\n- economy.md', 'Key deps: economy']:
                shop.write_text('# Shop\n' + declared, encoding='utf-8')
                baseline = checks.receipts(root, 'hash', ['design/gdd/*.md'])
                (root / 'receipt.json').write_text(json.dumps(baseline), encoding='utf-8')
                shop.write_text(shop.read_text(encoding='utf-8') + '\nChange', encoding='utf-8')
                scope = checks.review_scope(root, 'receipt.json')
                self.assertIn('design/gdd/economy.md', scope['scope'])

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.checks = importlib.import_module('checks')

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
        return p

    def test_missing_inputs_do_not_pass(self):
        self.assertEqual(self.checks.stories(self.root)['status'], 'NOT ASSESSED — NO DATA')
        self.assertEqual(self.checks.run_command(self.root, 'build')['status'], 'NOT ASSESSED — NO DATA')

    def test_receipt_reports_deleted_hash_character_filename(self):
        p = self.write('design/gdd/system#1.md', '# System')
        baseline = self.checks.receipts(self.root, 'hash', ['design/gdd/*.md'])
        self.write('receipt.json', json.dumps(baseline))
        with self.assertRaisesRegex(ValueError, 'paths without #'):
            self.checks.receipts(self.root, 'sections-hash', ['design/gdd/*.md'])
        p.unlink()
        result = self.checks.receipts(self.root, 'check', ['design/gdd/*.md'], 'receipt.json')
        self.assertEqual(result['observations'][0]['status'], 'REMOVED')

    def test_actual_command_success_and_failure_receipts(self):
        import json
        self.write('project.yaml', 'commands:\n  test: ' + json.dumps([sys.executable, '-c', 'print("sample output")']) + '\n  build: ' + json.dumps([sys.executable, '-c', 'raise SystemExit(7)']) + '\n')
        self.assertEqual(self.checks.run_command(self.root, 'test')['exit_code'], 0)
        self.assertEqual(self.checks.run_command(self.root, 'build')['exit_code'], 7)

    def test_artifact_patterns_and_denominators(self):
        self.write('.game-studio/resources/docs/workflow-catalog.yaml', 'phases:\n  concept:\n    steps:\n      - id: a\n        artifact: {glob: "design/*.md", pattern: "Ready:[[:space:]]*yes"}\n      - id: b\n')
        self.write('design/one.md', 'Ready: yes')
        r = self.checks.artifacts(self.root, phase='concept')
        self.assertEqual(r['steps'], 2)
        self.assertEqual(r['observations'][0]['status'], 'PRESENT')
        self.assertEqual(r['observations'][1]['status'], 'NO_CHECK')
        with self.assertRaises(ValueError):
            self.checks.artifacts(self.root, phase='typo')

    def test_receipts_detect_change_and_deleted_sections(self):
        self.write('design/one file.md', '# Design\n## A\nfirst\n## B\nsecond')
        stamp = self.checks.receipts(self.root, 'sections-hash', ['design/one file.md'])
        self.write('receipt.json', __import__('json').dumps(stamp))
        self.write('design/one file.md', '# Design\n## A\nchanged')
        result = self.checks.receipts(self.root, 'sections-check', ['design/one file.md'], 'receipt.json')
        self.assertIn('REMOVED', [row['status'] for row in result['observations']])
        self.assertIn('CHANGED', [row['status'] for row in result['observations']])

    def test_dependencies_cycles_and_missing_targets(self):
        self.write('docs/architecture/adr-a.md', '## ADR Dependencies\n- adr-b.md\n')
        self.write('docs/architecture/adr-b.md', '## ADR Dependencies\n- adr-a.md\n- adr-missing.md\n')
        result = self.checks.dependencies(self.root)
        self.assertTrue(result['cycles'])
        self.assertTrue(result['missing'])

    def test_dependency_tables_do_not_reverse_used_by(self):
        self.write('docs/architecture/adr-0001.md', '## ADR Dependencies\n| **Depends On** | None |\n| **Used By** | ADR-0002 |\n')
        self.write('docs/architecture/adr-0002.md', '## ADR Dependencies\n| **Depends On** | ADR-0001 |\n')
        r = self.checks.dependencies(self.root)
        self.assertFalse(r['cycles'])
        self.assertEqual(r['graph']['docs/architecture/adr-0001.md'], [])

    def test_review_scope_retains_deleted_inputs(self):
        import json
        source = self.write('design/gdd/one.md', '# Input')
        old = self.checks.receipts(self.root, 'hash', ['design/gdd/*.md'])
        self.write('review.json', json.dumps(old))
        source.unlink()
        r = self.checks.review_scope(self.root, 'review.json')
        self.assertIn('design/gdd/one.md', r['changed'])


if __name__ == '__main__':
    unittest.main()
