"""Confined Markdown observations and explicitly requested, local edits."""
import re

from paths import atomic_write, confined

HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*$")
FENCE = re.compile(r"^ {0,3}(\x60{3,}|~{3,})(.*)$")
COMMENT = re.compile(r"\x60+[^\x60]*\x60+|(<!--)")
FIELD = re.compile(r"^(?P<prefix>[ \t]*(?:>[ \t]*)?(?:[-+][ \t]+)?)(?P<open>\*\*)?"
                   r"(?P<name>[^*:\r\n]+?)(?P<before>\*\*)?:(?P<after>\*\*)?"
                   r"(?P<space>[ \t]*)(?P<value>.*?)(?P<trailing>[ \t]*)$")
PLACEHOLDER = re.compile(r"\[(?:to be designed|to be written|tbd)\]|^\s*_?TODO\b", re.I)
UTF8_BOM = b"\xef\xbb\xbf"


def text_parts(data):
    """Separate the BOM; do not perform universal-newline translation."""
    bom = UTF8_BOM if data.startswith(UTF8_BOM) else b""
    text = data[len(bom):].decode("utf-8")
    return bom, text, "\r\n" if "\r\n" in text else "\n"


def visible_lines(lines):
    """Expose prose outside fences and HTML comments without changing line positions."""
    fence = None
    in_comment = False
    for raw in lines:
        line = raw.rstrip("\r\n")
        if fence:
            marker = FENCE.match(line)
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            yield ""
            continue
        marker = FENCE.match(line) if not in_comment else None
        if marker:
            fence = marker[1]
            yield ""
            continue
        cleaned = ""
        while line:
            if in_comment:
                end = line.find("-->")
                if end < 0:
                    break
                in_comment = False
                line = line[end + 3:]
            else:
                start = next((m.start() for m in COMMENT.finditer(line) if m[1]), -1)
                if start < 0:
                    cleaned += line
                    break
                cleaned += line[:start]
                in_comment = True
                line = line[start + 4:]
        yield cleaned


def sections(lines):
    visible = list(visible_lines(lines))
    rows = []
    for index, line in enumerate(visible):
        heading = HEADING.match(line)
        if heading:
            rows.append({"title": re.sub(r"[ \t]+#+$", "", heading[2]),
                         "level": len(heading[1]), "start": index + 1, "end": len(lines)})
    for index, row in enumerate(rows):
        for subsequent in rows[index + 1:]:
            if subsequent["level"] <= row["level"]:
                row["end"] = subsequent["start"] - 1
                break
        prose = [line for line in visible[row["start"]:row["end"]]
                 if line.strip() and not HEADING.match(line) and not re.fullmatch(r"\s*(?:-{3,}|\*{3,}|_{3,})\s*", line)]
        row["status"] = ("PLACEHOLDER" if any(PLACEHOLDER.search(line) for line in prose)
                         else "COMPLETE" if prose else "EMPTY")
    return rows


def match_section(rows, wanted):
    def normalize(title):
        return " ".join(title.split()).casefold()

    level = re.match(r"^(#{1,6})\s+(.+)$", wanted)
    title = normalize(level[2] if level else wanted)
    candidates = [row for row in rows if normalize(row["title"]) == title
                  and (not level or row["level"] == len(level[1]))]
    if len(candidates) > 1:
        raise ValueError(f"Ambiguous Markdown section: {wanted}")
    return candidates[0] if candidates else None


def edit_field(lines, name, value, after, newline):
    if not re.fullmatch(r"[^*:\r\n]+", name) or not name.strip() or "\r" in value or "\n" in value:
        raise ValueError("A Markdown field name and value must fit on one line")
    fields = {}
    for i, line in enumerate(visible_lines(lines)):
        heading = HEADING.match(line)
        if heading and len(heading[1]) >= 2:
            break
        if field := FIELD.match(line):
            fields.setdefault(field["name"].strip().casefold(), []).append((i, field))

    def find(label):
        candidates = fields.get(label.strip().casefold(), [])
        if len(candidates) > 1:
            raise ValueError(f"Ambiguous Markdown field: {label}")
        return candidates[0] if candidates else None

    current = find(name)
    if current:
        i, _ = current
        content = lines[i]
        raw = FIELD.match(content.rstrip("\r\n"))
        if not raw or raw["name"].strip().casefold() != name.strip().casefold():
            raise ValueError(f"Cannot preserve formatting of Markdown field: {name}")
        end = raw.end("value")
        comment = next((item for item in COMMENT.finditer(raw["value"]) if item[1]), None)
        if comment:
            suffix = raw["value"][comment.start():]
            if not re.fullmatch(r"(?:<!--.*?-->[ \t]*)+", suffix):
                raise ValueError(f"Cannot preserve an embedded Markdown field comment: {name}")
            end = raw.start("value") + len(raw["value"][:comment.start()].rstrip(" \t"))
        lines[i] = content[:raw.start("value")] + value + content[end:]
        return i + 1
    anchor = find(after) if after else None
    if not anchor:
        raise ValueError(f"Markdown field not found: {name}; specify an existing --after field to add it")
    i, match = anchor
    if not lines[i].endswith(("\r", "\n")):
        lines[i] += newline
    line = match[0][:match.start("name")] + name + match[0][match.end("name"):match.start("value")] + value
    lines.insert(i + 1, line + newline)
    return i + 2


def command(root, action, relative, targets, *, body=False, body_data=None, after=None):
    path = confined(root, relative)
    data = path.read_bytes()
    bom, text, newline = text_parts(data)
    lines = text.splitlines(keepends=True)
    rows = sections(lines)
    result = {"path": relative, "action": action}
    if action == "list":
        if targets:
            raise ValueError("Markdown list takes only a file")
        return {**result, "status": "OBSERVED", "sections": rows}
    if action == "status":
        selected = [match_section(rows, title) or {"title": title, "status": "NOT_FOUND"}
                    for title in targets] if targets else rows
        return {**result, "status": "OBSERVED", "sections": selected}
    if action == "set-field":
        if len(targets) != 2:
            raise ValueError("Markdown set-field needs FILE FIELD VALUE")
        line = edit_field(lines, *targets, after, newline)
    else:
        if len(targets) != 1:
            raise ValueError(f"Markdown {action} needs FILE HEADING")
        selected = match_section(rows, targets[0])
        if not selected:
            raise ValueError(f"Markdown section not found: {targets[0]}")
        line, end = selected["start"], selected["end"]
        if action == "extract":
            return {**result, "status": "OBSERVED", "section": selected,
                    "text": "".join(lines[line if body else line - 1:end])}
        if body_data is None:
            raise ValueError(f"Markdown {action} needs an explicit body")
        _, payload, _ = text_parts(body_data)
        replacement = newline.join(payload.rstrip("\r\n").splitlines())
        if replacement:
            replacement += newline
        if action == "replace":
            if not lines[line - 1].endswith(("\r", "\n")) and replacement:
                lines[line - 1] += newline
            boundary = end
            while boundary > line and not lines[boundary - 1].strip():
                boundary -= 1
            lines[line:boundary] = [replacement] if replacement else []
        elif action == "insert-before":
            if not replacement:
                raise ValueError("Markdown insert-before needs a nonempty body")
            before = newline if line > 1 and lines[line - 2].strip() else ""
            lines.insert(line - 1, before + replacement + newline)
        else:
            raise ValueError(f"Unknown Markdown action: {action}")
    rendered = bom + "".join(lines).encode("utf-8")
    if rendered != data:
        atomic_write(path, rendered)
    return {**result, "status": "UNCHANGED" if rendered == data else "UPDATED", "line": line}
