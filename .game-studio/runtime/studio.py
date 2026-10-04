"""Installed command-line entry point. Run --help for supported interfaces."""
import argparse
import json
from pathlib import Path
import sys
import yaml
import checks
import config
import context
import hooks
from paths import atomic_write, confined, digest, plain


def parser():
    p = argparse.ArgumentParser(description='Codex Game Studios explicit project helpers')
    sub = p.add_subparsers(dest='command', required=True)
    for name in ['config', 'recover', 'artifacts', 'stories', 'dependencies', 'coherence',
                 'gdd-structure', 'review-scope', 'receipts', 'checkpoint', 'settings', 'run', 'hooks']:
        s = sub.add_parser(name)
        s.add_argument('--root', required=True, type=Path, help='Explicit consumer project root')
        s.add_argument('--output', help='Optional repository-relative JSON receipt path')
        if name == 'config':
            s.add_argument('system', nargs='?')
            s.add_argument('--keys', help='Optional comma-separated dotted setting names')
        elif name == 'artifacts':
            group = s.add_mutually_exclusive_group()
            group.add_argument('--phase')
            group.add_argument('--path')
        elif name == 'gdd-structure':
            s.add_argument('patterns', nargs='*', default=['design/gdd/*.md'])
        elif name == 'receipts':
            s.add_argument('action', choices=['hash', 'check', 'sections-hash', 'sections-check'])
            s.add_argument('patterns', nargs='+')
            s.add_argument('--receipt')
        elif name == 'review-scope':
            s.add_argument('--receipt')
        elif name == 'checkpoint':
            s.add_argument('--save', help='Read an explicitly authored repository-relative checkpoint and save it')
        elif name == 'settings':
            s.add_argument('assignment', nargs='?', help='dotted.key=YAML-value; omitted to inspect')
            s.add_argument('--local', action='store_true')
            s.add_argument('--dry-run', action='store_true')
        elif name == 'run':
            s.add_argument('name', help='Reviewed commands.<name> argv list in project.yaml')
            s.add_argument('--timeout', type=float, default=300)
        elif name == 'hooks':
            s.add_argument('--python', default=sys.executable, help='Interpreter with runtime dependencies')
    return p


def settings(root, assignment, local=False, dry_run=False):
    if not assignment:
        return config.resolve(root)
    key, sep, value_text = assignment.partition('=')
    if not sep or not key or any(not p for p in key.split('.')):
        raise ValueError('Expected dotted.key=YAML-value')
    if local and key not in config.LOCAL:
        raise ValueError(f'{key} is locked to project.yaml')
    value = yaml.load(value_text, Loader=config.Loader)
    if key == 'engine.name' and (not isinstance(value, str) or not value.strip()):
        raise ValueError('engine.name must be a nonempty project engine name')
    if key in config.ENUMS and not any(type(value) is type(v) and value == v for v in config.ENUMS[key]):
        raise ValueError(f'Invalid value for {key}: {value!r}')
    if key.startswith('workflow_overrides.system_overrides.') and value not in config.ENUMS['modes.workflow']:
        raise ValueError('Invalid system workflow tier')
    if key == 'modes.automation_always_ask' and (not isinstance(value, list) or not all(isinstance(v, str) for v in value)):
        raise ValueError('modes.automation_always_ask must be a list of strings')
    if key.startswith('commands.') and (not isinstance(value, list) or not value or not all(isinstance(v, str) and v for v in value)):
        raise ValueError('Commands must be nonempty argv lists')
    if key == 'testing.strict' and not isinstance(value, bool):
        raise ValueError('testing.strict scalar must be true or false')
    if local and not confined(root, 'project.yaml').exists():
        raise ValueError('Local settings require project.yaml')
    path = confined(root, 'project.local.yaml' if local else 'project.yaml')
    data = config.load(path)
    node = data
    parts = key.split('.')
    for part in parts[:-1]:
        node = node.setdefault(part, {})
        if not isinstance(node, dict):
            raise ValueError('Assignment would overwrite a scalar ancestor')
    node[parts[-1]] = value
    rendered = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    if not dry_run:
        atomic_write(path, rendered.encode())
    return {'path': path.name, 'assignment': key, 'value': value, 'dry_run': dry_run,
            'note': 'YAML serialized; original comments are not retained. Inspect diff.'}


def checkpoint(root, save=None):
    recovered = context.recover(root)
    current = recovered['checkpoint']
    if not save:
        return current
    if current['status'] == 'DISABLED':
        raise ValueError('Session state disabled')
    source = confined(root, save)
    data = source.read_bytes()
    if not data.strip():
        raise ValueError('An empty checkpoint is not saved state')
    destination = confined(root, current['path'])
    if destination.exists():
        prior = destination.read_bytes()
        backup = destination.with_name('previous-' + digest(prior)[:12] + '.md')
        atomic_write(backup, prior)
    atomic_write(destination, data)
    return {'status': 'SAVED', 'path': current['path'], 'bytes': len(data), 'hash': digest(data)}


def main(argv=None):
    args = parser().parse_args(argv)
    root = plain(args.root)
    if not root.is_dir():
        raise ValueError('Project root does not exist')
    name = args.command
    if name == 'config':
        result = config.resolve(root, args.system)
        if args.keys:
            aliases = {'automation': 'modes.automation', 'workflow': 'modes.workflow', 'review_mode': 'modes.review_mode',
                       'rigor': 'modes.rigor', 'story_granularity': 'modes.story_granularity', 'automation_always_ask': 'modes.automation_always_ask'}
            wanted = [aliases.get(k, k) for k in args.keys.split(',')]
            result['values'] = {k: v for k, v in result['values'].items() if any(k == w or k.startswith(w + '.') for w in wanted)}
            result['sources'] = {k: v for k, v in result['sources'].items() if k in result['values']}
    elif name == 'recover':
        result = context.recover(root)
    elif name == 'artifacts':
        result = checks.artifacts(root, args.phase, args.path)
    elif name == 'receipts':
        result = checks.receipts(root, args.action, args.patterns, args.receipt)
    elif name == 'review-scope':
        result = checks.review_scope(root, args.receipt)
    elif name == 'gdd-structure':
        result = checks.gdd_structure(root, args.patterns)
    elif name == 'checkpoint':
        result = checkpoint(root, args.save)
    elif name == 'settings':
        result = settings(root, args.assignment, args.local, args.dry_run)
    elif name == 'run':
        if args.timeout <= 0:
            raise ValueError('Timeout must be positive')
        result = checks.run_command(root, args.name, args.timeout)
    elif name == 'hooks':
        result = hooks.definition(root, args.python)
    else:
        result = getattr(checks, name)(root)
    text = json.dumps(result, ensure_ascii=False, indent=2, default=str) + '\n'
    if args.output:
        atomic_write(confined(root, args.output), text.encode())
    print(text, end='')
    if name == 'run' and result.get('exit_code') != 0:
        return 2 if result['status'] == checks.NO_DATA else result.get('exit_code') or 1
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError) as e:
        print(f'Game Studios: {e}', file=sys.stderr)
        raise SystemExit(2)
