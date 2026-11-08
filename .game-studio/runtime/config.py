"""Explicit-root YAML settings, per-leaf provenance and upstream rigor semantics."""
import copy
import re
import yaml
from paths import confined, plain

LOCAL = {'modes.review_mode', 'modes.automation', 'modes.automation_always_ask',
         'team.size', 'performance.enforce', 'features.session_state',
         'features.token_budget_warn_at', 'features.read_guard', 'features.read_guard_kb',
         *('testing.strict.' + k for k in
         ('logic', 'integration', 'visual', 'ui', 'config'))}
ENUMS = {
    'modes.rigor': ['minimal', 'standard', 'full'],
    'modes.workflow': ['minimal', 'standard', 'full'],
    'modes.review_mode': ['solo', 'lean', 'full'],
    'modes.automation': ['collaborative', 'guided', 'autonomous'],
    'modes.story_granularity': ['coarse', 'balanced', 'fine'],
    'docs.density': ['terse', 'balanced', 'thorough'],
    'qa.level': ['minimal', 'standard', 'full'],
    'team.size': ['individual', 'small', 'studio'],
    'performance.enforce': ['warn', 'block', 'off'],
    'platform.cert_tier': ['none', 'itch', 'steam', 'console'],
    'accessibility.target': ['none', 'standard', 'aaa'],
    'project.stage': ['Concept', 'Systems Design', 'Technical Setup', 'Pre-Production', 'Production', 'Polish', 'Release'],
    'features.session_state': ['on', 'off'],
    'features.read_guard': ['on', 'off', True, False],
}
for key in ['platform.online', 'workflow_overrides.edge_cases', 'workflow_overrides.tuning_knobs',
            'workflow_overrides.art_bible_strict', *('testing.strict.' + k for k in
            ('logic', 'integration', 'visual', 'ui', 'config'))]:
    ENUMS[key] = [True, False]
RIGOR_KEYS = ['modes.workflow', 'docs.density', 'qa.level', 'modes.story_granularity', 'modes.review_mode', 'team.size']
RIGOR = dict(zip(['minimal', 'standard', 'full'], [
    ['minimal', 'terse', 'minimal', 'coarse', 'solo', 'individual'],
    ['standard', 'balanced', 'standard', 'balanced', 'lean', 'individual'],
    ['full', 'thorough', 'full', 'fine', 'full', 'studio']]))
DEFAULTS = {'modes.rigor': 'minimal', 'modes.automation': 'collaborative',
            'performance.enforce': 'warn', 'features.session_state': 'on',
            'features.read_guard': 'on', 'features.read_guard_kb': 40,
            'modes.automation_always_ask': ['scope_changes', 'file_deletions', 'schema_changes']}
OPTIONAL = {'engine.name'}


class Loader(yaml.SafeLoader):
    yaml_implicit_resolvers = copy.deepcopy(yaml.SafeLoader.yaml_implicit_resolvers)


# YAML 1.2 boolean spellings; on/off must remain strings for the upstream enum.
for first, resolvers in Loader.yaml_implicit_resolvers.items():
    Loader.yaml_implicit_resolvers[first] = [(tag, regex) for tag, regex in resolvers
                                           if tag != 'tag:yaml.org,2002:bool']
Loader.add_implicit_resolver('tag:yaml.org,2002:bool', re.compile(r'^(?:true|false|True|False|TRUE|FALSE)$'), list('tTfF'))


def merge_settings(first, second):
    """Repeated mapping keys retain earlier siblings; later leaves win."""
    return {**first, **{k: merge_settings(first[k], v)
                       if isinstance(v, dict) and isinstance(first.get(k), dict) else v
                       for k, v in second.items()}}


def mapping(loader, node):
    result, marks = {}, {}
    prefix = getattr(loader, "setting_path", ())
    diagnostics = getattr(loader, "duplicate_notes", None)
    for k, v in node.value:
        key = loader.construct_object(k)
        if not isinstance(key, str):
            raise ValueError(f"Non-string YAML key at line {k.start_mark.line + 1}: {key!r}")
        dotted = ".".join((*prefix, key))
        line = k.start_mark.line + 1
        if key in result:
            message = f"Duplicate YAML key {dotted}: lines {marks[key]} and {line}"
            if diagnostics is None:
                raise ValueError(message + "; repair it before editing or executing commands")
            diagnostics.append(message + "; mapping blocks merged, later values win")
        loader.setting_path = (*prefix, key)
        try:
            value = loader.construct_object(v)
        finally:
            loader.setting_path = prefix
        if isinstance(result.get(key), dict) and isinstance(value, dict):
            value = merge_settings(result[key], value)
        result[key], marks[key] = value, line
    return result


Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def load(path, duplicate_notes=None):
    if not path.exists():
        return {}
    loader = Loader(path.read_text(encoding="utf-8-sig"))
    loader.duplicate_notes = duplicate_notes
    try:
        data = loader.get_single_data()
    except (yaml.YAMLError, RecursionError) as e:
        raise ValueError(f"Invalid YAML in {path.name}: {e}") from e
    finally:
        loader.dispose()
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain a mapping")
    return data


