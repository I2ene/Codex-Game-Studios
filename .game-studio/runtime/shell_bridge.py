"""Small native boundary for reused Bash algorithms; stdout remains machine-readable."""
import argparse
import json
from pathlib import Path
import shlex
import sys

import config
import engine_table
import observations
from paths import atomic_write, confined, plain


def scalar(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def argv_text(value):
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise ValueError("Expected a nonempty JSON argv array; shell command strings are not accepted")
    return " ".join(shlex.quote(item) for item in value)


def check_path(root, value, external=False, tree=False):
    candidate = Path(value)
    path = plain(candidate) if candidate.is_absolute() else plain(root / candidate) if external else confined(root, value)
    if not external and not path.is_relative_to(root):
        raise ValueError(f"Path escapes the explicit project: {value}")
    if tree and path.is_dir():
        for item in path.rglob("*"):
            if not any(part in {".git", "node_modules"} for part in item.relative_to(path).parts):
                plain(item)
    return path


def save_references(root, files):
    if not files or any(item.isdigit() for item in files):
        print("not_assessed\tPaste numbers are host-specific; provide explicit accessible image files.")
        return 3
    inputs = []
    for item in files:
        path = check_path(root, item, external=True)
        if not path.is_file():
            print("missing\t" + item)
            return 4
        extension = path.suffix.lower()
        if extension not in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
            raise ValueError("Reference input must be an accessible PNG, JPEG, GIF, or WebP file")
        inputs.append((item, path.read_bytes(), ".jpg" if extension == ".jpeg" else extension))
    directory = confined(root, "references")
    for original, data, extension in inputs:
        existing = None
        if directory.is_dir():
            for path in sorted(directory.iterdir()):
                safe = confined(root, path.relative_to(root).as_posix())
                if safe.is_file() and safe.read_bytes() == data:
                    existing = safe
                    break
        if existing:
            print("kept\t" + existing.relative_to(root).as_posix() + "\t" + original)
            continue
        number = 1
        while (directory / f"pasted-{number}{extension}").exists():
            number += 1
        relative = f"references/pasted-{number}{extension}"
        destination = confined(root, relative)
        directory.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as output:
            output.write(data)
        print("saved\t" + relative + "\t" + original)
    return 0


def apply_batch(root, manifest):
    """Commit a cut planner's outputs together, restoring files on failure."""
    records = plain(manifest).read_text(encoding="utf-8-sig").splitlines()
    changes = {}
    for record in records:
        source, sep, target = record.partition("\t")
        if not sep or "\t" in target:
            raise ValueError("Invalid cut write manifest")
        destination = check_path(root, target)
        if destination.exists() and not destination.is_file():
            raise ValueError(f"Cut output is not a file: {target}")
        data = plain(source).read_bytes()
        if destination in changes and changes[destination] != data:
            raise ValueError("Conflicting cut writes target the same path")
        changes[destination] = data
    changes = {path: data for path, data in changes.items() if not path.exists() or path.read_bytes() != data}
    before = {path: path.read_bytes() if path.exists() else None for path in changes}
    applied = []
    try:
        for path, data in changes.items():
            atomic_write(path, data)
            applied.append(path)
    except Exception:
        for path in reversed(applied):
            if before[path] is None:
                path.unlink()
            else:
                atomic_write(path, before[path])
        raise
    for path in changes:
        print("wrote\t" + path.relative_to(root).as_posix())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["get", "argv", "json-argv", "project-state", "path", "tree",
                                              "clean", "set", "references", "batch", "bundler-version", "list-files"])
    parser.add_argument("items", nargs="*")
    parser.add_argument("--root", required=True)
    parser.add_argument("--external", action="store_true")
    parser.add_argument("--stage", action="store_true")
    args = parser.parse_args()
    root = plain(args.root)
    if not root.is_dir():
        raise ValueError("Explicit project root must exist")
    op = args.operation
    if op == "bundler-version":
        from engine import web_bundler
        record = web_bundler(root)
        value = record.get("installed") or record.get("declared_range")
        if isinstance(value, str) and __import__("re").fullmatch(r"\d+\.\d+\.\d+(?:[-+][\w.-]+)?", value):
            print(value)
        return 0
    if op == "batch":
        apply_batch(root, args.items[0])
        return 0
    if op == "list-files":
        for item in args.items:
            directory = check_path(root, item)
            for file in engine_table.source_files(root, directory.relative_to(root).as_posix()):
                relative = file.relative_to(root).as_posix()
                print("./" + relative if directory == root else relative)
        return 0
    if op == "references":
        return save_references(root, args.items)
    if op in {"path", "tree"}:
        for value in args.items:
            print(check_path(root, value, args.external, tree=op == "tree"))
        return 0
    if op == "json-argv":
        print(argv_text(json.loads(args.items[0])))
        return 0
    if op == "project-state":
        for key, fact in observations.project_state(root, args.stage)["facts"].items():
            value = fact["value"]
            print(key + "\t" + (scalar(value) if value is not None else "unknown" if key == "source_files" else "-") +
                  "\t" + fact["source"])
        return 0
    resolved = config.resolve(root, require_clean=op in {"argv", "clean", "set"})
    if op == "clean":
        return 0
    if op == "set":
        import studio
        result = studio.settings(root, args.items[0])
        print(json.dumps(result, ensure_ascii=False, default=str))
        return 0
    key = args.items[0]
    if op == "argv":
        value = resolved["values"].get(key)
        if value is not None:
            print(argv_text(value))
    elif key in {"code_root", "test_root"}:
        record = engine_table.describe(resolved)[key]
        if record["status"] == "INVALID":
            raise ValueError(record["reason"])
        print(scalar(record["value"]))
    else:
        print(scalar(resolved["values"].get(key)))
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, IndexError) as error:
        print("Game Studios: " + str(error), file=sys.stderr)
        raise SystemExit(2)
