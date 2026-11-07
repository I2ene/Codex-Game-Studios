"""Plan and verify a byte-preserving edit to a single YAML setting."""
import json
import re

import yaml

import config
from markdown_ops import text_parts


def render_leaf(value, style=None):
    if isinstance(value, str) and style == "'":
        return "'" + value.replace("'", "''") + "'"
    if isinstance(value, str) and style == '"':
        return json.dumps(value, ensure_ascii=False)
    lines = yaml.safe_dump(value, default_flow_style=True, allow_unicode=True, width=1000000).splitlines()
    if lines[-1:] == ["..."]:
        lines.pop()
    if len(lines) != 1:
        raise ValueError("Cannot preserve a single-line YAML layout for this value")
    return lines[0]


def plan(path, parts, value):
    original = path.read_bytes() if path.exists() else b""
    bom, text, newline = text_parts(original)
    old = config.flatten(config.load(path))
    dotted = ".".join(parts)
    if any(key.startswith(dotted + ".") for key in old):
        raise ValueError(f"Assignment would replace a mapping: {dotted}")
    if any(part not in old and not re.fullmatch(r"[\w-]+", part) for part in parts):
        raise ValueError(f"Cannot insert a non-simple YAML key: {dotted}")
    root_node = yaml.compose(text, Loader=config.Loader)
    node = root_node
    remaining = list(parts)
    index, edit = 0, "inserted"
    if node is None:
        if text and not text.endswith(("\n", "\r")):
            text += newline
        index = len(text)
        updated = text + nested(remaining, value, 0, newline)
        edit = "created" if not original else "inserted"
    else:
        while remaining:
            if not isinstance(node, yaml.MappingNode):
                raise ValueError("Assignment would overwrite a scalar ancestor")
            key = remaining[0]
            match = next((v for k, v in node.value if k.value == key), None)
            if match is None:
                updated, index = insert(text, node, remaining, value, newline)
                break
            remaining.pop(0)
            if remaining:
                node = match
                continue
            if isinstance(match, yaml.MappingNode):
                raise ValueError(f"Assignment would replace a mapping: {dotted}")
            start, end = match.start_mark, match.end_mark
            if start.line != end.line or getattr(match, "style", None) in ("|", ">"):
                raise ValueError(f"Cannot safely edit a multiline YAML value: {dotted}")
            if dotted in old and type(old[dotted]) is type(value) and old[dotted] == value:
                return original, {"status": "UNCHANGED", "line": start.line + 1, "readback": value,
                                  "previous": old[dotted]}
            index = start.index
            rendered = render_leaf(value, getattr(match, "style", None))
            if start.index == end.index and start.index and text[start.index - 1] == ":":
                rendered = " " + rendered
            updated = text[:start.index] + rendered + text[end.index:]
            edit = "replaced"
            break
    after = config.flatten(yaml.load(updated, Loader=config.Loader))
    expected = {**old, dotted: value}
    if after.keys() != expected.keys() or any(type(after[key]) is not type(item) or after[key] != item
                                              for key, item in expected.items()):
        raise ValueError("Configuration preview did not round-trip with only the requested leaf changed")
    return bom + updated.encode("utf-8"), {"status": "WOULD_UPDATE", "edit": edit,
                                           "line": text.count("\n", 0, index) + 1,
                                           "readback": after[dotted], "previous": old.get(dotted)}


def nested(parts, value, indent, newline):
    result = []
    for i, key in enumerate(parts):
        rendered = (" " + render_leaf(value)) if i == len(parts) - 1 else ""
        result.append(" " * (indent + 2 * i) + key + ":" + rendered + newline)
    return "".join(result)


def insert(text, node, parts, value, newline):
    if node.flow_style:
        end = node.end_mark.index - 1
        body = value
        for key in reversed(parts[1:]):
            body = {key: body}
        # Existing flow maps may have a trailing comma; do not add a second one.
        leading = ", " if node.value and not text[:end].rstrip().endswith(",") else " " if node.value else ""
        update = leading + parts[0] + ": " + render_leaf(body)
        return text[:end] + update + text[end:], end
    indent = node.value[0][0].start_mark.column if node.value else node.start_mark.column
    end = node.end_mark.index
    if end == len(text):
        leading = newline if text and not text.endswith(("\r", "\n")) else ""
    else:
        # The next token may be indented in the parent; insert before its full line.
        end = text.rfind("\n", 0, end) + 1
        leading = ""
    return text[:end] + leading + nested(parts, value, indent, newline) + text[end:], end
