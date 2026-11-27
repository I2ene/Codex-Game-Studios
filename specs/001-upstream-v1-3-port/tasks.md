# Tasks: Complete upstream v1.3.0 Codex port

**Input**: [spec.md](spec.md), [plan.md](plan.md), [data-model.md](data-model.md), [contracts](contracts/port.md)

## Phase 1: Setup
- [X] T001 Freeze and verify three Git references and clean isolated branch; record public versions in specs/001-upstream-v1-3-port/research.md.
- [X] T002 Verify official Spec Kit v1.4.5/Codex integration and protect existing files; create .specify/memory/constitution.md and feature artifacts with generated template/setup scripts.
- [X] T003 Compare upstream and native implementations by independent runtime/workflow/resource ownership; capture decisions in specs/001-upstream-v1-3-port/plan.md.

## Phase 2: Foundation
- [ ] T004 Merge abc0de79 as a genuine ancestor; resolve each conflict after comparing the pinned source.
- [X] T005 Extend docs/upstream-file-map.tsv for every 409 delta, preserving prior source rows; implement SourceMapping.source_version, SourceMapping.disposition, SourceMapping.paths and SourceMapping.verification per data-model.md and verify against fixed Git diff.
- [X] T006 Establish shared script/resource/native path interfaces in specs/001-upstream-v1-3-port/contracts/port.md; exclude Spec Kit from manifest and discovery validation in tools/validate.py.

## Phase 3: US1 First playable and iteration
- [X] T007 [P] [US1] Port 69 genre profiles/index/themes from upstream .claude/genres to .game-studio/resources/genres with branch/source-preservation regression in tests/test_v13_resources.py.
- [X] T008 [P] [US1] Port upstream brief/one-shot templates to .game-studio/resources/docs/templates, preserving BriefAndEvidence.provenance per data-model.md.
- [X] T009 [P] [US1] Port start/brainstorm/prototype route, card/build/self-check/handover/change/files from upstream skills to .agents/skills/gs-*/references; preserve BriefAndEvidence.verdicts/participants per data-model.md and branch regression tests/test_v13_workflows.py.
- [X] T010 [P] [US1] Reuse/adapt new/changed one-shot/page-shot/door-in/references-save/tune/share/vendor helpers in .game-studio/scripts; retain argv/exits/file effects and accessible attachment fallback, with tests/test_v13_helpers.py.
- [X] T011 [US1] Execute installed brief/build/browser/screenshot/iterate/tune/share/import procedures in temporary consumers; make reproducible tools/v13_integration_sample.py and retain raw evidence outside public payload.

## Phase 4: US2 Grow, feature and cut
- [X] T012 [P] [US2] Port upstream Grow and cut workflow to .agents/skills/gs-prototype/references/one-shot-5-grow.md and gs-cut, including prerequisites, copied baseline, sampled replay, authorized keep/undo and no-Git behavior.
- [X] T013 [P] [US2] Reuse/adapt one-shot-grow/cut-read/cut-apply/itch-zip helpers in .game-studio/scripts, preserving BriefAndEvidence.features per data-model.md; add tests/test_v13_helpers.py for cut/restore/renumber and failure paths.
- [X] T014 [US2] Execute installed Grow/build/rules/smoke/replay/feature/cut/restore in tools/v13_integration_sample.py; verify missing-browser/nonrepeatable branches and original source preservation.

## Phase 5: US3 Engine configuration and Web
- [X] T015 [P] [US3] Reuse upstream engines.tsv/reader and Web scaffold/starters/locks in .game-studio/resources/engines and scripts; verify preview/collision/LF/TSV behavior in tests/test_v13_helpers.py.
- [X] T016 [P] [US3] Adapt config.py/engine.py/observations.py and shared command helpers for EngineConfiguration.name/roots/commands/goal per data-model.md; tests/test_v13_runtime.py cover nested/legacy/'.'/invalid and actual test outcomes.
- [X] T017 [P] [US3] Port setup-engine Web/test-setup/smoke references into .agents/skills and engine docs into .game-studio/resources/engine-reference; distinguish browser/build/zero-tests outcomes.
- [X] T018 [US3] Compare reusable helper stdout/exits/file effects with pinned upstream on equivalent fixtures; inspect four-engine consistency and explicit argv/pins in tests/test_v13_runtime.py.

