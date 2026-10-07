"""Hash-owned project installation. Preflight, rollback, no unmanaged pruning."""
import json
from pathlib import Path
import re
from paths import atomic_write, confined, digest, plain

BEGIN, END = '<!-- BEGIN CODEX GAME STUDIOS -->', '<!-- END CODEX GAME STUDIOS -->'
STATE = '.game-studio/install-state.json'


def managed(relative):
    return (relative.startswith('.agents/skills/gs-') or relative.startswith('.codex/agents/gs-')
            or relative.startswith('.game-studio/')) and relative not in {
                STATE, '.game-studio/context.json', '.game-studio/hooks.json', '.game-studio/install.lock'}


def payload(source, verify=True):
    source = plain(source)
    result = {}
    for directory in ['.agents/skills', '.codex/agents', '.game-studio']:
        start = confined(source, directory)
        if not start.is_dir():
            raise ValueError(f'Incomplete release: {directory}')
        for p in sorted(start.rglob('*')):
            plain(p)
            rel = p.relative_to(source).as_posix()
            if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc' and managed(rel):
                result[rel] = p.read_bytes()
    if verify:
        release = json.loads(result.get('.game-studio/release.json', b'{}'))
        actual = {p: digest(b) for p, b in result.items() if p != '.game-studio/release.json'}
        if release.get('schema') != 1 or release.get('files') != actual:
            raise ValueError('Release manifest missing or payload changed; verify the release before installation')
    return result


def build_manifest(source):
    source = plain(source)
    contents = payload(source, verify=False)
    release = {'schema': 1, 'version': contents['.game-studio/VERSION'].decode().strip(),
               'files': {p: digest(b) for p, b in contents.items() if p != '.game-studio/release.json'}}
    atomic_write(confined(source, '.game-studio/release.json'), (json.dumps(release, indent=2, sort_keys=True) + '\n').encode())
    return release


def install(source, target, dry_run=False):
    source, target = plain(source), plain(target)
    if source == target or source.is_relative_to(target) or target.is_relative_to(source):
        raise ValueError('Source and target must not overlap')
    if target.exists() and not target.is_dir():
        raise ValueError('Target must be a directory')
    if dry_run:
        return _install(source, target, True)
    # Serialize before reading target ownership/conflicts; do not apply stale plans.
    lock = confined(target, '.game-studio/install.lock')
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = lock.open('x')
    except FileExistsError as e:
        raise ValueError('Install lock exists; inspect interrupted/concurrent installation before retry') from e
    try:
        handle.write('Installation in progress. Do not run two installers.\n')
        handle.close()
        return _install(source, target, False)
    finally:
        handle.close()
        lock.unlink()


def _install(source, target, dry_run):
    desired = payload(source)
    state_path = confined(target, STATE)
    previous = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else None
    if previous is not None and (not isinstance(previous, dict) or previous.get('schema') != 1
                                 or not isinstance(previous.get('files'), dict)):
        raise ValueError('Invalid install-state ledger; do not overwrite it')
    old = previous['files'] if previous else {}
    for rel, sha in old.items():
        confined(target, rel)
        if not managed(rel) or not isinstance(sha, str) or not re.fullmatch(r'[0-9a-f]{64}', sha):
            raise ValueError(f'Invalid ledger entry: {rel}')
    conflicts = []
    for rel in set(desired) | set(old):
        p = confined(target, rel)
        if p.exists():
            if not p.is_file():
                conflicts.append(rel + ' (not a file)')
                continue
            current = digest(p.read_bytes())
            if rel in old and current != old[rel]:
                conflicts.append(rel + ' (edited managed file)')
            elif rel not in old and (rel not in desired or p.read_bytes() != desired[rel]):
                conflicts.append(rel + ' (unowned collision)')
    agents = confined(target, 'AGENTS.md')
    text = agents.read_text(encoding='utf-8') if agents.exists() else ''
    if text.count(BEGIN) != text.count(END) or text.count(BEGIN) > 1:
        raise ValueError('Malformed managed AGENTS.md block')
    if BEGIN in text:
        start, stop = text.index(BEGIN), text.index(END) + len(END)
        if stop < start:
            raise ValueError('Malformed managed AGENTS.md block order')
        current_block = text[start:stop]
        if not previous or digest(current_block.encode()) != previous.get('instruction_hash'):
            conflicts.append('AGENTS.md (edited or unowned framework block)')
    fragment = desired['.game-studio/AGENTS.fragment.md'].decode('utf-8').strip()
    block = BEGIN + '\n' + fragment + '\n' + END
    updated = text[:start] + block + text[stop:] if BEGIN in text else text + ('\n' if text and not text.endswith('\n') else '') + '\n' + block + '\n'
    if conflicts:
        raise ValueError('Installation conflicts; preserve and reconcile:\n' + '\n'.join(sorted(conflicts)))
    stale = sorted(set(old) - set(desired))
    writes = dict(desired)
    writes['AGENTS.md'] = updated.encode()
    project = confined(target, 'project.yaml')
    if not project.exists():
        version = desired['.game-studio/VERSION'].decode().strip()
        writes['project.yaml'] = f'schema_version: 1\nframework:\n  version: {version}\n'.encode()
    state = {'schema': 1, 'version': desired['.game-studio/VERSION'].decode().strip(),
             'files': {p: digest(b) for p, b in desired.items()}, 'instruction_hash': digest(block.encode())}
    writes[STATE] = (json.dumps(state, indent=2, sort_keys=True) + '\n').encode()
    changed = [p for p, b in writes.items() if not confined(target, p).exists() or confined(target, p).read_bytes() != b]
    report = {'version': state['version'], 'write': sorted(changed), 'remove_owned': stale,
              'dry_run': dry_run, 'instruction_override': confined(target, 'AGENTS.override.md').exists()}
    if dry_run:
        return report
    snapshots = {p: confined(target, p).read_bytes() if confined(target, p).is_file() else None
                 for p in set(changed) | set(stale)}
    try:
        for p in stale:
            path = confined(target, p)
            if path.exists():
                path.unlink()
        # Ownership state is committed last.
        for p in sorted(changed, key=lambda p: p == STATE):
            atomic_write(confined(target, p), writes[p])
    except Exception:
        for p, data in snapshots.items():
            path = confined(target, p)
            if data is None:
                if path.exists():
                    path.unlink()
            else:
                atomic_write(path, data)
        raise
    return report
