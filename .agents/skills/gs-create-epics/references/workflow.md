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


Explicitly resolved — use as-is; `--review` overrides `review_mode`. No block →
defaults in `.game-studio/resources/docs/config-resolution.md`.

## Resolve this run's settings

Run `python .game-studio/runtime/studio.py config --root <project-root>` explicitly. Use effective values and provenance. Duplicate keys or malformed YAML are errors: inspect and repair the source configuration before dependent writes or commands; no merged values are authoritative after an error.



Ask with the question tool. Without one, list the options numbered and end your turn
to wait. A skipped question grants no approval. For optional questions continue with a stated reasonable assumption; keep genuinely required unresolved decisions pending.

## Native phase execution

Every referenced phase inherits the native contracts above. Role or agent wording
describes a professional responsibility: apply it in the parent when delegation is
unavailable or unauthorized, read its gate file yourself, and label parent work.
Only actual delegated participants count as independent reviews. Existing task
authorization covers in-scope writes and implementation; later example approval
questions are for unresolved choices, not a requirement to ask again per file.
Bash helpers under .game-studio/scripts require a compatible shell and the consumer
root as working directory; inspect their TSV output. Native studio.py commands use
--root explicitly and emit JSON; never parse them as historical colon-prefixed rows.

# Create Epics

An epic is a bounded body of work for one architectural module: **what** gets built
and which decisions govern it. How to build it is for the stories. Run it once per
layer as development reaches that layer: Feature epics written before Core is
nearly done describe a design that will have changed.

**Writes:** `production/epics/[epic-slug]/EPIC.md` per epic and its row in
`production/epics/index.md`, within the user-authorized scope.
**Next:** `$gs-create-stories [epic-slug]` per epic. This skill never writes a story.

Asks follow `.game-studio/resources/docs/automation-modes.md` (collaborative resolves open decisions, guided
asks on major choices, autonomous logs and goes on; `automation_always_ask`
categories require input only for decisions outside existing authorization).

Checklist (copy it and tick as you go):

```
- [ ] Phase 1: scope and tier
- [ ] Phase 2: inputs loaded and reported
- [ ] Phase 3: each epic shown, "Shall I create Epic: …?" asked one at a time
- [ ] Phase 4: producer review run, or its skip noted
- [ ] Phase 5: each EPIC.md and index row written within authorization
- [ ] Phase 6: closing block printed
```

## Phase 1: Scope and tier

The text typed after the skill name, with any `--review <mode>` pair removed:

- `all`: every system, in layer order.
- `layer: foundation` (or `core`, `feature`, `presentation`): that layer only.
- a system name: that system only.
- nothing: the request's own words when they name a layer or system ("foundation
  and core"); else ask "Which layer or system would you like epics for?"

**Tier.** The project's `workflow` value sets what is required (Phase 2). Each
in-scope system's own GDD bar comes from its `system_overrides` row, when it has one.

**At `minimal`, tell the user first:** this step is optional at this tier, because
`$gs-create-stories` builds the epic from `design/game-brief.md` by itself. Then go on
when they asked for epics.

## Phase 2: Load the inputs

### `minimal`: the brief

Read `design/game-brief.md`. None: stop, "No `design/game-brief.md` — run `$gs-start`
or `$gs-brainstorm` first." Never ask for GDDs, a systems index, an architecture
document, ADRs, a TR registry or a control manifest, and never send the user to
`$gs-design-system`, `$gs-map-systems` or `$gs-create-architecture` first: this tier has none
by design.

Report first, word for word:

```
Loaded: design/game-brief.md · engine [name version from the engine_values line]
At minimal this step is optional: $gs-create-stories builds the epic from the brief by itself.
```

The epics come from the brief's MVP feature list, in its **Build order**. A short
brief is one epic, slugged from the brief's working title (the slug `$gs-create-stories`
uses when nothing is typed). When the user asks for the work grouped, make one epic
per group of MVP features that ship together. Every epic names its slug, since
`$gs-create-stories` needs it typed.

### `standard` and `full`: the design and the architecture

