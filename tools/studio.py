"""Distribution entry point. Installation never modifies Codex user configuration."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.game-studio/runtime'))


def main():
    if len(sys.argv) > 1 and sys.argv[1] in {'install', 'upgrade'}:
        p = argparse.ArgumentParser(description='Install/upgrade reviewed framework into a separate project')
        p.add_argument('operation', choices=['install', 'upgrade'])
        p.add_argument('--target', required=True, type=Path)
        p.add_argument('--dry-run', action='store_true')
        a = p.parse_args()
        from installer import install
        print(json.dumps(install(ROOT, a.target, a.dry_run), indent=2))
        return 0
    import studio
    return studio.main()


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError) as e:
        print(f'Game Studios: {e}', file=sys.stderr)
        raise SystemExit(2)
