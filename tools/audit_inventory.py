"""Refresh the per-source audit without regenerating reviewed native content."""
import collections
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

SCRIPTS = {
    'artifact-check': ('artifacts', 'Catalog globs/alternatives/patterns and denominators'),
    'adr-dep-graph': ('dependencies', 'Declared ADR dependencies, missing targets and cycles'),
    'story-status': ('stories', 'Real status enumeration; missing inputs never pass'),
    'review-receipts': ('receipts', 'SHA-256 whole-file/section changes and deletions'),
    'review-scope': ('review-scope', 'Declared GDD dependencies and conservative unresolved scope'),
    'project-coherence': ('coherence/engine-reference', 'Executed project-first version/render/physics/runner/export comparisons; explicit fixture version probe tested; real engine execution not assessed'),
    'gdd-structure-check': ('gdd-structure', 'Eight-section headings; quality/tier verdict remains professional review'),
    'rotate-session-state': ('checkpoint --save', 'Explicit authored checkpoint and hash-named backup; no inferred work/pruning'),
}
HOOKS = {
    'yaml-helper': ('config/settings', ['.game-studio/runtime/config.py', '.game-studio/runtime/studio.py'], 'Executed YAML precedence/local/rigor/error tests'),
    'session-start': ('SessionStart/recover', ['.game-studio/runtime/hooks.py', '.game-studio/runtime/context.py'], 'Fixture event I/O executed; trusted callback not assessed'),
    'post-compact': ('PostCompact/recover', ['.game-studio/runtime/hooks.py'], 'Shared output fields tested; SessionStart provides additional context; trusted delivery not assessed'),
    'pre-compact': ('PreCompact/checkpoint', ['.game-studio/runtime/hooks.py'], 'Reminder only; does not infer state'),
    'session-stop': ('Stop/checkpoint', ['.game-studio/runtime/hooks.py'], 'Stop is no-op; explicit checkpoint replaces inferred summary'),
    'log-agent': ('SubagentStart', ['.game-studio/runtime/hooks.py'], 'Actual supplied agent fields; parent records returned work'),
    'log-agent-stop': ('SubagentStop', ['.game-studio/runtime/hooks.py'], 'Actual supplied agent fields; no fictitious participants'),
    'detect-gaps': ('artifacts/coherence', ['.game-studio/runtime/checks.py'], 'Explicit observation replaces every-task scan'),
    'validate-commit': ('Relevant skill checks', ['.agents/skills/gs-code-review/SKILL.md'], 'No shell command interception or blanket enforcement; game checks not assessed'),
    'validate-push': ('Tests/release checklist', ['.agents/skills/gs-release-checklist/SKILL.md'], 'Explicit authorized delivery; game build/release checks not assessed'),
    'validate-assets': ('Asset audit/project validators', ['.agents/skills/gs-asset-audit/SKILL.md'], 'Real assets required; asset quality not assessed'),
    'validate-skill-change': ('Native format/behavior checks', ['tools/validate.py', '.agents/skills/gs-skill-test/SKILL.md'], 'Format and targeted runtime tests executed; full inference evaluation not assessed'),
}