1. **The system GDDs.** `python .game-studio/runtime/studio.py gdd-structure --root <project-root>` lists every
   system GDD; the game concept, systems index, pillars, cross-reviews and the other
   non-system documents are left out for you. Their count is **N**. N is 0: stop,
   "No system GDDs found in `design/gdd/` — run `$gs-design-system` first."
2. **What is in scope.** Each GDD's `## Summary` quick reference gives its layer and
   priority. A GDD with no Summary (older GDDs predate it) takes its layer from
   `design/gdd/systems-index.md`. Never treat an absent `## Summary` as an absent system:
   it never drops one from scope.
3. **The architecture.** `docs/architecture/architecture.md` is required at both
   tiers: missing, stop with
   "No `docs/architecture/architecture.md` — run `$gs-create-architecture` first." Never invent module boundaries.
4. **For in-scope systems only**, by section, never whole:
   - each GDD's Overview and Acceptance Criteria
     (`python .game-studio/runtime/studio.py markdown --root <project-root> extract design/gdd/<file>.md "Overview"`);
   - `bash .game-studio/scripts/adr-status.sh` for every ADR's status, layer and missing
     sections; then the GDD Requirements Addressed, Decision and Engine
     Compatibility sections of the ADRs that cover in-scope systems;
   - `docs/architecture/tr-registry.yaml`: the entries whose `system:` is an
     in-scope system;
   - the control manifest's `Manifest Version` line (read if present at `standard`,
     required at `full`);
   - `docs/engine-reference/<engine>/VERSION.md` for the engine's risk levels.

Report before defining anything, with the real state:

```
Loaded: [N] system GDDs, [n] in scope ([names]) · [M] ADRs ([A] Accepted, [P] Proposed) · manifest v[date | absent] · engine [name version from the engine_values line]
```

At `full`, every in-scope GDD needs all 8 sections and Approved status, and the TR
registry and control manifest are required. At `standard`, the GDDs need their 5
required sections, and only critical (Foundation-layer) ADRs are expected.

## Phase 3: Define each epic, ask one at a time

