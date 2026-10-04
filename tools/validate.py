"""Native distribution format checks; never claims semantic/game execution."""
import json
from pathlib import Path
import re
import sys
import tomllib
import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate():
    errors = []
    skills = list((ROOT / '.agents/skills').glob('*/SKILL.md'))
    roles = list((ROOT / '.codex/agents').glob('*.toml'))
    if len(skills) != 74 or len(roles) != 49:
        errors.append('Expected 74 skills and 49 roles')
    for p in skills:
        text = p.read_text(encoding='utf-8')
        try:
            meta = yaml.safe_load(text.split('---', 2)[1])
            if set(meta) != {'name', 'description'} or meta['name'] != p.parent.name or not meta['description']:
                errors.append(str(p.relative_to(ROOT)) + ': metadata')
        except (KeyError, IndexError, yaml.YAMLError):
            errors.append(str(p.relative_to(ROOT)) + ': invalid frontmatter')
        for link in re.findall(r'\]\(([^\s)]+)\)', text):
            if not link.startswith(('http', '#')) and not (p.parent / link).is_file():
                errors.append(str(p.relative_to(ROOT)) + ': broken resource ' + link)
    for p in roles:
        data = tomllib.loads(p.read_text(encoding='utf-8'))
        if set(data) != {'name', 'description', 'developer_instructions'} or data['name'] != p.stem:
            errors.append(str(p.relative_to(ROOT)) + ': role metadata or setting pin')
    for base in ['.agents', '.codex/agents', '.game-studio/resources']:
        for p in (ROOT / base).rglob('*'):
            if p.is_file() and p.suffix in {'.md', '.toml', '.yaml'}:
                text = p.read_text(encoding='utf-8')
                if re.search(r'CLAUDE_(PROJECT|SKILL)|\.claude/|^!`|^allowed-tools:', text, re.M):
                    errors.append(str(p.relative_to(ROOT)) + ': obsolete execution path')
                if any(token in text for token in ['D:\\File\\GameDesign', 'D:\\Game\\PersonalRPG', 'rpg-game-design']):
                    errors.append(str(p.relative_to(ROOT)) + ': private coupling')
    inventory = json.loads((ROOT / 'docs/migration/inventory.json').read_text())
    if len(inventory['files']) != 485 or len({r['source'] for r in inventory['files']}) != 485:
        errors.append('Inventory is incomplete/duplicated')
    for row in inventory['files']:
        if row['disposition'] not in {'native', 'replace', 'retain', 'unsupported'} or not row['verification']:
            errors.append('Invalid migration disposition: ' + row['source'])
    return {'status': 'FORMAT', 'skills': len(skills), 'roles': len(roles), 'upstream_files': len(inventory['files']), 'errors': errors}


if __name__ == '__main__':
    result = validate()
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result['errors']))
