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
import checkpoint_ops
import config_edit
import markdown_ops
import observations
from paths import atomic_write, confined, plain


def parser():
    p = argparse.ArgumentParser(description='Codex Game Studios explicit project helpers')
    sub = p.add_subparsers(dest='command', required=True)
    for name in ['config', 'recover', 'artifacts', 'stories', 'dependencies', 'coherence', 'engine-reference',
                 'gdd-structure', 'review-scope', 'receipts', 'checkpoint', 'settings', 'run', 'hooks',
                 'markdown', 'project-state', 'read-guard', 'write-guard', 'test-scaffold', 'skill-lint']:
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
            s.add_argument('--report', help='Link an actual existing report when generating its JSON companion')
            s.add_argument('--optional-pattern', action='append', help='Declare a reviewed pattern optional at snapshot generation; absent undeclared patterns remain required')
        elif name == 'review-scope':
            s.add_argument('--receipt')
        elif name == 'checkpoint':
            mode = s.add_mutually_exclusive_group()
            mode.add_argument('--save', help='Read an explicitly authored repository-relative checkpoint and save it')
            mode.add_argument('--append', help='Append a repository-relative authored narrative once')
        elif name == 'markdown':
            s.add_argument('action', choices=['list', 'status', 'extract', 'replace', 'insert-before', 'set-field'])
            s.add_argument('path')
            s.add_argument('targets', nargs='*')
            s.add_argument('--body', action='store_true', help='Extract without the heading')
            s.add_argument('--body-file', help='Read repository-relative replacement or insertion text; defaults to stdin')
            s.add_argument('--after', help='An existing header field to insert after')
        elif name == 'project-state':
            s.add_argument('--stage', action='store_true', help='Only return stage and phase facts')
        elif name == 'read-guard':
            s.add_argument('action', choices=['check', 'sections'])
            s.add_argument('path')
            s.add_argument('--bounded', choices=['yes', 'no'], default='no')
        elif name == 'write-guard':
            s.add_argument('action', choices=['check', 'overwrite', 'config', 'prototype', 'freeze', 'artifact'])
            s.add_argument('targets', nargs='+')
            s.add_argument('--tool', choices=['Write', 'Edit'], default='Write')
        elif name == 'test-scaffold':
            s.add_argument('engine')
            mode = s.add_mutually_exclusive_group()
            mode.add_argument('--list', action='store_true', dest='listing')
            mode.add_argument('--dry-run', action='store_true')
            s.add_argument('--module')
            s.add_argument('--project')
            s.add_argument('--date', dest='setup_date')
        elif name == 'skill-lint':
            s.add_argument('name')
        elif name == 'settings':
            s.add_argument('assignment', nargs='?', help='dotted.key=YAML-value; omitted to inspect')
            s.add_argument('--local', action='store_true')
            s.add_argument('--dry-run', action='store_true')
        elif name == 'run':
            s.add_argument('name', help='Reviewed commands.<name> argv list in project.yaml')
            s.add_argument('--timeout', type=float, default=300)
        elif name == 'hooks':
            s.add_argument('--python', default=sys.executable, help='Interpreter with runtime dependencies')
        elif name == 'coherence':
            s.add_argument('--probe', action='store_true', help='Explicitly execute reviewed commands.engine_probe argv')
    return p


def settings(root, assignment, local=False, dry_run=False):
    if not assignment:
        return config.resolve(root)
    key, sep, value_text = assignment.partition('=')
    if not sep or not key or not value_text.strip() or any(not p for p in key.split('.')):
        raise ValueError('Expected dotted.key=YAML-value')
    if local and key not in config.LOCAL:
        raise ValueError(f'{key} is locked to project.yaml')
    value = yaml.load(value_text, Loader=config.Loader)
    if isinstance(value, dict):
        raise ValueError('Set a YAML leaf, not a mapping')
    if key == 'features.read_guard_kb' and (type(value) is not int or value <= 0):
        raise ValueError('features.read_guard_kb must be a positive integer')
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
    resolved = config.resolve(root, require_clean=True)
    path = confined(root, 'project.local.yaml' if local else 'project.yaml')
    rendered, plan = config_edit.plan(path, key.split('.'), value)
    notes = []
    if key == 'modes.review_mode':
        notes.append('Explicit review mode shadows the rigor-derived review mode.')
    if not local and resolved['sources'].get(key) == 'project.local.yaml':
        notes.append('A whitelisted project.local.yaml value shadows the project assignment.')
    if not dry_run and plan['status'] != 'UNCHANGED':
        atomic_write(path, rendered)
        plan['status'] = 'UPDATED'
    return {'path': path.name, 'assignment': key, 'value': value, 'dry_run': dry_run,
            **plan, 'notes': notes}


