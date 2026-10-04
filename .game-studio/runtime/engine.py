"""Project engine records and declared-vs-observed comparisons; no inferred engine."""
import json
from pathlib import Path
import re
from config import resolve
from paths import confined, plain


def version(text):
    match = re.search(r'(?<!\d)(\d+)\.(\d+)(?:\.(\d+))?', str(text or ''))
    if not match:
        return None
    major, minor, patch = match.groups()
    return ('6' if major == '6000' else major) + '.' + minor + ('.' + patch if patch is not None else '')


def row(text, label):
    match = re.search(r'(?im)^\|\s*\*{0,2}' + re.escape(label) + r'\*{0,2}\s*\|\s*([^|]+)\|', text)
    return match.group(1).strip() if match else None


def references(root):
    root = plain(root)
    values = resolve(root)['values']
    name = values.get('engine.name')
    family = name.lower() if isinstance(name, str) and re.fullmatch(r'[\w -]+', name) else None
    project_rel = values.get('engine.reference_root')
    if project_rel is None and family:
        project_rel = 'docs/engine-reference/' + family
    package_rel = '.game-studio/resources/engine-reference/' + family if family else None

    def documents(relative):
        if not relative:
            return {}
        folder = confined(root, relative)
        return {p.relative_to(folder).as_posix(): plain(p).relative_to(root).as_posix()
                for p in sorted(folder.rglob('*.md')) if p.is_file()} if folder.is_dir() else {}

    project_docs = documents(project_rel)
    if any(rel.startswith('.game-studio/') for rel in project_docs.values()) or project_rel and project_rel.startswith('.game-studio/'):
        raise ValueError('engine.reference_root must be project-owned; packaged resources are historical background')
    version_path = project_docs.get('VERSION.md')
    text = confined(root, version_path).read_text(encoding='utf-8-sig') if version_path else ''
    return {'configured_engine': name, 'configured_version': values.get('engine.version'),
            'project': {'root': project_rel, 'documents': project_docs, 'version_record': row(text, 'Engine Version'),
                        'installed_record': row(text, 'Installed at pin time'),
                        'status': 'PROJECT RECORDS — VERIFY EVIDENCE' if version_path else 'NOT ASSESSED — NO PROJECT VERSION RECORD'},
            'background': {'root': package_rel, 'documents': documents(package_rel),
                           'status': 'HISTORICAL EXAMPLES — NOT PROJECT AUTHORITY'},
            'rule': 'Read project documents first. Missing project version/API evidence stays unknown; packaged versions never fill it. Verify current official sources and actual toolchain before version-qualified claims.'}


