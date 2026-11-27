"""Executable shell regressions on synthetic fixtures, not game-quality evidence."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from test_v13_helpers import shell

ROOT = Path(__file__).resolve().parents[1]
HELPERS = ROOT / ".game-studio/scripts"

class CutReplayRegressions(unittest.TestCase):
    def setUp(self):
        self.bash = shell()
        if not self.bash:
            self.skipTest("Compatible Bash unavailable")
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve() / "consumer fixture"
        self.root.mkdir()
        self.story = "production/epics/core/story-coins.md"
        self.ev = "production/qa/evidence/grow-tiny"

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
        return target

    def run_script(self, name, *args, scripts=HELPERS, mode="ok", code=0):
        env = dict(os.environ, GAME_STUDIO_PYTHON=sys.executable, PYTHONUTF8="1", FIXTURE_RUN=mode)
        result = subprocess.run([self.bash, (scripts / (name + ".sh")).as_posix(), *args,
                                 "--root", self.root.as_posix()], cwd=self.root,
                                env=env, capture_output=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, code, result.stderr + result.stdout)
        return result.stdout

    def cut_fixture(self, status):
        self.write("design/game-brief.md", "# Game Brief: Coins\n\n## Features\n- [ ] Coins\n\n## Out of scope\n\n")
        self.write(self.story, "# Coins\n\n**Status**: " + status + "\n**Requirement**: Brief MVP feature 1\n")
        self.write("src/game.ts", "// User game code remains unchanged\n")

    def cut(self):
        return self.run_script("cut-apply", "--brief", "design/game-brief.md", "--cut", "1", "Later")

    def back(self):
        return self.run_script("cut-apply", "--brief", "design/game-brief.md", "--back", "Coins", "not_yet")

    def status(self):
        text = (self.root / self.story).read_text(encoding="utf-8")
        return next(line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith("**Status**:"))

    def test_cut_and_back_preserve_initial_independent_block(self):
        self.cut_fixture("Blocked — waiting for art approval")
        self.cut()
        self.assertEqual(self.status(), "Blocked — waiting for art approval")
        self.back()
        self.assertEqual(self.status(), "Blocked — waiting for art approval")
        self.assertIn("Brief MVP feature 1", (self.root / self.story).read_text(encoding="utf-8"))
        self.assertEqual((self.root / "src/game.ts").read_text(encoding="utf-8"), "// User game code remains unchanged\n")

    def test_back_preserves_independent_block_added_after_cut(self):
        self.cut_fixture("Ready")
        self.cut()
        story = self.root / self.story
        text = story.read_text(encoding="utf-8")
        line = next(row for row in text.splitlines() if row.startswith("**Status**:"))
        story.write_text(text.replace(line, "**Status**: Blocked — new dependency failed"), encoding="utf-8")
        self.back()
        self.assertEqual(self.status(), "Blocked — new dependency failed")

    def test_cut_only_block_restores_prior_ready_and_keeps_completed_status(self):
        self.cut_fixture("Ready")
        self.cut()
        self.assertIn("cut by /cut", self.status())
        self.back()
        self.assertEqual(self.status(), "Ready")
        self.cut_fixture("Complete")
        self.cut(); self.back()
        self.assertEqual(self.status(), "Complete")

    def grow_fixture(self):
        copied = self.root / ".fixture-studio"
        shutil.copytree(ROOT / ".game-studio/runtime", copied / "runtime", ignore=shutil.ignore_patterns("__pycache__"))
        scripts = copied / "scripts"
        scripts.mkdir()
        for name in ("one-shot-grow.sh", "native-runtime.sh", "engine-row.awk"):
            shutil.copyfile(HELPERS / name, scripts / name)
        (copied / "resources/engines").mkdir(parents=True)
        shutil.copyfile(ROOT / ".game-studio/resources/engines/engines.tsv", copied / "resources/engines/engines.tsv")
        (scripts / "one-shot-run.sh").write_text("""#!/usr/bin/env bash
out=$2
case "$FIXTURE_RUN" in
  fail) printf 'not_assessed\tfixture browser unavailable\n'; exit 4 ;;
  na_zero) printf 'not_assessed\tfixture missing hooks\ndone\t0\n'; exit 0 ;;
  no_shot) printf 'done\t180\tplay\n'; exit 0 ;;
esac
mkdir -p "$(dirname "$out")"
printf 'fresh-screenshot' > "$out"
if [ "$FIXTURE_RUN" = wrong_shot ]; then
  printf 'shot\telsewhere.png\t16\n'
else
  printf 'shot\t%s/%s\t16\n' "$(pwd)" "$out"
fi
case "$FIXTURE_RUN" in
  existing_error|new_error) printf 'error\t10\tpre-existing optional audio failure\n' ;;
esac
case "$FIXTURE_RUN" in
  new_error) printf 'error\t35\tnew optional audio failure\nuncaught\t1\n' ;;
  crash_stop) printf 'crash\t60\tstep failed\ndone\t60\tplay\tcrash\n'; exit 0 ;;