def main():
    path = ROOT / 'docs/migration/inventory.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    rows = data['files']
    # One Git batch reads the audited blobs, including originals of edited root docs.
    proc = subprocess.run(['git', '-c', f'safe.directory={ROOT.as_posix()}', 'cat-file', '--batch'],
                          input=('\n'.join(data['baseline'] + ':' + r['source'] for r in rows) + '\n').encode(),
                          cwd=ROOT, stdout=subprocess.PIPE, check=True)
    position = 0
    for row in rows:
        end = proc.stdout.index(b'\n', position)
        header = proc.stdout[position:end].decode().split()
        if len(header) != 3 or header[1] != 'blob':
            raise ValueError('Missing audited source: ' + row['source'])
        size = int(header[2])
        original = proc.stdout[end + 1:end + 1 + size]
        position = end + size + 2
        row['sha256'] = hashlib.sha256(original).hexdigest()
        rel, name = row['source'], Path(row['source']).stem
        disposition, targets, installed = 'retain', [rel], False
        status, reason = 'FORMAT', 'Audited upstream history retained; not installed as native runtime'
        if rel.startswith('.claude/skills/'):
            parts = rel.split('/')
            base = '.agents/skills/gs-' + parts[2]
            if parts[3] == 'SKILL.md':
                disposition, targets = 'native', [base + '/SKILL.md', base + '/references/workflow.md']
                reason = 'Native metadata/procedure adapter; full domain workflow retained; discovered by actual CLI, inference quality not assessed'
            else:
                targets = [base + '/references/' + '/'.join(parts[3:])]
                reason = 'Professional contract/reference retained with path and authorization adaptation'
            installed = True
        elif rel.startswith('.claude/agents/'):
            disposition, targets, installed = 'native', ['.codex/agents/gs-' + name + '.toml'], True
            reason = 'Native three-field TOML; domain responsibilities retained; model/permissions inherit; custom-role launch not assessed'
        elif rel.startswith(('.claude/docs/', '.claude/rules/')):
            target = '.game-studio/resources/' + rel[len('.claude/'):]
            neutral = '/templates/' in rel or '/director-gates/' in rel or rel.startswith('.claude/rules/') and name not in {'agent-memory', 'skill-authoring'}
            disposition, targets, installed = 'retain' if neutral else 'replace', [target], True
            reason = 'Professional standards/template/gate retained with scoped native routing' if neutral else 'Native configuration/routing/collaboration mechanics replace host-specific behavior; domain guidance retained'
        elif rel.startswith('.claude/scripts/'):
            disposition, installed = 'replace', True
            if name in SCRIPTS:
                command, reason = SCRIPTS[name]
                targets, status = ['.game-studio/runtime/checks.py' if name != 'rotate-session-state' else '.game-studio/runtime/studio.py'], 'EXECUTED'
                if name == 'project-coherence':
                    targets += ['.game-studio/runtime/engine.py', '.game-studio/resources/docs/engine-reference-resolution.md']
                row['native_interface'] = command
            elif name == 'migrate-v1-config':
                disposition, installed, targets, status = 'unsupported', False, ['.agents/skills/gs-adopt/SKILL.md', 'UPGRADING.md'], 'NOT ASSESSED'
                reason = 'Automatic legacy Markdown conversion/finalization retired; explicit reviewed reconciliation available'
            else:
                targets, status = ['.agents/skills/gs-setup-engine/SKILL.md'], 'NOT ASSESSED'
                reason = 'Godot parse adapter is project-provided; no engine/runtime assumed or tested'
        elif rel.startswith('.claude/hooks/'):
            if name in HOOKS:
                interface, targets, reason = HOOKS[name]
                disposition, installed = 'replace', True
                row['native_interface'] = interface
                status = 'EXECUTED' if name in {'yaml-helper', 'session-start', 'post-compact', 'pre-compact', 'session-stop', 'log-agent', 'log-agent-stop', 'detect-gaps', 'validate-skill-change'} else 'NOT ASSESSED'
            else:
                disposition, targets, status = 'unsupported', [], 'NOT ASSESSED'
                reason = 'No stable native instruction-read transcript API' if name == 'log-instructions' else 'No native Notification event; host notifications require separate authorization'
        elif rel in {'.claude/settings.json', '.claude/statusline.sh'}:
            disposition, targets, status = 'unsupported', [], 'NOT ASSESSED'
            reason = 'Claude permissions/statusline excluded; no global settings or native trust changed'
        elif rel.startswith('docs/engine-reference/'):
            targets, installed = ['.game-studio/resources/engine-reference/' + rel[len('docs/engine-reference/'):]], True
            reason = 'Historical engine knowledge retained; actual engine/version/API verification required per consumer; engine execution not assessed'
        elif rel.startswith('CCGS Skill Testing Framework/'):
            if rel.split('/')[-1] in {'quality-rubric.md', 'skill-test-spec.md', 'agent-test-spec.md'}:
                targets = ['.game-studio/resources/testing/' + rel.split('CCGS Skill Testing Framework/', 1)[1]]
                disposition, installed = 'replace', True
                reason = 'Native professional evaluation rubric; not an executable test specification'
            else:
                reason = 'Archived professional test scenario retained for future representative inference evaluation; host assertions are not executable native tests'
                status = 'NOT ASSESSED'
        elif rel.endswith('CLAUDE.md'):
            disposition, targets = 'replace', ['.game-studio/AGENTS.fragment.md', '.game-studio/resources/docs/rules-reference.md']
            installed = True
            reason = 'Bounded AGENTS instructions plus scoped rules replace @ imports and Claude path auto-loading'
        elif rel in {'README.md', 'CONTRIBUTING.md', 'SECURITY.md', 'UPGRADING.md', 'project.yaml', '.gitattributes', '.gitignore'}:
            disposition, reason = 'replace', 'Native distribution/contributor interface; original retained in audited Git baseline'
        elif rel == 'LICENSE':
            targets, installed = ['LICENSE', '.game-studio/LICENSE'], True
            reason = 'MIT/Donchitos attribution preserved unchanged'
        elif rel == 'CHANGELOG.md':
            reason = 'Original release history retained; native 2.0.0 entry added separately'
        row.update(disposition=disposition, targets=targets, target=targets[0] if targets else None,
                   installed=installed, verification_status=status, verification=reason)
        for target in targets:
            if not (ROOT / target).is_file():
                raise ValueError('Inventory target missing: ' + target)
    data['disposition_semantics'] = {'native': 'Adopt as native entry/schema', 'replace': 'Replace platform mechanics',
                                    'retain': 'Preserve professional knowledge or audited history; installed flag distinguishes them',
                                    'unsupported': 'Explicitly unsupported original platform behavior'}
    data['deferred'] = ['Full native inference evaluation of 74 workflows/49 roles', 'Engine/game/asset/release validation without consumer inputs', 'Trusted hook delivery and custom-role launch']
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'files': len(rows), 'dispositions': dict(collections.Counter(r['disposition'] for r in rows)), 'baseline_hashes': 'verified'}))


if __name__ == '__main__':
    main()
