import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from install_design import install
from validate_design import validate


class InstallDesignTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = tempfile.TemporaryDirectory(prefix='ccgs-design-test-')
        self.addCleanup(self.sandbox.cleanup)
        self.base = Path(self.sandbox.name)
        self.source = self.base / 'framework'
        self.target = self.base / 'game project'
        (self.source / 'codex').mkdir(parents=True)
        self.target.mkdir()
        skill = self.source / '.agents/skills/demo/SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text('---\nname: demo\ndescription: Use when testing an install fixture.\n---\n\nFixture.\n', encoding='utf-8')
        license_path = self.source / 'LICENSE'
        license_path.write_bytes(b'fixture source\n')
        for name in ('README.md', 'compatibility.md', 'validate_design.py', 'install_design.py'):
            (self.source / 'codex' / name).write_text('fixture\n', encoding='utf-8')
        manifest = {'skills': ['demo'], 'roles': [], 'source_files': [{'path': 'LICENSE',
                    'sha256': hashlib.sha256(license_path.read_bytes()).hexdigest()}]}
        (self.source / 'codex/manifest.json').write_text(json.dumps(manifest), encoding='utf-8')

    def test_existing_destination_aborts_before_any_copy(self):
        marker = self.target / '.agents/skills/demo/SKILL.md'
        marker.parent.mkdir(parents=True)
        marker.write_text('my existing skill', encoding='utf-8')
        with self.assertRaises(FileExistsError):
            install(self.source, self.target)
        self.assertEqual(marker.read_text(encoding='utf-8'), 'my existing skill')
        self.assertFalse((self.target / 'codex').exists())

    def test_tampered_source_aborts_before_any_copy(self):
        (self.source / 'LICENSE').write_text('changed source', encoding='utf-8')
        with self.assertRaises(ValueError):
            install(self.source, self.target)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_snapshot_path_must_stay_in_project(self):
        with self.assertRaises(ValueError):
            install(self.source, self.target, '../outside')
        self.assertEqual(list(self.target.iterdir()), [])

    def test_context_paths_must_be_repository_relative(self):
        outside = self.base / 'shared/context.md'
        outside.parent.mkdir()
        outside.write_text('external facts', encoding='utf-8')
        for path in ('../shared/context.md', str(outside)):
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    install(self.source, self.target, context_entry=path)
                self.assertEqual(list(self.target.iterdir()), [])

    def test_dry_run_does_not_write(self):
        result = install(self.source, self.target, dry_run=True)
        self.assertTrue(result['dry_run'])
        self.assertEqual(list(self.target.iterdir()), [])

    def test_source_hash_accepts_only_line_ending_conversion(self):
        manifest_path = self.source / 'codex/manifest.json'
        data = json.loads(manifest_path.read_text(encoding='utf-8'))
        data['hash_normalization'] = 'lf-text'
        manifest_path.write_text(json.dumps(data), encoding='utf-8')
        (self.source / 'LICENSE').write_bytes(b'fixture source\r\n')
        self.assertEqual(validate(self.source)['skills'], 1)
        (self.source / 'LICENSE').write_bytes(b'different source\r\n')
        with self.assertRaises(ValueError):
            validate(self.source)

    def test_context_and_existing_project_files_are_preserved(self):
        context = self.target / 'context/当前记录.md'
        context.parent.mkdir()
        context.write_text('existing project facts', encoding='utf-8')
        agents = self.target / 'AGENTS.md'
        agents.write_text('project instructions', encoding='utf-8')
        config = self.target / 'project.yaml'
        config.write_text('existing configuration', encoding='utf-8')
        install(self.source, self.target, context_entry='context/当前记录.md')
        self.assertEqual(validate(self.target)['skills'], 1)
        self.assertEqual(context.read_text(encoding='utf-8'), 'existing project facts')
        self.assertEqual(agents.read_text(encoding='utf-8'), 'project instructions')
        self.assertEqual(config.read_text(encoding='utf-8'), 'existing configuration')
        data = json.loads((self.target / 'codex/context.json').read_text(encoding='utf-8'))
        self.assertEqual(data['context_entry'], 'context/当前记录.md')

    def test_windows_style_context_is_serialized_as_posix(self):
        context = self.target / 'docs/context.md'
        context.parent.mkdir()
        context.write_text('portable project facts', encoding='utf-8')
        install(self.source, self.target, context_entry='docs\\context.md')
        data = json.loads((self.target / 'codex/context.json').read_text(encoding='utf-8'))
        self.assertEqual(data['context_entry'], 'docs/context.md')
        self.assertEqual(validate(self.target)['skills'], 1)


if __name__ == '__main__':
    unittest.main()
