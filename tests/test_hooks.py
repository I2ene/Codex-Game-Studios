from pathlib import Path
import sys
import tempfile
import unittest
import importlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.game-studio/runtime'))


class HookTests(unittest.TestCase):
    def test_invalid_event_and_session_context(self):
        hooks = importlib.import_module('hooks')
        with self.assertRaises(ValueError):
            hooks.handle({'hook_event_name': 'Notification'})
        with tempfile.TemporaryDirectory() as root:
            p = Path(root)
            (p / '.game-studio').mkdir()
            result = hooks.handle({'hook_event_name': 'SessionStart', 'cwd': root, 'session_id': 'fixture-session', 'source': 'startup'})
            self.assertEqual(result['hookSpecificOutput']['hookEventName'], 'SessionStart')
            self.assertIn('ABSENT', result['hookSpecificOutput']['additionalContext'])

    def test_post_compact_uses_shared_output_fields(self):
        hooks = importlib.import_module('hooks')
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / '.game-studio').mkdir()
            result = hooks.handle({'hook_event_name': 'PostCompact', 'cwd': root, 'session_id': 'fixture-session'})
            self.assertNotIn('hookSpecificOutput', result)
            self.assertIn('ABSENT', result['systemMessage'])

    def test_recovery_serializes_valid_yaml_date(self):
        hooks = importlib.import_module('hooks')
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / '.game-studio').mkdir()
            (Path(root) / 'project.yaml').write_text('framework: {last_upgraded: 2026-09-25}\n', encoding='utf-8')
            for event in ['SessionStart', 'PostCompact']:
                result = hooks.handle({'hook_event_name': event, 'cwd': root, 'session_id': 'fixture-session'})
                self.assertIn('2026-09-25', str(result))

    def test_participant_event_and_no_permission_grants(self):
        hooks = importlib.import_module('hooks')
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / '.game-studio').mkdir()
            e = {'hook_event_name': 'SubagentStart', 'cwd': root, 'session_id': 'fixture', 'agent_id': 'real-field', 'agent_type': 'gs-qa-lead'}
            result = hooks.handle(e)
            self.assertNotIn('permissionDecision', str(result))
            self.assertEqual(hooks.handle({**e, 'hook_event_name': 'PreToolUse', 'tool_name': 'Bash', 'tool_input': {'command': 'git push'}}), {})

    def test_definitions_have_real_events_and_windows_override(self):
        hooks = importlib.import_module('hooks')
        definition = hooks.definition(Path('/project with spaces'), sys.executable)
        self.assertNotIn('PermissionRequest', definition['hooks'])
        for groups in definition['hooks'].values():
            self.assertEqual(groups[0]['hooks'][0]['type'], 'command')
            self.assertIn('commandWindows', groups[0]['hooks'][0])


if __name__ == '__main__':
    unittest.main()