def flatten(data, prefix='', ancestors=()):
    if id(data) in ancestors:
        raise ValueError('Recursive YAML aliases are unsupported')
    out = {}
    for key, value in data.items():
        name = f'{prefix}.{key}' if prefix else key
        entries = (flatten(value, name, (*ancestors, id(data))) if isinstance(value, dict) else {name: value})
        overlap = out.keys() & entries.keys()
        if overlap:
            raise ValueError("Ambiguous setting paths: " + ", ".join(sorted(overlap)))
        out.update(entries)
    return out


def resolve(root, system=None, *, require_clean=False):
    root = plain(root)
    base_path, local_path = confined(root, 'project.yaml'), confined(root, 'project.local.yaml')
    if local_path.exists() and not base_path.exists():
        raise ValueError('project.local.yaml requires project.yaml')
    values, sources, notes = {}, {}, []
    settings_data = []
    for path in (base_path, local_path):
        duplicate_notes = []
        settings_data.append(flatten(load(path, None if require_clean else duplicate_notes)))
        notes.extend(f"{path.name}: {note}" for note in duplicate_notes)
    base, local = settings_data
    duplicate_keys = bool(notes)
    for key in local:
        if key not in LOCAL and key != 'schema_version' and not key.startswith('framework.'):
            notes.append(f'Local override ignored: {key}; move it to project.yaml')
    keys = set(base) | (set(local) & LOCAL) | set(ENUMS) | set(DEFAULTS) | OPTIONAL
    for key in sorted(keys):
        for data, source in ((local if key in LOCAL else {}, 'project.local.yaml'), (base, 'project.yaml')):
            if key not in data or data[key] is None:
                continue
            value = data[key]
            if key == 'features.read_guard_kb' and (type(value) is not int or value <= 0):
                notes.append(f'Invalid {key} in {source}; expected a positive integer')
                continue
            if key == 'engine.name' and (not isinstance(value, str) or not value.strip()):
                notes.append(f'Invalid engine.name in {source}; expected a nonempty project engine name')
                continue
            if key in ENUMS and not any(type(value) is type(v) and value == v for v in ENUMS[key]):
                notes.append(f'Invalid {key} in {source}: {value!r}; fallback applied')
                continue
            if key == 'modes.automation_always_ask' and (not isinstance(value, list) or not all(isinstance(v, str) for v in value)):
                raise ValueError(f'{key} must be a list of strings')
            values[key], sources[key] = value, source
            break
    for key, rel in [('modes.review_mode', 'production/review-mode.txt'), ('project.stage', 'production/stage.txt')]:
        p = confined(root, rel)
        if p.exists():
            legacy = p.read_text(encoding='utf-8-sig').strip()
            if key not in values and legacy in ENUMS[key]:
                values[key], sources[key] = legacy, rel
            elif key in values and legacy != values[key]:
                notes.append(f'Stale legacy mirror {rel}; project setting wins')
    rigor = values.get('modes.rigor', 'minimal')
    for key, value in zip(RIGOR_KEYS, RIGOR[rigor]):
        if key not in values:
            values[key], sources[key] = value, f'rigor:{rigor}'
    for key, value in DEFAULTS.items():
        if key not in values:
            values[key], sources[key] = value, 'default'
    for key in set(ENUMS) | OPTIONAL:
        values.setdefault(key, None)
        sources.setdefault(key, 'unset')
    legacy_strict = base.get('testing.strict')
    if legacy_strict is not None:
        if not isinstance(legacy_strict, bool):
            raise ValueError('Legacy testing.strict scalar must be true or false')
        for kind in ['logic', 'integration', 'visual', 'ui', 'config']:
            key = 'testing.strict.' + kind
            if values[key] is None:
                values[key], sources[key] = legacy_strict, 'project.yaml:testing.strict'
    for key, value in list(values.items()):
        if key.startswith('workflow_overrides.system_overrides.') and value not in ENUMS['modes.workflow']:
            raise ValueError(f'Invalid per-system workflow tier: {key}')
    if system:
        key = 'workflow_overrides.system_overrides.' + system
        if key in values:
            values['modes.workflow'], sources['modes.workflow'] = values[key], key
    # Stricter-only GDD section flags default from the effective tier.
    for key in ['edge_cases', 'tuning_knobs', 'art_bible_strict']:
        name = 'workflow_overrides.' + key
        if values.get('modes.workflow') == 'full' and values.get(name) is False:
            notes.append(f'{name}=false cannot relax full workflow requirements')
            values[name], sources[name] = True, 'workflow:full'
    return {'root': str(root), 'values': values, 'sources': sources, 'notes': notes, 'duplicate_keys': duplicate_keys}