def coherence(root, probe=False):
    from checks import files, run_command
    root = plain(root)
    settings = resolve(root)
    values = settings['values']
    refs = references(root)
    observations = []
    name, declared = values.get('engine.name'), values.get('engine.version')

    def observe(check, status, **facts):
        observations.append({'check': check, 'status': status, **facts})

    def compare(check, expected, actual, **facts):
        wanted, got = version(expected), version(actual)
        if not wanted or not got or len(got.split('.')) < len(wanted.split('.')):
            observe(check, 'NOT ASSESSED', declared=expected, observed=actual, reason='Missing or unparseable version evidence', **facts)
        else:
            observed_pin = '.'.join(got.split('.')[:len(wanted.split('.'))])
            observe(check, 'MATCH' if wanted == observed_pin else 'DIFFERS', declared=expected, observed=actual,
                    comparison='Configured numeric pin precision; Unity 6000.N = 6.N; build suffix not compared', **facts)

    compare('pinned-reference', declared, refs['project']['version_record'], source=refs['project']['documents'].get('VERSION.md'))
    installed = refs['project']['installed_record']
    if installed and version(installed) and not re.search(r'NOT DETERMINED|NOT ASSESSED', installed, re.I):
        compare('installed-at-pin', declared, installed, note='Recorded historical probe, not current binary execution')
    else:
        observe('installed-at-pin', 'NOT ASSESSED', recorded=installed, reason='No recorded installed-version probe')
    if probe:
        execution = run_command(root, 'engine_probe', 30)
        output = execution.get('stdout', '').splitlines()
        if execution.get('exit_code') == 0 and output:
            compare('installed-binary', declared, output[0], execution=execution)
        else:
            observe('installed-binary', 'NOT ASSESSED', execution=execution, reason='Explicit commands.engine_probe did not supply version evidence')
    else:
        observe('installed-binary', 'NOT ASSESSED', reason='No binary executed. Review commands.engine_probe argv and explicitly opt in with coherence --probe.')

    project_root_rel = values.get('engine.project_root', '.')
    project_root = confined(root, project_root_rel)
    marker_files = {'Godot': 'project.godot', 'Unity': 'ProjectSettings/ProjectVersion.txt'}
    marker, text, project_version = None, '', None
    if name in marker_files:
        marker = confined(project_root, marker_files[name])
        if marker.is_file():
            text = marker.read_text(encoding='utf-8-sig')
            expression = r'config/features\s*=\s*PackedStringArray\(\s*"([^"]+)"' if name == 'Godot' else r'm_EditorVersion:\s*([^\s]+)'
            match = re.search(expression, text)
            project_version = match.group(1) if match else None
    elif name == 'Unreal':
        markers = files(project_root, '*.uproject')
        if len(markers) == 1:
            marker = markers[0]
            project_version = json.loads(marker.read_text(encoding='utf-8-sig')).get('EngineAssociation')
        elif len(markers) > 1:
            observe('project-marker', 'NOT ASSESSED', reason='Multiple Unreal project markers; configure a specific engine.project_root')
    compare('project-version', declared, project_version, source=marker.relative_to(root).as_posix() if marker else None)

    if name == 'Godot':
        rendering = re.search(r'(?m)^renderer/rendering_method\s*=\s*"([^"]+)"', text)
        actual_rendering = rendering.group(1) if rendering else None
        desired = {'Compatibility': 'gl_compatibility', 'compatibility': 'gl_compatibility', 'GL Compatibility': 'gl_compatibility',
                   'Forward+': 'forward_plus', 'Forward Plus': 'forward_plus', 'forward_plus': 'forward_plus', 'Mobile': 'mobile', 'mobile': 'mobile'}.get(values.get('engine.rendering'))
        observe('rendering', ('MATCH' if desired == actual_rendering else 'DIFFERS') if desired and actual_rendering else 'NOT ASSESSED',
                declared=values.get('engine.rendering'), observed=actual_rendering, reason=None if desired and actual_rendering else 'No declared/explicit project rendering method; defaults not guessed')
        physics = values.get('engine.physics')
        code_rel = values.get('code_root', 'src')
        code_root = confined(root, code_rel)
        found_2d = [p.relative_to(root).as_posix() for pattern in ['**/*.gd', '**/*.tscn'] for p in files(code_root, pattern)
                    if re.search(r'\b(Node2D|CharacterBody2D|RigidBody2D|Area2D|StaticBody2D)\b', p.read_text(encoding='utf-8-sig'))] if code_root.is_dir() else []
        status = 'DIFFERS' if physics and 'jolt' in str(physics).lower() and found_2d else 'OBSERVED' if physics and code_root.is_dir() else 'NOT ASSESSED'
        observe('physics', status, declared=physics, found_2d=found_2d,
                note='Jolt is a 3D backend; found 2D usage needs reconciliation. Absence of 2D matches is not a physics correctness verdict.')
    else:
        observe('rendering', 'NOT ASSESSED', reason='No built-in project rendering comparison for this engine')
        observe('physics', 'NOT ASSESSED', reason='No built-in project physics comparison for this engine')

    for command_name in ['test', 'build', 'smoke']:
        argv = values.get('commands.' + command_name)
        if not isinstance(argv, list) or not argv or not all(isinstance(a, str) and a for a in argv):
            observe(command_name + '-command', 'NOT ASSESSED', reason='No valid reviewed argv command')
            continue
        observe(command_name + '-command', 'OBSERVED', argv=argv, note='Recorded only; not executed')
        runners = []
        for argument in argv[1:]:
            candidate = argument.removeprefix('res://').replace('\\', '/')
            if re.search(r'\.(gd|cs|py|sh)$', candidate) and not Path(candidate).is_absolute() and ':' not in candidate:
                runners.append(candidate)
                path = confined(project_root, candidate)
                observe(command_name + '-entry:' + candidate, 'MATCH' if path.is_file() else 'DIFFERS', path=path.relative_to(root).as_posix())
        if not runners:
            observe(command_name + '-entry', 'NOT ASSESSED', reason='No explicit project script argument; module/method adapters need their own validator')
        if command_name == 'build':
            exports = [i for i, arg in enumerate(argv) if arg in {'--export-debug', '--export-release', '--export-pack'}]
            if exports:
                cfg = confined(project_root, 'export_presets.cfg')
                names = re.findall(r'(?m)^name\s*=\s*"([^"]+)"', cfg.read_text(encoding='utf-8-sig')) if cfg.is_file() else []
                requested = [argv[i + 1] for i in exports if i + 1 < len(argv)]
                observe('export-presets', 'MATCH' if len(requested) == len(exports) and all(p in names for p in requested) else 'DIFFERS',
                        requested=requested, available=names, file_present=cfg.is_file())
            else:
                observe('export-presets', 'NOT ASSESSED', reason='No Godot export flag in build argv; project adapter must validate its own targets')
    return {'status': 'OBSERVED', 'settings': settings, 'engine_reference': refs, 'observations': observations,
            'counts': {state: sum(r['status'] == state for r in observations) for state in ['MATCH', 'DIFFERS', 'NOT ASSESSED', 'OBSERVED']},
            'note': 'Named comparisons only. DIFFERS must be reconciled; unassessed checks never imply consistency. No engine build, test or certification verdict.'}