Process by layer: Foundation, then Core, Feature, Presentation; within a layer, the
systems index order (at `minimal`, the brief's Build order). For each system, its
module from `architecture.md` (at `minimal`, the brief's feature group).

**Requirement coverage** (not at `minimal`). Each TR-ID of the system is:

- **covered** when an **Accepted** ADR addresses it;
- **untraced** otherwise. A requirement whose only ADR is `Proposed` (or any other
  status) is untraced, never covered: its row reads `❌ No ADR (ADR-NNNN Proposed)`,
  so `$gs-create-stories` still sees that ADR and blocks its story.

Untraced requirements are listed under **Untraced Requirements**. The ⚠️ warning
below is for each untraced requirement at `full`, and only for untraced
Foundation-layer requirements at `standard`; any other untraced requirement at
`standard` is listed as information, with no warning.

```
## Epic: [System Name]
**Layer**: [Foundation | Core | Feature | Presentation]
**GDD**: design/gdd/[file].md   (at minimal: design/game-brief.md, MVP features [list])
**Architecture Module**: [module]
**Governing ADRs**: [Accepted ADRs, or "none"]
**Engine Risk**: [LOW | MEDIUM | HIGH — the highest among governing ADRs, else VERSION.md's]
**Requirements covered by Accepted ADRs**: [n / total]
**Untraced Requirements**: [TR-IDs with why, or "None"]
```

The warning, when it applies: "⚠️ [N] requirements in [system] have no Accepted ADR.
Their stories will be written with no governing ADR, or Blocked on a Proposed one.
Run `$gs-architecture-decision` first if they need a decision, or go on and accept the
gap."

Then ask, **for this epic alone**: "Shall I create Epic: [name]?" Options: Yes,
create it / Skip this epic / Pause — I need to write ADRs first. Show and ask the
next epic only after this answer. Never fold several epics into one question.

Existing authorization can cover the whole named batch. Show each epic and preserve its scope; ask only when its decisions or effects remain unresolved. Do not reinterpret a clear batch approval as approval for one file only.

## Phase 4: Producer review

Read the `review_gate` line above. `skill-gates=skip` (solo or lean): no agent; note
`PR-EPIC skipped — [Solo | Lean] mode` in the reply and the closing block.
`skill-gates=run`: read [pr-epic-gate.md](pr-epic-gate.md) and
`.game-studio/resources/docs/director-gates.md`, and run it now, after every epic in scope is
defined and before any write. On a skip, do not load it.

## Phase 5: Write each epic

For each epic the user said yes to, in order:

**Already has an `EPIC.md`:** never overwrite it. Ask "An EPIC.md already exists for
[name]. Update it in place, or skip it?" Options: Update in place / Skip this epic.
An update edits only what this skill owns (the header fields other than Stories,
Overview, Governing ADRs, GDD Requirements, Definition of Done) and leaves the
`**Stories**` line and any `## Stories` table as they are: `$gs-create-stories` wrote
them, and resetting them orphans the stories already there.

**New:** present the intended EPIC.md and index changes. Existing authorization covers in-scope writes; obtain a decision only for unresolved scope. Immediately before writing, run `python .game-studio/runtime/studio.py write-guard --root <project-root> overwrite
production/epics/[epic-slug]/EPIC.md`. Inspect its JSON findings. An OVERWRITE finding means the file exists: do not replace it as new; use the authorized in-place update path or resolve the choice with the user.

`docs.density` sets the depth of the Overview (`terse` bullets, `balanced` a short
paragraph, `thorough` full prose with ADR rationale and risks); the tables stay
whole at every density.

```markdown
# Epic: [System Name]

> **Layer**: [Foundation | Core | Feature | Presentation]
> **GDD**: design/gdd/[file].md
> **Architecture Module**: [module]
> **Status**: Ready
> **Stories**: Not yet created — run `$gs-create-stories [epic-slug]`

## Overview

[What this epic implements, from the GDD Overview and the module's responsibilities]

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|-----|------------------|-------------|
| ADR-NNNN: [title] | [one line] | LOW/MEDIUM/HIGH |

## GDD Requirements

| TR-ID | Requirement | ADR Coverage |
|-------|-------------|--------------|
| TR-[system]-001 | [requirement text from the registry] | ADR-NNNN ✅ |
| TR-[system]-002 | [requirement text] | ❌ No ADR (ADR-NNNN Proposed) |

## Definition of Done

- Every story implemented, reviewed and closed with `$gs-story-done`
- Every acceptance criterion of design/gdd/[file].md verified
- Logic and Integration stories have passing tests in the test root
- Visual/Feel and UI stories have retained screenshots in `production/qa/evidence/`
  (a lead sign-off too for Visual/Feel)
```

At `minimal`, the GDD line names `design/game-brief.md`, the Governing ADRs and GDD
Requirements tables are left out, and a **Scope** list holds the epic's MVP
features in Build order.

**`production/epics/index.md`:** one row per epic. An epic that already has a row
keeps it: update it in place, never add a second row, never reset its Stories cell.

```markdown
# Epics Index

Last Updated: [date]
Engine: [name version]

| Epic | Layer | System | GDD | Stories | Status |
|------|-------|--------|-----|---------|--------|
| [name] | [layer] | [system] | [file] | Not yet created | Ready |
```

## Phase 6: Close

At `standard` and `full`, once Foundation and Core epics exist, add: "Foundation and
Core epics are what the Pre-Production → Production gate needs. `$gs-gate-check
production` checks readiness." Never at `minimal`.

Every epic's content comes from the GDDs, ADRs and architecture docs (the brief at
`minimal`); none is invented.

**The run's last reply ends with this block** (repeat it if you showed it earlier):

```
Verdict: COMPLETE — [N] epics written: [slugs]
Review: [PR-EPIC skipped — Solo mode | skipped — Lean mode | its verdict]
Index: production/epics/index.md [created | updated]
Next step: $gs-create-stories [first-epic-slug]
```

When the user skipped or declined every epic: `Verdict: BLOCKED — no epic written
([why])`. No in-scope system found: `Verdict: BLOCKED — no eligible systems in
[scope]`.
