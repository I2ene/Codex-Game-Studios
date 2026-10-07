# Evaluation scenarios: gs-create-stories

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-create-stories/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Epic with 3 stories, all ADRs Accepted

**Fixture:**
- `project.yaml`: `engine.name: Godot`, `modes.workflow: full`,
  `modes.review_mode: lean`, `modes.story_granularity: fine` (one story per
  acceptance criterion)
- `production/epics/combat/EPIC.md` exists with 3 GDD requirements and its
  governing ADRs listed
- The epic's GDD exists with exactly one acceptance criterion per requirement (one
  is a damage formula)
- All governing ADR files exist with `## Status` Accepted
- `docs/architecture/control-manifest.md` exists
- `docs/architecture/tr-registry.yaml` has TR-IDs for all 3 requirements
- `production/epics/index.md` has a row for the epic with `Not yet created`

**Input:** `$gs-create-stories combat`

**Domain checks:**
- [ ] Exactly 3 stories are drafted — one per acceptance criterion at `fine`
- [ ] Each story file has the header fields Epic, Status, Layer, Type, Manifest Version, and a Context block with GDD, `Requirement: TR-[system]-NNN`, ADR Governing Implementation, ADR Version, Engine/Risk
- [ ] Each story has Acceptance Criteria, QA Test Cases, Test Evidence and Dependencies sections
- [ ] The formula story is typed Logic with evidence path `tests/unit/[system]/…` (the Godot test root)
- [ ] "QL-STORY-READY skipped — Lean mode." appears and each QA Test Cases section reads "N/A — no qa-lead specs at this tier…" (no improvised test cases)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Files are named `production/epics/combat/story-NNN-[slug].md`
- [ ] Skill does NOT start implementation

---

### Case 2: Failure Path — Named epic does not exist

**Fixture:**
- `project.yaml`: `modes.workflow: full`
- `production/epics/` contains other epics but no `nonexistent-epic/` directory

**Input:** `$gs-create-stories nonexistent-epic`

**Domain checks:**
- [ ] Skill outputs a clear error naming `production/epics/nonexistent-epic/EPIC.md`
- [ ] No story files, EPIC.md or index row are written
- [ ] Skill recommends `$gs-create-epics`
- [ ] Skill does NOT fall through to the `minimal` brief-synthesis branch at `full`

---

### Case 3: Blocked Story — ADR is Proposed

**Fixture:**
- `project.yaml`: `modes.workflow: full`, `modes.review_mode: solo`,
  `modes.story_granularity: fine`
- EPIC.md exists with 2 requirements, one acceptance criterion each; both
  governing ADR files exist
- Requirement 1 is governed by an ADR with `## Status` Accepted
- Requirement 2 is governed by ADR-0007 with `## Status` Proposed

**Input:** `$gs-create-stories [epic-slug]`

**Domain checks:**
- [ ] The ADR status is taken from the ADR's `## Status` section, not assumed
- [ ] Story 2 has `Status: Blocked` and the note names ADR-0007 and `$gs-architecture-decision accept` — never a bare `$gs-architecture-decision`, which starts a new ADR
- [ ] Variant — ADR-0007's `## Status` reads `Superseded by ADR-0009`: story 2 is still `Status: Blocked`, and its note names ADR-0009 as the ADR to point it at
- [ ] Story 1 has `Status: Ready` — the blocked ADR does not affect it
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Both story files are written (blocked stories are still written — just flagged)

---

### Case 4: Edge Case — No argument provided
**Fixture:**
- `project.yaml`: `modes.workflow: standard`
- `production/epics/` contains 2 epic subdirectories, each with an `EPIC.md`

**Input:** `$gs-create-stories` (no argument)

**Domain checks:**
- [ ] Skill asks "Which epic would you like to break into stories?" rather than erroring
- [ ] Both epics from the glob are offered as options
- [ ] Preserve unresolved human decisions and declines; perform authorized routine writes and ask only for missing decisions or scope.
- [ ] Skill does NOT silently pick an epic without user input
- [ ] Skill does NOT take the `minimal` brief-synthesis branch at `standard`