esac
printf 'scene\t1\tplay\ndone\t180\tplay\tcomplete\n'
""", encoding="utf-8", newline="\n")
        self.write("prototypes/tiny/index.html", "<script>/* synthetic fixture */</script>")
        self.write("dist-single/index.html", "<script>/* synthetic fixture */</script>")
        self.write(self.ev + "/replay.args", "stop\t180\nlog\tEnter\n")
        self.write(self.ev + "/reference.tsv", "scene\t1\tplay\ndone\t180\tplay\tcomplete\n")
        self.write(self.ev + "/exact", "yes\n")
        self.write(self.ev + "/accepted.tsv", "prior accepted rows\n")
        self.write(self.ev + "/accepted.png", "prior accepted screenshot")
        return scripts

    def accepted(self):
        return tuple((self.root / self.ev / name).read_bytes() for name in ("accepted.tsv", "accepted.png"))

    def test_failed_story_replay_cannot_accept_or_replace_prior_pair(self):
        scripts = self.grow_fixture()
        prior = self.accepted()
        self.write(self.ev + "/story.png", "stale story screenshot")
        output = self.run_script("one-shot-grow", "replay", "tiny", "--as", "story", scripts=scripts, mode="fail", code=4)
        self.assertIn("not_assessed", output)
        self.run_script("one-shot-grow", "accept", "tiny", scripts=scripts, code=4)
        self.assertEqual(self.accepted(), prior)

    def test_unassessed_or_screenshotless_story_cannot_accept(self):
        scripts = self.grow_fixture()
        prior = self.accepted()
        for mode in ("na_zero", "no_shot", "wrong_shot", "crash_stop"):
            with self.subTest(mode=mode):
                self.run_script("one-shot-grow", "replay", "tiny", "--as", "story", scripts=scripts, mode=mode, code=4)
                self.run_script("one-shot-grow", "accept", "tiny", scripts=scripts, code=4)
                self.assertEqual(self.accepted(), prior)

    def test_completed_replay_compares_existing_game_error_as_an_observation(self):
        scripts = self.grow_fixture()
        self.write(self.ev + "/accepted.tsv",
                   "error\t10\tpre-existing optional audio failure\nscene\t1\tplay\ndone\t180\tplay\tcomplete\n")
        prior = self.accepted()
        result = self.run_script("one-shot-grow", "replay", "tiny", "--as", "story", scripts=scripts, mode="existing_error")
        self.assertIn("errors\t1\n", result)
        self.assertIn("against\taccepted\nmatch\tyes\n", result)
        self.assertEqual(self.accepted(), prior)

    def test_complete_replay_with_new_error_can_be_declined_or_explicitly_accepted(self):
        scripts = self.grow_fixture()
        self.write(self.ev + "/accepted.tsv",
                   "error\t10\tpre-existing optional audio failure\nscene\t1\tplay\ndone\t180\tplay\tcomplete\n")
        prior = self.accepted()
        result = self.run_script("one-shot-grow", "replay", "tiny", "--as", "story", scripts=scripts, mode="new_error")
        self.assertIn("errors\t3\n", result)
        self.assertIn("match\tno\terror\t35\tnew optional audio failure\n", result)
        self.assertIn("was\tscene\t1\tplay\n", result)
        # Decline the proposed replacement by leaving the accepted pair alone.
        self.assertEqual(self.accepted(), prior)
        # The approval path runs a separate command on the exact reviewed pair.
        replacement = tuple((self.root / self.ev / name).read_bytes() for name in ("story.tsv", "story.png"))
        accepted = self.run_script("one-shot-grow", "accept", "tiny", scripts=scripts)
        self.assertIn("accepted\t", accepted)
        self.assertEqual(self.accepted(), replacement)

    def test_successful_replay_accepts_matching_pair_but_modified_or_stale_pair_does_not(self):
        scripts = self.grow_fixture()
        self.run_script("one-shot-grow", "replay", "tiny", "--as", "story", scripts=scripts)
        self.run_script("one-shot-grow", "accept", "tiny", scripts=scripts)
        self.assertEqual(self.accepted(), tuple((self.root / self.ev / name).read_bytes() for name in ("story.tsv", "story.png")))
        prior = self.accepted()
        self.write(self.ev + "/story.png", "unrelated screenshot")
        self.run_script("one-shot-grow", "accept", "tiny", scripts=scripts, code=4)
        self.assertEqual(self.accepted(), prior)
        self.run_script("one-shot-grow", "replay", "tiny", "--as", "story", scripts=scripts)
        (self.root / "dist-single/index.html").unlink()
        self.run_script("one-shot-grow", "replay", "tiny", "--as", "story", scripts=scripts, code=4)
        self.run_script("one-shot-grow", "accept", "tiny", scripts=scripts, code=4)
        self.assertEqual(self.accepted(), prior)

if __name__ == "__main__":
    unittest.main()
