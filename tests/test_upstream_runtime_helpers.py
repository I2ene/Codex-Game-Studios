"""Native, root-confined equivalents of deterministic upstream utilities."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUNTIME = Path(__file__).resolve().parents[1] / ".game-studio/runtime"
sys.path.insert(0, str(RUNTIME))
import hooks
import studio


class UpstreamRuntimeHelpersTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "consumer with spaces"
        self.root.mkdir()

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text if isinstance(text, bytes) else text.encode())
        return path

    def cli(self, *arguments, stdin=None, code=0):
        p = subprocess.run([sys.executable, "-B", str(RUNTIME / "studio.py"), *arguments,
                            "--root", str(self.root)], input=stdin, capture_output=True,
                           encoding="utf-8")
        self.assertEqual(p.returncode, code, p.stderr)
        return json.loads(p.stdout) if code == 0 else p.stderr

    def test_markdown_sections_are_bounded_and_fenced_headings_are_not_sections(self):
        self.write("a.md", "# Intro\n\n## Rules\n[To be designed]\n~~~md\n## Decoy\n~~~\n### Detail\n\n## End\nReal text.\n")
        self.assertEqual([r["title"] for r in self.cli("markdown", "list", "a.md")["sections"]],
                         ["Intro", "Rules", "Detail", "End"])
        rows = self.cli("markdown", "status", "a.md", "Rules", "unknown")["sections"]
        self.assertEqual([r["status"] for r in rows], ["PLACEHOLDER", "NOT_FOUND"])
        self.assertIn("### Detail", self.cli("markdown", "extract", "a.md", "Rules", "--body")["text"])
        self.assertNotIn("## End", self.cli("markdown", "extract", "a.md", "Rules", "--body")["text"])

    def test_markdown_edits_preserve_bom_and_other_bytes(self):
        path = self.write("a.md", b"\xef\xbb\xbf# Doc\r\n> **Status**: Ready <!-- review handoff -->\r\n\r\n## Rules\r\nold\r\n\r\n## Tail\r\nkeep  \r\n")
        self.cli("markdown", "set-field", "a.md", "Status", "In Review")
        self.cli("markdown", "replace", "a.md", "Rules", stdin="new\n")
        self.cli("markdown", "insert-before", "a.md", "Tail", stdin="## Inserted\ninserted\n")
        self.assertEqual(path.read_bytes(), b"\xef\xbb\xbf# Doc\r\n> **Status**: In Review <!-- review handoff -->\r\n\r\n"
                         b"## Rules\r\nnew\r\n\r\n## Inserted\r\ninserted\r\n\r\n## Tail\r\nkeep  \r\n")
        self.cli("markdown", "set-field", "a.md", "Owner", "QA", "--after", "Status")
        self.assertIn(b"> **Owner**: QA\r\n", path.read_bytes())

    def test_markdown_refuses_ambiguous_or_escaping_edits(self):
        path = self.write("a.md", "## Rules\nfirst\n## Rules\nsecond\n")
        original = path.read_bytes()
        self.assertIn("Ambiguous", self.cli("markdown", "replace", "a.md", "Rules", stdin="new", code=2))
        self.assertIn("Unsafe relative path", self.cli("markdown", "set-field", "../outside.md", "Status", "Ready", code=2))
        self.assertEqual(path.read_bytes(), original)

    def test_project_state_respects_stage_sources_and_never_guesses_ambiguous_code_root(self):
        self.write("project.yaml", "project: {stage: Production}\n")
        self.write("production/stage.txt", "Polish\n")
        self.write("src/a.py", "pass")
        self.write("Source/a.cpp", "// fixture")
        result = self.cli("project-state")["facts"]
        self.assertEqual(result["stage"]["value"], "Production")
        self.assertEqual(result["stage"]["source"], "project.yaml")
        self.assertEqual(result["stage_txt"]["value"], "Polish")
        self.assertIsNone(result["code_root"]["value"])
        self.assertIsNone(result["source_files"]["value"])
        self.assertNotIn("source_files", self.cli("project-state", "--stage")["facts"])

    def test_read_guard_reports_large_unbounded_read_and_real_headings(self):
        self.write("project.yaml", "features: {read_guard_kb: 1}\n")
        self.write("design/huge.md", "## Actual\n~~~md\n## Decoy\n~~~\n" + "a" * 1500)
        self.assertEqual(self.cli("read-guard", "check", "design/huge.md")["status"], "LARGE")
        self.assertEqual(self.cli("read-guard", "check", "design/huge.md", "--bounded", "yes")["status"], "OBSERVED")
        result = self.cli("read-guard", "sections", "design/huge.md")
        self.assertEqual([h["title"] for h in result["sections"]], ["Actual"])

    def test_write_guard_observes_config_prototype_freeze_and_missing_artifacts(self):
        self.write("project.yaml", "code_root: src\n")
        self.write("project.local.yaml", "engine: {name: Unity}\nmodes: {automation: typo}\n")
        self.write("production/localization/freeze-status.md", "**Status:** ACTIVE\n")
        self.write("prototypes/tiny.py", "from src.core import data\n")
        self.write("tests/README.md", "Existing\n")
        expected = {
            ("config", "project.local.yaml"): {"NOT_LOCAL", "ENUM"},
            ("prototype", "prototypes/tiny.py"): {"PROTOTYPE_HEADER", "PROTOTYPE_IMPORT"},
            ("freeze", "assets/data/strings/en.csv"): {"FREEZE"},
            ("overwrite", "tests/README.md"): {"OVERWRITE"},
            ("artifact", "design/missing.md"): {"ARTIFACT"},
        }
        for args, codes in expected.items():
            with self.subTest(args=args):
                out = self.cli("write-guard", *args)
                self.assertTrue(codes.issubset({r["code"] for r in out["findings"]}), out)
        self.assertEqual(self.cli("write-guard", "overwrite", "tests/README.md", "--tool", "Edit")["findings"], [])

    def test_write_guard_observes_upstream_existing_file_protections(self):
        protected = ("production/epics/core/EPIC.md", "project.godot",
                     "tests/helpers/factories.gd", "docs/tech-debt-register.md",
                     "docs/engine-reference/godot/modules/audio.md")
        for relative in protected:
            with self.subTest(path=relative):
                self.assertEqual(self.cli("write-guard", "overwrite", relative)["findings"], [])
                path = self.write(relative, "User-owned content.\n")
                initial = path.read_bytes()
                result = self.cli("write-guard", "overwrite", relative)
                self.assertEqual([(r["code"], r["path"]) for r in result["findings"]],
                                 [("OVERWRITE", relative)])
                self.assertEqual(self.cli("write-guard", "overwrite", relative,
                                          "--tool", "Edit")["findings"], [])
                self.assertEqual(path.read_bytes(), initial)
        unprotected = "tests/helpers-not/factories.gd"
        self.write(unprotected, "Unrelated file.\n")
        self.assertEqual(self.cli("write-guard", "overwrite", unprotected)["findings"], [])

    def test_markdown_readers_stay_available_but_duplicate_config_blocks_edits(self):
        project = self.write("project.yaml", "modes: {rigor: minimal}\nmodes: {rigor: full}\n")
        doc = self.write("design/doc.md", "# Doc\nStatus: Ready\n\n## Rules\nOriginal rules.\n")
        self.write("replacement.md", "Replacement content.\n")
        initial = doc.read_bytes(), project.read_bytes()
        self.assertTrue(self.cli("config")["duplicate_keys"])
        self.assertIn("Rules", [r["title"] for r in self.cli("markdown", "list", "design/doc.md")["sections"]])
        self.assertEqual(self.cli("markdown", "status", "design/doc.md", "Rules")["sections"][0]["status"],
                         "COMPLETE")
        self.assertIn("Original rules.", self.cli("markdown", "extract", "design/doc.md", "Rules")["text"])
        for args in (("replace", "design/doc.md", "Rules", "--body-file", "replacement.md"),
                     ("insert-before", "design/doc.md", "Rules", "--body-file", "replacement.md"),
                     ("set-field", "design/doc.md", "Status", "Complete")):
            with self.subTest(action=args[0]):
                error = self.cli("markdown", *args, "--output", "edit-result.json", code=2)
                self.assertIn("duplicate", error.lower())
                self.assertEqual((doc.read_bytes(), project.read_bytes()), initial)
                self.assertFalse((self.root / "edit-result.json").exists())

    def test_scaffold_dry_run_creates_nothing_and_create_never_clobbers(self):
        before = self.write("tests/README.md", b"user tests\r\n")
        result = self.cli("test-scaffold", "Godot", "--dry-run")
        self.assertIn("WOULD_CREATE", {r["status"] for r in result["files"]})
        self.assertFalse((self.root / "tests/unit").exists())
        result = self.cli("test-scaffold", "Godot")
        self.assertEqual(before.read_bytes(), b"user tests\r\n")
        self.assertTrue((self.root / "tests/unit/.gitkeep").is_file())
        self.assertIn("CREATED", {r["status"] for r in result["files"]})
        self.cli("test-scaffold", "Unreal", "--module", "../escape", "--dry-run", code=2)

    def test_skill_lint_checks_native_metadata_and_hides_code_headings(self):
        self.write(".agents/skills/gs-demo/SKILL.md", "---\nname: gs-wrong\ndescription: Demo.\n---\n"
                   "## Phase 1\n~~~md\n## Phase 2\n~~~\n\n## 2. Build\n\n## Next Step\n$gs-demo\n")
        row, = self.cli("skill-lint", "gs-demo")["skills"]
        self.assertIn("NAME_MISMATCH", {item["code"] for item in row["findings"]})
        self.assertEqual(row["phases"], ["Phase 1", "2. Build"])
        self.assertEqual(row["last_section"], "Next Step")

    def test_settings_preserve_config_bytes_and_refuse_group_overwrite(self):
        path = self.write("project.yaml", b"\xef\xbb\xbf# banner\r\nmodes:  # modes\r\n"
                          b"  rigor: 'standard'  # keep me\r\ncommands:\r\n  test: [python, -V]\r\n")
        original = path.read_bytes()
        studio.settings(self.root, "modes.rigor=full", dry_run=True)
        self.assertEqual(path.read_bytes(), original)
        studio.settings(self.root, "modes.rigor=full")
        expected = original.replace(b"'standard'", b"'full'")
        self.assertEqual(path.read_bytes(), expected)
        studio.settings(self.root, "modes.automation=guided")
        expected = expected.replace(b"commands:", b"  automation: guided\r\ncommands:")
        self.assertEqual(path.read_bytes(), expected)
        with self.assertRaises(ValueError):
            studio.settings(self.root, "modes=broken")
        self.assertEqual(path.read_bytes(), expected)

    def test_checkpoint_updates_markers_preserves_narrative_and_append_is_idempotent(self):
        path = self.write("production/session-state/active.md",
                          b"# Session\r\n<!-- Example: <!-- /CHECKPOINT --> -->\r\n"
                          b"<!-- CHECKPOINT -->\r\nold\r\n<!-- /CHECKPOINT -->\r\n\r\nNarrative.\r\n")
        self.write("new.md", "fresh\n")
        self.cli("checkpoint", "--save", "new.md")
        self.assertIn(b"<!-- CHECKPOINT -->\r\nfresh\r\n<!-- /CHECKPOINT -->\r\n\r\nNarrative.\r\n", path.read_bytes())
        self.write("append.md", "New narrative.\n")
        self.cli("checkpoint", "--append", "append.md")
        self.assertEqual(self.cli("checkpoint", "--append", "append.md")["status"], "UNCHANGED")
        self.assertEqual(path.read_bytes().count(b"New narrative."), 1)
        path.write_bytes(b"<!-- CHECKPOINT -->\nbroken\n")
        self.cli("checkpoint", "--save", "new.md", code=2)
        self.assertEqual(path.read_bytes(), b"<!-- CHECKPOINT -->\nbroken\n")


    def test_duplicate_config_blocks_command_and_checkpoint_writes(self):
        project = self.write("project.yaml", "commands:\n  test: [python, -V]\ncommands:\n  test: [python, -V]\n")
        target = self.write("production/session-state/active.md", b"# User state\n")
        self.write("checkpoint.md", "new state\n")
        self.assertIn("duplicate", self.cli("run", "test", code=2).lower())
        self.assertIn("duplicate", self.cli("checkpoint", "--save", "checkpoint.md", code=2).lower())
        self.assertEqual(target.read_bytes(), b"# User state\n")
        self.assertEqual(project.read_bytes().count(b"commands:"), 2)

    def test_recover_and_save_use_only_the_configured_checkpoint_when_enabled(self):
        self.write(".game-studio/context.json", json.dumps({"checkpoint": "notes/设计进度.md"}))
        self.write("notes/authored.md", "Current phase: confirmed section.\n")
        target = self.root / "notes/设计进度.md"
        fallback = self.root / "production/session-state/active.md"
        config = self.write("project.yaml", "features: {session_state: off}\n")
        disabled = self.cli("recover")["checkpoint"]
        self.assertEqual(disabled, {"path": "notes/设计进度.md", "status": "DISABLED"})
        self.assertIn("disabled", self.cli("checkpoint", "--save", "notes/authored.md", code=2).lower())
        self.assertFalse(target.exists())
        self.assertFalse(fallback.exists())
        config.write_bytes(b"features: {session_state: on}\n")
        self.assertEqual(self.cli("recover")["checkpoint"]["status"], "ABSENT")
        self.cli("checkpoint", "--save", "notes/authored.md")
        saved = self.cli("recover")["checkpoint"]
        self.assertEqual(saved["path"], "notes/设计进度.md")
        self.assertEqual(saved["status"], "PRESENT")
        self.assertIn("confirmed section", saved["text"])
        self.assertFalse(fallback.exists())

    def test_linked_story_evidence_reports_source_report_and_required_image_drift(self):
        evidence = "production/qa/evidence/story-001/"
        source, image = "src/view.gd", evidence + "view.png"
        report, companion = evidence + "evidence.md", evidence + "evidence.receipt.json"
        self.write(source, "before\n")
        self.write(image, b"retained image fixture")
        self.write(report, "Observed the accepted screen.\n")
        self.cli("receipts", "hash", source, image, "--report", report, "--output", companion)
        args = ("receipts", "check", source, image, "--receipt", companion)
        current = self.cli(*args)
        self.assertEqual(current["report"], report)
        self.assertTrue(current["unchanged_inputs"])
        self.write(source, "changed\n")
        drift = self.cli(*args)
        self.assertFalse(drift["unchanged_inputs"])
        self.assertEqual(drift["report_status"], "UNCHANGED")
        self.assertIn((source, "CHANGED"), {(r["path"], r["status"]) for r in drift["observations"]})
        self.write(report, "Changed observation.\n")
        self.assertEqual(self.cli(*args)["report_status"], "CHANGED")
        (self.root / image).unlink()
        missing_image = self.cli(*args)
        self.assertEqual(missing_image["required_unresolved"], [image])
        self.assertIn((image, "REMOVED"), {(r["path"], r["status"]) for r in missing_image["observations"]})
        (self.root / companion).unlink()
        missing_companion = self.cli(*args)
        self.assertEqual(missing_companion["baseline_status"], "MISSING")
        self.assertFalse(missing_companion["unchanged_inputs"])

    def test_config_derives_named_bootstrap_facts_from_effective_sources(self):
        self.write("project.yaml", """modes: {rigor: standard}
