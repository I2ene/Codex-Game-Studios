import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / '.game-studio/runtime'))


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'project with spaces'
        self.root.mkdir()

    def write(self, path, text):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
        return p

    def test_config_precedence_rigor_and_local_scope(self):
        config = importlib.import_module('config')
        self.write('project.yaml', 'modes:\n  rigor: full\n  automation: guided\ntesting:\n  strict:\n    logic: true\n    integration: false\nworkflow_overrides:\n  system_overrides:\n    combat: minimal\n')
        self.write('project.local.yaml', 'modes:\n  rigor: minimal\n  automation: autonomous\ntesting:\n  strict:\n    logic: false\n')
        result = config.resolve(self.root, 'combat')
        self.assertEqual(result['values']['modes.workflow'], 'minimal')
        self.assertEqual(result['values']['docs.density'], 'thorough')
        self.assertEqual(result['values']['modes.automation'], 'autonomous')
        self.assertFalse(result['values']['testing.strict.logic'])
        self.assertFalse(result['values']['testing.strict.integration'])
        self.assertTrue(any('modes.rigor' in n for n in result['notes']))

    def test_config_malformed_duplicate_and_orphan_are_observable(self):
        config = importlib.import_module('config')
        for content in ('modes: [', 'modes: {}\nmodes: {}\n', 'modes:\n\trigor: full\n'):
            self.write('project.yaml', content)
            with self.assertRaises(ValueError):
                config.resolve(self.root)
        (self.root / 'project.yaml').unlink()
        self.write('project.local.yaml', 'modes: {automation: guided}')
        with self.assertRaises(ValueError):
            config.resolve(self.root)

    def test_enum_fallback_legacy_and_on_off(self):
        config = importlib.import_module('config')
        self.write('project.yaml', 'modes: {rigor: standard, review_mode: bogus}\nfeatures: {session_state: off}\n')
        self.write('production/review-mode.txt', 'full')
        r = config.resolve(self.root)
        self.assertEqual(r['values']['modes.review_mode'], 'full')
        self.assertEqual(r['values']['features.session_state'], 'off')
        self.assertTrue(r['notes'])

    def test_context_is_optional_and_confined(self):
        context = importlib.import_module('context')
        self.assertEqual(context.recover(self.root)['checkpoint']['status'], 'ABSENT')
        self.write('.game-studio/context.json', '{"checkpoint":"../outside.md"}')
        with self.assertRaises(ValueError):
            context.recover(self.root)
        self.write('.game-studio/context.json', '{"checkpoint":"notes/state.md","records":["notes/design.md"]}')
        self.write('notes/state.md', 'Active: sample\nNext: review')
        r = context.recover(self.root)
        self.assertEqual(r['checkpoint']['status'], 'PRESENT')
        self.assertEqual(r['records'][0]['status'], 'ABSENT')

    def test_install_preserves_existing_files_and_is_idempotent(self):
        installer = importlib.import_module('installer')
        original = 'User instructions\n'
        self.write('AGENTS.md', original)
        self.write('project.yaml', 'engine: {name: Unity}\n')
        self.write('.codex/config.toml', '# user settings\n')
        installer.install(REPO, self.root, dry_run=True)
        self.assertFalse((self.root / '.agents').exists())
        installer.install(REPO, self.root)
        self.assertTrue((self.root / 'AGENTS.md').read_text().startswith(original))
        self.assertEqual((self.root / 'project.yaml').read_text(), 'engine: {name: Unity}\n')
        self.assertEqual((self.root / '.codex/config.toml').read_text(), '# user settings\n')
        self.assertEqual(len(list((self.root / '.agents/skills').glob('*/SKILL.md'))), 74)
        installer.install(REPO, self.root)
        self.assertEqual((self.root / 'AGENTS.md').read_text().count('BEGIN CODEX GAME STUDIOS'), 1)

    def test_install_edit_conflict_has_no_partial_writes(self):
        installer = importlib.import_module('installer')
        installer.install(REPO, self.root)
        skill = self.root / '.agents/skills/gs-start/SKILL.md'
        skill.write_text('User edit', encoding='utf-8')
        state = (self.root / '.game-studio/install-state.json').read_bytes()
        with self.assertRaises(ValueError):
            installer.install(REPO, self.root)
        self.assertEqual(skill.read_text(), 'User edit')
        self.assertEqual((self.root / '.game-studio/install-state.json').read_bytes(), state)

    def test_overlap_and_corrupt_ledger_rejected(self):
        installer = importlib.import_module('installer')
        with self.assertRaises(ValueError):
            installer.install(REPO, REPO / 'sandbox')
        self.write('.game-studio/install-state.json', '{"files":{"../escape":"abc"}}')
        with self.assertRaises(ValueError):
            installer.install(REPO, self.root)

    def test_upgrade_updates_owned_and_removes_only_owned(self):
        import shutil
        installer = importlib.import_module('installer')
        source = Path(self.tmp.name) / 'release'
        for folder in ['.agents', '.codex/agents', '.game-studio']:
            shutil.copytree(REPO / folder, source / folder, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        obsolete = source / '.game-studio/resources/obsolete.txt'
        obsolete.write_text('Retired owned resource', encoding='utf-8')
        installer.build_manifest(source)
        installer.install(source, self.root)
        user_file = self.write('.agents/skills/user-skill/SKILL.md', 'user skill')
        gone = obsolete
        gone.unlink()
        owned = source / '.agents/skills/gs-help/references/workflow.md'
        owned.write_text(owned.read_text(encoding='utf-8') + '\nUpgrade content\n', encoding='utf-8')
        (source / '.game-studio/VERSION').write_text('2.0.1', encoding='utf-8')
        installer.build_manifest(source)
        installer.install(source, self.root)
        self.assertFalse((self.root / gone.relative_to(source)).exists())
        self.assertIn('Upgrade content', (self.root / owned.relative_to(source)).read_text(encoding='utf-8'))
        self.assertEqual(user_file.read_text(), 'user skill')

    def test_failed_install_restores_original_files(self):
        installer = importlib.import_module('installer')
        self.write('AGENTS.md', 'Keep original\n')
        real = installer.atomic_write
        count = 0

        def failing(path, data):
            nonlocal count
            count += 1
            if count == 3:
                raise OSError('injected write failure')
            return real(path, data)

        with patch.object(installer, 'atomic_write', side_effect=failing):
            with self.assertRaises(OSError):
                installer.install(REPO, self.root)
        self.assertEqual((self.root / 'AGENTS.md').read_text(), 'Keep original\n')
        self.assertFalse((self.root / '.game-studio/install-state.json').exists())
        self.assertFalse((self.root / '.game-studio/install.lock').exists())

    def test_symlink_path_rejected(self):
        import os
        paths = importlib.import_module('paths')
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        try:
            os.symlink(outside, self.root / 'linked', target_is_directory=True)
        except OSError:
            self.skipTest('OS does not permit creating test symlinks')
        with self.assertRaises(ValueError):
            paths.confined(self.root, 'linked/input.md')

    def test_legacy_scalar_testing_strict(self):
        config = importlib.import_module('config')
        self.write('project.yaml', 'testing: {strict: true}\n')
        r = config.resolve(self.root)
        for kind in ['logic', 'integration', 'visual', 'ui', 'config']:
            self.assertTrue(r['values']['testing.strict.' + kind])

    def test_windows_junction_rejected(self):
        import os
        import subprocess
        if os.name != 'nt':
            self.skipTest('Windows junction capability')
        paths = importlib.import_module('paths')
        outside = Path(self.tmp.name) / 'junction-target'
        outside.mkdir()
        link = self.root / 'linked'
        command = "New-Item -ItemType Junction -Path '" + str(link).replace("'", "''") + "' -Target '" + str(outside).replace("'", "''") + "' | Out-Null"
        proc = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', command], capture_output=True)
        if proc.returncode != 0:
            self.skipTest('OS denied junction creation')
        try:
            with self.assertRaises(ValueError):
                paths.confined(self.root, 'linked/input.md')
            outside.rmdir()
            with self.assertRaises(ValueError):
                paths.plain(link)
            outside.mkdir()
        finally:
            os.rmdir(link)  # Removes this test-created junction, not its target.
        self.assertTrue(outside.is_dir())

    def test_edited_instruction_block_preserved(self):
        installer = importlib.import_module('installer')
        installer.install(REPO, self.root)
        p = self.root / 'AGENTS.md'
        edited = p.read_text(encoding='utf-8').replace('Codex Game Studios', 'User edited studio')
        p.write_text(edited, encoding='utf-8')
        with self.assertRaises(ValueError):
            installer.install(REPO, self.root)
        self.assertEqual(p.read_text(encoding='utf-8'), edited)

    def test_dry_run_missing_target_does_not_create_it(self):
        installer = importlib.import_module('installer')
        target = Path(self.tmp.name) / 'missing'
        installer.install(REPO, target, True)
        self.assertFalse(target.exists())

    def test_install_lock_precedes_target_preflight(self):
        installer = importlib.import_module('installer')
        self.write('.game-studio/install.lock', 'Another install in progress')
        with patch.object(installer, 'payload', side_effect=AssertionError('preflight before lock')):
            with self.assertRaisesRegex(ValueError, 'lock exists'):
                installer.install(REPO, self.root)
        self.assertEqual((self.root / '.game-studio/install.lock').read_text(), 'Another install in progress')

    def test_full_flags_cannot_relax_sections(self):
        config = importlib.import_module('config')
        self.write('project.yaml', 'modes: {rigor: full}\nworkflow_overrides: {edge_cases: false, tuning_knobs: false}\n')
        r = config.resolve(self.root)
        self.assertTrue(r['values']['workflow_overrides.edge_cases'])
        self.assertTrue(r['values']['workflow_overrides.tuning_knobs'])

    def test_custom_engine_fact_is_preserved(self):
        config = importlib.import_module('config')
        studio = importlib.import_module('studio')
        self.write('project.yaml', 'engine: {name: CustomEngine, version: "1.0"}\n')
        self.assertEqual(config.resolve(self.root)['values']['engine.name'], 'CustomEngine')
        studio.settings(self.root, 'engine.name=RenPy')
        self.assertEqual(config.resolve(self.root)['values']['engine.name'], 'RenPy')

    def test_atomic_write_preserves_preexisting_temp_collision(self):
        import os
        paths = importlib.import_module('paths')
        destination = self.root / 'output.json'
        collision = destination.with_name(destination.name + f'.studio-{os.getpid()}.tmp')
        collision.write_bytes(b'USER OWNED TEMP')
        with self.assertRaises(FileExistsError):
            paths.atomic_write(destination, b'NEW')
        self.assertEqual(collision.read_bytes(), b'USER OWNED TEMP')
        self.assertFalse(destination.exists())


if __name__ == '__main__':
    unittest.main()
