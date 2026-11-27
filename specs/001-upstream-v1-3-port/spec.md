# Feature Specification: Complete upstream v1.3.0 Codex port

**Feature Branch**: `codex/upstream-1.3-port`

**Created**: 2026-11-27

**Status**: Ready for implementation

**Input**: Deliver the complete upstream v1.3.0 professional workflows and reusable implementation as a Codex-native release, preserving existing users and real authorization.

## User Scenarios & Testing

### User Story 1 - Make and revise a first playable (Priority: P1)
A user gives a game idea, accepts a brief, receives a browser playable checked against that brief, then requests changes, tunes it or shares it.

**Why this priority**: This is upstream's main entry route.

**Independent Test**: Install into a temporary empty consumer, use the installed resources to create a brief and playable, run browser observations and inspect screenshots, revise, apply tuning and export delivery files.

**Acceptance Scenarios**:
1. Given a vague idea, questions offer two or three candidates, one genre-informed round and retained original words; guessed fields and unsupported device/network substitutions are explicit.
2. Given an accepted brief, the build preserves Keep/Avoid/out-of-scope, all named systems and references; scripted/no-input observations and viewed screenshots support line-by-line verdicts, one repair round and honest handover.
3. Given an old brief or existing engine, its information and engine/paper routes survive; a browser sketch for an engine project returns to its applicable prototype review rather than silently converting the project.
4. Given requested changes, each round preserves unrelated hand edits and pinned tuning values, performs a light relevant retest, and offers keep/revert with actual Git authorization.
5. Given import/share requests, imported source bytes remain unchanged and delivery excludes development-only files; missing browser/attachment access is reported as unassessed.

### User Story 2 - Grow and finish the game (Priority: P1)
A user chooses to grow a one-shot, develops one feature at a time and chooses cuts from facts.

**Why this priority**: A useful first playable needs the complete continuation path.

**Independent Test**: Grow a temporary playable, compare deterministic replay, run build/unit/smoke, add a feature, preview/apply selected cuts and restore a removed planning item.

**Acceptance Scenarios**:
1. Given eligible one-shot and explicit Grow choice, prerequisites and root collisions are checked, the source is copied unchanged, seeded/input replay compares actual results, and applicable checks precede acceptance.
2. Given a nonrepeatable source, screenshots/errors support only observed equivalence and replay remains NOT ASSESSED; unavailable tooling is never a pass.
3. Given a feature sitting, user hand edits survive, smoke/replay differences are shown, and acceptance/revert acts only on that round's agreed files.
4. Given cut facts, only user-selected cuts change plans; Keep, feature renumbering, story references, completed/unfinished stories and restoration remain coherent. Code removal is a separate choice. Dates/freezes apply to the relevant project goals.

### User Story 3 - Use Web and existing engine configuration (Priority: P1)
A consumer can use Web or an existing engine with shared paths, observations and commands.

**Why this priority**: All entry paths and scripts require consistent project facts.

**Independent Test**: Run table/config/root/scaffold/test observations on four engine fixtures, overrides, root '.', unset/unknown engine and explicit invalid paths.

**Acceptance Scenarios**:
1. Given nested and old top-level root keys, nested shared keys take priority, old keys remain compatible, and invalid explicit paths produce a diagnostic without scanning a fallback directory.
2. Given Web, detection, setup, state, assets, scaffold, run/build/test/smoke and engine references agree; explicit command argument arrays and engine pins remain authoritative.
3. Given a scaffold preview or existing package, preview writes nothing and collisions preserve existing files. Installing the framework does not install or run consumer dependencies.
4. Given a failed unit test, browser test or zero-tests run, actual separate outcomes remain visible rather than being combined into a false success.

### User Story 4 - Continue professional studio work (Priority: P1)
Existing users retain all professional lifecycle responsibilities while receiving upstream's updated lenses, story flow and fixes.

**Why this priority**: The adaptation must preserve the complete professional framework.

**Independent Test**: Compare changed workflow/role sections against upstream and evaluate focused fixtures for section gates, story features, engine lenses and testability.

**Acceptance Scenarios**:
1. Given design/Art Bible/architecture review, each applicable professional lens and dependency is covered, and parent-thread work is labeled without claiming an independent reviewer or signature.
2. Given code review, at most one authorized engine helper supplies fresh-context evidence when available; testability and conclusions remain accountable and missing independence is explicit.
3. Given stories from a brief, built and unbuilt Features keep identity; core/thin/deepen sequencing, required deeper design, Own calls, epic/brief status and actual evidence govern closure.
4. Given minimal review, backup failure or quoted Git commands, the corrected upstream branch semantics apply without weakening existing write ownership, approval or missing-evidence rules.