engine: {name: Godot, version: '4.6', language: GDScript}
specialists: {code: godot-gdscript-specialist}
platform: {targets: [Web], gamepad_support: Partial, primary_input: Touchscreen}
performance: {frame_budget_ms: 16.7}
testing: {strict: {logic: true}}
""")
        self.write("project.local.yaml", "testing: {strict: {logic: false}}\n")
        keys = "gate_level,engine_values,specialists,review_gate,input_methods,perf_budgets"
        derived = self.cli("config", "--keys", keys)["derived"]
        self.assertEqual(set(derived), set(keys.split(",")))
        self.assertEqual(derived["gate_level"]["logic"], {"value": "advisory", "source": "project.local.yaml"})
        self.assertEqual(derived["gate_level"]["config"]["smoke_check"], "blocking")
        self.assertEqual(derived["engine_values"]["version"]["value"], "4.6")
        self.assertEqual(derived["specialists"]["primary"]["value"], "gs-godot-specialist")
        self.assertEqual(derived["specialists"]["code"]["value"], "gs-godot-gdscript-specialist")
        self.assertEqual(derived["review_gate"]["skill_gates"], "skip")
        self.assertEqual(derived["review_gate"]["phase_gates"], "run")
        self.assertEqual(derived["input_methods"]["value"], ["keyboard/mouse", "gamepad", "touch"])
        self.assertEqual(derived["perf_budgets"]["frame_budget_ms"]["value"], 16.7)

    def test_unreal_coherence_reads_only_explicit_build_version(self):
        self.write("project.yaml", "engine: {name: Unreal, version: '5.7.2', path: toolchain}\n")
        self.write("toolchain/Engine/Build/Build.version", '{"MajorVersion": 5, "MinorVersion": 7, "PatchVersion": 1}')
        rows = {row["check"]: row for row in self.cli("coherence")["observations"]}
        self.assertEqual(rows["installed-build-version"]["status"], "DIFFERS")
        self.assertEqual(rows["installed-build-version"]["observed"], "5.7.1")
        self.assertEqual(rows["installed-binary"]["status"], "NOT ASSESSED")

    def test_project_state_counts_planning_artifacts_and_distinguishes_inferred_phase(self):
        self.write("design/game-brief.md", "# Brief\n")
        self.write("production/sprints/sprint-001.md", "# Sprint\n")
        self.write("production/milestones/milestone-001.md", "# Milestone\n")
        self.write("prototypes/demo/index.html", "<p>Demo</p>")
        self.write("prototypes/demo/extra.txt", "Second file; still one prototype\n")
        self.write("production/epics/loop/story-001.md", "# Story\n")
        self.write(".git", "gitdir: /unused/read-only")
        facts = self.cli("project-state")["facts"]
        self.assertEqual(facts["concept"]["value"], "design/game-brief.md")
        self.assertEqual([facts[key]["value"] for key in ("sprint", "milestone", "prototype")], [1, 1, 1])
        self.assertEqual(facts["phase_inferred"]["value"], "pre-production")
        self.assertIsNone(facts["stage"]["value"])


    def test_hook_recovery_does_not_cross_a_nested_project_configuration(self):
        self.write(".game-studio/VERSION", "2.0.0")
        self.write("nested/project.yaml", "schema_version: 1")
        (self.root / "nested/subfolder").mkdir()
        with self.assertRaisesRegex(ValueError, "No installed framework"):
            hooks.project_root(self.root / "nested/subfolder")

    def test_scaffold_path_list_does_not_require_project_configuration(self):
        self.write("project.yaml", "broken: [")
        result = self.cli("test-scaffold", "Godot", "--list")
        self.assertIn("tests/unit/.gitkeep", [item["path"] for item in result["files"]])
        self.assertFalse((self.root / "tests").exists())
