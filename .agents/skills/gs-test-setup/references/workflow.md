## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

## Native execution contract

Use current project instructions, user authorization and inherited model/permissions.
Read `.game-studio/resources/docs/native-runtime.md` for platform mechanics and only
the domain references needed for this task. Config is an explicit command, not shell
preprocessing. Workflow inputs come from the user's request, not injected variables.
Tool-shaped examples below are procedural briefs; use tools actually exposed by the
host. They do not declare APIs or grant permissions. Existing task authorization
satisfies routine writes already in scope; do not repeat per-file approval questions.

Roles describe expertise. Delegate only when authorized and useful; otherwise apply
the role yourself and label the review as performed by the parent. Never fabricate
participant IDs, independent reviews or sign-off. Record real delegated participants.
Missing evidence means NOT ASSESSED — NO DATA. Resolve engine/version from this
project; engine reference versions are examples and require current verification.


**Automation mode**: Resolve `modes.automation` (`project.local.yaml` →
`project.yaml` → default `collaborative`). Every `ask the user` call and
every file write follows `.game-studio/resources/docs/automation-modes.md`
(collaborative resolves open choices · guided resolves major choices · autonomous records in-scope choices;
`automation_always_ask` categories require input only outside existing authorization).

## Resolve this run's settings

Run `python .game-studio/runtime/studio.py config --root <project-root>` explicitly. Use effective values and provenance. If duplicate keys are reported, inspect the merged values to repair configuration before dependent writes or commands.


**Automation mode**: Resolve `modes.automation` (`project.local.yaml` →
`project.yaml` → default `collaborative`). Every `ask the user` call and
every file write follows `.game-studio/resources/docs/automation-modes.md`
(collaborative resolves open decisions · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

# Test Setup

This skill scaffolds the automated testing infrastructure for the project.
It detects the configured engine, generates the appropriate test runner
configuration, creates the standard directory layout, and wires up CI/CD
so tests run on every push.

Run this once during the Technical Setup phase, before any implementation
begins. A test framework installed at sprint start costs 30 minutes.
A test framework installed at sprint four costs 3 sprints.

**Output:** `tests/` directory structure + `.github/workflows/tests.yml`

---

## Phase 1: Detect Engine and Existing State

**Read `.agents/skills/gs-test-setup/references/1-detect.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 2: Present Plan

**Read `.agents/skills/gs-test-setup/references/2-plan.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 3: Create Directory Structure

**Read `.agents/skills/gs-test-setup/references/3-directories.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 4: Create CI/CD Workflow

**Read `.agents/skills/gs-test-setup/references/4-ci.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 5: Create Smoke Test Seed

**Read `.agents/skills/gs-test-setup/references/5-smoke-seed.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 6: Post-Setup Summary

**Read `.agents/skills/gs-test-setup/references/6-summary.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Collaborative Protocol

- **Never overwrite existing test files** — only create files that are missing.
  If a test runner file exists, leave it as-is.
- **Always ask before creating files** — Phase 2 requires explicit approval.
- **Engine detection is non-negotiable** — if the engine is not configured,
  stop and redirect to `$gs-setup-engine`. Do not guess.
- **`force` flag skips the "already exists" early-exit but never overwrites.**
  It means "create any missing files even if the directory already exists."
- For Unity CI, note that the `UNITY_LICENSE` secret must be configured
  manually. Do not attempt to automate license management.
