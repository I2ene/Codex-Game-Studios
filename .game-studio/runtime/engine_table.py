"""Shared upstream engine facts and source-aware project root resolution."""
import csv
import os
from pathlib import Path

from paths import confined, plain, relative_parts

TABLE = Path(__file__).resolve().parents[1] / "resources/engines/engines.tsv"
COLUMNS = ("engine", "code_root", "test_root", "asset_root", "run", "build", "test", "smoke")
SKIP_TOP = {".claude", ".game-studio", ".agents", ".codex", ".git", ".specify", ".scratch",
            ".venv", ".worktrees", "production", "design", "docs", "tests", "studio-tests",
            "prototypes", "tools", "node_modules", "dist", "dist-single", "coverage", "test-results",
            "playwright-report"}
DENY_CODE = {".claude", ".game-studio", ".agents", ".codex", ".git", ".specify", "production",
             "design", "docs", "tests", "studio-tests", "prototypes"}
DENY_TEST = DENY_CODE - {"tests"}


def table():
    with TABLE.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source, delimiter="\t")
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError("Invalid engine table columns")
        result = {}
        for row in reader:
            if None in row or any(not isinstance(row[key], str) or not row[key] for key in COLUMNS):
                raise ValueError("Incomplete engine table row")
            name = row["engine"].casefold()
            if name in result:
                raise ValueError(f"Duplicate engine table row: {row['engine']}")
            result[name] = {key: None if item == "-" else item for key, item in row.items()}
        return result


def lookup(name):
    family = name.strip().casefold() if isinstance(name, str) else ""
    if family.startswith("unreal"):
        family = "unreal"
    return table().get(family)


def _root_unset(value):
    return value is None or (isinstance(value, str) and
                             (not value.strip() or value.startswith("[") or value in {"null", "~"}))


def root_value(root, value, key, *, explicit=False, kind=None):
    result = {"value": None, "source": key, "status": "UNSET", "reason": None}
    if _root_unset(value):
        return result
    try:
        if not isinstance(value, str):
            raise ValueError("expected a repository-relative directory")
        normalized = value.rstrip("/")
        while normalized.startswith("./"):
            normalized = normalized[2:]
        normalized = normalized or "."
        if "\\" in normalized or "//" in normalized or "/./" in normalized:
            raise ValueError("use a plain forward-slash directory path")
        parts = relative_parts(normalized)
        denied = DENY_TEST if kind == "test_root" or key.endswith("test_root") else DENY_CODE
        if parts and parts[0].casefold() in denied:
            raise ValueError("framework or planning directories are not code/test roots")
        if not explicit and "<Module>" in normalized:
            return {**result, "value": normalized, "status": "TEMPLATE",
                    "reason": "Supply the actual project module before using this table path"}
        path = confined(root, normalized)
        if explicit:
            parent = root
            for part in parts:
                names = {entry.name for entry in parent.iterdir()} if parent.is_dir() else set()
                if part not in names:
                    spelling = next((entry for entry in names if entry.casefold() == part.casefold()), None)
                    raise ValueError(f"spelled {spelling!r} on disk, not {part!r}" if spelling else f"no directory {normalized!r}")
                parent /= part
            if not path.is_dir():
                raise ValueError(f"no directory {normalized!r}")
        result.update(value=path.relative_to(root).as_posix(), status="VALID" if path.is_dir() else "ABSENT")
    except (OSError, ValueError) as error:
        result.update(status="INVALID", reason=str(error))
    return result


def describe(resolved):
    root = plain(resolved["root"])
    values = resolved["values"]
    record = lookup(values.get("engine.name")) or {}
    notes = []
    roots = {}
    for kind in ("code_root", "test_root"):
        nested, legacy = "engine." + kind, kind
        supplied = [key for key in (nested, legacy) if not _root_unset(values.get(key))]
        if len(supplied) == 2 and values[nested] != values[legacy]:
            notes.append(f"{nested} takes priority over legacy {legacy}")
        selected = supplied[0] if supplied else None
        if selected:
            roots[kind] = root_value(root, values[selected], selected, explicit=True, kind=kind)
        else:
            roots[kind] = root_value(root, record.get(kind), "engine.name", kind=kind)
    return {"engine": record.get("engine"), "configured_engine": values.get("engine.name"),
            **roots, "asset_root": record.get("asset_root"), "notes": notes,
            "commands": {name: {"argv": values.get("commands." + name),
                                "source": resolved["sources"].get("commands." + name, "unset"),
                                "suggestion": record.get(name)} for name in ("run", "build", "test", "smoke")}}


def source_files(root, relative):
    """Prune top-level framework/generated directories before traversing a flat source root."""
    root = plain(root)
    directory = confined(root, relative)
    if not directory.is_dir():
        return []
    result = []
    for current, directories, files in os.walk(directory, followlinks=False):
        base = Path(current)
        if base == root:
            directories[:] = [name for name in directories if name not in SKIP_TOP]
        for name in directories:
            confined(root, (base / name).relative_to(root).as_posix())
        for name in files:
            result.append(confined(root, (base / name).relative_to(root).as_posix()))
    return sorted(result)
