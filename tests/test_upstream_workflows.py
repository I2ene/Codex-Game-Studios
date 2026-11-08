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

    def test_split_checkpoint_routes_keep_disabled_work_and_recover_real_artifacts(self):
        phases = {
            'design-system': ('3-file-skeleton.md', '4-section-design.md', '5-post-design.md'),
            'ux-design': ('3-file-skeleton.md', '4-authoring.md', '5-crossref-handoff.md'),
            'prototype': ('4-plan.md', 'spike-mode.md'),
        }
        for skill, files in phases.items():
            route = self.text(skill)
            for phase in files:
                with self.subTest(skill=skill, phase=phase):
                    self.assertIn(phase, route)
                    body = self.text(skill, phase)
                    self.assertNotIn('production/session-state/active.md', body)
                    self.assertRegex(body, r"(?is)checkpoint.{0,140}enabled.{0,240}checkpoint --save")
                    self.assertRegex(body, r"(?i)DISABLED[^\n]*(?:skip|continue|omit)")
            if skill != 'prototype':
                resume = route.split('## 7. Recovery & Resume', 1)[1].split('\n## ', 1)[0]
                self.assertNotIn('production/session-state/active.md', resume)
                self.assertRegex(resume, r"(?s)recover --root <project-root>.*?PRESENT.*?DISABLED.*?actual")
                self.assertIn('next incomplete section', resume)
        spike = self.text('prototype', 'spike-mode.md')
        self.assertRegex(spike, r"(?s)SPIKE-NOTE\.md.*?DISABLED[^\n]*(?:skip|continue|omit)")
        self.assertIn('brief', spike)
        self.assertIn('sprint', spike)

    def test_story_evidence_producer_and_both_consumers_share_receipt_contract(self):
        docs = ROOT / '.game-studio/resources/docs/review-receipts.md'
        link = '.game-studio/resources/docs/review-receipts.md#story-capture-receipts'
        producer = self.text('dev-story')
        self.assertIn(link, producer)
        self.assertIn('--report <evidence.md> --output <evidence.receipt.json>', producer)
        for skill in ('story-done', 'test-evidence-review'):
            with self.subTest(skill=skill):
                text = self.text(skill)
                self.assertIn(link, text)
                self.assertIn('--receipt <evidence.receipt.json>', text)
                self.assertNotIn('stamp.json', text)
        contract = docs.read_text(encoding='utf-8').split('## Story capture receipts', 1)[1]
        self.assertIn('production/qa/evidence/<story-slug>/evidence.receipt.json', contract)
        self.assertRegex(contract, r"(?s)report_status.*?required_unresolved.*?unchanged_inputs")
        self.assertRegex(contract, r"(?is)companion is absent[^.]*freshness as NOT ASSESSED")
        self.assertRegex(contract, r"(?is)source.{0,120}POTENTIALLY STALE")
        self.assertRegex(contract, r"(?is)required image.{0,200}evidence gate")

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