def checkpoint(root, save=None, append=None):
    if save or append:
        config.resolve(root, require_clean=True)
    current = context.recover(root)['checkpoint']
    if not (save or append):
        return current
    if current['status'] == 'DISABLED':
        raise ValueError('Session state disabled')
    return checkpoint_ops.save(root, current['path'], save or append, append=bool(append))


def main(argv=None):
    # Codex tool transport consumes UTF-8, including on Windows legacy locales.
    for stream in [sys.stdout, sys.stderr]:
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
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
            wanted = [aliases.get(k.strip(), k.strip()) for k in args.keys.split(',')]
            requested = config.derived(result, wanted)
            if requested:
                result['derived'] = requested
            result['values'] = {k: v for k, v in result['values'].items() if any(k == w or k.startswith(w + '.') for w in wanted)}
            result['sources'] = {k: v for k, v in result['sources'].items() if k in result['values']}
    elif name == 'recover':
        result = context.recover(root)
    elif name == 'artifacts':
        result = checks.artifacts(root, args.phase, args.path)
    elif name == 'receipts':
        if args.report and not args.action.endswith('hash'):
            raise ValueError('--report is only valid for receipt generation')
        if args.optional_pattern is not None and not args.action.endswith('hash'):
            raise ValueError('--optional-pattern is only valid at snapshot generation; checks inherit its saved classification')
        result = checks.receipts(root, args.action, args.patterns, args.receipt, args.report, args.optional_pattern)
    elif name == 'review-scope':
        result = checks.review_scope(root, args.receipt)
    elif name == 'gdd-structure':
        result = checks.gdd_structure(root, args.patterns)
    elif name == 'checkpoint':
        result = checkpoint(root, args.save, args.append)
    elif name == 'markdown':
        if args.body and args.action != 'extract' or args.after and args.action != 'set-field':
            raise ValueError('--body applies to extract, --after applies to set-field')
        edits_body = args.action in {'replace', 'insert-before'}
        if args.body_file and not edits_body:
            raise ValueError('--body-file applies to replace or insert-before')
        if edits_body or args.action == 'set-field':
            config.resolve(root, require_clean=True)
        content = None
        if edits_body:
            content = confined(root, args.body_file).read_bytes() if args.body_file else sys.stdin.buffer.read()
        result = markdown_ops.command(root, args.action, args.path, args.targets, body=args.body,
                                      body_data=content, after=args.after)
    elif name == 'project-state':
        result = observations.project_state(root, args.stage)
    elif name == 'read-guard':
        result = observations.read_guard(root, args.action, args.path, args.bounded == 'yes')
    elif name == 'write-guard':
        result = observations.write_guard(root, args.action, args.targets, args.tool)
    elif name == 'test-scaffold':
        result = observations.test_scaffold(root, args.engine, listing=args.listing, dry_run=args.dry_run,
                                            module=args.module, project=args.project, setup_date=args.setup_date)
    elif name == 'skill-lint':
        result = observations.skill_lint(root, args.name)
    elif name == 'settings':
        result = settings(root, args.assignment, args.local, args.dry_run)
    elif name == 'run':
        if args.timeout <= 0:
            raise ValueError('Timeout must be positive')
        result = checks.run_command(root, args.name, args.timeout)
    elif name == 'hooks':
        result = hooks.definition(root, args.python)
    elif name == 'coherence':
        result = checks.coherence(root, args.probe)
    elif name == 'engine-reference':
        from engine import references
        result = references(root)
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
    except (ValueError, OSError, KeyError, yaml.YAMLError) as e:
        print(f'Game Studios: {e}', file=sys.stderr)
        raise SystemExit(2)
