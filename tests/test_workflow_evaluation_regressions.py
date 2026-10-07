"""Bounded FORMAT guards for workflow branches and downstream obligations.

These checks inspect applicable instructions, not model execution. Manual review
must still trace the same cases through their complete native procedures.
"""
import re
import unittest

from test_evaluation_contracts import ROOT, TESTING, case, domain_checks, missing_clauses


def section(text, heading):
    match = re.search(r"^" + re.escape(heading) + r"\n.*?(?=^#{1,3} |\Z)", text, re.M | re.S)
    return match.group(0) if match else ""


def scoped_checks(text, label):
    match = re.search(r"^\*\*Domain checks \(" + re.escape(label) + r"\):\*\*\n"
                      r"(.*?)(?=^\*\*|^---|\Z)", text, re.M | re.S)
    return match.group(1) if match else ""


class WorkflowBranchTests(unittest.TestCase):
    def test_art_bible_tail_allows_parent_drafts_with_section_approval(self):
        text = (ROOT / ".agents/skills/gs-art-bible/references/workflow.md").read_text(encoding="utf-8")
        protocol = section(text, "## Collaborative Protocol")
        self.assertNotRegex(protocol, r"(?i)never draft a section yourself|no section may be written from the orchestrator")
        self.assertEqual(missing_clauses(protocol, {
            "applicable specialist work": r"parent[^\n]*specialist expertise[^\n]*authorized delegate",
            "accurate authorship": r"label[^\n]*parent[^\n]*actual participant",
            "individual approvals": r"each section[^\n]*approval",
            "surface differences": r"disagreements[^\n]*user",
        }), [])
        checks = domain_checks(case((TESTING / "skills/art-bible.md").read_text(encoding="utf-8"), 1))
        self.assertEqual(missing_clauses(checks, {
            "unavailable delegation in collaborative mode": r"collaborative[^\n]*delegation[^\n]*unavailable[^\n]*parent",
            "downstream protocol": r"Collaborative Protocol[^\n]*(?:draft|write)",
        }), [])

    def test_release_phase_five_collects_applicable_completed_parent_reviews(self):
        text = (ROOT / ".agents/skills/gs-team-release/references/workflow.md").read_text(encoding="utf-8")
        gate = section(text, "### Phase 5: Go/No-Go")
        self.assertNotRegex(gate, r"(?i)if spawned|when it is not\s+spawned|cannot spawn agents")
        self.assertEqual(missing_clauses(gate, {
            "technical review parent path": r"full[^\n]*technical-director[^\n]*parent[^\n]*authorized",
            "mode skips independent of spawn": r"lean[^\n]*solo[^\n]*(?:skip|not run)",
            "collect security by applicability": r"security-engineer[^\n]*online[^\n]*multiplayer[^\n]*player data",
            "collect network by applicability": r"network-programmer[^\n]*multiplayer",
            "phase four join": r"Phase 4[^\n]*(?:localization|performance)[^\n]*analytics",
            "record evidence provenance": r"each[^\n]*(?:result|assessment)[^\n]*source[^\n]*parent[^\n]*participant",
            "unknown never approval": r"NOT ASSESSED[^\n]*never[^\n]*approval",
        }), [])
        checks = domain_checks(case((TESTING / "skills/team-release.md").read_text(encoding="utf-8"), 3))
        self.assertEqual(missing_clauses(checks, {
            "online parent assessments survive aggregation": r"parent[^\n]*security[^\n]*network[^\n]*technical-director[^\n]*Phase 5",
        }), [])

    def test_missing_and_unassessable_inputs_have_separate_result_branches(self):
        architecture = case((TESTING / "skills/architecture-review.md").read_text(encoding="utf-8"), 4)
        readiness = case((TESTING / "skills/story-readiness.md").read_text(encoding="utf-8"), 7)
        for text, labels in [(architecture, ["4a", "4b"]), (readiness, ["7a", "7b", "7c"])]:
            self.assertNotIn("**Domain checks:**", text, "unconditional merged checks mix exclusive inputs")
            for label in labels:
                self.assertTrue(scoped_checks(text, label), "missing result branch " + label)
        missing_master = scoped_checks(architecture, "4a")
        malformed_adr = scoped_checks(architecture, "4b")
        self.assertIn("no docs/architecture/architecture.md", missing_master)
        self.assertNotIn("none carries a scannable section", missing_master)
        self.assertIn("retrofit", malformed_adr)
        self.assertIn("Not assessed", malformed_adr)
        self.assertNotIn("no docs/architecture/architecture.md", malformed_adr)
        empty = scoped_checks(readiness, "7a")
        unknown = scoped_checks(readiness, "7b")
        absent_adr = scoped_checks(readiness, "7c")
        self.assertIn("no stories in scope", empty)
        self.assertNotIn("ADR check", empty)
        self.assertIn("NOT ASSESSED", unknown)
        self.assertIn("retrofit", unknown)
        self.assertNotIn("no stories in scope", unknown)
        self.assertIn("BLOCKED", absent_adr)
        self.assertIn("referenced ADR is missing", absent_adr)
        self.assertNotIn("retrofit", absent_adr)

        planned = case((TESTING / "skills/review-all-gdds.md").read_text(encoding="utf-8"), 3)
        self.assertNotIn("**Domain checks:**", planned)
        self.assertIn("CONCERNS", scoped_checks(planned, "3a"))
        self.assertNotIn("Verdict is FAIL", scoped_checks(planned, "3a"))
        self.assertIn("Verdict is FAIL", scoped_checks(planned, "3b"))

    def test_retrofit_completion_requires_summary_quick_reference_and_readback(self):
        text = case((TESTING / "skills/design-system.md").read_text(encoding="utf-8"), 2)
        checks = domain_checks(text)
        self.assertEqual(missing_clauses(checks, {
            "replace placeholder summary": r"Summary[^\n]*replac[^\n]*To be designed",
            "quick reference sources": r"Quick reference[^\n]*Layer[^\n]*Priority[^\n]*Key deps",
            "file readback prevents false completion": r"read[^\n]*file[^\n]*Summary[^\n]*Quick reference[^\n]*placeholder",
            "preserve completed bodies": r"complete sections[^\n]*not[^\n]*(?:re-authored|overwritten)",
        }), [])
        self.assertNotRegex(checks, r"(?i)only (?:fills?|writes?) (?:the )?three")
        new_gdd = domain_checks(case((TESTING / "skills/design-system.md").read_text(encoding="utf-8"), 1))
        self.assertRegex(new_gdd, r"read[^\n]*file[^\n]*Summary[^\n]*Quick reference")

    def test_release_parallel_quality_and_readiness_join_at_go_no_go(self):
        text = (TESTING / "skills/team-release.md").read_text(encoding="utf-8")
        for number in [1, 3]:
            checks = domain_checks(case(text, number))
            self.assertNotRegex(checks, r"(?i)results[^\n]*(?:precede|before) Phase 4")
            self.assertRegex(checks, r"Phase 3[^\n]*results[^\n]*Phase 5")
        shared = text.split("## Applicable domain checks")[-1]
        self.assertEqual(missing_clauses(shared, {
            "parallel condition": r"Phases? 3[^\n]*4[^\n]*independent[^\n]*authorization[^\n]*tools[^\n]*capacity",
            "serial and queue fallback": r"parent[^\n]*sequential[^\n]*queue",
            "real dependency remains": r"data dependenc[^\n]*wait",
        }), [])
        workflow = (ROOT / ".agents/skills/gs-team-release/references/workflow.md").read_text(encoding="utf-8")
        phase_four = section(workflow, "### Phase 4: Localization, Performance, and Analytics")
        self.assertRegex(phase_four, r"Phase 3[^\n]*independent")
        self.assertRegex(phase_four, r"dependenc[^\n]*wait")

    def test_team_scope_and_blockers_do_not_require_real_delegates(self):
        for p in sorted((ROOT / ".agents/skills").glob("gs-team-*/references/workflow.md")):
            with self.subTest(team=p.parent.parent.name):
                text = p.read_text(encoding="utf-8")
                start = text.index("**Announce the active set")
                stop = text.find("\n## ", start)
                announcement = text[start:stop if stop >= 0 else None]
                self.assertNotRegex(announcement, r"(?i)agents this run will actually\s+spawn|it is spawned, not")
                self.assertRegex(announcement, r"Parent coverage[^\n]*actual delegated participants")
                recovery = section(text, "## Error Recovery Protocol")
                self.assertRegex(recovery, r"(?i)parent work[^\n]*authorized delegate[^\n]*BLOCKED")
                self.assertIn("partial report", recovery)

        shared = (ROOT / ".game-studio/resources/docs/error-recovery-protocol.md").read_text(encoding="utf-8")
        self.assertNotRegex(shared, r"never fill[^\n]*content of your own")
        self.assertRegex(shared, r"parent work[^\n]*authorized delegate[^\n]*BLOCKED")
        self.assertRegex(shared, r"parent assessment\s+can satisfy[^\n]*actually performed")
        narrative = (ROOT / ".agents/skills/gs-team-narrative/references/workflow.md").read_text(encoding="utf-8")
        self.assertNotIn("do not read the gate file in this session", narrative)
        self.assertRegex(narrative, r"parent[^\n]*read the gate definition[^\n]*required context")

    def test_specialist_required_means_expertise_not_mandatory_agent_call(self):
        text = (ROOT / ".agents/skills/gs-design-system/references/workflow.md").read_text(encoding="utf-8")
        for letter in ["B", "C"]:
            paragraph = next(line for line in text.splitlines()
                             if line.startswith("**Do NOT draft Section " + letter))
            self.assertRegex(paragraph, r"applicable[^\n]*expertise[^\n]*parent[^\n]*authorized")
        protocol = section(text, "## Collaborative Protocol")
        self.assertRegex(protocol, r"Specialist routing[^\n]*parent[^\n]*authorized delegate")


if __name__ == "__main__":
    unittest.main()
