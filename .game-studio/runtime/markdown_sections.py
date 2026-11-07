"""Complete ATX section spans, adapted from upstream md-section.sh."""
import re

HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
PLACEHOLDER = re.compile(r"\[(?:To be designed|TBD|To be written)\]|^\s*_?TODO\b", re.I)


def visible_lines(lines):
    fence, comment = None, False
    for line in lines:
        m = FENCE.match(line)
        if fence:
            if m and m[1][0] == fence[0] and len(m[1]) >= len(fence) and not m[2].strip():
                fence = None
            yield ""
            continue
        if not comment and m:
            fence = m[1]
            yield ""
            continue
        # Comment markers in inline code are literal, not block delimiters.
        chunks = re.split(r"(`+[^`]*`+|<!--|-->)", line)
        visible = []
        for chunk in chunks:
            if chunk == "<!--":
                comment = True
            elif chunk == "-->" and comment:
                comment = False
            elif not comment:
                visible.append(chunk)
        yield "".join(visible)


def parse(text):
    lines = text.splitlines()
    visible = list(visible_lines(lines))
    headings = [(i, len(m[1]), m[2].strip()) for i, line in enumerate(visible) if (m := HEADING.match(line))]
    rows = []
    for j, (start, level, title) in enumerate(headings):
        stop = next((i for i, n, _ in headings[j + 1:] if n <= level), len(lines))
        body = visible[start + 1:stop]
        status = ("PLACEHOLDER" if any(PLACEHOLDER.search(line) for line in body)
                  else "COMPLETE" if any(line.strip() and line.strip() != "---" and not HEADING.match(line) for line in body)
                  else "EMPTY")
        rows.append({"level": level, "title": title, "first": start + 1, "last": stop,
                     "status": status, "text": "\n".join(lines[start:stop])})
    return rows
