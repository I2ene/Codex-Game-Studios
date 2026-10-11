"""Bounded FORMAT regressions for evaluation obligations, not model pass claims.

Each check scopes related clauses to the relevant case or execution path. Human
comparison with the professional procedure is still required for semantic review.
"""
import re
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTING = ROOT / ".game-studio/resources/testing"


def case(text, number):
    match = re.search(r"^### Case " + re.escape(str(number)) + r":.*?(?=^### Case |\Z)", text, re.M | re.S)
    return match.group(0) if match else ""


def domain_checks(text):
    """Only obligations count; fixture text cannot stand in for a check."""
    active = False
    lines = []
    for line in text.splitlines():
        if line.startswith("**Domain checks") or line.startswith("## Applicable domain checks"):
            active = True
        elif line.startswith(("### Case ", "**Fixture", "**Input", "**Expected", "---")):
            active = False
        if active and line.startswith("- [ ]"):
            lines.append(line)
    return "\n".join(lines)


def missing_clauses(text, obligations):
    return [name for name, pattern in obligations.items()
            if not re.search(pattern, text, re.I | re.S)]


GODOT_FACTORY = {
    "named helper class": r"class_name",
    "static factory with defaults": r"static[^\n]*make_\*[^\n]*default parameters",
    "source header": r"Based on: design/gdd/player\.md",
    "confirmed framework API": r"confirmed[^\n]*(?:gdUnit4|framework)[^\n]*API",
    "existing test patterns": r"samples?[^\n]*existing test",
    "bounded GDD reads": r"(?:section|heading)[^\n]*(?:Formulas|Edge Cases)",
}
UNITY_HELPERS = {
    "assertions and factory files": r"GameAssertions\.cs[^\n]*GameFactory\.cs",
    "installed NUnit API": r"NUnit[^\n]*(?:installed|confirmed)[^\n]*(?:API|version)",
    "assembly usage note": r"usage note[^\n]*test assembly",
}


