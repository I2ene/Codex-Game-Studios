"""Explicit project-state, guard, scaffold, and native skill observations."""
from datetime import date
import configparser
import json
import re
from urllib.parse import urlsplit, urlunsplit

import checks
import config
from markdown_ops import sections, text_parts, visible_lines
from paths import confined

SOURCE_EXTENSIONS = {".gd", ".gdshader", ".cs", ".cpp", ".cc", ".c", ".h", ".hpp", ".rs",
                     ".py", ".js", ".ts", ".lua", ".java", ".kt"}
CODE_ROOTS = {"godot": "src", "unity": "Assets", "unreal": "Source"}
WATCHED = ("design/", "docs/architecture/", "production/session-state/")
NON_TEXT = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp", ".tif", ".tiff"}


def code_root(root, resolved):
    value = resolved["values"].get("code_root")
    if value is not None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("code_root must be a repository-relative directory")
        target = confined(root, value)
        return target.relative_to(root).as_posix(), resolved["sources"]["code_root"]
    engine = str(resolved["values"].get("engine.name") or "").lower()
    if engine in CODE_ROOTS:
        return CODE_ROOTS[engine], "engine.name"
    candidates = [entry.name for entry in root.iterdir() if entry.name in CODE_ROOTS.values()
                  and confined(root, entry.name).is_dir()]
    return (candidates[0], "detected") if len(candidates) == 1 else (None, "unset")


def project_state(root, stage_only=False):
    resolved = config.resolve(root)
    facts = {}

    def fact(key, value, source):
        facts[key] = {"value": value, "source": source}

    stage_file = confined(root, "production/stage.txt")
    raw_stage = next((line.strip() for line in stage_file.read_text(encoding="utf-8-sig").splitlines() if line.strip()),
                     None) if stage_file.is_file() else None
    project_file = confined(root, "project.yaml")
    yaml_stage = config.flatten(config.load(project_file, [])).get("project.stage")
    stage = resolved["values"]["project.stage"]
    fact("stage_yaml", yaml_stage, "project.yaml" if project_file.is_file() else "unset")
    fact("stage_txt", raw_stage, "production/stage.txt" if stage_file.is_file() else "unset")
    fact("stage", stage, resolved["sources"]["project.stage"])
    fact("phase", stage.lower().replace(" ", "-") if stage else None, "project.stage" if stage else "unset")
    if stage_only:
        return {"status": "OBSERVED", "facts": facts, "notes": resolved["notes"]}
    fact("root", str(root), "explicit root")
    fact("engine", resolved["values"]["engine.name"], resolved["sources"]["engine.name"])
    relative, source = code_root(root, resolved)
    fact("code_root", relative, source)
    code = confined(root, relative) if relative else None
    count = (sum(p.suffix.lower() in SOURCE_EXTENSIONS for p in checks.files(code, "**/*"))
             if code and code.is_dir() else None)
    fact("source_files", count, relative if count is not None else "unset")
    concept = next((path for path in ("design/gdd/game-concept.md", "design/game-brief.md")
                    if confined(root, path).is_file()), None)
    fact("concept", concept, concept or "absent")
    index = "design/gdd/systems-index.md"
    fact("systems_index", index if confined(root, index).is_file() else None, index)
    for key, pattern in {"gdd_files": "design/gdd/*.md", "adr": "docs/architecture/adr-*.md",
                         "story": "production/epics/**/story-*.md", "sprint": "production/sprints/*.md",
                         "milestone": "production/milestones/*.md"}.items():
        fact(key, len(checks.files(root, pattern)), pattern)
    prototypes = confined(root, "prototypes")
    fact("prototype", sum(confined(root, p.relative_to(root).as_posix()).is_dir() for p in prototypes.iterdir())
         if prototypes.is_dir() else 0, "prototypes/*/")
    git_dir = confined(root, ".git")
    git_config = confined(root, ".git/config") if git_dir.is_dir() else None
    origin = None
    if git_config and git_config.is_file():
        ini = configparser.ConfigParser(interpolation=None, strict=False)
        try:
            ini.read(git_config, encoding="utf-8")
            origin = ini.get('remote "origin"', "url", fallback=None)
            if origin and "://" in origin:
                parsed = urlsplit(origin)
                origin = urlunsplit((parsed.scheme, parsed.netloc.rsplit("@", 1)[-1], parsed.path, "", ""))
        except (configparser.Error, ValueError):
            pass  # Facts remain unavailable; no Git is executed and no external Git dir is opened.
    fact("origin_url", origin, ".git/config" if origin else "unset")
    if count is not None and count >= 10:
        inferred = ("production", "source_files>=10")
    elif facts["story"]["value"]:
        inferred = ("pre-production", "story>=1")
    elif facts["adr"]["value"]:
        inferred = ("technical-setup", "adr>=1")
    elif facts["systems_index"]["value"]:
        inferred = ("systems-design", "systems_index")
    elif concept:
        inferred = ("concept", "concept")
    else:
        inferred = (None, "no phase evidence")
    fact("phase_inferred", *inferred)
    return {"status": "OBSERVED", "facts": facts, "notes": resolved["notes"]}


