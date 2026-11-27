# Implementation Plan: Complete upstream v1.3.0 Codex port

**Branch**: `codex/upstream-1.3-port` | **Date**: 2026-11-27 | **Spec**: [spec.md](spec.md)

## Summary
Merge the frozen upstream release as an ancestor, then port every professional delta into reviewed native skills, roles, resources and runtime. Reuse Bash/awk/JS and templates; adapt actual host boundaries and existing configuration/ownership interfaces. Retain generic Spec Kit artifacts for review, not an additional user workflow.

## Technical Context
- Language/version: Python 3.11+, Bash/awk, JavaScript/TypeScript, Markdown/YAML/TOML.
- Dependencies: existing requirements.txt; Bash for shell helpers; Node/package manager and a browser only for explicit Web work. Spec Kit v1.4.5 official source `6ba8beefff8d6408cadd62038e92d459093e33a8` is isolated maintainer tooling.
- Storage: owned project files, YAML configuration, JSON receipts and upstream prototype evidence files with distinct consumers.
- Testing: unittest, validate.py, integration_sample.py, temporary installed-consumer browser exercise, upstream-vs-native helper comparisons and candidate CI.
- Target platforms: Windows, Linux, macOS; no real game engine builds required.
- Scope: 409 upstream deltas, 78 expected skill entries, 49 roles, 69 genre profiles plus index/themes, 38 script deltas and complete affected studio lifecycle.
- Performance: preserve upstream run limits and finite browser checks; no unsupported performance claims.

## Constitution Check
All five principles pass before research and after design: source histories/attribution retained; payload boundary and user ownership unchanged; no model/tool grants; actual evidence classified; isolated review candidate only. No governance exception is needed.

## Project Structure
- `.agents/skills/gs-*/`: native entry, workflow, lenses and phase resources.
- `.codex/agents/gs-*.toml`: expert roles without host permission metadata.
- `.game-studio/scripts/`, `runtime/`: reused utilities and native adapters.
- `.game-studio/resources/{genres,engines,docs,rules,testing}/`: genre data, engine table/scaffold, templates, professional rules and evaluation guidance.
- `tests/`, `tools/`: semantic regressions, temporary consumer verification, release checks.
- `docs/upstream-file-map.tsv`, `docs/upstream-compatibility.md`: versioned traceability and necessary differences.
- `specs/001-upstream-v1-3-port/`: formal specification, plan, contracts, tasks and reproducible acceptance procedure.

## Phase 0: Research decisions
See [research.md](research.md). Compare both implementations before selecting reuse/adaptation/equivalence. Preserve previous mapping rows and add source-version columns. Inspect each source diff, not only paths or counts.

## Phase 1: Interfaces and data
See [data-model.md](data-model.md) and [port contracts](contracts/port.md).
Nested shared engine roots take priority over compatible old keys; invalid explicit overrides fail closed. Keep explicit argv and pins. Use upstream engine TSV as shared facts. Native receipt JSON and upstream prototype evidence remain separate. Parent-thread professional execution remains valid and labeled. Aliases invoke canonical workflow once with original arguments.

## Phase 2: Implementation sequence and ownership
1. Freeze source versions, initialize isolated Spec Kit tooling and create artifacts; merge upstream history without blanket conflict resolution.
2. Runtime owner: all changed/new scripts, engine table/scaffolds, Python config/engine/observations and focused runtime tests.
3. Workflow owner: all skill/role professional deltas, one-shot phases, lenses, aliases, route and evidence/approval semantics, focused workflow tests.
4. Resource owner: genre profiles, templates (excluding Web/scaffold templates owned by runtime), rules, engine reference docs and changed evaluation guidance/catalog, focused resource/evaluation tests.
5. Root integrator: cross-cutting docs/config catalogs, version/map/license/release checks, compatibility and installed browser/upgrade verification. Resolve shared interfaces before merging owner results. Owners never overwrite each other's files.
6. Execute all requirements, analyze consistency, converge against actual implementation, append remaining tasks and implement them. Do not declare completion from checked task boxes alone.

## Necessary host differences
- Replace host auto-imports, private transcript access and fixed grants/model/effort with native config, accessible explicit attachments and actual tools/authorization.
- Preserve parent execution and honest independent-review attribution; retain at most one optional engine helper where upstream requires that bound.
- Keep native hash receipts/ownership/atomic checkpoint safety and reviewed approvals. Do not wrap ordinary already-authorized work in redundant confirmation.
- Browser-sketch route in an existing non-Web project returns to applicable prototype Phases 6–9; one-shot Grow is offered only in its intended route.
- Real staged files/hand edits are protected by path-scoped Git operations; replay agreement is only sampled evidence, not proof nothing broke.
- Preserve blocking evidence for testable acceptance criteria; only actual human-playtest-only criteria may be explicitly deferred.

## Verification strategy
Each task names upstream/native paths and verification. Test runtime behavior and specific failure branches, preserve previous regression coverage, manually compare phase→output→consumer semantics. Execute [quickstart.md](quickstart.md) against installed temporary consumers. Build manifest only after payload review. Final handoff includes exact base/upstream/head, full mapping, actual CI and limitations. Spec Kit analysis/convergence summaries go to review conversation; no private execution logs enter the repository.
