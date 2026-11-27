"""Verify source-map coverage and native destinations, not model/game behavior."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def git(root, *args):
    return subprocess.check_output(["git", "-c", "core.autocrlf=false", *args], cwd=root)


def changes(root, source_base, source_target):
    result = []
    fields = git(root, "diff", "--name-status", "-z", "-M", source_base, source_target).decode().split("\0")
    i = 0
    while i < len(fields) and fields[i]:
        status, name = fields[i:i + 2]
        i += 2
        if status.startswith(("R", "C")):
            before, after = name, fields[i]
            i += 1
        else:
            before, after = ("-", name) if status == "A" else (name, "-") if status == "D" else (name, name)
        result.append((status, before, after))
    return result


def audit(root, source_base, source_target, require_ancestry=False):
    root = Path(root).resolve()
    errors = []
    with (root / "docs/upstream-file-map.tsv").open(encoding="utf-8", newline="") as stream:
        rows = [row for row in csv.DictReader(stream, delimiter="\t")
                if row.get("source_base") == source_base and row.get("source_target") == source_target]
    expected = Counter(changes(root, source_base, source_target))
    actual = Counter((row["git_status"], row["source_before"], row["source_after"]) for row in rows)
    for entry in expected - actual:
        errors.append("Unmapped source delta: " + repr(entry))
    for entry in actual - expected:
        errors.append("Extra/duplicate source delta: " + repr(entry))
    for row in rows:
        source = row["source_after"] if row["source_after"] != "-" else row["source_before"]
        for key in ["source_purpose", "native_after", "disposition", "rationale", "verification"]:
            if not row.get(key, "").strip():
                errors.append(source + ": missing " + key)
        if row["disposition"] not in {"reuse", "host adaptation", "verified equivalent", "host boundary"}:
            errors.append(source + ": unknown disposition")
        target = (root / row["native_after"]).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            errors.append(source + ": missing/conflicting native destination " + row["native_after"])
        elif row["disposition"] == "reuse" and row["source_after"] != "-":
            raw = git(root, "show", source_target + ":" + row["source_after"])
            if hashlib.sha256(raw).digest() != hashlib.sha256(target.read_bytes()).digest():
                errors.append(source + ": reuse differs byte-for-byte; classify/document the adaptation")
    if require_ancestry:
        for sha in [source_base, source_target]:
            result = subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=root)
            if result.returncode:
                errors.append("Source is not an ancestor of HEAD: " + sha)
    return {"status": "FORMAT", "source_base": source_base, "source_target": source_target,
            "source_deltas": sum(expected.values()), "mapped_rows": len(rows), "errors": errors,
            "boundary": "Coverage, paths and reuse hashes only; semantic execution requires separate evidence."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-base", required=True)
    parser.add_argument("--source-target", required=True)
    parser.add_argument("--require-ancestry", action="store_true")
    args = parser.parse_args()
    result = audit(ROOT, args.source_base, args.source_target, args.require_ancestry)
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result["errors"]))