DERIVED_KEYS = {"gate_level", "engine_values", "specialists", "review_gate", "input_methods", "perf_budgets"}


def derived(resolved, wanted=None):
    """Named bootstrap facts without granting a gate or inferring a missing setting."""
    wanted = DERIVED_KEYS if wanted is None else DERIVED_KEYS.intersection(wanted)
    values, sources = resolved["values"], resolved["sources"]
    result = {}

    def field(key):
        return {"value": values.get(key), "source": sources.get(key, "unset")}

    if "gate_level" in wanted:
        levels = {}
        for kind in ("logic", "integration", "visual", "ui", "config"):
            key = "testing.strict." + kind
            explicit = values.get(key)
            levels[kind] = {"value": ("blocking" if explicit else "advisory") if explicit is not None
                            else ("advisory" if kind == "config" else "blocking"),
                            "source": sources[key] if explicit is not None else "default"}
            if kind == "config":
                levels[kind]["smoke_check"] = "advisory" if explicit is False else "blocking"
        result["gate_level"] = levels
    if "engine_values" in wanted:
        result["engine_values"] = {key: field("engine." + key) for key in ("name", "version", "language")}
    if "specialists" in wanted:
        family = str(values.get("engine.name") or "").casefold()
        primary = {"godot": "gs-godot-specialist", "unity": "gs-unity-specialist",
                   "unreal": "gs-unreal-specialist"}.get(family)
        roles = {"primary": {"value": primary, "source": "engine.name" if primary else "unset"}}

        def native_role(value):
            return (value if value.startswith("gs-") else "gs-" + value) if isinstance(value, str) and value else None

        for kind in ("code", "shader", "ui", "additional"):
            role = field("specialists." + kind)
            if kind == "additional":
                role["value"] = [name for item in role["value"] if (name := native_role(item))] if isinstance(role["value"], list) else []
            else:
                role["value"] = native_role(role["value"])
            roles[kind] = role
        result["specialists"] = roles
    if "review_gate" in wanted:
        mode = values["modes.review_mode"]
        result["review_gate"] = {"skill_gates": "run" if mode == "full" else "skip",
                                 "phase_gates": "run" if mode in {"lean", "full"} else "skip",
                                 "mode": mode, "source": sources["modes.review_mode"]}
    if "input_methods" in wanted:
        methods = []
        targets = values.get("platform.targets")
        if isinstance(targets, list) and any(isinstance(item, str) and item.casefold() in {"pc", "web"} for item in targets):
            methods.append("keyboard/mouse")
        for method in ("gamepad", "touch"):
            if str(values.get(f"platform.{method}_support", "")).casefold() in {"full", "partial"}:
                methods.append(method)
        primary = values.get("platform.primary_input")
        if isinstance(primary, str) and primary.strip():
            normalized = primary.casefold().strip()
            compact = re.sub(r"[^a-z]", "", normalized)
            if compact in {"keyboard", "mouse", "keyboardmouse", "mousekeyboard", "keyboardandmouse", "mouseandkeyboard", "kbm"}:
                normalized = "keyboard/mouse"
            elif compact in {"gamepad", "controller", "gamecontroller", "joypad"}:
                normalized = "gamepad"
            elif compact in {"touch", "touchscreen"}:
                normalized = "touch"
            if normalized not in methods:
                methods.append(normalized)
        result["input_methods"] = {"value": methods, "primary": primary,
                                   "source": "project.yaml:platform" if any(k.startswith("platform.") and sources[k] != "unset" for k in values) else "unset"}
    if "perf_budgets" in wanted:
        result["perf_budgets"] = {key: field("performance." + key) for key in
                                  ("target_framerate", "frame_budget_ms", "draw_call_limit", "memory_ceiling_mb")}
    return result
