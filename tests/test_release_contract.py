"""Release/source contracts with negative cases; no model or game quality claim."""
import csv
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".game-studio/runtime"))
import installer
spec = importlib.util.spec_from_file_location("upstream_audit", ROOT / "tools/upstream_audit.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class ReleaseContractTests(unittest.TestCase):
    def test_development_tools_never_enter_manifest_or_consumer(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            target = Path(temporary) / "consumer"
            for name, body in {
                ".agents/skills/gs-sample/SKILL.md": "Native skill",
                ".codex/agents/gs-sample.toml": "Native role",
                ".game-studio/VERSION": "2.2.0",
                ".game-studio/AGENTS.fragment.md": "Native instructions",
                ".agents/skills/speckit-plan/SKILL.md": "Developer-only instruction",
                ".specify/memory/constitution.md": "Developer-only rules",
                "specs/001-port/spec.md": "Development specification",
            }.items():
                p = source / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(body, encoding="utf-8")
            manifest = installer.build_manifest(source)
            self.assertEqual(len(manifest["files"]), 4)
            installer.install(source, target)
            self.assertTrue((target / ".agents/skills/gs-sample/SKILL.md").is_file())
            self.assertFalse((target / ".agents/skills/speckit-plan").exists())
            self.assertFalse((target / ".specify").exists())
            self.assertFalse((target / "specs").exists())
            self.assertEqual(installer.install(source, target)["write"], [])

    def test_release_names_and_aliases_are_actual_discoverable_files(self):
        contract = json.loads((ROOT / ".game-studio/entrypoints.json").read_text(encoding="utf-8"))
        actual = {p.parent.name for p in (ROOT / ".agents/skills").glob("gs-*/SKILL.md")}
        self.assertEqual(actual, set(contract["skills"]))
        self.assertEqual({p.stem for p in (ROOT / ".codex/agents").glob("gs-*.toml")}, set(contract["roles"]))
        for old, canonical in contract["aliases"].items():
            self.assertIn(old, actual)
            self.assertIn(canonical, actual)
            self.assertNotEqual(old, canonical)

    def test_missing_mandated_installed_helper_is_rejected(self):
        validator_spec = importlib.util.spec_from_file_location("helper_validator", ROOT / "tools/validate.py")
        validator = importlib.util.module_from_spec(validator_spec)
        validator_spec.loader.exec_module(validator)
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            skill = root / ".agents/skills/gs-example/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("Run `.game-studio/scripts/test-scaffold.sh web`; do not write by hand.", encoding="utf-8")
            errors = validator.native_reference_errors(root)
            self.assertTrue(any("missing installed helper" in e and "test-scaffold.sh" in e for e in errors))
            helper = root / ".game-studio/scripts/test-scaffold.sh"
            helper.parent.mkdir(parents=True)
            helper.write_text("# fixture", encoding="utf-8")
            self.assertEqual(validator.native_reference_errors(root), [])

    def test_story_close_does_not_defer_unrun_testable_persistence(self):
        text = (ROOT / ".game-studio/resources/testing/skills/story-done.md").read_text(encoding="utf-8")
        feel = text.split("**Case 2a", 1)[1].split("**Case 2b", 1)[0]
        persistence = text.split("**Case 2b", 1)[1].split("**Case 2c", 1)[0]
        self.assertIn("subjective feel", feel)
        self.assertIn("COMPLETE WITH NOTES is permitted", feel)
        self.assertNotIn("Pickup state persists", feel)
        self.assertIn("Pickup state persists", persistence)
        self.assertIn("mark it UNTESTED, never DEFERRED", persistence)
        self.assertIn("default blocking Logic gate", persistence)
        self.assertIn("at best NOT ASSESSED, never COMPLETE WITH NOTES", persistence)
        self.assertNotIn("**Domain checks:**", text.split("### Case 2:", 1)[1].split("### Case 3:", 1)[0])

    def test_map_catches_semantic_disposition_lie_and_missing_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "docs").mkdir()
            (root / "native.md").write_text("adapted", encoding="utf-8")
            fields = ["source_base", "source_target", "git_status", "source_before", "source_after",
                      "source_purpose", "native_after", "disposition", "rationale", "verification"]
            row = dict(zip(fields, ["old", "new", "M", "source.md", "source.md", "workflow",
                                   "native.md", "reuse", "reuse source", "fixture test"]))
            def write(rows):
                with (root / "docs/upstream-file-map.tsv").open("w", encoding="utf-8", newline="") as stream:
                    writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t")
                    writer.writeheader()
                    writer.writerows(rows)
            def git_fixture(_root, *args):
                if args[0] == "diff":
                    return b"M\0source.md\0"
                return b"original"
            with patch.object(audit, "git", side_effect=git_fixture):
                write([row])
                self.assertTrue(any("byte-for-byte" in e for e in audit.audit(root, "old", "new")["errors"]))
                row["disposition"] = "host adaptation"
                write([row])
                self.assertEqual(audit.audit(root, "old", "new")["errors"], [])
                row["native_after"] = "missing.md"
                write([row])
                self.assertTrue(any("missing/conflicting" in e for e in audit.audit(root, "old", "new")["errors"]))
                write([row, row])
                self.assertTrue(any("duplicate" in e for e in audit.audit(root, "old", "new")["errors"]))
                write([])
                self.assertTrue(any("Unmapped" in e for e in audit.audit(root, "old", "new")["errors"]))


if __name__ == "__main__":
    unittest.main()
