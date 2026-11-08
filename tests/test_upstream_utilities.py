"""Run upstream data utilities against a non-game, multilingual fixture."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HELPERS = ROOT / ".game-studio/scripts"


def shell():
    if os.name == "nt":
        git = shutil.which("git")
        if git:
            for parent in Path(git).resolve().parents:
                candidate = parent / "bin/bash.exe"
                if candidate.is_file():
                    return str(candidate)
        return None  # Do not launch the Windows WSL entry-point as a probe.
    return shutil.which("bash")


class UpstreamUtilitiesTests(unittest.TestCase):
    def setUp(self):
        self.bash = shell()
        if not self.bash:
            self.skipTest("Compatible Bash is unavailable")
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "测试 consumer"
        self.root.mkdir()

    def write(self, path, text):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8", newline="\n")

    def call(self, name, *args):
        result = subprocess.run([self.bash, (HELPERS / (name + ".sh")).as_posix(),
                                 "--root", self.root.as_posix(), *args],
                                cwd=self.root, capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
        return result.stdout.decode("utf-8").replace("\r\n", "\n")

    def test_story_facts_acceptance_minimum_uses_selected_granularity(self):
        self.write("production/epics/combat/story-001.md", """# Story 001

> **Status:** Ready
> **Type:** Logic
> **Estimate:** S
> **GDD:** design/gdd/combat.md
> **TR-ID:** TR-combat-001

## Acceptance Criteria
- [ ] Hit lands within range.
""")
        coarse = self.call("story-facts", "--all", "--lint", "--granularity", "coarse")
        fine = self.call("story-facts", "--all", "--lint", "--granularity", "fine")
        self.assertIn("ac_below_min", coarse)
        self.assertNotIn("ac_below_min", fine)
        self.assertIn("TR-combat-001", fine)

    def test_registry_does_not_reuse_retired_ids_or_match_other_system_slug(self):
        self.write("docs/architecture/tr-registry.yaml", """version: 1
requirements:
- id: TR-combat-008
  source: design/gdd/combat.md
  status: deprecated
- id: TR-combat-ai-050
  source: design/gdd/combat-ai.md
  status: active
""")
        self.assertIn("TR-combat-009", self.call("registry", "next-id", "tr", "combat"))
        self.assertIn("TR-combat-ai-051", self.call("registry", "next-id", "tr", "combat-ai"))

    def test_adr_status_finds_file_by_numeric_id_and_uses_verified_date(self):
        self.write("docs/architecture/adr-0007-combat.md", """# ADR-0007

## Status
Accepted

## Date
2026-09-01

## Last Verified
2026-10-12

## ADR Dependencies
| **Depends On** | none |
""")
        rows = self.call("adr-status", "ADR-0007")
        self.assertIn("adr-0007-combat.md", rows)
        self.assertIn("\tAccepted\t", rows)
        self.assertIn("\t2026-10-12\t2026-10-12\t", rows)


if __name__ == "__main__":
    unittest.main()
