"""Explicit checkpoint edits, including the upstream marked active.md format."""
from markdown_ops import FENCE, text_parts
from paths import atomic_write, confined, digest

OPEN = "<!-- CHECKPOINT -->"
CLOSE = "<!-- /CHECKPOINT -->"
STATUS_CLOSE = "<!-- /STATUS -->"
DEFAULT = "production/session-state/active.md"


def markers(lines):
    found = {OPEN: [], CLOSE: [], STATUS_CLOSE: []}
    fence = None
    comment = False
    for i, raw in enumerate(lines):
        line = raw.strip()
        marker = FENCE.match(raw.rstrip("\r\n")) if not comment else None
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            continue
        if marker:
            fence = marker[1]
            continue
        if comment:
            if "-->" in line:
                comment = False
            continue
        if line in found:
            found[line].append(i)
        elif "<!--" in line and "-->" not in line.split("<!--", 1)[1]:
            comment = True
    return found


def save(root, relative, source_relative, append=False):
    path = confined(root, relative)
    source = confined(root, source_relative)
    if path == source:
        raise ValueError("Checkpoint source and destination must be different files")
    original = path.read_bytes() if path.exists() else b""
    bom, text, newline = text_parts(original)
    lines = text.splitlines(keepends=True)
    found = markers(lines)
    openings, closings = found[OPEN], found[CLOSE]
    if (len(openings) != len(closings) or len(openings) > 1
            or openings and openings[0] >= closings[0]):
        raise ValueError("Checkpoint markers are missing, repeated, or out of order")
    payload = source.read_bytes()
    _, content, source_newline = text_parts(payload)
    if not content.strip():
        raise ValueError("An empty checkpoint is not saved state")
    content_lines = content.rstrip("\r\n").splitlines()
    if any(line.strip() in {OPEN, CLOSE, STATUS_CLOSE} for line in content_lines):
        raise ValueError("Checkpoint body must not contain checkpoint or status boundary markers")
    if not original:
        newline = source_newline
    normalized = newline.join(content_lines) + newline
    if append:
        if text.rstrip("\r\n").splitlines()[-len(content_lines):] == content_lines:
            rendered = original
        else:
            prefix = text + (newline if text and not text.endswith(("\r", "\n")) else "")
            rendered = bom + (prefix + normalized).encode()
    elif openings:
        rendered = bom + ("".join(lines[:openings[0] + 1]) + normalized + "".join(lines[closings[0]:])).encode()
    elif relative == DEFAULT and original:
        after = found[STATUS_CLOSE][0] + 1 if len(found[STATUS_CLOSE]) == 1 else 0
        prefix = "".join(lines[:after])
        if prefix and not prefix.endswith(("\r", "\n")):
            prefix += newline
        block = OPEN + newline + normalized + CLOSE + newline
        rendered = bom + (prefix + block + newline + "".join(lines[after:])).encode()
    else:
        rendered = payload
    if rendered != original:
        if original and not append:
            backup = confined(root, path.with_name("previous-" + digest(original)[:12] + ".md").relative_to(root).as_posix())
            if backup.exists() and backup.read_bytes() != original:
                raise ValueError("A different file already occupies the checkpoint backup path")
            if not backup.exists():
                atomic_write(backup, original)
        atomic_write(path, rendered)
    return {"status": "UNCHANGED" if rendered == original else "APPENDED" if append else "SAVED",
            "path": relative, "bytes": len(rendered), "hash": digest(rendered)}
