# General workflow implementation plan

> For agentic workers: execute inline using superpowers:executing-plans. Use one
> fresh reviewer at the end when available. The user authorized continued execution,
> checks, branch commits, push and a draft PR; do not merge main.

Goal: installable and upgradable engine-neutral Codex Game Studios 2.0.
Architecture: native skill/role adapters with complete professional references,
portable explicit helpers, ownership-based installation and optional hooks/context.
Tech stack: Markdown, YAML, TOML, Python 3.11+, PyYAML 6.x.
Spec: docs/migration/architecture.md.

## Constraints and review focus

Preserve user model/permissions, MIT and lifecycle semantics. No private game data or
machine paths. Verify malformed settings, instruction overrides, edited managed files,
path traversal/symlinks, failed commands and untrusted hooks.

### 1. Inventory and native content

- [x] Inspect every tracked source category and prior branch differences.
- [x] Generate per-file migration inventory with SHA-256, disposition and verification.
- [x] Adapt all skills/roles, preserve professional contracts/templates/rules.
- [x] Replace entry, onboarding, settings, collaboration and recovery interfaces.
- [x] Validate metadata, links, commands and platform residuals.

Files: tools/migrate_upstream.py, .agents/skills, .codex/agents, .game-studio/resources,
docs/migration/inventory.json, AGENTS.md. Native adapters consume professional source
from the audited baseline. Inventory explicitly distinguishes retain/replace/unsupported.

### 2. Configuration, context and installation

- [x] Write behavioral tests and observe expected failures.
- [x] Implement resolve(root, system=None), recover(root), install(source,target,dry_run).
- [x] Test per-leaf precedence, rigor/local scope, malformed YAML and explicit roots.
- [x] Test fresh/existing install, same-version reinstall, edited files, upgrade/removal,
      corrupt ledgers, dry run and failed-write rollback.

Files: .game-studio/runtime/config.py, context.py, installer.py, tests/test_runtime.py.

### 3. Helpers and optional hooks

- [x] Test artifacts, hash receipts, dependency/story observations and missing evidence.
- [x] Implement explicit CLI and argv command execution with honest status/exit receipts.
- [x] Implement event JSON handlers and hook-definition generation; test invalid input,
      SessionStart recovery and real participant fields without permission decisions.
- [x] Validate native discovery and hook availability without bypassing trust.

Files: .game-studio/runtime/checks.py, hooks.py, studio.py, tools/studio.py,
tests/test_checks.py, tests/test_hooks.py.

### 4. Delivery

- [x] Run isolated applicable design→development→review→delivery sample and retain receipts.
- [x] Document installation, upgrade, integration, scope and unassessed limitations.
- [x] Add CI, perform fresh review, fix material findings and run affected checks.
- [x] Commit/push as I2ene; create and attach draft PR; verify main remains baseline.

Files: README.md, UPGRADING.md, docs/install.md, docs/integration.md,
docs/migration/verification.md, .github/workflows/framework.yml.
