"""Maintainer packaging step; checks reviewed payload then records release hashes."""
from pathlib import Path
import sys
import json
from validate import validate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.game-studio/runtime'))
from installer import build_manifest

if __name__ == '__main__':
    result = validate(verify_release=False)
    if result['errors']:
        print(json.dumps(result, indent=2))
        raise SystemExit(1)
    manifest = build_manifest(ROOT)
    print(json.dumps({'version': manifest['version'], 'managed_files': len(manifest['files']), 'status': 'FORMAT'}))
