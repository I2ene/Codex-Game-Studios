# Codex Game Studios

Version **2.0.0** — a reusable Codex workflow for game projects, adapted from
Donchitos' MIT-licensed Claude Code Game Studios 1.1.2.

Install into a separate new or existing project. The framework provides **74 native
skills**, **49 inheriting expertise roles**, professional standards, phase gates,
contracts and templates for design, architecture, implementation, review, QA,
performance investigation, builds, release and live operations. It chooses no engine,
model, permissions or personal workspace.

```text
<python-with-PyYAML> tools/studio.py install --target <absolute-project-root> --dry-run
<python-with-PyYAML> tools/studio.py install --target <absolute-project-root>
```

Python 3.11+ and PyYAML 6.x are required. Use [installation instructions](docs/install.md)
for environment setup, [upgrade instructions](UPGRADING.md) for ownership/conflicts,
and [project integration](docs/integration.md) for configuration, recovery and adapters.
After installation, open Codex in the consumer and use `$gs-start`, `$gs-adopt` or
`$gs-help`. Relevant skills also match natural-language requests.

| Area | Capabilities |
|---|---|
| Design | concepts/pillars, system GDDs, MDA/player psychology, UX, art/audio/narrative, economy/balance, content/assets |
| Architecture/development | engine/version selection, ADRs, requirements/registries, epics/stories, prototypes, implementation, code reviews |
| Quality | stage/story readiness, QA plans, tests/evidence, accessibility/security, playtests, profiling, soak/regression analysis |
| Delivery/operations | sprint/milestone tracking, build/test adapters, release/launch checklists, patch notes, hotfixes, live operations |
| Framework runtime | explicit config/recovery, artifact/story/dependency observations, SHA-256 review receipts, opt-in command hooks |

Minimal/standard/full rigor preserves upstream mode-dependent requirements. Small
projects use the short brief-to-story path; larger projects use appropriate phase
gates. Roles supply expertise; actual delegation is optional, authorized and recorded.
No fictitious director participation or independent sign-off is produced.

Installation preserves user configuration, instructions outside its bounded block,
engine files, records and user skills. Upgrades preflight hash ownership and reject
edited managed files. No global Codex configuration, engine installation, approval
policy or hook trust is changed. Optional context uses repository-relative paths.

[Migration inventory](docs/migration/inventory.json) covers all **485 upstream files**
with source hashes, dispositions, destinations and verification methods. See the
[capability checklist](docs/migration/capabilities.md), [automation mapping](docs/migration/automation.md),
[platform reference](docs/migration/platform-evidence.md) and [validation procedure](docs/migration/verification.md).

Run the validation procedure against the checkout you are reviewing. Format checks,
helper execution and game evidence are reported separately; no archived run is shipped
as proof for a new checkout. Game balance, performance, engine builds, platform
certification, custom-role launch and trusted hook callbacks require actual
consumer/host evidence. A source archive is not a game build.

Contributor checks:

```text
python tools/validate.py
python -m unittest discover -s tests -v
python tools/integration_sample.py
```

`.claude/`, original top-level reference documents and `CCGS Skill Testing Framework/`
remain upstream audit/history material, excluded from consumer installation. Native
runtime content lives in `.agents`, `.codex/agents` and `.game-studio`. They are not
claimed to run as Claude commands in Codex.

[MIT license](LICENSE), copyright (c) 2026 Donchitos, retained unchanged.
