"""Explicit-root YAML settings, per-leaf provenance and upstream rigor semantics."""
import copy
import re
import yaml
from paths import confined, plain

LOCAL = {'modes.review_mode', 'modes.automation', 'modes.automation_always_ask',
         'team.size', 'performance.enforce', 'features.session_state',
         'features.token_budget_warn_at', *('testing.strict.' + k for k in
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
            'modes.automation_always_ask': ['scope_changes', 'file_deletions', 'schema_changes']}
OPTIONAL = {'engine.name'}


class Loader(yaml.SafeLoader):
    yaml_implicit_resolvers = copy.deepcopy(yaml.SafeLoader.yaml_implicit_resolvers)


# YAML 1.2 boolean spellings; on/off must remain strings for the upstream enum.
for first, resolvers in Loader.yaml_implicit_resolvers.items():
    Loader.yaml_implicit_resolvers[first] = [(tag, regex) for tag, regex in resolvers
                                           if tag != 'tag:yaml.org,2002:bool']
Loader.add_implicit_resolver('tag:yaml.org,2002:bool', re.compile(r'^(?:true|false|True|False|TRUE|FALSE)$'), list('tTfF'))


def mapping(loader, node):
    result = {}
    for k, v in node.value:
        key = loader.construct_object(k)
        if not isinstance(key, str) or key in result:
            raise ValueError(f'Duplicate or non-string YAML key: {key!r}')
        result[key] = loader.construct_object(v)
    return result


Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def load(path):
    if not path.exists():
        return {}
    try:
        data = yaml.load(path.read_text(encoding='utf-8-sig'), Loader=Loader)
    except (yaml.YAMLError, RecursionError) as e:
        raise ValueError(f'Invalid YAML in {path.name}: {e}') from e
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f'{path.name} must contain a mapping')
    return data


def flatten(data, prefix='', ancestors=()):
    if id(data) in ancestors:
        raise ValueError('Recursive YAML aliases are unsupported')
    out = {}
    for key, value in data.items():
        name = f'{prefix}.{key}' if prefix else key
        if isinstance(value, dict):
            out.update(flatten(value, name, (*ancestors, id(data))))
        else:
            out[name] = value
    return out


def resolve(root, system=None):
    root = plain(root)
    base_path, local_path = confined(root, 'project.yaml'), confined(root, 'project.local.yaml')
    if local_path.exists() and not base_path.exists():
        raise ValueError('project.local.yaml requires project.yaml')
    base, local = flatten(load(base_path)), flatten(load(local_path))
    values, sources, notes = {}, {}, []
    for key in local:
        if key not in LOCAL and key != 'schema_version' and not key.startswith('framework.'):
            notes.append(f'Local override ignored: {key}; move it to project.yaml')
    keys = set(base) | (set(local) & LOCAL) | set(ENUMS) | set(DEFAULTS) | OPTIONAL
    for key in sorted(keys):
        for data, source in ((local if key in LOCAL else {}, 'project.local.yaml'), (base, 'project.yaml')):
            if key not in data or data[key] is None:
                continue
            value = data[key]
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
    return {'root': str(root), 'values': values, 'sources': sources, 'notes': notes}
