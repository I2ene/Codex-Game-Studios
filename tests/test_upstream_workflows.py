"""FORMAT regression checks for native workflow adapters, not game evidence."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('architecture-decision', 'architecture-review', 'create-architecture', 'create-epics', 'create-stories', 'dev-story', 'gate-check', 'story-done', 'story-readiness', 'start')

class WorkflowAdapterTests(unittest.TestCase):
    def text(self, skill, name='workflow.md'):
        return (ROOT / '.agents/skills' / ('gs-' + skill) / 'references' / name).read_text(encoding='utf-8')

    def test_receipts_use_companion_arguments(self):
        load = self.text('architecture-review', '1-load.md')
        save = self.text('architecture-review', '8-write.md')
        self.assertIn('--receipt <companion.json>', load)
        self.assertIn('--report <report.md> --output <companion.json>', save)
        self.assertNotIn('Reviewed-Content-Hash', self.text('architecture-review', '7-report.md'))

    def test_stage_setting_is_native_assignment(self):
        text = self.text('gate-check', '6-update-stage.md')
        self.assertIn('project.stage=<new-stage>', text)
        self.assertNotIn('stage_txt', text)
        self.assertNotIn('write both stage files', text)

    def test_checkpoint_disabled_and_explicit_save(self):
        for skill in ('dev-story', 'story-done'):
            with self.subTest(skill=skill):
                text = self.text(skill)
                self.assertIn('DISABLED', text)
                self.assertIn('checkpoint --save <authored-file>', text)
                self.assertNotIn('--root <project-root> checkpoint', text)
                self.assertNotIn('production/session-state/active.md', text)

    def test_no_obsolete_host_or_shadow_phases(self):
        for name in NAMES:
            base = ROOT / '.agents/skills' / ('gs-' + name)
            for path in base.rglob('*.md'):
                with self.subTest(path=str(path)):
                    self.assertNotIn('.claude/', path.read_text(encoding='utf-8'))
                    if path.parent.name == 'references' and path.parent.parent.name == 'references':
                        self.assertFalse((path.parent.parent / path.name).exists(), 'duplicate phase authorities')

    def test_phase_routes_are_resolvable_links(self):
        for name in ('gate-check', 'architecture-review', 'architecture-decision', 'create-architecture'):
            base = ROOT / '.agents/skills' / ('gs-' + name) / 'references'
            text = self.text(name)
            for phase in base.glob('[0-9]*.md'):
                with self.subTest(phase=str(phase)):
                    self.assertRegex(text, r'\]\(' + re.escape(phase.name) + r'\)')