**Fixture (no epics):**
- `project.yaml`: `modes.workflow: standard`
- `production/epics/` holds no `EPIC.md`

**Domain checks (no epics):**
- [ ] No "Which epic…" question is asked with an empty option list
- [ ] The stop names `$gs-create-epics` and nothing is written

---

### Case 5: Director Gate — Full mode, one story returns GAPS from QL-STORY-READY

**Fixture:**
- `project.yaml`: `modes.workflow: full`, `modes.review_mode: full`,
  `modes.story_granularity: fine`
- EPIC.md exists with 2 requirements, one acceptance criterion each; both
  governing ADRs Accepted
- QL-STORY-READY returns ADEQUATE for story 1 and GAPS for story 2 (one vague
  acceptance criterion)
- At the GAPS question the user picks `Revise flagged criteria`

**Input:** `$gs-create-stories [epic-slug]`

**Domain checks:**
- [ ] `qa-lead` is consulted once for all stories (not once per story, and not a second time for story 1's specs); the only follow-up call covers story 2 alone
- [ ] Per-story verdicts use ADEQUATE / GAPS / INADEQUATE and name the failing criterion
- [ ] The GAPS verdict goes to the user with the three options — story 2's criteria are not revised before the user chooses
- [ ] Story 2's revised criteria are shown before the write ask; it carries no specs until ADEQUATE
- [ ] Had the user picked `Accept and proceed`, story 2 would be written with its criteria unchanged and its QA Test Cases reading `*Test cases not yet defined — run $gs-qa-plan to generate them.*`
- [ ] Story 1's QA Test Cases section contains Given/When/Then (Logic/Integration) or Setup/Verify/Pass condition (Visual/Feel, UI) blocks from the gate
- [ ] No "QL-STORY-READY skipped" note appears in `full` mode

---

### Case 6: Minimal tier — epic synthesized from the brief, then a return visit
**Fixture:**
- `project.yaml`: `engine.name: Godot`, `engine.version: "4.6"`, and no `modes`
  keys — `modes.rigor` defaults to `minimal`, so `workflow`, `qa.level` and the
  review mode resolve to `minimal` / `minimal` / `solo`
- `design/game-brief.md` with working title "Lantern Keeper", a Player goal & fail
  state, 2 MVP features and a Build order
- `<project-engine-reference>/godot/VERSION.md` is absent
- No `production/epics/` directory

**Input:** `$gs-create-stories`

**Domain checks:**
- [ ] Nothing, `EPIC.md` included, is written before the single write ask, and that ask names `EPIC.md`
- [ ] Each story reads `Requirement: Brief MVP feature N`, `N/A (minimal — no ADRs)` in its ADR fields and `N/A (minimal — no control manifest)` as its Manifest Version
- [ ] Each story's Risk is `NOT ASSESSED (no VERSION.md risk rating)` — never a guessed level
- [ ] Each QA Test Cases section reads the "N/A — no qa-lead specs at this tier…" line
- [ ] The index line names `production/epics/index.md`, not the systems index

**Fixture (return visit):**
- As above after that run: `production/epics/lantern-keeper/` holds `EPIC.md` (a
  2-row Stories table), `story-001-…` and `story-002-…`; the brief now lists a 3rd
  MVP feature

**Domain checks (return visit):**
- [ ] `story-001` and `story-002` are unchanged
- [ ] The new story is numbered 003, on from the highest existing number
- [ ] `EPIC.md` keeps its two rows and every other section; exactly one row is appended

**Fixture (an `EPIC.md` with no stories yet):**
- As the first fixture, but `$gs-create-epics` was run anyway, so
  `production/epics/lantern-keeper/EPIC.md` exists (scope from the brief, Stories
  "Not yet created") and the folder holds no story files

**Domain checks (an `EPIC.md` with no stories yet):**
- [ ] Every section of the existing `EPIC.md` other than its Stories table is unchanged
- [ ] The Step 5 ask says *update* `EPIC.md`

---
