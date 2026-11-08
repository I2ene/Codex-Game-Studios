"""Executable behavior checks for the 1.2.0 upstream alignment."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".game-studio/runtime"))
import checks
import config
import studio


class UpstreamBehaviorTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "fixture with spaces"
        self.root.mkdir()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
        return target

    def test_duplicate_yaml_merges_for_inspection_but_blocks_writes(self):
        path = self.write("project.yaml", "modes:\n  rigor: full\n  automation: guided\nmodes:\n  automation: autonomous\n")
        original = path.read_bytes()
        result = config.resolve(self.root)
        self.assertEqual(result["values"]["modes.rigor"], "full")
        self.assertEqual(result["values"]["modes.automation"], "autonomous")
        self.assertTrue(any("modes" in note and "1" in note and "4" in note
                            for note in result["notes"]), result["notes"])
        with self.assertRaises(ValueError):
            studio.settings(self.root, "modes.automation=guided")
        self.assertEqual(path.read_bytes(), original)

    def test_dotted_yaml_key_must_not_shadow_nested_permission_boundary(self):
        self.write("project.yaml", "modes.rigor: minimal\nmodes: {rigor: full}\n")
        with self.assertRaisesRegex(ValueError, "Ambiguous setting"):
            config.resolve(self.root)

    def test_receipt_keeps_required_absence_and_out_of_scope_drift_visible(self):
        self.write("a.md", "# A\n")
        self.write("b.md", "# B\n")
        self.write("review.md", "# Actual review\n")
        stamp = checks.receipts(self.root, "hash", ["a.md", "b.md", "missing.md"], report="review.md")
        self.write("receipt.json", json.dumps(stamp))
        self.assertFalse(checks.receipts(self.root, "check", stamp["patterns"], "receipt.json")["unchanged_inputs"])
        self.write("b.md", "# Changed B\n")
        observations = checks.receipts(self.root, "check", ["a.md"], "receipt.json")["observations"]
        self.assertEqual({row["path"]: row["status"] for row in observations}, {"a.md": "UNCHANGED", "b.md": "CHANGED"})

    def test_adr_number_resolves_to_slug_and_cycle_does_not_include_descendant(self):
        def adr(number, slug, dependency):
            self.write(f"docs/architecture/adr-{number:04d}-{slug}.md",
                       f"# ADR-{number:04d}: {slug}\n\n## ADR Dependencies\n\n| **Depends On** | {dependency} |\n")
        adr(1, "a", "ADR-0002")
        adr(2, "b", "ADR-0001")
        adr(3, "dependent", "ADR-0001")
        adr(4, "unfinished", "[ADR IDs this depends on, or none]")
        result = checks.dependencies(self.root)
        self.assertEqual(result["missing"], [])
        self.assertEqual({Path(node).stem for node in result["cycle_members"]}, {"adr-0001-a", "adr-0002-b"})
        self.assertEqual([Path(node).stem for node in result["blocked_by_cycle"]], ["adr-0003-dependent"])
        self.assertEqual([Path(node).stem for node in result["unfilled_dependencies"]], ["adr-0004-unfinished"])

    def test_gdd_placeholders_and_fenced_headings_are_not_complete_sections(self):
        self.write("design/gdd/combat.md", "# Combat\n\n## Overview\n[To be designed]\n\n" +
                   "~~~text\n## Formulas\n~~~\n\n## Detailed Design\nReal rules.\n")
        document = checks.gdd_structure(self.root, ["design/gdd/*.md"])["documents"][0]
        self.assertIn("Overview", document["placeholder"])
        self.assertIn("Formulas", document["absent"])
        self.assertIn("Detailed Rules", document["present"])


if __name__ == "__main__":
    unittest.main()
