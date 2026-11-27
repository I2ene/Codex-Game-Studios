"""Runtime contracts for the frozen upstream v1.3 port."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUNTIME = Path(__file__).resolve().parents[1] / ".game-studio/runtime"
sys.path.insert(0, str(RUNTIME))
import config
import observations
import studio


class V13RuntimeTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "消费者 project"
        self.root.mkdir()

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def state(self):
        return observations.project_state(self.root)["facts"]

    def test_nested_roots_beat_legacy_and_are_reported_by_engine_row(self):
        self.write("project.yaml", "engine: {name: Web, code_root: game, test_root: checks}\ncode_root: src\ntest_root: tests\n")
        for path in ("game/main.ts", "checks/unit/a.test.ts", "src/old.ts"):
            self.write(path, "// fixture")
        facts = self.state()
        self.assertEqual(facts["code_root"]["value"], "game")
        self.assertEqual(facts["code_root"]["source"], "engine.code_root")
        result = config.derived(config.resolve(self.root), ["engine_row"])["engine_row"]
        self.assertEqual(result["test_root"]["value"], "checks")
        self.assertEqual(result["code_root"]["source"], "engine.code_root")
        self.assertEqual(result["commands"]["test"]["suggestion"], "npm test")
        self.assertIsNone(result["commands"]["test"]["argv"])
        self.assertTrue(any("code_root" in note for note in result["notes"]))

    def test_unset_nested_roots_fall_through_legacy_then_table(self):
        for kind, default, legacy in (("code_root", "src", "scripts"),
                                      ("test_root", "tests", "checks")):
            self.write(default + "/.gitkeep", "")
            self.write(legacy + "/.gitkeep", "")
            for unset in ("", "   ", "[TO BE CONFIGURED]", "null", "~", None):
                for fallback in ("legacy", "table", "unset-legacy"):
                    settings = {"engine": {"name": "Web", kind: unset}}
                    if fallback == "legacy":
                        settings[kind] = legacy
                    elif fallback == "unset-legacy":
                        settings[kind] = unset
                    self.write("project.yaml", json.dumps(settings))
                    with self.subTest(kind=kind, unset=unset, fallback=fallback):
                        row = config.derived(config.resolve(self.root), ["engine_row"])["engine_row"]
                        value = row[kind]
                        self.assertEqual(value["value"], legacy if fallback == "legacy" else default)
                        self.assertEqual(value["source"], kind if fallback == "legacy" else "engine.name")
                        self.assertEqual(value["status"], "VALID")
                        self.assertFalse(any(kind in note for note in row["notes"]))

    def test_invalid_explicit_roots_stop_unset_fallback_chain(self):
        for kind, default, legacy in (("code_root", "src", "scripts"),
                                      ("test_root", "tests", "checks")):
            self.write(default + "/.gitkeep", "")
            self.write(legacy + "/.gitkeep", "")
            for nested, top in (("missing", legacy), ("missing", None),
                                ("", "missing"), (None, "missing")):
                settings = {"engine": {"name": "Web", kind: nested}}
                if top is not None:
                    settings[kind] = top
                self.write("project.yaml", json.dumps(settings))
                with self.subTest(kind=kind, nested=nested, legacy=top):
                    row = config.derived(config.resolve(self.root), ["engine_row"])["engine_row"][kind]
                    self.assertEqual(row["status"], "INVALID")
                    self.assertIsNone(row["value"])
                    self.assertIn("no directory", row["reason"])
                    self.assertEqual(row["source"], "engine." + kind if nested == "missing" else kind)

    def test_invalid_explicit_root_never_scans_default_or_wrong_case(self):
        self.write("src/should-not-count.ts", "// default fallback")
        self.write("Scripts/also-not-count.ts", "// actual spelling")
        for value in ("missing", "../escape", "scripts", ".game-studio", "src//child"):
            self.write("project.yaml", "engine: {name: Web, code_root: " + json.dumps(value) + "}\n")
            with self.subTest(value=value):
                facts = self.state()
                self.assertIsNone(facts["code_root"]["value"])
                self.assertIsNone(facts["source_files"]["value"])
                self.assertIn("invalid", facts["code_root"]["source"])

    def test_flat_root_prunes_framework_and_generated_files_before_counting(self):
        self.write("project.yaml", "engine: {name: Web, code_root: .}\n")
        self.write("game.ts", "// one game file")
        for folder in (".game-studio", ".agents", ".codex", ".git", "node_modules", "dist", "dist-single", "tests", "prototypes", ".specify"):
            self.write(folder + "/decoy.ts", "// unrelated")
        self.assertEqual(self.state()["source_files"]["value"], 1)

    def test_unknown_and_unset_engine_do_not_become_web(self):
        self.write("src/file.ts", "// directory alone is not an engine")
        for source in ("", "engine: {name: CustomEngine}\n"):
            self.write("project.yaml", source)
            row = config.derived(config.resolve(self.root), ["engine_row"])["engine_row"]
            self.assertIsNone(row["code_root"]["value"])
            self.assertIsNone(row["commands"]["test"]["argv"])
            self.assertIsNone(row["commands"]["test"]["suggestion"])

    def test_explicit_argv_and_engine_version_survive_table_defaults(self):
        argv = [sys.executable, "-c", "print('actual argv')"]
        self.write("project.yaml", "engine: {name: Web, version: '7.0.0'}\ncommands:\n  test: " + json.dumps(argv) + "\n")
        result = config.resolve(self.root)
        row = config.derived(result, ["engine_row", "specialists"])
        self.assertEqual(result["values"]["engine.version"], "7.0.0")
        self.assertEqual(row["engine_row"]["commands"]["test"]["argv"], argv)
        self.assertEqual(row["specialists"]["primary"]["value"], "gs-lead-programmer")

    def test_goal_enum_and_local_fact_boundary(self):
        self.write("project.yaml", "project: {goal: learn}\n")
        self.write("project.local.yaml", "project: {goal: sell}\nengine: {code_root: elsewhere}\n")
        result = config.resolve(self.root)
        self.assertEqual(result["values"]["project.goal"], "learn")
        self.assertTrue(any("project.goal" in row for row in result["notes"]))
        with self.assertRaises(ValueError):
            studio.settings(self.root, "project.goal=typo")

    def test_web_coherence_observes_actual_bundler_without_executing_it(self):
        self.write("project.yaml", "engine: {name: Web, version: '6.1.2'}\n")
        self.write("package.json", json.dumps({"scripts": {"build": "webpack"}, "devDependencies": {"webpack": "^6.1.0"}}))
        self.write("node_modules/webpack/package.json", '{"version":"6.1.2"}')
        from engine import coherence
        result = {row["check"]: row for row in coherence(self.root)["observations"]}
        self.assertEqual(result["installed-bundler"]["status"], "MATCH")
        self.assertEqual(result["installed-bundler"]["package"], "webpack")
        self.assertEqual(result["installed-binary"]["status"], "NOT ASSESSED")

    def test_web_test_scaffold_uses_bundled_browser_config_and_preserves_user_files(self):
        self.write("tests/README.md", "User notes\n")
        preview = observations.test_scaffold(self.root, "Web", dry_run=True)
        self.assertIn("playwright.config.ts", [item["path"] for item in preview["files"]])
        self.assertFalse((self.root / "playwright.config.ts").exists())
        observations.test_scaffold(self.root, "Web")
        self.assertEqual((self.root / "tests/README.md").read_text(), "User notes\n")
        self.assertIn(".game-studio/scripts/page-shot.sh", (self.root / "playwright.config.ts").read_text())

    def test_quoted_commit_message_is_not_an_all_tracked_flag(self):
        first = observations.write_guard(self.root, "git", ["git commit -m 'mention git commit -a, do not stage'"])
        second = observations.write_guard(self.root, "git", ["git -C . commit -qam 'actual all tracked'"])
        self.assertEqual(first["findings"][0]["all_tracked"], False)
        self.assertEqual(second["findings"][0]["all_tracked"], True)
        self.assertEqual(observations.write_guard(self.root, "git", ["echo 'git commit -a'"])["findings"], [])

    def test_cut_transaction_restores_first_output_when_second_write_fails(self):
        from unittest.mock import patch
        import shell_bridge
        a = self.write("a.md", "original a")
        b = self.write("b.md", "original b")
        aa = self.write("new-a.md", "updated a")
        bb = self.write("new-b.md", "updated b")
        manifest = self.write("writes.tsv", f"{aa}\ta.md\n{bb}\tb.md\n")
        original = shell_bridge.atomic_write
        count = 0
        def fail_second(path, data):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError("injected cut write failure")
            return original(path, data)
        with patch.object(shell_bridge, "atomic_write", side_effect=fail_second):
            with self.assertRaises(OSError):
                shell_bridge.apply_batch(self.root.resolve(), manifest)
        self.assertEqual(a.read_text(encoding="utf-8"), "original a")
        self.assertEqual(b.read_text(encoding="utf-8"), "original b")

    def test_checkpoint_archive_failure_keeps_current_state_unchanged(self):
        from unittest.mock import patch
        import checkpoint_ops
        active = self.write("production/session-state/active.md", "# Actual state\nUnrelated hand notes.\n")
        self.write("new.md", "Next state\n")
        with patch.object(checkpoint_ops, "atomic_write", side_effect=OSError("archive failure")):
            with self.assertRaises(OSError):
                studio.checkpoint(self.root, save="new.md")
        self.assertEqual(active.read_text(encoding="utf-8"), "# Actual state\nUnrelated hand notes.\n")


    def test_web_playwright_config_is_protected_from_whole_file_overwrite(self):
        self.write("playwright.config.ts", "// user configuration\n")
        result = observations.write_guard(self.root, "overwrite", ["playwright.config.ts"])
        self.assertIn("OVERWRITE", {row["code"] for row in result["findings"]})


    def test_test_scaffold_follows_valid_nested_test_root_and_diagnoses_bad_override(self):
        self.write("checks/.gitkeep", "")
        self.write("project.yaml", "engine: {name: Web, test_root: checks}\n")
        preview = observations.test_scaffold(self.root, "Web", dry_run=True)
        self.assertIn("checks/unit/.gitkeep", [row["path"] for row in preview["files"]])
        observations.test_scaffold(self.root, "Web")
        self.assertTrue((self.root / "checks/unit/.gitkeep").is_file())
        self.assertIn("checks/integration", (self.root / "playwright.config.ts").read_text(encoding="utf-8"))
        self.write("project.yaml", "engine: {name: Web, test_root: wrong}\n")
        with self.assertRaisesRegex(ValueError, "test_root"):
            observations.test_scaffold(self.root, "Web", dry_run=True)


    def test_four_engine_default_test_roots_preserve_table_semantics(self):
        expected = {"Web": "tests", "Godot": "tests", "Unity": "Assets/Tests", "Unreal": "Source/<Module>/Private/Tests"}
        for name, relative in expected.items():
            self.write("project.yaml", "engine: {name: " + name + "}\n")
            with self.subTest(engine=name):
                result = config.derived(config.resolve(self.root), ["engine_row"])["engine_row"]["test_root"]
                self.assertEqual(result["value"], relative)
                self.assertEqual(result["source"], "engine.name")
                self.assertNotEqual(result["status"], "INVALID")
