# Integrate an arbitrary game project

Install into the existing repository, inspect the dry run, then use gs-adopt to map
actual work to applicable lifecycle steps. Preserve the current engine, directory
layout and professional records. The framework supplies expertise and templates;
it does not force every stage for a small task or supply a ready-made game.

Configuration facts belong in project.yaml. Leave rigor-derived knobs absent unless
you intentionally override them. Custom layouts use code_root/test_root; engine.name,
engine.version and optional engine.reference_root identify actual toolchain/reference
records. Packaged engine examples need current official verification. Local overrides
follow the documented whitelist; neither configuration file configures Codex permissions.

```yaml
schema_version: 1
modes:
  rigor: standard
  automation: guided
code_root: src
test_root: tests
commands:
  test: ["<test-executable>", "<argument>"]
  build: ["<build-executable>", "<argument>"]
```

Commands are reviewed argv lists. Keep paths with spaces as one element. For a shell
pipeline, write a project-owned script and name its executable/arguments explicitly.
Only execute commands within the user's authorized scope. `run test --root <root>`
records actual exit/output/time; `run build` needs a real build adapter. A source archive is not an engine build or platform certification.

Optional context interface (.game-studio/context.json):

```json
{"checkpoint":"production/session-state/active.md","records":["design/game-brief.md"]}
```

All paths are relative inside this repository. No connector, personal skill, NAS or
external working directory is assumed. Recover reports absent/unreadable records;
save explicit authored state with checkpoint --save <relative-file>. Configuration
features.session_state=off disables checkpoint recovery/saving. Keep context/checkpoints
out of Git if they contain local working state; installer does not edit your .gitignore.

Role profiles inherit the current session. Parent-applied role knowledge is reported
as parent work. Delegation needs real authorization and available tools; record actual
participant IDs and results. Parallelism is optional and only for independent work.
Review modes and stage gates retain the professional upstream contracts and strictest
verdict handling. A missing prerequisite, skipped gate or unavailable input must be
named. NOT ASSESSED never becomes a clean pass.

For upstream 1.x projects, follow the [upgrade guide](../UPGRADING.md). Native
review receipts require a fresh reviewed SHA-256 JSON baseline. Read
[configuration resolution](../.game-studio/resources/docs/config-resolution.md),
[context management](../.game-studio/resources/docs/context-management.md) and
[runtime tooling](tooling.md) for exact interfaces.
