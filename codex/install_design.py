"""Install a design snapshot into another project without overwriting files."""
import argparse
import json
import shutil
from pathlib import Path
from validate_design import relative_path, validate


def install(source, target, source_dirname='.ccgs-source', context_entry=None,
            project_context_file=None, dry_run=False):
    source = Path(source).resolve()
    target = Path(target).resolve()
    raw_target = (target / source_dirname).resolve()
    if raw_target == target or not raw_target.is_relative_to(target):
        raise ValueError('Source snapshot directory must stay inside the target project')
    if target == source:
        raise ValueError('Do not install into the framework checkout itself')
    validate(source)
    manifest = json.loads((source / 'codex/manifest.json').read_text(encoding='utf-8'))
    plan = []
    for name in manifest['skills']:
        base = Path('.agents/skills') / name
        plan.extend((path, target / path.relative_to(source)) for path in (source / base).rglob('*') if path.is_file())
    for name in manifest['roles']:
        path = source / '.codex/agents' / (name + '.toml')
        plan.append((path, target / path.relative_to(source)))
    for name in ('README.md', 'compatibility.md', 'manifest.json', 'validate_design.py', 'install_design.py'):
        plan.append((source / 'codex' / name, target / 'codex' / name))
    for entry in manifest['source_files']:
        plan.append((source / entry['path'], raw_target / entry['path']))
    context_target = target / 'codex/context.json'
    collisions = []
    for src, dst in plan:
        if not src.is_file():
            raise ValueError('Missing source: ' + str(src))
        if not dst.resolve().is_relative_to(target):
            raise ValueError('Destination escapes project: ' + str(dst))
        if dst.exists():
            collisions.append(str(dst.relative_to(target)))
    if context_target.exists():
        collisions.append('codex/context.json')
    for item in (context_entry, project_context_file):
        if item and not relative_path(target, item, 'project context').is_file():
            raise ValueError('Configured context must exist: ' + item)
    if collisions:
        raise FileExistsError('Existing files preserved; review upgrade separately: ' + ', '.join(collisions))
    if dry_run:
        return {'copy_count': len(plan), 'dry_run': True}
    for src, dst in plan:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    context = {'schema_version': 1, 'framework_source_root': raw_target.relative_to(target).as_posix()}
    if context_entry:
        context['context_entry'] = relative_path(target, context_entry, 'context_entry').relative_to(target).as_posix()
    if project_context_file:
        context['project_context_file'] = relative_path(target, project_context_file, 'project_context_file').relative_to(target).as_posix()
    context_target.write_text(json.dumps(context, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'copy_count': len(plan), 'skills': len(manifest['skills']), 'roles': len(manifest['roles'])}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, type=Path)
    parser.add_argument('--source-dirname', default='.ccgs-source')
    parser.add_argument('--context-entry')
    parser.add_argument('--project-context-file')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    print(json.dumps(install(Path(__file__).resolve().parents[1], args.target,
                            args.source_dirname, args.context_entry,
                            args.project_context_file, args.dry_run), ensure_ascii=False))
