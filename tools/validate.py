"""Native distribution format checks; never claims semantic/game execution."""
import json
import hashlib
import unicodedata
from urllib.parse import unquote, urlsplit
from pathlib import Path
import re
import sys
import tomllib
import yaml

ROOT = Path(__file__).resolve().parents[1]


IGNORED = {'.git', '.venv', '.worktrees', '.scratch', '__pycache__', 'node_modules'}


def content_files(root):
    for p in root.rglob('*'):
        if not any(part in IGNORED for part in p.relative_to(root).parts) and p.is_file():
            yield p


def markdown_body(text):
    return re.sub(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1[^\n]*(?:\n|$)', '', text, flags=re.M | re.S)


def heading_ids(text):
    ids, counts = set(), {}
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', markdown_body(text), re.M):
        title = re.sub(r'<[^>]+>', '', title).lower().strip()
        title = ''.join(c for c in title if c in '-_ ' or unicodedata.category(c)[0] in 'LN')
        slug = title.replace(' ', '-')
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        ids.add(slug + (f'-{count}' if count else ''))
    ids.update(re.findall(r'(?:id|name)=["\']([^"\']+)', text))
    return ids


def document_errors(root):
    errors = []
    for p in content_files(root):
        if p.suffix != '.md':
            continue
        body = markdown_body(p.read_text(encoding='utf-8'))
        for match in re.finditer(r'(?<!!)\[[^]\n]+\]\((<[^>]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\)', body):
            target = unquote(match[1].strip('<>'))
            # A template variable is a consumer-authored destination, not a shipped file.
            if any(c in target for c in '<>[]*'):
                continue
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            file = (p.parent / url.path) if url.path else p
            if not file.exists() and url.path.startswith(('.game-studio/', '.agents/', '.codex/')):
                file = root / url.path
            if not file.exists():
                errors.append(f'{p.relative_to(root).as_posix()}: broken link {target}')
            elif url.fragment and file.is_file() and file.suffix == '.md' and url.fragment not in heading_ids(file.read_text(encoding='utf-8')):
                errors.append(f'{p.relative_to(root).as_posix()}: broken anchor {target}')
    return errors


def manifest_errors(root):
    errors = []
    try:
        release = json.loads((root / '.game-studio/release.json').read_text(encoding='utf-8'))
        actual = {}
        for base in ['.agents/skills', '.codex/agents', '.game-studio']:
            for p in content_files(root / base):
                rel = p.relative_to(root).as_posix()
                if p.suffix != '.pyc' and rel != '.game-studio/release.json':
                    actual[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
        if release.get('schema') != 1 or release.get('files') != actual:
            errors.append('Release manifest does not match the complete native payload; run tools/build_release.py after review')
        if release.get('version') != (root / '.game-studio/VERSION').read_text(encoding='utf-8').strip():
            errors.append('Release manifest version differs from VERSION')
    except (ValueError, OSError) as e:
        errors.append('Release manifest: ' + str(e))
    return errors


def test_catalog_errors(root):
    errors = []
    base = root / '.game-studio/resources/testing'
    try:
        catalog = yaml.safe_load((base / 'catalog.yaml').read_text(encoding='utf-8'))
        for kind, entries in [('skills', (root / '.agents/skills').glob('*/SKILL.md')), ('roles', (root / '.codex/agents').glob('*.toml'))]:
            expected = {p.parent.name if kind == 'skills' else p.stem for p in entries}
            rows = catalog[kind]
            names = [row['name'] for row in rows]
            if len(names) != len(set(names)) or set(names) != expected:
                errors.append('Evaluation catalog differs from native ' + kind)
            for row in rows:
                spec = base / row['spec']
                if not spec.is_file():
                    errors.append('Missing evaluation scenario: ' + row['spec'])
        if catalog.get('schema') != 1:
            errors.append('Evaluation catalog schema')
    except (KeyError, TypeError, ValueError, OSError) as e:
        errors.append('Evaluation catalog: ' + str(e))
    return errors


def validate(verify_release=True):
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
                if re.search(r'(?:[A-Z]:[/\\]Users[/\\](?!<)[^/\\\s]+|/Users/(?!<)[^/\s]+|/home/(?!<)[^/\s]+)', text):
                    errors.append(str(p.relative_to(ROOT)) + ': private coupling')
                if re.search(r'injected commit subjects|Both blocks are resolved before|AGENTS\.md-imported|\[NOT CHECKED\]|RECEIPT: NONE|Codex 2\.1\.63|is_always_ask_category|\[version\]\$gs-[\w-]+\.md', text):
                    errors.append(str(p.relative_to(ROOT)) + ': retired interface consumer')
                if re.search(r'independent Claude session|You MUST issue.*native delegation|Agent delegation \(MANDATORY\)|It prints.*`(?:PRESENT:|ADRS)`|`ADRS:`|`NO_DEPS_SECTION`', text):
                    errors.append(str(p.relative_to(ROOT)) + ': obsolete delegation/output contract')
                if re.search(r'orchestrator whose prompt|named path is your write authorisation|File writes are delegated', text):
                    errors.append(str(p.relative_to(ROOT)) + ': inferred authorization/delegation')
                if base in {'.agents', '.codex/agents'} and re.search(r'\.game-studio/resources/engine-reference/(godot|unity|unreal)/', text):
                    errors.append(str(p.relative_to(ROOT)) + ': packaged engine authority path')
    for p in (ROOT / '.agents/skills').glob('*/references/workflow.md'):
        if '## Project engine reference contract' not in p.read_text(encoding='utf-8'):
            errors.append(str(p.relative_to(ROOT)) + ': missing shared engine interface')
    for name in ['design-review', 'architecture-review', 'review-all-gdds']:
        p = ROOT / '.agents/skills' / ('gs-' + name) / 'references/workflow.md'
        if '.game-studio/resources/docs/review-receipts.md' not in p.read_text(encoding='utf-8'):
            errors.append(name + ': missing linked receipt contract')
    for p in content_files(ROOT):
        if p.name.upper().startswith('CLAUDE'):
            errors.append(str(p.relative_to(ROOT)) + ': retired host filename')
    errors.extend(document_errors(ROOT))
    errors.extend(test_catalog_errors(ROOT))
    if verify_release:
        errors.extend(manifest_errors(ROOT))
    for retired in ['.claude', 'CLAUDE.md', 'CCGS Skill Testing Framework', 'docs/migration', 'docs/superpowers']:
        if (ROOT / retired).exists():
            errors.append('Retired distribution content: ' + retired)
    return {'status': 'FORMAT', 'skills': len(skills), 'roles': len(roles), 'errors': errors}


if __name__ == '__main__':
    result = validate()
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result['errors']))
