# Native execution interfaces

Native runtime helpers use Python 3.11+ with PyYAML 6.x. Invoke with an explicit absolute project
root; launch from any directory. Skill metadata has name/description only. No shell
preprocessing, imported permission grants or automatic memory injection exists.

`python <project-root>/.game-studio/runtime/studio.py <command> --root <project-root>`
supports config, recover, artifacts, stories, dependencies, coherence, engine-reference, gdd-structure,
review-scope, receipts, checkpoint, settings, run, hooks, markdown, project-state,
read-guard, write-guard, test-scaffold and skill-lint. Use `--help` for actual
arguments. Bash-prefixed examples in older engine references require a compatible
shell or translation to the local command tool; they are never auto-executed.

Repository skills are `$gs-<name>` or an ordinary natural-language request. Historical slash command examples are procedural notation, not runtime entries. Native roles are `gs-<role>`;
expertise-role examples are delegation briefs, not a tool schema. Use the available
host delegation tool only after authorization. If it cannot select custom roles,
pass the role's developer_instructions in the brief. Track real work in a project
artifact or the host's actual tools; a task/team runtime is optional.

Configuration: local whitelisted leaves → project leaves → legacy stage/review mirror
→ rigor expansion → defaults. Invalid enums fall back with notes; invalid YAML, orphan local config, ambiguous dotted paths
and invalid per-system tiers are errors. Read-only config resolution reports duplicate
keys with source lines and merges repeated maps (later leaf wins). Fix duplicates
before writes or command execution.
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

## Upstream helpers

The active utilities under `.game-studio/scripts/` reuse upstream Bash/awk
observation logic. They are optional for installation and recovery. To run them
use Bash 3.2+ with awk and ordinary command-line utilities; on Windows use Git
for Windows Bash or another compatible Bash that can read the project paths.
Invoke them explicitly from the consumer root or supply `--root`. See `--help`
for each real interface; do not treat the TSV as professional approval.
If the tools are unavailable, inspect the same project inputs explicitly and
record the missing execution evidence.

| Utility | Observation |
| --- | --- |
| `adr-status.sh` | ADR status, layer, dates, effective version and missing sections |
| `story-facts.sh` | Story fields, sprint scope, test evidence and acceptance-criterion lint by granularity |
| `registry.sh` | Exact IDs and registry references, next IDs and validations (including existing retired IDs) |
| `asset-scan.sh`, `content-count.sh` | Asset rules and content inventory. Pass the actual project engine with `--engine` when scanning engine files. |
| `bug-stats.sh`, `debt-register.sh`, `flaky-stats.sh` | Open bugs, debt prioritization and repeated test outcomes |
| `code-markers.sh`, `inputs-check.sh`, `plan-math.sh` | Source markers, file/input observations and planning arithmetic |

No automatic permission, shell command, notification, registry mutation or
background update is installed by these utilities. Python validates and writes
configuration using a single YAML interpretation. Use read-guard/write-guard
explicitly as observations and use an approved configuration or engine runner
for tests; there is no generic command interceptor.

For phase operations use `markdown list|status|extract` to inspect complete
sections. `replace` and `insert-before` read a body from stdin or `--body-file`;
`set-field` accepts a single value. Confined explicit writes do not grant
authorization. `project-state` reports facts and source, not a gate. Derived
configuration observations are available through `config --keys`.