def read_guard(root, action, relative, bounded=False):
    path = confined(root, relative)
    relative = path.relative_to(root).as_posix()
    if action == "sections":
        if not path.is_file():
            return {"path": relative, "status": "ABSENT", "sections": []}
        _, text, _ = text_parts(path.read_bytes())
        return {"path": relative, "status": "OBSERVED", "sections": sections(text.splitlines(keepends=True))}
    resolved = config.resolve(root)
    values, sources = resolved["values"], resolved["sources"]
    enabled = values.get("features.read_guard", "on") not in (False, "off")
    limit = values.get("features.read_guard_kb", 40)
    threshold = limit * 1024
    watched = relative.startswith(WATCHED) and path.suffix.lower() not in NON_TEXT
    size = path.stat().st_size if path.is_file() else None
    return {"path": relative, "status": "ABSENT" if size is None else
            "LARGE" if enabled and watched and not bounded and size > threshold else "OBSERVED",
            "guard": "on" if enabled else "off", "guard_source": sources.get("features.read_guard", "default"),
            "threshold": threshold, "threshold_source": sources.get("features.read_guard_kb", "default"),
            "watched": watched, "size": size, "bounded": bounded}


def config_findings(root, relative, content, previous=None):
    try:
        notes = []
        values = config.flatten(config.load(content, notes))
        old = config.flatten(config.load(previous, [])) if previous and previous.is_file() else {}
    except (ValueError, OSError) as error:
        return [{"code": "CONFIG_INVALID", "path": relative, "detail": str(error)}]
    findings = [{"code": "CONFIG_INVALID", "path": relative, "detail": note} for note in notes]
    for key, value in values.items():
        if key in old and old[key] == value and type(old[key]) is type(value):
            continue
        row = {"path": relative, "key": key, "value": value}
        if relative == "project.local.yaml" and key not in config.LOCAL and key != "schema_version" and not key.startswith("framework."):
            findings.append({"code": "NOT_LOCAL", **row})
        allowed = config.ENUMS.get(key)
        if allowed and value is not None and not any(type(value) is type(item) and value == item for item in allowed):
            findings.append({"code": "ENUM", "allowed": allowed, **row})
        if key == "modes.review_mode":
            findings.append({"code": "REVIEW_MODE", **row})
    return findings


