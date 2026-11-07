## Native checkpoint interface

Read .game-studio/resources/docs/context-management.md. Explicitly run recover
--root <project-root> and use checkpoint.path as <resolved-checkpoint>. If DISABLED,
skip checkpoint reads/writes; do not create a fixed fallback. Otherwise write the
current concise authored state to a temporary repository-local Markdown file and
run checkpoint --save <authored-file> --root <project-root>. Preserve useful fields
from the prior snapshot, reconcile current facts and replace stale state; the helper
keeps a hash-named backup. Do not append unbounded history or infer unseen work.
Existing task authorization covers routine state writes; state never grants consent.

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


Explicitly resolved — use as-is; `--review` overrides `review_mode` for this run. No
block → defaults in `.game-studio/resources/docs/config-resolution.md`.

## Resolve this run's settings

Run `python .game-studio/runtime/studio.py config --root <project-root>` explicitly. Use effective values and provenance. If duplicate keys are reported, inspect the merged values to repair configuration before dependent writes or commands.


block → defaults in `.game-studio/resources/docs/config-resolution.md`.

# Prototype

## Purpose

This is the **concept prototype** — a fast, throwaway build that answers one question:
*"Is this core idea actually fun to interact with?"*

**Default use** — run right after `$gs-brainstorm` and `$gs-setup-engine`, before writing
GDDs or architecture docs. Its verdict determines whether the concept is worth the
investment of full design documentation.

**Mid-production?** You can also run this at any stage to test a specific mechanic,
design change, or technical question. Pass `--spike` to activate spike mode: a
lightweight ~4-hour build with no GDD prerequisites and no phase gate implications.

**Already have GDDs and architecture complete?** To validate the full game loop
before committing to Production, run `$gs-vertical-slice` instead.

---

## Phase 1: Define the Question

**Read `.agents/skills/gs-prototype/references/1-question.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 2: Load Concept Context

**Read `.agents/skills/gs-prototype/references/2-load-context.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 3: Choose the Prototype Path

**Read `.agents/skills/gs-prototype/references/3-choose-path.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 4: Plan the Prototype

**Read `.agents/skills/gs-prototype/references/4-plan.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 5: Implement

**Read `.agents/skills/gs-prototype/references/5-implement.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 6: Playtest Debrief

**Read `.agents/skills/gs-prototype/references/6-debrief.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 7: Generate Prototype Report

**Read `.agents/skills/gs-prototype/references/7-report.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 8: Creative Director Review

**Read `.agents/skills/gs-prototype/references/8-cd-review.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 9: Summary and Next Steps

**Read `.agents/skills/gs-prototype/references/9-summary.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Spike Mode

**Triggered by:** `--spike` flag OR "Mid-production spike" entry choice in Phase 1.

**Read `.agents/skills/gs-prototype/references/spike-mode.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

### Important Constraints

- Prototype code must NEVER import from production source files
- Production code must NEVER import from prototype directories
- If the recommendation is PROCEED, production implementation is written from
  scratch — prototype code is never refactored into production
- Total effort is hard-capped at 1 day (concept prototypes test one mechanic)
- Test ONE mechanic — if scope grows, stop and simplify the question
- No polish. No menus, no game over, no music, no UI unless it IS the mechanic
- If stuck after 2 hours of engine iteration, reframe the question or switch paths
- **3 PIVOT iterations → force a KILL decision.** If this is the third time the
  same concept has produced a PIVOT verdict, the concept likely doesn't work.
  Ask: "Is this the right idea, or am I in the sunk cost trap?" A new concept
  prototyped fresh will almost always beat a fourth iteration of a struggling one.
- Building 2-3 different concept variants and picking the best one is a healthier
  strategy than iterating one concept to death. Natural selection between prototypes
  beats willpower.
- **Networked/multiplayer games:** A local prototype cannot validate the feel of a
  networked mechanic. Latency fundamentally changes how combat, movement, and
  prediction feel — a prototype running at 0ms local will feel entirely different at
  80ms network delay. Use a local prototype to validate that the mechanic is
  *interesting*. Do not use it as evidence that it *feels good* under real network
  conditions. Network feel requires real peers or simulated latency (e.g., throttle
  tools, network condition simulators).
