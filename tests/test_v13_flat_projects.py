"""Installed Web detection and flat-project source-boundary regressions."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".game-studio/runtime"))
import config
import installer
import observations


def bash():
    if os.name != "nt":
        return shutil.which("bash")
    git = shutil.which("git")
    if git:
        for parent in Path(git).resolve().parents:
            candidate = parent / "bin/bash.exe"
            if candidate.is_file():
                return str(candidate)
    return None


class FlatProjectTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve() / "consumer project"
        self.root.mkdir()

    def write(self, relative, content):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        return target

    def run_helper(self, script):
        executable = bash()
        if not executable:
            self.skipTest("Compatible Bash is unavailable")
        env = dict(os.environ, GAME_STUDIO_PYTHON=sys.executable, PYTHONUTF8="1")
        proc = subprocess.run([executable, script.as_posix(), "--root", self.root.as_posix()],
                              cwd=self.root, capture_output=True, encoding="utf-8", errors="replace",
                              env=env, timeout=40)
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        return [line.split("\t") for line in proc.stdout.splitlines()]

    def test_installed_flat_javascript_project_ignores_delivered_framework_sources(self):
        # Build only the isolated release copy, then use the real installer. The
        # source repository manifest is owned by the release maintainer.
        if not bash():
            self.skipTest("Compatible Bash is unavailable")
        release = self.root.parent / "release copy"
        for directory in (".agents/skills", ".codex/agents", ".game-studio"):
            shutil.copytree(ROOT / directory, release / directory,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        installer.build_manifest(release)
        self.write("package.json", '{"name":"plain-game","private":true}')
        self.write("game.js", "globalThis.consumerGame = {};\n")
        installer.install(release, self.root)
        self.assertTrue((self.root / ".game-studio/install-state.json").is_file())
        self.assertTrue((self.root / ".game-studio/resources/engines/web/scaffold/src/main.ts").is_file())
        before = {p.relative_to(self.root): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in self.root.rglob("*") if p.is_file()}
        script = self.root / ".game-studio/scripts/web-detect.sh"
        rows = self.run_helper(script)
        with self.subTest(observation="language"):
            self.assertEqual(next(row[1] for row in rows if row[0] == "language"), "JavaScript")
        with self.subTest(observation="code candidates"):
            self.assertEqual([row[1] for row in rows if row[0] == "code_root_candidate"], ["."])
        with self.subTest(observation="test files"):
            self.assertEqual(next(row[1] for row in rows if row[0] == "test_files"), "0")
        with self.subTest(observation="hook"):
            self.assertEqual(next(row[1] for row in rows if row[0] == "hook"), "absent")
        after = {p.relative_to(self.root): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(after, before)
        self.write("modules/game.ts", "window.game = {};\n")
        own_rows = self.run_helper(script)
        self.assertEqual(next(row[1] for row in own_rows if row[0] == "language"), "TypeScript")
        self.assertEqual([row[1] for row in own_rows if row[0] == "code_root_candidate"], [".", "modules"])
        self.assertIn(["hook", "present", "modules/game.ts"], own_rows)

    def flat_fixture(self):
        self.write("project.yaml", "engine: {name: Web, code_root: .}\n")
        self.write("game.js", "// Main game code\n")
        self.write("gameplay/movement.js", "// Real movement code\n")
        for directory in ("vendor", "build"):
            for index in range(6):
                self.write(f"{directory}/decoy-{index}.js", "// TODO third-party or generated code\n")

    def test_flat_source_count_and_phase_exclude_vendor_and_build_but_keep_game_code(self):
        self.flat_fixture()
        facts = observations.project_state(self.root)["facts"]
        with self.subTest(observation="source count"):
            self.assertEqual(facts["source_files"]["value"], 2)
        with self.subTest(observation="inferred phase"):
            self.assertIsNone(facts["phase_inferred"]["value"])
        for index in range(8):
            self.write(f"gameplay/feature-{index}.js", "// Real game code\n")
        actual = observations.project_state(self.root)["facts"]
        self.assertEqual(actual["source_files"]["value"], 10)
        self.assertEqual(actual["phase_inferred"]["value"], "production")

    def test_flat_default_marker_scan_uses_game_sources_not_vendor_or_build(self):
        self.flat_fixture()
        rows = self.run_helper(ROOT / ".game-studio/scripts/code-markers.sh")
        self.assertIn(["scanned_files", "2", "."], rows)
        self.assertIn(["todo", "0"], rows)

    def test_slash_roots_are_invalid_explicit_values_without_fallback(self):
        for kind, fallback in (("code_root", "src"), ("test_root", "tests")):
            self.write(fallback + "/.gitkeep", "")
            for value in ("/", "///"):
                for nested in (True, False):
                    settings = {"engine": {"name": "Web"}}
                    if nested:
                        settings["engine"][kind] = value
                        settings[kind] = fallback
                    else:
                        settings[kind] = value
                    self.write("project.yaml", json.dumps(settings))
                    with self.subTest(kind=kind, value=value, nested=nested):
                        row = config.derived(config.resolve(self.root), ["engine_row"])["engine_row"][kind]
                        self.assertEqual(row["status"], "INVALID")
                        self.assertIsNone(row["value"])
                        self.assertEqual(row["source"], "engine." + kind if nested else kind)

    def test_period_roots_and_unset_fallback_still_resolve_to_flat_project(self):
        for kind in ("code_root", "test_root"):
            for value in (".", "./", None, "", "[TO BE CONFIGURED]", "null"):
                self.write("project.yaml", json.dumps({"engine": {"name": "Web", kind: value}, kind: "."}))
                with self.subTest(kind=kind, value=value):
                    row = config.derived(config.resolve(self.root), ["engine_row"])["engine_row"][kind]
                    self.assertEqual(row["status"], "VALID")
                    self.assertEqual(row["value"], ".")
                    self.assertEqual(row["source"], "engine." + kind if value in {".", "./"} else kind)
