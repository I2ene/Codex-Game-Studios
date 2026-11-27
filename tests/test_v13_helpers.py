"""Executable upstream/native helper contracts on isolated, non-game fixtures."""
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
HELPERS = ROOT / ".game-studio/scripts"
UPSTREAM_COMMIT = "abc0de79d6ceb0b5d7aa693945849b3937afbe6a"


def shell():
    if os.name == "nt":
        git = shutil.which("git")
        if git:
            for parent in Path(git).resolve().parents:
                candidate = parent / "bin/bash.exe"
                if candidate.is_file():
                    return str(candidate)
        return None
    return shutil.which("bash")


class V13HelperTests(unittest.TestCase):
    def setUp(self):
        self.bash = shell()
        if not self.bash:
            self.skipTest("Compatible Bash is unavailable")
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve() / "游戏 fixture"
        self.root.mkdir()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
        return target

    def upstream_file(self, path):
        executable = shutil.which("git")
        if not executable or not (ROOT / ".git").exists():
            self.skipTest("Git checkout unavailable for upstream comparison")
        git = [executable, "-c", f"safe.directory={ROOT.as_posix()}", "-C", str(ROOT)]
        # Windows native inheritance can lose empty values after an environment patch.
        env = dict(os.environ)
        original = subprocess.run(git + ["show", UPSTREAM_COMMIT + ":.claude/" + path],
                                  capture_output=True, env=env)
        if original.returncode:
            shallow = subprocess.run(git + ["rev-parse", "--is-shallow-repository"],
                                     capture_output=True, env=env)
            if shallow.returncode == 0 and shallow.stdout.strip() == b"true":
                self.skipTest("Pinned upstream file unavailable in this shallow checkout")
        self.assertEqual(original.returncode, 0, original.stderr.decode(errors="replace"))
        destination = self.root.parent / "upstream" / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(original.stdout)
        return destination

    def run_script(self, name, *args, code=0, upstream=False):
        env = dict(os.environ, GAME_STUDIO_PYTHON=sys.executable, PYTHONUTF8="1")
        script = self.upstream_file("scripts/" + name + ".sh") if upstream else HELPERS / (name + ".sh")
        proc = subprocess.run([self.bash, script.as_posix(), *args, "--root", self.root.as_posix()],
                              cwd=self.root, capture_output=True, encoding="utf-8", errors="replace",
                              env=env, timeout=40)
        self.assertEqual(proc.returncode, code, proc.stderr + proc.stdout)
        return proc.stdout.replace("\r\n", "\n")

    def aliased_tmpdir(self):
        physical = self.root.parent / "scratch physical"
        physical.mkdir()
        alias = self.root.parent / "scratch-alias"
        try:
            alias.symlink_to(physical, target_is_directory=True)
        except OSError:
            if os.name != "nt":
                self.skipTest("OS denied temporary-directory symlink creation")
            command = "New-Item -ItemType Junction -Path '" + str(alias).replace("'", "''") + "' -Target '" + str(physical).replace("'", "''") + "' | Out-Null"
            made = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
                                  capture_output=True)
            if made.returncode:
                self.skipTest("OS denied temporary-directory junction creation")
        if alias.is_symlink():
            self.addCleanup(alias.unlink)
        else:
            self.addCleanup(os.rmdir, alias)  # Removes the junction, preserving its target.
        return alias.as_posix()

    def test_cut_restore_accepts_tool_scratch_under_aliased_tmpdir(self):
        from unittest.mock import patch
        self.write("design/game-brief.md", "# Game Brief: Fixture\n\n## Features\n- [ ] Coins\n\n## Out of scope\n\n")
        source = self.write("src/main.ts", "// User game source\n")
        with patch.dict(os.environ, {"TMPDIR": self.aliased_tmpdir()}):
            cut = self.run_script("cut-apply", "--brief", "design/game-brief.md", "--cut", "1", "Later", "--today", "2026-11-27")
            self.assertIn("cut\t1\tCoins", cut)
            restored = self.run_script("cut-apply", "--brief", "design/game-brief.md", "--back", "Coins", "not_yet", "--today", "2026-11-27")
            self.assertIn("back\t", restored)
        self.assertIn("- [ ] Coins", (self.root / "design/game-brief.md").read_text(encoding="utf-8"))
        self.assertEqual(source.read_text(encoding="utf-8"), "// User game source\n")

    def test_one_shot_run_canonicalizes_its_copied_page_before_native_boundary(self):
        from unittest.mock import patch
        self.write("prototypes/tiny/index.html", "<canvas></canvas><script>window.game={};</script>")
        browser = self.write("browser-fixture", "#!/usr/bin/env bash\nexit 1\n")
        browser.chmod(0o755)
        with patch.dict(os.environ, {"TMPDIR": self.aliased_tmpdir(), "PAGE_SHOT_BROWSER": browser.as_posix()}):
            result = self.run_script("one-shot-run", "prototypes/tiny", "evidence/run.png", "--log", "Enter", "--stop", "180", code=3)
        self.assertIn("not_assessed\t", result)

    def test_user_input_and_output_links_remain_rejected_under_tmp_alias(self):
        alias = self.aliased_tmpdir()
        (Path(alias) / "index.html").write_text("<canvas></canvas>", encoding="utf-8")
        self.write("index.html", "<canvas></canvas>")
        self.run_script("page-shot", alias + "/index.html", "evidence/input.png", code=2)
        self.run_script("page-shot", "index.html", alias + "/output.png", code=2)
        self.assertFalse((Path(alias) / "output.png").exists())

    def test_web_scaffold_preview_creates_nothing_then_preserves_existing_files(self):
        self.write("src/hook.ts", "// user hook\n")
        preview = self.run_script("web-scaffold", "--dry-run", "--starter", "three", "--title", "A < B & C")
        self.assertIn("WOULD_CREATE\tpackage-lock.json", preview)
        self.assertFalse((self.root / "package.json").exists())
        created = self.run_script("web-scaffold", "--starter", "three", "--title", "A < B & C")
        self.assertIn("EXISTS\tsrc/hook.ts", created)
        self.assertEqual((self.root / "src/hook.ts").read_text(encoding="utf-8"), "// user hook\n")
        self.assertIn("A &lt; B &amp; C", (self.root / "index.html").read_text(encoding="utf-8"))
        self.assertTrue((self.root / "tests/unit/rules.test.ts").is_file())
        self.assertFalse((self.root / "tests/unit/rules.test.ts.tmpl").exists())
        self.assertEqual(json.loads((self.root / "package.json").read_text(encoding="utf-8"))["dependencies"]["three"], "0.186.1")
        self.assertIn("refused\tpackage.json", self.run_script("web-scaffold", code=3))

    def test_engine_table_reader_agrees_with_upstream(self):
        rows = []
        for reader, table in ((HELPERS / "engine-row.awk", ROOT / ".game-studio/resources/engines/engines.tsv"),
                              (self.upstream_file("scripts/engine-row.awk"), self.upstream_file("engines/engines.tsv"))):
            script = f'awk -F"\\t" -v engine="uNrEaL Engine" -v col=asset_root -f "{reader.as_posix()}" "{table.as_posix()}"'
            out = subprocess.run([self.bash, "-c", script], capture_output=True, text=True, timeout=10)
            self.assertEqual(out.returncode, 0, out.stderr)
            rows.append(out.stdout.strip())
        self.assertEqual(rows, ["Content", "Content"])

    def test_web_detection_is_read_only_and_respects_existing_package_manager(self):
        self.write("package.json", json.dumps({"packageManager": "pnpm@10.4.0", "scripts":
                   {"dev": "webpack serve", "build": "webpack", "test": "jest", "smoke": "node smoke.js"},
                   "dependencies": {"three": "0.186.1"}, "devDependencies": {"webpack": "^6.1.0", "jest": "^30.0"}}))
        self.write("pnpm-lock.yaml", "lockfileVersion: '9.0'\n")
        self.write("package-lock.json", '{"lockfileVersion":3}')
        self.write("src/main.ts", "window.game = { step() {} };\n")
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = self.run_script("web-detect")
        self.assertIn("package_manager\tpnpm\tpackageManager: pnpm@10.4.0", result)
        self.assertIn("command\ttest\tpnpm test", result)
        self.assertIn("bundler\twebpack", result.lower())
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_web_asset_and_content_observations_accept_table_row(self):
        self.write("assets/art/player.txt", "asset fixture")
        self.write("data/levels/first.json", "{}")
        assets = self.run_script("asset-scan", "--engine", "Web")
        self.assertIn("engine\tweb", assets.lower())
        content = self.run_script("content-count", "found", "--engine", "Web")
        self.assertIn("found\tlevels\t1", content)

    def test_one_shot_new_keep_check_tune_and_share_preserve_source(self):
        self.run_script("one-shot-new", "tiny", "--title", "Tiny", "--question", "Does it move?")
        game = self.root / "prototypes/tiny"
        self.assertTrue((game / "config.js").is_file())
        self.run_script("one-shot-new", "tiny", code=4)
        # A small explicit slider follows the upstream single-line tuning grammar.
        (game / "config.js").write_text("// PROTOTYPE - NOT FOR PRODUCTION\nwindow.CONFIG = {\n speed: { value: 5, min: 1, max: 10, step: 1 },\n};\n")
        self.run_script("one-shot-tune", "prototypes/tiny", "Tuned in the panel: tiny", "speed 5 -> 7")
        self.assertIn("value: 7", (game / "config.js").read_text(encoding="utf-8"))
        self.assertIn("speed", (game / "feel-log.md").read_text(encoding="utf-8"))
        self.run_script("one-shot-new", "tiny", "--add", "tune.js")
        before = (game / "index.html").read_bytes()
        shared = self.run_script("one-shot-share", "prototypes/tiny")
        self.assertIn("dist\t", shared)
        self.assertEqual((game / "index.html").read_bytes(), before)
        for name in ("tune.js", "feel-log.md", "brief.md", "bot.js", "evidence"):
            self.assertFalse((game / "dist" / name).exists())

    def test_cut_restore_renumbers_stories_without_changing_code(self):
        self.write("design/game-brief.md", "# Game Brief: Fixture\n\n## Features\n- [x] Jump\n- [ ] Coins\n- [ ] Door\n\n## Out of scope\n\n")
        self.write("production/epics/main/story-001.md", "# Jump\nStatus: Complete\nRequirement: Brief MVP feature 1\n")
        self.write("production/epics/main/story-002.md", "# Coins\nStatus: Ready\nRequirement: Brief MVP feature 2\n")
        self.write("production/epics/main/story-003.md", "# Door\nStatus: Ready\nRequirement: Brief MVP feature 3\n")
        code = self.write("src/main.ts", "// Keep the actual game code\n")
        cut = self.run_script("cut-apply", "--brief", "design/game-brief.md", "--cut", "2", "Too much", "--today", "2026-11-27")
        self.assertIn("cut\t2\tCoins", cut)
        self.assertIn("Brief MVP feature 2", (self.root / "production/epics/main/story-003.md").read_text(encoding="utf-8"))
        self.assertIn("Blocked", (self.root / "production/epics/main/story-002.md").read_text(encoding="utf-8"))
        self.run_script("cut-apply", "--brief", "design/game-brief.md", "--back", "Coins", "not_yet", "--today", "2026-11-27")
        self.assertIn("Ready", (self.root / "production/epics/main/story-002.md").read_text(encoding="utf-8"))
        self.assertEqual(code.read_text(encoding="utf-8"), "// Keep the actual game code\n")

    def test_references_save_uses_explicit_files_instead_of_private_session_logs(self):
        self.write("supplied.png", "explicit image fixture")
        saved = self.run_script("references-save", "supplied.png")
        self.assertIn("saved\treferences/", saved)
        kept = self.run_script("references-save", "supplied.png")
        self.assertIn("kept\treferences/", kept)
        self.assertIn("not_assessed\t", self.run_script("references-save", "2", code=3))

    def test_door_import_preserves_source_hashes(self):
        source = self.write("source/index.html", "<html><title>Door</title><canvas></canvas><script>requestAnimationFrame(function frame(){});</script></html>")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        self.run_script("door-in", "source", "--name", "door", "--dry-run")
        self.assertFalse((self.root / "prototypes/door").exists())
        result = self.run_script("door-in", "source", "--name", "door")
        self.assertIn("copied\t1\tsame", result)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), digest)
        self.assertEqual((self.root / "prototypes/door/index.html").read_bytes(), source.read_bytes())

    def test_grow_record_preserves_yaml_comments_and_instructions(self):
        self.write("project.yaml", "# User comment\nengine:\n  name: null # unset deliberately\n")
        self.write("AGENTS.md", "# User instructions\nDo not rewrite me.\n")
        self.write("package.json", '{"devDependencies":{"vite":"8.3.4"}}')
        self.run_script("one-shot-grow", "record", "tiny")
        self.assertIn("# User comment", (self.root / "project.yaml").read_text(encoding="utf-8"))
        self.assertIn("# unset deliberately", (self.root / "project.yaml").read_text(encoding="utf-8"))
        self.assertEqual((self.root / "AGENTS.md").read_text(encoding="utf-8"), "# User instructions\nDo not rewrite me.\n")
        self.assertFalse((self.root / "CLAUDE.md").exists())

    def test_configured_test_argv_cannot_be_reinterpreted_as_shell(self):
        script = self.write("fake_test.py", "import sys\nprint('Tests  1 passed (1)')\nprint(sys.argv[1])\n")
        argv = [sys.executable, str(script), "$(touch should-not-exist); literal"]
        self.write("project.yaml", "engine: {name: Web}\ncommands:\n  test: " + json.dumps(argv) + "\n")
        self.write("package.json", '{"scripts":{"test":"vitest run"},"devDependencies":{"vitest":"5.0.5"}}')
        result = self.run_script("test-run", "Web", "--timeout", "10")
        self.assertIn("ran\tyes", result)
        self.assertFalse((self.root / "should-not-exist").exists())

    def test_data_reader_agrees_with_upstream_on_static_game(self):
        self.write("game/index.html", "<title>Fixture</title><canvas></canvas><script>const SPEED=5; requestAnimationFrame(loop); addEventListener('keydown', key);</script>")
        self.assertEqual(self.run_script("game-read", "game"), self.run_script("game-read", "game", upstream=True))

    def test_web_unit_failure_still_collects_browser_half_and_zero_tests_are_named(self):
        from unittest.mock import patch
        fake = self.write("tool-bin/npm", "#!/usr/bin/env bash\nif [ \"$2\" = test:unit ]; then\n"
                          "echo 'Tests  1 failed (1)'; echo unit >> \"$PWD/halves.txt\"; exit 1\n"
                          "fi\necho '1 passed (0.1s)'; echo e2e >> \"$PWD/halves.txt\"; exit 0\n")
        fake.chmod(0o755)
        self.write("project.yaml", "engine: {name: Web}\ncommands: {test: [npm, test]}\n")
        self.write("package.json", '{"scripts":{"test":"npm run test:unit && npm run test:e2e","test:unit":"vitest run","test:e2e":"playwright test"}}')
        with patch.dict(os.environ, {"PATH": str(fake.parent) + os.pathsep + os.environ["PATH"]}):
            result = self.run_script("test-run", "Web", "--timeout", "5")
        self.assertIn("unit_exit\t1", result)
        self.assertIn("e2e_exit\t0", result)
        self.assertIn("rule\tweb:failed", result)
        self.assertEqual((self.root / "halves.txt").read_text(encoding="utf-8").splitlines(), ["unit", "e2e"])
        fake.write_text("#!/usr/bin/env bash\necho 'No test files found'; exit 0\n", encoding="utf-8")
        self.write("package.json", '{"scripts":{"test":"vitest run"}}')
        with patch.dict(os.environ, {"PATH": str(fake.parent) + os.pathsep + os.environ["PATH"]}):
            zero = self.run_script("test-run", "Web", "--timeout", "5")
        self.assertIn("rule\tweb:zero-tests", zero)

    def test_missing_test_adapter_and_shell_override_never_run_suggested_commands(self):
        self.write("package.json", '{"scripts":{"test":"echo not executed"}}')
        result = self.run_script("test-run", "Web")
        self.assertIn("ran\tno", result)
        self.assertIn("native:no-test-adapter", result)
        self.run_script("test-run", "Web", "--cmd", "touch should-not-exist", code=2)
        self.assertFalse((self.root / "should-not-exist").exists())

    def test_share_refuses_an_output_outside_project_before_deletion(self):
        outside = self.root.parent / "outside"
        outside.mkdir()
        (outside / "index.html").write_text("<canvas></canvas>", encoding="utf-8")
        (outside / "dist").mkdir()
        (outside / "dist/user.txt").write_text("preserve", encoding="utf-8")
        self.run_script("one-shot-share", "../outside", code=2)
        self.assertEqual((outside / "dist/user.txt").read_text(encoding="utf-8"), "preserve")


    def test_internal_replays_delegate_their_temporary_output_root(self):
        self.check_internal_replays()

    def test_internal_replays_canonicalize_tool_scratch_under_aliased_tmpdir(self):
        self.check_internal_replays(self.aliased_tmpdir())

    def check_internal_replays(self, tmpdir=None):
        # A strict child stub exercises the caller/child output boundary without
        # making screenshots or requiring a browser on every unit-test host.
        copied = self.root / ".fixture-studio"
        shutil.copytree(ROOT / ".game-studio/runtime", copied / "runtime",
                        ignore=shutil.ignore_patterns("__pycache__"))
        scripts = copied / "scripts"
        scripts.mkdir()
        for name in ("one-shot-check.sh", "one-shot-grow.sh", "native-runtime.sh", "engine-row.awk"):
            shutil.copyfile(HELPERS / name, scripts / name)
        (copied / "resources/engines").mkdir(parents=True)
        shutil.copyfile(ROOT / ".game-studio/resources/engines/engines.tsv",
                        copied / "resources/engines/engines.tsv")
        stub = scripts / "one-shot-run.sh"
        stub.write_text("""#!/usr/bin/env bash
. "$(dirname "$0")/native-runtime.sh"
dir=$1; out=$2; shift 2
root=''; hash=inputs
while [ $# -gt 0 ]; do
  case "$1" in
    --root) root=$2; shift 2 ;;
    --quiet) hash=quiet; shift 2 ;;
    *) shift ;;
  esac
done
case "$dir" in /*|[A-Za-z]:*) ;; *) dir="$root/$dir" ;; esac
[ -f "$dir/index.html" ] || { echo 'missing delegated input page' >&2; exit 1; }
case "$out" in
  "$root"/*) ;;
  /*|[A-Za-z]:*) echo 'refused outside delegated root' >&2; exit 2 ;;
  *) out="$root/$out" ;;
esac
gs_native tree "$dir" --root "$root" --external >/dev/null || exit 2
gs_native path "$out" --root "$root" >/dev/null || exit 2
mkdir -p "$(dirname "$out")"; printf x > "$out"
printf 'shot\\t%s\\t1\\n' "$out"
printf 'screen\\t60\\t1280x720\\t%s\\tdrawn\\n' "$hash"
printf 'playinput\\t2\\nscene\\t1\\tplay\\nuncaught\\t0\\ndone\\t60\\t1\\tplay\\tend\\tcomplete\\n'
""", encoding="utf-8")
        stub.chmod(0o755)
        self.write("prototypes/tiny/index.html", "<canvas></canvas>")
        env = dict(os.environ, GAME_STUDIO_PYTHON=sys.executable, PYTHONUTF8="1")
        if tmpdir is not None:
            env["TMPDIR"] = tmpdir
        def run(name, *args):
            proc = subprocess.run([self.bash, (scripts / name).as_posix(), *args, "--root", self.root.as_posix()],
                                  cwd=self.root, capture_output=True, encoding="utf-8", env=env, timeout=25)
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            return proc.stdout
        with self.subTest(lane="responds"):
            checked = run("one-shot-check.sh", "prototypes/tiny", "--keys", "Enter ArrowRight")
            self.assertIn("responds\tchanged", checked)
        with self.subTest(lane="grow-reference"):
            replayed = run("one-shot-grow.sh", "replay", "tiny", "--as", "reference", "--stop", "180", "--log", "Enter")
            self.assertIn("exact\tyes", replayed)


    def test_page_shot_persistent_profile_survives_browser_failure(self):
        # The real save/load browser lane is covered by the installed integration
        # exercise. Here an unavailable browser proves --profile does not crash
        # before launch and that even a failed visit does not delete saved data.
        browser = self.write("browser-fixture", "#!/usr/bin/env bash\nexit 1\n")
        browser.chmod(0o755)
        self.write("index.html", "<html><canvas></canvas></html>")
        from unittest.mock import patch
        with patch.dict(os.environ, {"PAGE_SHOT_BROWSER": browser.as_posix()}):
            self.run_script("page-shot", "index.html", "evidence/first.png", "--profile", "evidence/profile", code=3)
            marker = self.write("evidence/profile/saved-data", "retain between visits")
            self.run_script("page-shot", "index.html", "evidence/second.png", "--profile", "evidence/profile", code=3)
        self.assertEqual(marker.read_text(encoding="utf-8"), "retain between visits")

    def test_preparation_missing_does_not_execute_editor_test_adapter(self):
        spy = self.write("spy.py", "from pathlib import Path\nPath('spy-ran').write_text('ran')\nprint('Test Completed. Result={Success} Path={Fixture}')\n")
        self.write("Fixture.uproject", '{"EngineAssociation":"5.8"}')
        self.write("project.yaml", "engine: {name: Unreal}\ncommands:\n  test: " + json.dumps([sys.executable, str(spy)]) + "\n")
        stopped = self.run_script("test-run", "Unreal")
        self.assertIn("ran\tno", stopped)
        self.assertIn("native:no-preparation", stopped)
        self.assertFalse((self.root / "spy-ran").exists())
        skipped = self.run_script("test-run", "Unreal", "--no-build")
        self.assertIn("ran\tyes", skipped)
        self.assertTrue((self.root / "spy-ran").exists())
        (self.root / "spy-ran").unlink()
        self.write("addons/gdUnit4/bin/GdUnitCmdTool.gd", "# runner presence fixture")
        self.write("project.yaml", "engine: {name: Godot}\ncommands:\n  test: " + json.dumps([sys.executable, str(spy)]) + "\n")
        stopped = self.run_script("test-run", "Godot")
        self.assertIn("native:no-preparation", stopped)
        self.assertFalse((self.root / "spy-ran").exists())
        delegated = self.run_script("test-run", "Godot", "--prepared")
        self.assertIn("ran\tyes", delegated)
        self.assertIn("delegated", delegated)

    def test_web_test_filter_uses_effective_legacy_root_and_rejects_invalid_override(self):
        self.write("checks/unit/example.test.ts", "// fixture")
        self.write("project.yaml", "engine: {name: Web}\ntest_root: checks\ncommands: {test: [npm, test]}\n")
        self.write("package.json", '{"scripts":{"test":"npm run test:unit && npm run test:e2e","test:unit":"vitest run","test:e2e":"playwright test"}}')
        plan = self.run_script("test-run", "Web", "--dry-run", "--filter", "checks/unit")
        self.assertIn("half\tunit\tnpm run test:unit -- 'checks/unit'", plan)
        self.write("project.yaml", "engine: {name: Web, test_root: missing}\ntest_root: checks\ncommands: {test: [npm, test]}\n")
        self.run_script("test-run", "Web", "--dry-run", "--filter", "checks/unit", code=2)


    def test_content_scanner_and_grow_guard_use_effective_legacy_code_root(self):
        self.write("project.yaml", "engine: {name: Web}\ncode_root: game\n")
        self.write("game/characters/hero.json", "{}")
        result = self.run_script("content-count", "found", "--engine", "Web")
        self.assertIn("found\tcharacters\t1", result)
        self.run_script("one-shot-new", "tiny")
        guard = self.run_script("one-shot-grow", "guard", "tiny", code=3)
        self.assertIn("guard\troot\tfail", guard)