def write_guard(root, action, targets, tool="Write"):
    findings = []
    if action == "artifact":
        for relative in targets:
            path = confined(root, relative)
            findings.append({"code": "ARTIFACT", "path": relative, "status": "PRESENT" if path.is_file() else "MISSING"})
        return {"status": "OBSERVED", "findings": findings}
    if len(targets) > (2 if action in {"check", "config", "prototype"} else 1):
        raise ValueError(f"Unexpected additional path for write-guard {action}")
    path = confined(root, targets[0])
    relative = path.relative_to(root).as_posix()
    proposal = confined(root, targets[1]) if len(targets) == 2 else path

    def add(code, **details):
        findings.append({"code": code, "path": relative, **details})

    protected = {"AGENTS.md", "project.yaml", "project.local.yaml", "production/sprint-status.yaml",
                 "production/session-state/active.md", "design/registry/entities.yaml"}
    protected.update(scaffold_paths(None, None).keys())
    protected.update({f"Assets/Tests/{part}/{part}Tests.asmdef" for part in ("EditMode", "PlayMode")})
    protected.update({"tests/unit/.gitkeep", "tests/integration/.gitkeep"})
    if action in {"check", "overwrite"} and tool == "Write" and path.exists() and (
            relative in protected or re.fullmatch(r"Source/[^/]+/Private/Tests/README\.md", relative)):
        add("OVERWRITE", detail="Existing project-owned artifact; use a targeted edit.")
    if action in {"check", "config"}:
        if relative in {"project.yaml", "project.local.yaml"}:
            if proposal.is_file():
                findings.extend(config_findings(root, relative, proposal, path if proposal != path else None))
            else:
                add("SKIPPED", rule="config", detail="No readable proposed configuration")
        elif relative == "production/review-mode.txt":
            add("REVIEW_MODE", detail="Legacy mirror; use project.yaml for an explicit setting.")
    if action in {"check", "prototype"} and path.suffix.lower() in SOURCE_EXTENSIONS | {".tscn", ".tres"}:
        resolved = config.resolve(root)
        source, _ = code_root(root, resolved)
        in_prototype = relative.startswith("prototypes/")
        in_code = bool(source and (source == "." or relative.startswith(source.rstrip("/") + "/")))
        if in_prototype or in_code:
            if not proposal.is_file():
                add("SKIPPED", rule="prototype", detail="No readable source or proposal")
            else:
                lines = proposal.read_text(encoding="utf-8-sig").splitlines()
                if in_prototype and not any(re.search(r"\b(PROTOTYPE|VERTICAL SLICE)\b", line) for line in lines[:10]):
                    add("PROTOTYPE_HEADER")
                target = source if in_prototype else "prototypes"
                if not target or target == ".":
                    add("SKIPPED", rule="prototype imports", detail="No distinct configured code root")
                else:
                    prefix = re.escape(target.rstrip("/"))
                    pattern = re.compile(r"(?<![\w/])(?:res://)?(?:\./)?" + prefix + r"(?:[/\\]|\.(?=\w))")
                    for line, text in enumerate(lines, 1):
                        if pattern.search(text):
                            add("PROTOTYPE_IMPORT", line=line, direction="into-production" if in_prototype else "into-prototypes")
    if action in {"check", "freeze"} and relative.startswith("assets/data/strings/"):
        freeze = confined(root, "production/localization/freeze-status.md")
        if freeze.is_file():
            for line in freeze.read_text(encoding="utf-8-sig").splitlines():
                if re.match(r"^\s*(?:[-*>]\s*)?Status:\s*ACTIVE\b", line.replace("*", ""), re.I):
                    add("FREEZE", source="production/localization/freeze-status.md")
                    break
    return {"path": relative, "status": "OBSERVED", "findings": findings,
            "note": "Explicit observations only; findings do not authorize or intercept a write."}


def scaffold_paths(engine, module):
    paths = {"tests/README.md": None, "production/qa/evidence/.gitkeep": b"",
             ".github/workflows/tests.yml": None, "tests/smoke/critical-paths.md": None}
    if engine == "godot":
        paths.update({"tests/unit/.gitkeep": b"", "tests/integration/.gitkeep": b""})
    if engine == "unity":
        for part in ("EditMode", "PlayMode"):
            name = part + "Tests"
            assembly = {"name": name, "references": [], "optionalUnityReferences": ["TestAssemblies"],
                        "includePlatforms": ["Editor"] if part == "EditMode" else []}
            paths[f"Assets/Tests/{part}/{name}.asmdef"] = (json.dumps(assembly, indent=2) + "\n").encode()
    if engine == "unreal" and module:
        paths[f"Source/{module}/Private/Tests/README.md"] = (
            "# Automation tests\n\nAdd project-owned automation tests to this module. "
            "Confirm the configured automation filter and run command before execution.\n").encode()
    return paths


