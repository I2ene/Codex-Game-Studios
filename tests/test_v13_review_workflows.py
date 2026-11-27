"""Regressions for accepted file scope and resolved engine workflow contracts."""

import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def workflow(skill, name):
    return (ROOT / '.agents' / 'skills' / ('gs-' + skill) / 'references' / name).read_text(encoding='utf-8')


class ReviewWorkflowTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('git'), 'Git unavailable')
    def test_documented_accept_commits_only_the_agreed_files(self):
        phase = workflow('prototype', 'one-shot-4-change.md').split('- **Accept:**', 1)[1].split('- **Undo it:**', 1)[0]
        add = re.search(r'`(git [^`\n]*\badd [^`\n]+)`', phase).group(1)
        commit = re.search(r'`(git [^`\n]*\bcommit [^`\n]+)`', phase).group(1)

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            index = root / '.git' / 'iteration.index'
            import os
            env = dict(os.environ, GIT_INDEX_FILE=str(index))

            def git(*args):
                result = subprocess.run(['git', *args], cwd=root, env=env, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                return result.stdout.strip()

            def write(path, content):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding='utf-8')

            git('init', '-q')
            git('config', 'user.name', 'Iteration Test')
            git('config', 'user.email', 'iteration@example.invalid')
            code = 'prototypes/demo/config.js'
            notes = 'prototypes/demo/private-notes.txt'
            staged = 'prototypes/demo/other.js'
            write(code, 'speed = 1;\n')
            write(staged, 'before\n')
            git('add', '--', code, staged)
            git('commit', '-qm', 'initial')
            write(code, 'speed = 2;\n')
            write(notes, 'outside the accepted change\n')
            write(staged, 'staged elsewhere\n')
            git('add', '--', staged)
            original_index_entry = git('ls-files', '--stage', '--', staged)
            write(staged, 'further hand edits\n')

            for command in (add, commit):
                paths = 'prototypes/demo' if '<the paths added>' in command else code
                command = (command.replace('<the paths added>', paths).replace('<agreed file paths>', code)
                           .replace('<name>', 'demo').replace('<N>', '1').replace('<what>', 'speed')
                           .replace("<the brief's path>", 'prototypes/demo/brief.md'))
                git(*shlex.split(command)[1:])

            self.assertEqual(git('diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD').splitlines(), [code])
            self.assertEqual(git('show', f'HEAD:{code}'), 'speed = 2;')
            self.assertEqual(git('ls-files', '--stage', '--', staged), original_index_entry)
            self.assertEqual(git('ls-files', '--others', '--exclude-standard', '--', notes), notes)
            self.assertEqual((root / staged).read_text(encoding='utf-8'), 'further hand edits\n')

    def test_setup_verifies_actual_pin_and_custom_project_references_before_reporting(self):
        setup = workflow('setup-engine', 'workflow.md')
        verify = workflow('setup-engine', '8-verify.md').split('## 8.5', 1)[0]
        summary = workflow('setup-engine', '12-output-summary.md')
        self.assertIn('## 8. Verify project reference routing', setup)
        self.assertNotIn('AGENTS.md Import', setup)
        self.assertIn('`configured_engine`', verify)
        self.assertIn('`configured_version`', verify)
        self.assertIn('`project.root`', verify)
        self.assertIn('`project.documents`', verify)
        self.assertIn('`DIFFERS`', verify)
        self.assertIn('`NOT ASSESSED`', verify)
        self.assertIn('Section 8', summary)
        self.assertIn('project.documents', summary)
        self.assertNotIn('[updated]', next(line for line in summary.splitlines() if line.startswith('AGENTS.md:')))
        self.assertNotIn('docs/engine-reference/<engine>', summary)

        command = re.search(r'(?m)^python \.game-studio/runtime/studio\.py engine-reference --root <project-root>$', verify)
        self.assertIsNotNone(command)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            reference = root / 'team/verified/web'
            reference.mkdir(parents=True)
            (reference / 'VERSION.md').write_text('| Engine Version | 8.3.4 |\n', encoding='utf-8')
            (root / 'project.yaml').write_text('engine:\n  name: Web\n  version: "8.3.4"\n  reference_root: team/verified/web\n', encoding='utf-8')
            argv = shlex.split(command.group())
            argv[:2] = [sys.executable, str(ROOT / argv[1])]
            argv[-1] = str(root)
            result = subprocess.run(argv, capture_output=True, encoding='utf-8', text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            facts = json.loads(result.stdout)
            self.assertEqual((facts['configured_engine'], facts['configured_version']), ('Web', '8.3.4'))
            self.assertEqual(facts['project']['root'], 'team/verified/web')
            self.assertEqual(facts['project']['documents']['VERSION.md'], 'team/verified/web/VERSION.md')

    def test_dev_story_engine_check_routes_resolved_documents_through_review_and_summary(self):
        story = workflow('dev-story', 'workflow.md')
        routing = story.split('## Phase 4:', 1)[1].split('## Phase 5:', 1)[0]
        brief = story.split('**Then run the engine check**', 1)[-1].split('## Phase 6:', 1)[0]
        summary = story.split('## Phase 7:', 1)[1]
        self.assertIn('lead-programmer', routing)
        self.assertNotIn('docs/engine-reference/', routing)
        self.assertNotIn('docs/engine-reference/', brief)
        for value in ('project.root', 'project.documents', 'parent', 'delegate', 'NOT ASSESSED'):
            self.assertIn(value, brief)
        for value in ('engine check', 'participant', 'reference'):
            self.assertIn(value, summary.lower())

    def test_dev_story_routes_new_replay_errors_through_the_difference_decision(self):
        text = workflow('dev-story', 'workflow.md')
        replay = text.split('**A grown game: the same-seed run.**', 1)[1].split('No such folder:', 1)[0]
        difference = replay.split('**`match no`:**', 1)[1].split('- **', 1)[0]
        self.assertIn('Options: Yes', difference)
        self.assertIn('accepted` row', difference)
        self.assertIn('INCOMPLETE', difference)
        self.assertRegex(replay, r'(?is)errors.*already present.*new errors.*same difference decision')
