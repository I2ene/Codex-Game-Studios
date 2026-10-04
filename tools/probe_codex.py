"""Read-only native discovery probe. No model calls, trust changes or permission overrides."""
import argparse
import json
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import time


def probe(root):
    executable = shutil.which('codex')
    if not executable:
        return {'status': 'NOT ASSESSED', 'reason': 'Codex CLI unavailable'}
    process = subprocess.Popen([executable, 'app-server', '--stdio'], cwd=root,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, encoding='utf-8', errors='replace')
    responses = queue.Queue()

    def reader():
        for line in process.stdout:
            try:
                responses.put(json.loads(line))
            except json.JSONDecodeError:
                pass

    threading.Thread(target=reader, daemon=True).start()
    threading.Thread(target=lambda: list(process.stderr), daemon=True).start()

    def call(number, method, params):
        process.stdin.write(json.dumps({'id': number, 'method': method, 'params': params}) + '\n')
        process.stdin.flush()
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            response = responses.get(timeout=max(.1, deadline - time.monotonic()))
            if response.get('id') == number:
                return response
        raise TimeoutError(method)

    try:
        init = call(1, 'initialize', {'clientInfo': {'name': 'game-studios-discovery', 'version': '2.0.0'}, 'capabilities': {'experimentalApi': True}})
        process.stdin.write('{"method":"initialized"}\n')
        process.stdin.flush()
        skills = call(2, 'skills/list', {'cwds': [str(Path(root).resolve())], 'forceReload': True})
        hook_list = call(3, 'hooks/list', {'cwds': [str(Path(root).resolve())]})
        names, errors = [], []
        for entry in skills.get('result', {}).get('data', []):
            names += [s['name'] for s in entry.get('skills', []) if s['name'].startswith('gs-')]
            errors += [e for e in entry.get('errors', []) if '.agents' in e.get('path', '') and 'gs-' in e.get('path', '')]
        # No personal skill/config metadata is returned or persisted.
        return {'status': 'EXECUTED', 'native_skills': sorted(set(names)), 'count': len(set(names)),
                'framework_errors': errors, 'protocol_errors': [x['error'] for x in [init, skills, hook_list] if 'error' in x],
                'hooks_api_available': 'result' in hook_list,
                'note': 'Read-only discovery only; no skill inference, custom-role launch or trusted callback delivery.'}
    finally:
        process.stdin.close()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait(timeout=5)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', required=True, type=Path)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    result = probe(args.root)
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    print(text)