def test_scaffold(root, engine, *, listing=False, dry_run=False, module=None, project=None, setup_date=None):
    engine = engine.casefold()
    if engine not in CODE_ROOTS:
        raise ValueError("Test scaffolds are provided for Godot, Unity, and Unreal")
    today = date.fromisoformat(setup_date) if setup_date else date.today()
    if module is None and engine == "unreal":
        markers = checks.files(root, "*.uproject")
        if len(markers) == 1:
            module = markers[0].stem
    if module is not None and not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", module):
        raise ValueError("Unreal module must be a single identifier")
    if project is not None and not re.fullmatch(r"[\w .-]+", project):
        raise ValueError("Project name must be plain text")
    paths = scaffold_paths(engine, module)
    version = None if listing else config.resolve(root, require_clean=not dry_run)["values"].get("engine.version")
    runner = {"godot": "GdUnit4", "unity": "Unity Test Framework", "unreal": "Unreal Automation"}[engine]
    needs = [{"id": "test_runner", "path": "tests/README.md", "detail": f"Verify {runner} and configure the reviewed test argv."},
             {"id": "ci_adapter", "path": ".github/workflows/tests.yml", "detail": "Author CI from the reviewed runner, actual engine version and platform requirements."}]
    if not version:
        needs.append({"id": "engine_version", "path": "project.yaml", "detail": "Record the verified engine version."})
    if engine == "unreal" and not module:
        needs.append({"id": "unreal_module", "path": "Source/", "detail": "Name the project test module with --module."})
    heading = f" — {project}" if project else ""
    paths["tests/README.md"] = (f"# Project tests{heading}\n\n"
                                f"Setup date: {today.isoformat()}\n\nRunner: {runner}.\n\n"
                                "Record the reviewed test command in project.yaml. The scaffold is not executed evidence.\n").encode()
    paths["tests/smoke/critical-paths.md"] = (
        b"# Smoke critical paths\n\n| Path | Steps | Expected result | Evidence |\n| --- | --- | --- | --- |\n")
    planned = [(relative, confined(root, relative), data) for relative, data in paths.items()]
    rows = []
    for relative, path, data in planned:
        row = {"path": relative}
        if listing:
            row["status"] = "LISTED"
        elif path.exists():
            row["status"] = "EXISTS"
        elif data is None:
            row.update(status="SKIPPED", reason="Requires a reviewed CI adapter")
        elif dry_run:
            row["status"] = "WOULD_CREATE"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            try:
                with confined(root, relative).open("xb") as output:
                    output.write(data)
            except FileExistsError:
                row["status"] = "EXISTS"
            else:
                row["status"] = "CREATED"
        rows.append(row)
    return {"engine": engine, "mode": "list" if listing else "dry-run" if dry_run else "write",
            "status": "OBSERVED", "files": rows, "needs": needs}


def skill_lint(root, name):
    if name != "all" and not re.fullmatch(r"(?:gs-)?[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Provide a native skill name or all")
    if name == "all":
        paths = checks.files(root, ".agents/skills/gs-*/SKILL.md")
    else:
        native = name if name.startswith("gs-") else "gs-" + name
        candidate = confined(root, f".agents/skills/{native}/SKILL.md")
        if not candidate.is_file():
            raise ValueError(f"No such native skill: {native}")
        paths = [candidate]
    results = []
    for path in paths:
        _, text, _ = text_parts(path.read_bytes())
        lines = text.splitlines(keepends=True)
        markers = [i for i, line in enumerate(lines) if line.strip() == "---"]
        metadata, findings = {}, []
        if len(markers) < 2 or markers[0] != 0:
            findings.append({"code": "FRONTMATTER_MISSING"})
        else:
            try:
                metadata = config.yaml.load("".join(lines[1:markers[1]]), Loader=config.Loader) or {}
                if not isinstance(metadata, dict):
                    raise ValueError("Expected a metadata mapping")
            except (ValueError, config.yaml.YAMLError) as error:
                metadata = {}
                findings.append({"code": "FRONTMATTER_INVALID", "detail": str(error)})
            lines = lines[markers[1] + 1:]
        if metadata.get("name") != path.parent.name:
            findings.append({"code": "NAME_MISMATCH", "value": metadata.get("name")})
        if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
            findings.append({"code": "DESCRIPTION_MISSING"})
        for field in sorted(metadata.keys() - {"name", "description", "license", "compatibility", "metadata"}):
            findings.append({"code": "HOST_METADATA", "key": field})
        references = checks.files(root, path.parent.relative_to(root).as_posix() + "/references/**/*.md")
        headings, titles = sections(lines), []
        for document in [lines] + [item.read_text(encoding="utf-8-sig").splitlines(keepends=True) for item in references]:
            for row in sections(document):
                if row["level"] == 2 and re.match(r"(?i)^(?:phase\s+\d+\b|\d+\.(?:\s|$))", row["title"]):
                    titles.append(row["title"])
            for line in visible_lines(document):
                if re.search(r"\$\{?CLAUDE_(?:PROJECT_DIR|SKILL_DIR)\}?", line):
                    findings.append({"code": "RETIRED_HOST_REFERENCE"})
        results.append({"name": path.parent.name, "path": path.relative_to(root).as_posix(),
                        "files": 1 + len(references), "phases": list(dict.fromkeys(titles)),
                        "last_section": next((row["title"] for row in reversed(headings) if row["level"] == 2), None),
                        "findings": findings})
    return {"status": "FORMAT" if results else checks.NO_DATA, "skills": results}
