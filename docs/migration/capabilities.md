# Capability migration checklist

Audit baseline: b21fa0f7f289fc3e726cf36fb12b9bc1e7a51e4d (upstream 1.1.2).
[inventory.json](inventory.json) lists all 485 tracked source files with original
Git-blob SHA-256, disposition, targets, installed flag and verification scope.
Hashes were rechecked from the audited baseline using Git batch I/O.

| Disposition | Count | Meaning |
|---|---:|---|
| Native adoption | 123 | 74 skill entry/procedure adapters and 49 role profiles |
| Replace mechanics | 68 | Native routing/config, helper/hook interfaces and contributor docs |
| Retain knowledge/history | 289 | Contracts/templates/gates/rules/engine knowledge or archived scenarios; installed flag distinguishes them |
| Unsupported original behavior | 5 | Claude settings/statusline, Notification/instruction-transcript callbacks, automatic Markdown migration |

Deferred validation is separate: full inference evaluation of 74 workflows/49 roles,
trusted hook delivery/custom-role launch, and engine/game/release outcomes need actual
host/consumer inputs. None is passed.

| Capability | Native entry / resource | Evidence |
|---|---|---|
| Concept/pillars | gs-brainstorm/prototype; concept/pillars/brief templates | Full procedures retained; parent brief fixture only |
| Systems/balance/UX | gs-map-systems/design-system/design-review/balance-check/ux-design/ux-review | GDD sections, MDA/psychology, formulas/tuning and tier contracts retained; game evaluation not assessed |
| Technical setup | gs-setup-engine/create-architecture/architecture-decision/architecture-review | Selection/upgrade reasoning and ADR/TR standards retained; actual engine facts preserved; engine execution not assessed |
| Pre-production | gs-create-control-manifest/create-epics/create-stories/vertical-slice | Registries/layers/traceability retained; minimal fixture story authored; broad game pipeline not assessed |
| Production | gs-dev-story/story-readiness/story-done/code-review and sprint/milestone workflows | Corrected source-import helper fixture; actual installed-procedure parent closure after an initial BLOCKED finding, four tests, explicit route/status; no director sign-off |
| Polish/QA | gs-team-polish/team-qa/qa-plan/smoke-check and regression/soak/evidence/playtest/perf/security/assets | Procedures/evidence standards retained; helpers tested; real visuals/assets/playtests/performance not assessed |
| Release/live operations | gs-team-release/team-live-ops/release-checklist/launch-checklist and localization/patch/hotfix | Certification/incident guidance retained; source archive helper executed; actual release stage guard BLOCKED and missing release evidence NOT ASSESSED; game build/deployment not assessed |
| 49 roles | .codex/agents/gs-*.toml | Native fields checked, settings inherit; responsibilities preserved; custom-role launch not assessed |
| 74 skills | .game-studio/resources/docs/skills-reference.md | Format checked and actually discovered in installed consumer; full inference behavior not evaluated |
| Contracts/templates/gates | .agents/skills/*/references; .game-studio/resources/docs/templates and director-gates | Professional knowledge, tier applicability and missing-evidence verdicts retained |
| Scoped rules | .game-studio/resources/rules; managed AGENTS block | Explicit routing; Claude glob frontmatter is not native auto-loading |
| Install/upgrade | tools/studio.py; docs/install.md; UPGRADING.md | Fresh/existing/dry-run/idempotency/ownership/conflict/upgrade/removal/rollback/locking/junction fixtures executed |
| Config/settings | explicit config/settings; config-resolution.md/effects-map.md | Real YAML leaf precedence, local whitelist, rigor/legacy/system and malformed-input checks executed |
| Context | recover/checkpoint; context-management.md | Optional confined paths, disabled/missing state and recovery tested; saved text supplies no new authorization |
| Helpers/hooks | [automation.md](automation.md) | Every original script/hook mapped; direct I/O tests separated from trusted callback delivery |

All seven original stages and minimal/standard/full paths remain available. Apply
relevant prerequisites/gates for the current scope. Team workflows describe disciplines,
with optional useful authorized delegation; label parent work and actual participants.

Original .claude and CCGS specifications stay audited and excluded from installs.
Native testing rubrics preserve professional criteria while replacing host/model and
blanket per-file-approval assertions. These rubrics are not executable native tests.
