# Native execution interfaces

All helpers use Python 3.11+ with PyYAML 6.x. Invoke with an explicit absolute project
root; launch from any directory. Skill metadata has name/description only. No shell
preprocessing, imported permission grants or automatic memory injection exists.

`python <project-root>/.game-studio/runtime/studio.py <command> --root <project-root>`
supports config, recover, artifacts, stories, dependencies, coherence, engine-reference, gdd-structure,
review-scope, receipts, checkpoint, settings, run and hooks. Use `--help` for actual
arguments. Bash-prefixed examples in older engine references require a compatible
shell or translation to the local command tool; they are never auto-executed.

Repository skills are `$gs-<name>` or an ordinary natural-language request. Historical slash command examples are procedural notation, not runtime entries. Native roles are `gs-<role>`;
expertise-role examples are delegation briefs, not a tool schema. Use the available
host delegation tool only after authorization. If it cannot select custom roles,
pass the role's developer_instructions in the brief. Track real work in a project
artifact or the host's actual tools; a task/team runtime is optional.

Configuration: local whitelisted leaves → project leaves → legacy stage/review mirror
→ rigor expansion → defaults. Invalid enums fall back with notes; invalid YAML,
duplicates, orphan local configuration and invalid per-system tiers are errors.
Rigor minimal/standard/full sets workflow, density, QA, granularity, review and team
size, below explicit values. Unknown optional values remain unset. GDD stem identifies
system overrides; TR system alias is a fallback supplied by the calling skill.

Helpers inspect facts. Empty/missing game data, test adapters or build commands yield
NOT ASSESSED; success on a file check is not engine, balance, performance or release
certification. `run` executes explicitly configured argv without a shell and records
actual exit code/time/output. Never execute a project-defined command merely because
it exists: inspect it and ensure the user's scope authorizes it first.

Hooks are optional definitions generated for the installed project. Never install
them globally or merge into existing hook settings automatically. Codex must review
and trust definitions through its native UI/CLI. There is no Notification event,
stable transcript format, prompt hook execution or agent hook execution. Handlers
never return an allow permission decision, change tool inputs or infer hidden work.