class EvaluationContractTests(unittest.TestCase):
    def test_player_case_requires_factory_sources_and_confirmed_framework(self):
        text = (TESTING / "skills/test-helpers.md").read_text(encoding="utf-8")
        self.assertEqual(missing_clauses(domain_checks(case(text, 1)), GODOT_FACTORY), [])

    def test_unity_case_requires_both_files_and_version_confirmed_assertions(self):
        text = (TESTING / "skills/test-helpers.md").read_text(encoding="utf-8")
        self.assertEqual(missing_clauses(domain_checks(case(text, 6)), UNITY_HELPERS), [])

    def test_signal_checks_bind_capture_and_arity_to_project_version(self):
        text = (TESTING / "skills/test-helpers.md").read_text(encoding="utf-8")
        common = text.split("## Applicable domain checks")[-1]
        obligations = {
            "shared mutable capture": r"signal[^\n]*Dictionary[^\n]*(?:captured|capture)[^\n]*bool",
            "emission and non-emission": r"emitted[^\n]*not.emitted",
            "version predicate": r"Godot 4\.5[^\n]*variadic[^\n]*older[^\n]*arity",
            "framework failure registration": r"framework[^\n]*failure[^\n]*runner[^\n]*continu",
        }
        self.assertEqual(missing_clauses(common, obligations), [])

    def test_team_checks_cover_parent_and_capability_scoped_parallel_paths(self):
        for path in sorted((TESTING / "skills").glob("team-*.md")):
            with self.subTest(team=path.stem):
                text = path.read_text(encoding="utf-8")
                self.assertTrue("**Parent execution path:**" in text, "missing parent path")
                self.assertTrue("**Authorized delegation path:**" in text, "missing delegated path")
                parent = text.split("**Parent execution path:**")[-1].split("**Authorized delegation path:**")[0]
                delegated = text.split("**Authorized delegation path:**")[-1].split("### Case ")[0]
                self.assertEqual(missing_clauses(parent, {
                    "unavailable or unauthorized host": r"unavailable or unauthorized",
                    "labeled discipline work": r"parent[^\n]*discipline[^\n]*label",
                    "results and blockers": r"results[^\n]*block",
                }), [])
                self.assertEqual(missing_clauses(delegated, {
                    "authorization tool and capacity preconditions": r"user authorization[^\n]*host tool[^\n]*capacity",
                    "independent concurrency only": r"independent[^\n]*concurrent",
                    "join dependent work": r"dependent[^\n]*(?:wait|after)[^\n]*results",
                    "actual participant records": r"actual[^\n]*participant[^\n]*(?:record|label)",
                }), [])
                # A header caveat cannot exempt contradictory assertions in a case.
                cases = text.split("### Case ", 1)[-1]
                self.assertNotRegex(cases, r"(?i)Agent calls|via Agent|all file writes delegated|no files are written by the orchestrator|orchestrator writes no files|orchestrator does not write it directly")
                for line in cases.splitlines():
                    if re.search(r"(?:launch|consult|issu|spawn).*simultaneous|single batch|before any result is awaited", line, re.I):
                        self.assertIn("delegated path", line.lower(), line)

    def test_other_domain_obligations_remain_in_their_applicable_cases(self):
        obligations = [
            ("consistency-check", "4", {"empty registry stops unassessed": r"NOT ASSESSED[^\n]*entity registry empty[^\n]*stop"}),
            ("content-audit", None, {"Unity discovery outside data": r"Unity[^\n]*Assets/[^\n]*without[^\n]*data/"}),
            ("test-flakiness", None, {"same-code comparison": r"both passed and failed[^\n]*no code change"}),
            ("architecture-decision", "5", {"accept preserves original date": r"Accepted[^\n]*preserve[^\n]*Date", "unblocks dependents": r"Blocked[^\n]*Ready"}),
            ("patch-notes", "1", {"published and archive copies": r"docs/patch-notes/v0\.4\.0\.md[^\n]*production/releases/v0\.4\.0/patch-notes\.md"}),
            ("test-evidence-review", None, {"strict fallback chain": r"testing\.strict\.<type>[^\n]*legacy[^\n]*coding-standards"}),
        ]
        for name, number, checks in obligations:
            with self.subTest(resource=name, case=number):
                text = (TESTING / "skills" / (name + ".md")).read_text(encoding="utf-8")
                scope = domain_checks(case(text, number) if number else text)
                self.assertEqual(missing_clauses(scope, checks), [])

    def test_review_mode_alternatives_keep_checks_in_separate_blocks(self):
        for name, number, labels in [
            ("create-epics", 3, ["full mode", "override"]),
            ("map-systems", 5, ["lean mode", "solo mode"]),
        ]:
            with self.subTest(resource=name):
                text = case((TESTING / "skills" / (name + ".md")).read_text(encoding="utf-8"), number)
                self.assertFalse("**Domain checks:**" in text, "unscoped checks mix mutually exclusive modes")
                for label in labels:
                    self.assertTrue("**Domain checks (" + label + "):**" in text, label)

    def test_non_team_contracts_allow_labeled_parent_expertise(self):
        for name, number, clauses in [
            ("art-bible", 1, {"all sections": r"Every section[^\n]*parent[^\n]*authorized delegate",
                              "coherent batch": r"Sections 2.*4[^\n]*coherent[^\n]*one section at a time"}),
            ("art-bible", 2, {"revision ownership": r"flagged section[^\n]*parent[^\n]*authorized delegate"}),
            ("create-architecture", 1, {"both reviews": r"TD-ARCHITECTURE[^\n]*LP-FEASIBILITY[^\n]*parent[^\n]*authorized delegate",
                                       "parent gate inputs": r"parent[^\n]*gate definition[^\n]*context"}),
        ]:
            with self.subTest(resource=name, case=number):
                text = domain_checks(case((TESTING / "skills" / (name + ".md")).read_text(encoding="utf-8"), number))
                self.assertEqual(missing_clauses(text, clauses), [])
                self.assertNotRegex(text, r"never from the orchestrator|not by the orchestrator|parent session does not read")
        contract = (ROOT / ".agents/skills/gs-dev-story/references/CONTRACT.md").read_text(encoding="utf-8")
        self.assertRegex(contract, r"Source and test files[^\n]*parent[^\n]*authorized delegates")
        self.assertNotIn("this orchestrator writes none directly", contract)
        sprint = (ROOT / ".agents/skills/gs-sprint-plan/references/workflow.md").read_text(encoding="utf-8")
        self.assertRegex(sprint, r"\x60full\x60[^\n]*director gates[^\n]*parent[^\n]*authorized delegation")
        unity = case((TESTING / "roles/unity-specialist.md").read_text(encoding="utf-8"), 2)
        self.assertNotRegex(unity, r"Agent grant|grant covers")
        self.assertRegex(unity, r"professional scope[^\n]*host[^\n]*authorization")
        template = (ROOT / ".game-studio/resources/docs/templates/systems-index.md").read_text(encoding="utf-8")
        workflow = (ROOT / ".agents/skills/gs-map-systems/references/workflow.md").read_text(encoding="utf-8")
        for text in (template, workflow):
            self.assertRegex(text, r"Order (?:\||/) System (?:\||/) Priority (?:\||/) Layer (?:\||/) Expertise")
            self.assertNotIn("Delegation brief (s)", text)

    def test_game_ability_task_api_is_not_rewritten_as_host_delegation(self):
        text = tomllib.loads((ROOT / ".codex/agents/gs-ue-gas-specialist.toml").read_text(encoding="utf-8"))["developer_instructions"]
        cleanup = next(line for line in text.splitlines() if "Custom Ability Tasks" in line)
        self.assertTrue(re.search(r"call `EndTask\(\)`.*clean", cleanup), cleanup)

    def test_engine_routing_uses_host_authorization_without_fictional_grants(self):
        expected = {
            "godot": ["godot-gdscript-specialist", "godot-csharp-specialist", "godot-shader-specialist", "godot-gdextension-specialist"],
            "unity": ["unity-dots-specialist", "unity-shader-specialist", "unity-addressables-specialist", "unity-ui-specialist"],
            "unreal": ["ue-gas-specialist", "ue-blueprint-specialist", "ue-replication-specialist", "ue-umg-specialist"],
        }
        for engine, routes in expected.items():
            with self.subTest(engine=engine):
                path = ROOT / f".codex/agents/gs-{engine}-specialist.toml"
                instructions = tomllib.loads(path.read_text(encoding="utf-8"))["developer_instructions"]
                section = instructions.split("## Sub-Specialist Orchestration")[-1].split("\n## ")[0]
                self.assertFalse(re.search(r"(?i)tools:`? grant|enforced by the\s+harness", instructions), "fictional role grant")
                self.assertEqual(missing_clauses(section, {
                    "actual tools and authorization": r"actual host tools[^\n]*user authorization",
                    "parent fallback": r"parent[^\n]*expertise[^\n]*label",
                    "real participants": r"actual[^\n]*participant",
                }), [])
                for route in routes:
                    self.assertIn(route, section)


if __name__ == "__main__":
    unittest.main()
