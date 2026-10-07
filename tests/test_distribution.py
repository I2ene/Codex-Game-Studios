"""Release validation failures must be actionable before packaging."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_validate", ROOT / "tools/validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class DocumentTests(unittest.TestCase):
    def test_missing_relative_link_is_reported_from_nested_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "README.md").write_text("[Guide](docs/guide.md)\n", encoding="utf-8")
            guide = root / "docs/guide.md"
            guide.write_text("[Missing](../absent.md)\n", encoding="utf-8")
            errors = validator.document_errors(root)
            self.assertTrue(any("docs/guide.md" in e and "absent.md" in e for e in errors), errors)

    def test_valid_link_with_spaces_anchor_and_code_example(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a guide.md").write_text("# Start here\n", encoding="utf-8")
            (root / "README.md").write_text("[Guide](<a guide.md#start-here>)\n```text\n[Example](missing.md)\n```\n[Web](https://example.org/)\n", encoding="utf-8")
            self.assertEqual(validator.document_errors(root), [])

    def test_wrong_anchor_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Start\n[Broken](#absent)\n", encoding="utf-8")
            errors = validator.document_errors(root)
            self.assertTrue(any("absent" in e for e in errors), errors)


class ReleaseTests(unittest.TestCase):
    def test_added_unmanifested_payload_is_rejected(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".game-studio").mkdir()
            (root / ".game-studio/VERSION").write_text("2.0.0\n")
            (root / ".game-studio/release.json").write_text(json.dumps({"schema": 1, "version": "2.0.0", "files": {}}))
            errors = validator.manifest_errors(root)
            self.assertTrue(any("manifest" in e.lower() for e in errors), errors)

    def test_fresh_install_seed_matches_release_version(self):
        import sys
        sys.path.insert(0, str(ROOT / ".game-studio/runtime"))
        import installer
        import yaml
        with tempfile.TemporaryDirectory() as tmp:
            import shutil
            source, target = Path(tmp) / "release", Path(tmp) / "consumer"
            for folder in [".agents", ".codex/agents", ".game-studio"]:
                shutil.copytree(ROOT / folder, source / folder, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (source / ".game-studio/VERSION").write_text("2.0.99\n", encoding="utf-8")
            installer.build_manifest(source)
            installer.install(source, target)
            self.assertEqual(yaml.safe_load((target / "project.yaml").read_text())["framework"]["version"], "2.0.99")