### User Story 5 - Upgrade without disruption (Priority: P1)
A 2.1.0 consumer upgrades, restores context and reinstalls without losing its files or familiar commands.

**Why this priority**: Compatibility is part of the release contract.

**Independent Test**: Install the frozen previous release in temporary consumers, add user instructions/config/workbench/other skills, dry-run and upgrade, restore and reinstall; verify conflicts protect edited managed content.

**Acceptance Scenarios**:
1. Given old help/settings/changelog commands, one rename notice forwards original arguments into next-step/project-settings/write-changelog once.
2. Given owned and unowned files, upgrade preserves user data and reports edited managed conflicts before mutation; custom/disabled checkpoints and legacy paths still work.
3. Given Spec Kit development infrastructure, no development tool files or dependencies enter the consumer manifest or installation.

### User Story 6 - Independently review the adaptation (Priority: P1)
A maintainer can trace every upstream delta, reproduce checks and see honest limitations.

**Why this priority**: A complete port requires provenance and evidence beyond file counts.

**Independent Test**: Check Git ancestry and all 409 mapping rows, license propagation, installed references, release hashes, regression tests and exact-head CI.

**Acceptance Scenarios**:
1. Given the frozen source range, every changed file has a source purpose, prior native counterpart, final destination, disposition and verification reference, while previous mapping history remains available.
2. Given changed evaluation guidance, inputs, mutually exclusive branches, failure behavior and domain expectations survive; scenario counts never imply model passes.
3. Given a review candidate, precise base/upstream/head, necessary differences, actual checks and unassessed model/game behavior are supplied without private records.

### Edge Cases
- Missing Git/browser/Node, unsupported attachments, no configured engine, custom engines, nested/legacy root conflict, explicit invalid paths and '.' root.
- Import of standalone HTML, build-system Web projects and engine exports; original source read-only.
- Nonrepeatable replay, stage/write backup failure, pre-staged unrelated files, hand edits, missing/waived evidence and independent review unavailable.
- Existing package/lockfiles, user skills, conflicting managed files, custom checkpoint and existing workbench directories.

## Requirements

### Functional Requirements
- **FR-001**: Preserve the full frozen upstream delta, ancestry, licenses and traceability; prefer reused implementation and justify host differences (US6).
- **FR-002**: Provide genre-informed brief/build/check/handover with retained source words and honest evidence (US1).
- **FR-003**: Preserve import, iteration, tuning, delivery, baseline and accepted-round recovery behavior under real authorization (US1).
- **FR-004**: Provide complete Grow, replay, feature sitting, cut, plan synchronization and restore behavior (US2).
- **FR-005**: Unify four-engine configuration, paths, scaffold and observations while retaining existing explicit commands/pins and legacy keys (US3).
- **FR-006**: Preserve all studio responsibilities, applicable gates, story sequencing and upstream fixes with accurate participant/evidence reporting (US4).
- **FR-007**: Retain all 78 upstream skill entry names, 49 roles and renamed-entry compatibility without duplicate scenario claims (US5).
- **FR-008**: Preserve ownership, user instructions/config/data, checkpoints, context recovery, conflict refusal and repeat installation (US5).
- **FR-009**: Keep development-only Spec Kit out of release payload and real consumer dependencies (US5).
- **FR-010**: Preserve all changed evaluation semantics and provide reproducible structure, runtime and temporary consumer checks separated from game/model quality (US6).

### Key Entities
- Source mapping: frozen source versions, changed path, native before/after, disposition and evidence.
- Brief: user words, inferred decisions, features, named systems, Keep/Avoid/scope and optional date/freeze.
- Prototype evidence: observed browser runs/screenshots, replay inputs/results and unassessed boundaries.
- Project configuration: engine/pin/roots, goal and explicit commands, with source-aware compatibility.
- Installation ownership: managed hashes, instruction block and protected consumer files.

## Success Criteria

### Measurable Outcomes
- **SC-001**: All 409 source deltas are traceable and both frozen histories are ancestors of the candidate.
- **SC-002**: All 78 expected upstream entry names and 49 professional roles are discoverable after installation, including compatible legacy routes.
- **SC-003**: A temporary consumer completes the installed brief→browser→revise→Grow→replay→feature→cut/restore exercise with results recorded at their actual evidence level.
- **SC-004**: Previous-release upgrade, context recovery, repeated installation and conflict/user-file protection checks pass.
- **SC-005**: Full repository validation, affected/full tests and exact-head cross-platform CI have reviewable results; unavailable checks are explicit.

## Assumptions
The frozen upstream implementation defines professional behavior, not proof of Codex model execution. Synthetic browser fixtures verify helpers and procedure integration. Human fun/playtest quality, real engine builds and unavailable host events remain separately unassessed. No actual game is upgraded by this work.
