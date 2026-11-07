## Native checkpoint interface

Read .game-studio/resources/docs/context-management.md. Explicitly run recover
--root <project-root> and use checkpoint.path as <resolved-checkpoint>. If DISABLED,
skip checkpoint reads/writes; do not create a fixed fallback. Otherwise write the
current concise authored state to a temporary repository-local Markdown file and
run checkpoint --save <authored-file> --root <project-root>. Preserve useful fields
from the prior snapshot, reconcile current facts and replace stale state; the helper
keeps a hash-named backup. Do not append unbounded history or infer unseen work.
Existing task authorization covers routine state writes; state never grants consent.

## Native review evidence contract

Read .game-studio/resources/docs/review-receipts.md before freshness/scope decisions. It replaces old text-line
or embedded-hash consumption below. Choose a real report/companion pair explicitly;
first/missing/legacy JSON means fresh full review. Consume baseline_status,
report_status and unchanged_inputs plus observations/required_unresolved/optional_unresolved. Prior failures stay
failures. After actual review, write the human report then generate a linked JSON
with receipts hash --report <report> --output <companion> for inputs actually read.
Declare applicable optional inputs when generating the snapshot with repeated
--optional-pattern <pattern>; check inherits the saved classification. Required
unavailable inputs still block verdict reuse; stable absent optional inputs stay named.
Scope/mode/required coverage must be the same before prior-verdict reuse.

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

## Resolve this run's settings

Run `python .game-studio/runtime/studio.py config --root <project-root>` explicitly. Use effective values and provenance. If duplicate keys are reported, inspect the merged values to repair configuration before dependent writes or commands.


# Review All GDDs

This skill reads every system GDD simultaneously and performs two complementary
reviews that cannot be done per-GDD in isolation:

1. **Cross-GDD Consistency** — contradictions, stale references, and ownership
   conflicts between documents
2. **Game Design Holism** — issues that only emerge when you see all systems
   together: dominant strategies, broken economies, cognitive overload, pillar
   drift, competing progression loops

**This is distinct from `$gs-design-review`**, which reviews one GDD for internal
completeness. This skill reviews the *relationships* between all GDDs.

**When to run:**
- After all MVP-tier GDDs are individually approved
- After any GDD is significantly revised mid-production
- Before `$gs-create-architecture` begins (architecture built on inconsistent GDDs
  inherits those inconsistencies)

Every `ask the user` call follows `.game-studio/resources/docs/automation-modes.md`
(collaborative resolves open decisions · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

**Argument modes:**

**Focus:** `the workflow inputs` (blank = `full`)

- **No argument / `full`**: Both consistency and design theory passes
- **`consistency`**: Cross-GDD consistency checks only (faster)
- **`design-theory`**: Game design holism checks only
- **`since-last-review`**: Only GDDs modified since the last review report (git-based)

---

**`workflow`** per GDD (per `.game-studio/resources/docs/workflow-modes.md`): each GDD validates
against its effective tier — the project value, overridden per system by the
`system_overrides` row for that system when the block lists one. At `full`, validate all 8
sections across all GDDs. At `standard`, validate the 5 required sections;
optional sections (Player Fantasy, Tuning Knobs, conditional Formulas) are
surfaced as advisory only. At `minimal`, this skill is not applicable (no GDDs).

## Phase 1: Load Everything

**Read `.agents/skills/gs-review-all-gdds/references/1-load.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

### Parallel Execution

Phase 2 (Consistency) and Phase 3 (Design Theory) are independent — they read
the same GDD inputs but produce separate reports. Spawn both as parallel native delegation when authorized
agents simultaneously rather than waiting for Phase 2 to complete before
starting Phase 3. Collect both results before writing the combined report.

Spawn both as `game-designer` sub-agents (`expertise role: game-designer`) — GDD
consistency and design-theory review is its domain.

**When spawning the Phase 2 and Phase 3 agents, always pass:**
- The loaded GDD **content** each phase needs — **not file paths**. Paste the
  sections; the sub-agent has its own context and cannot re-read Phase 1's
  results, so a path forces a full re-read (and contradicts the "do not re-read"
  rule below). Pass only the phase's slice: Phase 2 (consistency) needs each GDD's
  Dependencies, Detailed Design/Rules, Formulas, Tuning Knobs and Acceptance
  Criteria; Phase 3 (design theory) needs Player Fantasy, progression/reward
  structure and the game pillars.
- The full TR registry contents if loaded in Phase 1b (paste the registry text, not just a file path)
- The specific checklist items assigned to that agent's phase (Phase 2 gets 2a–2f; Phase 3 gets 3a–3g)
- The engine name and version — `engine.name` and `engine.version` from `project.yaml`, resolving each field independently (if its key is absent or empty, use `docs/project-reference/technical-preferences.md`) — plus `<project-engine-reference>/VERSION.md`

Do not rely on the subagent to re-read these files — it has its own context window and cannot access Phase 1 results unless they are explicitly passed in the delegation brief.

---

## Phase 2: Cross-GDD Consistency

**Read `.agents/skills/gs-review-all-gdds/references/2-consistency.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 3: Game Design Holism

**Read `.agents/skills/gs-review-all-gdds/references/3-design-holism.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 4: Cross-System Scenario Walkthrough

**Read `.agents/skills/gs-review-all-gdds/references/4-scenarios.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 5: Output the Review Report

**Read `.agents/skills/gs-review-all-gdds/references/5-report.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 6: Write Report and Flag GDDs

**Read `.agents/skills/gs-review-all-gdds/references/6-write.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 7: Handoff

**Read `.agents/skills/gs-review-all-gdds/references/7-handoff.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Error Recovery Protocol

**First, verify the artifact.** A required output path must exist before the
phase is complete, whether the author is the parent or a real delegate. If it is
missing, identify the unmet contract: complete authorized parent work or resume
the actual participant, and report any blocker. A fluent response alone is not
evidence of a completed phase.

If required parent work or an authorized delegate is BLOCKED, encounters an error, or fails to complete: **surface it
immediately, don't proceed past a dependency it blocks, and always produce a
partial report** (retry scope here = fewer GDDs / single-system). Full procedure:
`.game-studio/resources/docs/error-recovery-protocol.md`.

---

## Collaborative Protocol

**In `collaborative` mode (the default).** For `guided` and `autonomous` modes,
see `.game-studio/resources/docs/automation-modes.md`. In `autonomous` mode the
PASS/CONCERNS/FAIL verdict is still printed and logged — only the closing
handoff widget is skipped.

1. **Read silently** — load all GDDs before presenting anything
2. **Show everything** — present the full consistency and design theory analysis
   before asking for any action
3. **Distinguish blocking from advisory** — not every issue needs to block
   architecture; be clear about which do
4. **Don't make design decisions** — flag contradictions and options, but never
   unilaterally decide which GDD is "right"
5. **Ask before writing** — confirm before writing the report or updating the
   systems index
6. **Be specific** — every issue must cite the exact GDD, section, and text
   involved; no vague warnings
