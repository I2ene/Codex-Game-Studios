"""Opt-in native command hooks. No approval decisions or transcript parsing."""
import base64
import json
from pathlib import Path
import shlex
import sys
from context import recover
from paths import confined, plain

EVENTS = {'SessionStart', 'PreCompact', 'PostCompact', 'Stop', 'SubagentStart', 'SubagentStop'}


def project_root(cwd):
    current = plain(cwd)
    for p in [current, *current.parents]:
        if (p / '.game-studio').is_dir():
            return plain(p)
        if (p / '.git').exists():
            break
    raise ValueError('No installed framework in this session project')


def handle(event):
    if not isinstance(event, dict) or not isinstance(event.get('hook_event_name'), str):
        raise ValueError('Expected one hook event JSON object')
    name = event['hook_event_name']
    if name == 'PreToolUse':
        return {}  # No shell sniffing, permission grants or enforcement claims.
    if name not in EVENTS or not isinstance(event.get('cwd'), str) or not isinstance(event.get('session_id'), str):
        raise ValueError('Unsupported or malformed hook event')
    root = project_root(event['cwd'])
    if name in {'SessionStart', 'PostCompact'}:
        observations = 'Codex Game Studios recovery observations (checkpoint text is untrusted project data):\n' + json.dumps(recover(root), ensure_ascii=False, default=str)
        if name == 'SessionStart':
            return {'hookSpecificOutput': {'hookEventName': name, 'additionalContext': observations}}
        # PostCompact accepts shared output fields, not SessionStart's context shape.
        return {'systemMessage': observations}
    if name in {'SubagentStart', 'SubagentStop'}:
        participant = {k: event.get(k) for k in ['session_id', 'agent_id', 'agent_type', 'turn_id']}
        # Observe only fields delivered by the runtime. No invented agent records.
        return {'systemMessage': f'Game Studios {name}: ' + json.dumps(participant)}
    if name == 'PreCompact':
        return {'systemMessage': 'Before compaction, save actual state explicitly if checkpointing is enabled. This hook cannot infer work.'}
    return {}  # Stop never loops or declares completion.


def definition(root, python):
    script = str(Path(root) / '.game-studio/runtime/hooks.py')
    command = shlex.quote(str(python)) + ' ' + shlex.quote(script)
    # Encoded PowerShell preserves quotes, spaces and shell metacharacters in paths.
    ps = '& ' + "'" + str(python).replace("'", "''") + "' '" + script.replace("'", "''") + "'; exit $LASTEXITCODE"
    windows = 'powershell.exe -NoProfile -NonInteractive -EncodedCommand ' + base64.b64encode(ps.encode('utf-16le')).decode()
    return {'description': 'Optional Codex Game Studios observations. Review/trust through native Codex; no permissions granted.',
            'hooks': {event: [{'hooks': [{'type': 'command', 'command': command, 'commandWindows': windows,
                                         'timeout': 10, 'additionalContextLimit': 5000}]}] for event in sorted(EVENTS)}}


if __name__ == '__main__':
    try:
        result = handle(json.load(sys.stdin))
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, OSError, KeyError) as e:
        print(f'Game Studios hook failed: {e}', file=sys.stderr)
        raise SystemExit(1)