## Phase 6: US4 Professional lifecycle
- [X] T019 [P] [US4] Port design-system/art-bible/architecture/code-review lenses and changed phase blocks into .agents/skills while preserving dependencies, per-section approval, accurate participants and bounded engine helper; test full downstream contracts in tests/test_v13_workflows.py.
- [X] T020 [P] [US4] Port Features/core-thin-deepen/Own calls/smoke/replay/EPIC-brief completion in story skills, preserving blocking evidence and scoped Git behavior in tests/test_v13_workflows.py.
- [X] T021 [P] [US4] Port all remaining changed skill blocks and 38 role deltas in .agents/skills and .codex/agents; preserve checkpoint append/disabled behavior, engine reference authority and professional responsibilities.
- [X] T022 [P] [US4] Port six rules and affected engine professional docs in .game-studio/resources; regress checkpoint failure, quoted commit scope, minimal Logic/Integration waiver and tuning data semantics in relevant tests.

## Phase 7: US5 Upgrade and compatibility
- [X] T023 [P] [US5] Add canonical gs-next-step/gs-project-settings/gs-write-changelog and thin help/settings/changelog aliases in .agents/skills; preserve original arguments/native settings and test single canonical routing in tests/test_v13_workflows.py.
- [X] T024 [US5] Replace fixed-count checks with expected entry/alias/role discovery and nonpayload Spec Kit checks in tools/validate.py and tests/test_runtime.py; implement OwnedInstallation.files per data-model.md.
- [X] T025 [US5] Run real frozen 2.1.0→candidate temporary upgrade, conflicts, instructions/config/checkpoint/workbench/other-skill preservation, restore and repeat install through tools/v13_integration_sample.py and tools/integration_sample.py.

## Phase 8: US6 Traceability and review
- [X] T026 [P] [US6] Port 20 changed skill/three role evaluation deltas and three renames to .game-studio/resources/testing; preserve fixtures/subscenarios/domain checks and reviewed native extras; update catalog.yaml and tests/test_v13_resources.py.
- [X] T027 [US6] Update README/NOTICE/CHANGELOG/UPGRADING, docs/upstream-compatibility.md and native indexes/config docs to final behavior, licenses, prerequisites and real limits; manually review every mapping family.
- [X] T028 [US6] Review payload, update VERSION/release.json with tools/build_release.py, validate links/catalog/manifest and run targeted/full unittest plus integration checks.
- [ ] T029 [US6] Run Spec Kit analyze/converge against specs/001-upstream-v1-3-port, append uncovered work and implement it; independently inspect full workflow-output-consumer relations and preserve previous regression fixes.
- [ ] T030 [US6] Commit/push candidate, create draft PR with exact refs/maps/differences/FORMAT-EXECUTED-NOT ASSESSED and wait exact-head CI; return independent review handoff without merging.

## Dependencies and parallel execution
T001–T003 precede T004–T006. Resource T007/T008/T022/T026, workflow T009/T012/T017/T019–T021/T023 and runtime T010/T013/T015/T016/T018 use distinct owned files and may proceed after foundation. Shared interfaces are coordinated, not overwritten. Installed exercises wait for their workflow+runtime+resource prerequisites. T024–T025 follow all payload changes; T027–T030 integrate every story.

## Implementation strategy
Deliver the entire bounded release, testing the first-playable story first as an integration slice rather than reducing the requested release to an MVP. Task boxes record actual completion only; evidence and remaining limitations go to the PR/review conversation. FORMAT checks and synthetic execution never substitute for all-model or game-quality proof.
