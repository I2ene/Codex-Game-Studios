"""Validate native design adapters and preserved sources; Python 3.11+."""
import argparse
import hashlib
import json
import re
import tomllib
from pathlib import Path, PureWindowsPath


def relative_path(root, value, label):
    path = Path(value.replace('\\', '/'))
    if path.is_absolute() or path.drive or PureWindowsPath(value).drive or '..' in path.parts:
        raise ValueError(label + ' must be repository-relative')
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(label + ' must stay inside its repository')
    return resolved


def source_digest(path, normalization):
    data = path.read_bytes()
    if normalization == 'lf-text':
        data.decode('utf-8')
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


def validate(root):
    root = Path(root).resolve()
    manifest = json.loads((root / 'codex/manifest.json').read_text(encoding='utf-8'))
    context_path = root / 'codex/context.json'
    context = json.loads(context_path.read_text(encoding='utf-8')) if context_path.exists() else {}
    source_root = relative_path(root, context.get('framework_source_root', '.'), 'framework_source_root')
    errors = []
    for entry in manifest['source_files']:
        path = relative_path(source_root, entry['path'], 'preserved source path')
        if not path.is_file():
            errors.append('Missing preserved source: ' + entry['path'])
        elif source_digest(path, manifest.get('hash_normalization', 'bytes')) != entry['sha256']:
            errors.append('Changed preserved source: ' + entry['path'])
    for name in manifest['skills']:
        path = root / '.agents/skills' / name / 'SKILL.md'
        if not path.is_file():
            errors.append('Missing native skill: ' + name)
            continue
        text = path.read_text(encoding='utf-8')
        front = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        if not front:
            errors.append('Invalid native frontmatter: ' + name)
            continue
        fields = dict(re.findall(r'^([a-z-]+):\s*(.+)$', front.group(1), re.M))
        if fields.get('name') != name or not fields.get('description'):
            errors.append('Invalid native discovery fields: ' + name)
        if set(fields) - {'name', 'description', 'license', 'metadata'}:
            errors.append('Provider-specific native fields: ' + name)
        for target in re.findall(r'\]\(([^)]+)\)', text[front.end():]):
            if not target.startswith(('https://', 'http://', '#')) and not (path.parent / target).is_file():
                errors.append('Broken native reference: ' + name + ' -> ' + target)
    for name in manifest['roles']:
        path = root / '.codex/agents' / (name + '.toml')
        if not path.is_file():
            errors.append('Missing native role: ' + name)
            continue
        try:
            data = tomllib.loads(path.read_text(encoding='utf-8'))
            if data.get('name') != name or not data.get('description') or not data.get('developer_instructions'):
                errors.append('Invalid native role fields: ' + name)
            if 'model' in data or 'model_reasoning_effort' in data:
                errors.append('Unexpected pinned model: ' + name)
        except tomllib.TOMLDecodeError as exc:
            errors.append('Invalid native role TOML: ' + name + ': ' + str(exc))
    for key in ('context_entry', 'project_context_file'):
        if context.get(key) and not relative_path(root, context[key], key).is_file():
            errors.append('Missing project context: ' + key)
    if errors:
        raise ValueError('\n'.join(errors))
    return {'skills': len(manifest['skills']), 'roles': len(manifest['roles']),
            'preserved_sources': len(manifest['source_files'])}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(validate(args.root), ensure_ascii=False))
