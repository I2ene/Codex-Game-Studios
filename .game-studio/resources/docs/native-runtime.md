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


## Browser, Grow and scope helpers

The new helpers retain upstream implementations and distinguish observations from
writes. Read each installed `--help` before invocation; these are actual script
interfaces, not inferred permissions. Use `GAME_STUDIO_PYTHON` for a Python 3.11+
interpreter with requirements when Bash cannot find that environment. On Windows,
`GAME_STUDIO_BASH` may name Git for Windows Bash for spawned Web tests; it is a
process/project tool choice, not a global configuration change.

| Action | Helpers and effects |
| --- | --- |
| Inspect | engine-row, web-detect, game-read, cut-read; one-shot-check `--keep`/`--checklist` report without runs or writes. Web scaffold `--list` previews. |
| Author/copy | one-shot-new, web-scaffold, door-in (preview first), references-save, tuning and selected cut-apply write explicit project files. Import reads original sources only; original byte checks remain separate. |
| Observe in browser | page-shot, one-shot-run, default one-shot-check and Grow replay run a real browser, use temporary copies and write evidence. `--record` validates and writes the selected check results; it is not `--keep`. Missing tooling is NOT ASSESSED. |
| Grow/recover | guard reads prerequisites; copy preserves the prototype, record writes native engine facts only as applicable, replay compares sampled evidence and accept updates its comparison baseline. Git commits/tags and undo follow the workflow's actual authorization and agreed files. |
| Deliver/network | one-shot-share and itch-zip write delivery output. vendor-three explicitly downloads pinned dependencies; authorized Grow/setup installs Web dependencies. None publishes automatically. |

Accessible explicit user files are the references-save input; no private host
transcript is scraped. If an attachment cannot be obtained as a file, request that
input and report the unavailable evidence. New browser TSV/YAML/image evidence has
prototype consumers; existing linked SHA-256 JSON report receipts retain theirs.

## Engine test preparation

`test-run.sh` runs reviewed `commands.test` argv. Required Godot import and Unreal
editor build use explicit shared `commands.test_import` and `commands.test_build`
argv respectively. When required preparation is absent or fails, no engine test pass
is claimed. Supply real project-specific executable/arguments; installing the
framework does not create or run them. `--no-build` explicitly opts out of Unreal
build; `--prepared` delegates preparation to the reviewed test adapter itself and
reports that fact, without claiming a separate external build was observed.

```yaml
commands:
  test_import: ["<godot-executable>", "--headless", "--path", ".", "--import"]
  test_build: ["<Unreal-build-executable>", "<project-specific-editor-build-arguments>"]
  test: ["<test-executable>", "<project-specific-test-arguments>"]
```

The table's shell command strings remain suggestions. They are not converted to
execution authorization or silently substituted for explicit consumer argv.
