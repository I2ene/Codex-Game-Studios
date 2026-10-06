"""Reproducible initial content adaptation from the audited upstream snapshot.

Maintainer tool, not an installer. Generated content must still be reviewed.
Original platform source remains archival and is excluded from consumer installation.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = 'b21fa0f7f289fc3e726cf36fb12b9bc1e7a51e4d'
SKILLS = sorted(p.parent.name for p in (ROOT / '.claude/skills').glob('*/SKILL.md'))
ROLES = sorted(p.stem for p in (ROOT / '.claude/agents').glob('*.md'))
SCRIPT_COMMANDS = {'artifact-check': 'artifacts', 'adr-dep-graph': 'dependencies',
                   'story-status': 'stories', 'review-receipts': 'receipts',
                   'review-scope': 'review-scope', 'project-coherence': 'coherence',
                   'gdd-structure-check': 'gdd-structure', 'rotate-session-state': 'checkpoint',
                   'migrate-v1-config': 'config'}


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.rstrip() + '\n', encoding='utf-8', newline='\n')


def split(text):
    if text.startswith('---\n'):
        front, body = text[4:].split('\n---', 1)
        return yaml.safe_load(front), body.lstrip()
    return {}, text


def adapt(text):
    # Only platform mechanics are transformed; domain analysis and contracts remain.
    text = re.sub(r'^!`[^\n]*`\s*$', '', text, flags=re.M)
    for name in SKILLS:
        text = text.replace(f'.claude/skills/{name}/SKILL.md', f'.agents/skills/gs-{name}/references/workflow.md')
        text = text.replace(f'.claude/skills/{name}/', f'.agents/skills/gs-{name}/references/')
        text = re.sub(r'(?<![\w:/])/' + re.escape(name) + r'\b', '$gs-' + name, text)
    for name in ROLES:
        text = text.replace(f'.claude/agents/{name}.md', f'.codex/agents/gs-{name}.toml')
    text = text.replace('.claude/docs/', '.game-studio/resources/docs/')
    text = text.replace('.claude/rules/', '.game-studio/resources/rules/')
    text = text.replace('docs/engine-reference/', '.game-studio/resources/engine-reference/')
    for name, command in SCRIPT_COMMANDS.items():
        text = re.sub(r'bash\s+(?:"?)\.claude/scripts/' + name + r'\.sh(?:"?)',
                      'python .game-studio/runtime/studio.py ' + command + ' --root <project-root>', text)
        text = text.replace(f'.claude/scripts/{name}.sh', f'.game-studio/runtime/studio.py {command}')
    text = text.replace('.claude/hooks/yaml-helper.sh', '.game-studio/runtime/studio.py config')
    text = re.sub(r'^.*(?:source |\. )[^\n]*yaml-helper[^\n]*\n', '', text, flags=re.M)
    text = re.sub(r'Resolved above — use as-is\.[\s\S]*?`\.game-studio/resources/docs/config-resolution.md`\.',
                  'Resolve settings explicitly with the native config command; retain its values and provenance.', text, count=1)
    text = text.replace('`${CLAUDE_PROJECT_DIR}`', '`<project-root>`').replace('${CLAUDE_PROJECT_DIR}', '<project-root>')
    text = text.replace('${CLAUDE_SKILL_DIR}', '<skill-directory>').replace('$CLAUDE_PROJECT_DIR', '<project-root>')
    text = text.replace('$ARGUMENTS', 'the workflow inputs').replace('AskUserQuestion', 'ask the user')
    text = text.replace('subagent_type:', 'expertise role:').replace('subagent_type=', 'expertise_role=')
    text = text.replace('Agent(', 'Delegation brief (').replace('Task(', 'Delegation brief (')
    text = text.replace('`Agent` tool', 'available native delegation tool')
    text = text.replace('`Agent` prompt', 'delegation brief')
    text = text.replace('Claude Code Game Studios', 'Codex Game Studios').replace('Claude Code', 'Codex')
    text = text.replace('CLAUDE.md', 'AGENTS.md').replace('CLAUDE.local.md', 'AGENTS.override.md')
    text = re.sub(r'(?i)\b(opus|sonnet|haiku)\b', 'inherited model', text)
    text = re.sub(r'(?i)\(model:\s*inherited model\)', '(session model)', text)
    text = re.sub(r'"May I write this to \[filepath\]\?"[^\n]*',
                  'use the existing task authorization; ask only for an unapproved material action', text)
    return text


COMMON = '''## Native execution contract

Use current project instructions, user authorization and inherited model/permissions.
Read `.game-studio/resources/docs/native-runtime.md` for platform mechanics and only
the domain references needed for this task. Config is an explicit command, not shell
preprocessing. Workflow inputs come from the user's request, not injected variables.
Tool-shaped examples below are procedural briefs; use tools actually exposed by the
host. They do not declare APIs or grant permissions. Existing task authorization
satisfies routine writes already in scope; do not repeat per-file approval questions.

Roles describe expertise. Delegate only when authorized and useful; otherwise apply
the role yourself and label the review as performed by the parent. Never fabricate
participant IDs, independent reviews or sign-off. Record real delegated participants.
Missing evidence means NOT ASSESSED — NO DATA. Resolve engine/version from this
project; engine reference versions are examples and require current verification.

'''


def main():
    for name in SKILLS:
        folder = ROOT / '.claude/skills' / name
        meta, body = split((folder / 'SKILL.md').read_text(encoding='utf-8-sig'))
        out = f'.agents/skills/gs-{name}'
        description = adapt(str(meta['description'])).replace('\n', ' ')
        write(out + '/SKILL.md', f'---\nname: gs-{name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n---\n\n# {name.replace("-", " ").title()}\n\n'
              + COMMON + 'Read [the complete procedure](references/workflow.md) and apply its relevant\n'
              'mode, prerequisites, role responsibilities and output contract.\n')
        write(out + '/references/workflow.md', COMMON + adapt(body))
        for p in folder.rglob('*'):
            if p.is_file() and p.name != 'SKILL.md':
                write(out + '/references/' + p.relative_to(folder).as_posix(), adapt(p.read_text(encoding='utf-8-sig')))
    for name in ROLES:
        meta, body = split((ROOT / '.claude/agents' / f'{name}.md').read_text(encoding='utf-8-sig'))
        instructions = COMMON + adapt(body)
        write(f'.codex/agents/gs-{name}.toml', f'name = "gs-{name}"\ndescription = {json.dumps(adapt(str(meta["description"])), ensure_ascii=False)}\ndeveloper_instructions = {json.dumps(instructions, ensure_ascii=False)}\n')
    for kind in ['docs', 'rules']:
        for p in (ROOT / '.claude' / kind).rglob('*'):
            if p.is_file():
                write(f'.game-studio/resources/{kind}/' + p.relative_to(ROOT / '.claude' / kind).as_posix(), adapt(p.read_text(encoding='utf-8-sig')))
    for p in (ROOT / 'docs/engine-reference').rglob('*'):
        if p.is_file():
            write('.game-studio/resources/engine-reference/' + p.relative_to(ROOT / 'docs/engine-reference').as_posix(), adapt(p.read_text(encoding='utf-8-sig')))
    write('.game-studio/LICENSE', (ROOT / 'LICENSE').read_text())
    files = subprocess.check_output(['git', '-c', f'safe.directory={ROOT.as_posix()}', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT, text=True).splitlines()
    rows = []
    for rel in files:
        p = ROOT / rel
        target, disposition, verification = rel, 'retain', 'Source retained; domain content is not platform migration'
        if rel.startswith('.claude/skills/'):
            parts = rel.split('/')
            target = f'.agents/skills/gs-{parts[2]}/references/' + ('workflow.md' if parts[3] == 'SKILL.md' else '/'.join(parts[3:]))
            disposition, verification = 'native', 'Metadata/resource validation; selected real native discovery and lifecycle sample'
        elif rel.startswith('.claude/agents/'):
            target, disposition, verification = f'.codex/agents/gs-{p.stem}.toml', 'native', 'TOML and inherited-setting validation; runtime role discovery where available'
        elif rel.startswith('.claude/docs/') or rel.startswith('.claude/rules/'):
            target = '.game-studio/resources/' + rel[len('.claude/'):]
            disposition, verification = 'replace', 'Adapted reference; native mechanics reviewed, professional content retained'
        elif rel.startswith('.claude/scripts/'):
            target = '.game-studio/runtime/studio.py ' + SCRIPT_COMMANDS.get(p.stem, 'run')
            disposition, verification = 'replace', 'Targeted helper tests; engine-dependent execution NOT ASSESSED without engine'
        elif rel.startswith('.claude/hooks/'):
            target, disposition, verification = '.game-studio/runtime/hooks.py', 'replace', 'Event I/O tests; runtime callbacks require native trust'
            if p.stem == 'yaml-helper':
                target, verification = '.game-studio/runtime/config.py', 'Configuration behavioral tests'
            if p.stem in {'notify', 'log-instructions'}:
                disposition, target, verification = 'unsupported', None, 'No native Notification event or stable instruction-read transcript API; explicit records/host notifications'
        elif rel in {'.claude/settings.json', '.claude/statusline.sh'}:
            target, disposition, verification = None, 'unsupported', 'Claude permissions/statusline never installed; current host settings inherited'
        elif rel.endswith('CLAUDE.md'):
            target, disposition, verification = 'AGENTS.md + scoped resource rules', 'replace', 'Managed instruction block and scoped rule routing; no @ imports'
        elif rel.startswith('docs/engine-reference/'):
            target = '.game-studio/resources/engine-reference/' + rel[len('docs/engine-reference/'):]
        baseline_bytes = subprocess.check_output(['git', '-c', f'safe.directory={ROOT.as_posix()}', 'show', f'{BASE}:{rel}'], cwd=ROOT)
        rows.append({'source': rel, 'sha256': hashlib.sha256(baseline_bytes).hexdigest(),
                     'disposition': disposition, 'target': target, 'verification': verification})
    write('docs/migration/inventory.json', json.dumps({'baseline': BASE, 'skills': SKILLS, 'roles': ROLES, 'files': rows}, indent=2))
    print(json.dumps({'skills': len(SKILLS), 'roles': len(ROLES), 'upstream_files': len(rows)}))


if __name__ == '__main__':
    main()
