# Evaluation scenarios: gs-story-readiness

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-story-readiness/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Fully ready story

**Fixture:**
- `project.yaml` sets `modes.workflow: full` and `modes.review_mode: solo`
- Story file exists at `production/epics/core/story-light-pickup.md` containing:
  - A `GDD: design/gdd/light-system.md` reference quoting the specific requirement
  - `TR-light-001`, present with `status: active` in `docs/architecture/tr-registry.yaml`
  - `ADR: ADR-0003`; `docs/architecture/adr-0003-inventory.md` has `## Status` Accepted
  - `Type: Logic`, an `## Acceptance Criteria` section with 3 testable items, and a `## Test Evidence` section naming the test path
  - An estimate, an Out of Scope statement, and `Dependencies: None`
  - Engine notes (or "N/A — no engine API involved"), the relevant manifest rules, and a performance note
  - A `Manifest Version:` equal to the one in `docs/architecture/control-manifest.md`
  - No TBD / UNRESOLVED markers and no asset paths
- A sprint plan in `production/sprints/` lists other stories

**Input:** `$gs-story-readiness production/epics/core/story-light-pickup.md`

**Domain checks:**
- [ ] ADR status is resolved from the one-scan `^## Status` Grep over `docs/architecture/adr-*.md`, not by reading each ADR in full, and ADR-0003 is found Accepted
- [ ] Skill looks up `TR-light-001` in `tr-registry.yaml` and finds it active
- [ ] The current manifest version is taken from a Grep of the manifest header, not a full read
- [ ] The "Passing Checks (N/[total])" section names all six groups — Design Completeness, Architecture Completeness, Scope Clarity, Open Questions, Asset References ("no asset references"), Definition of Done — with the passing items under each
- [ ] Verdict is READY when all checks pass
- [ ] Skill does not write any files
- [ ] Section 7 lists up to 3 other ready sprint stories — or states "Next ready stories: no sprint file found" / "none ready in [sprint]" rather than omitting the section

---

### Case 2: Blocked Path — Referenced ADR is Proposed (not Accepted)

**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- Story `production/epics/core/story-light-system.md` references `ADR-0005`
- `docs/architecture/adr-0005-light-system.md` exists with `## Status` Proposed
- All other story content is complete

**Input:** `$gs-story-readiness production/epics/core/story-light-system.md`

**Domain checks:**
- [ ] Verdict is BLOCKED (not NEEDS WORK or READY) when the ADR is Proposed at `full`
- [ ] Output explicitly names ADR-0005 as the blocker
- [ ] Output says to wait for the ADR's acceptance before implementing
- [ ] Skill does not output READY regardless of other checks passing
- [ ] Variant — same story at `modes.workflow: standard`, with `| **Layer** | Feature |` in ADR-0005's `## Engine Compatibility` table (non-critical): the story references the Proposed ADR, so the verdict is still BLOCKED — a referenced Proposed ADR blocks at every tier, because `$gs-dev-story` stops on it
- [ ] Variant — the same non-critical ADR at `standard`, now `Accepted`, with the story's `Manifest Version:` older than the control manifest's: the stale version is listed under Gaps as advisory, with its `Fix:` line, and the verdict is READY — an advisory gap does not downgrade it

---

### Case 3: Needs Work — Missing Acceptance Criteria (checked at every tier)

**Fixture:**
- `project.yaml` sets `modes.workflow: minimal`
- Story `production/epics/core/story-oxygen-drain.md` has `Type: Logic` but no `## Acceptance Criteria` section
- The story references no ADR, no TR-ID and no manifest version

**Input:** `$gs-story-readiness production/epics/core/story-oxygen-drain.md`

**Domain checks:**
- [ ] Verdict is NEEDS WORK (not BLOCKED or READY) when the Acceptance Criteria section is absent
- [ ] Output identifies the missing Acceptance Criteria specifically, with a `Fix:` line proposing measurable criteria
- [ ] No ADR, TR-ID or manifest gap is flagged — Architecture Completeness is N/A at `minimal`
- [ ] The story is not BLOCKED: nothing requires outside action (no missing/DRAFT dependency, no unowned UNRESOLVED question)
- [ ] Variant — the same `minimal` story with acceptance criteria traced to `design/game-brief.md`'s MVP feature (no `design/gdd/` path): "GDD requirement referenced" passes — the brief stands in for the GDD at `minimal`
- [ ] Variant — the story also names `ADR-0005`, whose `## Status` is `Proposed`: the verdict is BLOCKED at `minimal` too — the referenced-ADR rule is the one Architecture Completeness item that is not N/A

---

### Case 4: Edge Case — Stale manifest version

**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- Story has `Manifest Version: 2026-01-15` in its header
- `docs/architecture/control-manifest.md` has `Manifest Version: 2026-03-10`
- Everything else in the story passes

**Input:** `$gs-story-readiness production/epics/core/story-mirror-rotation.md`

**Domain checks:**
- [ ] Skill gets the current version by grepping `Manifest Version` in `docs/architecture/control-manifest.md`
- [ ] Skill compares the story's embedded version against the current one
- [ ] At `full`, a stale manifest version results in NEEDS WORK (not BLOCKED, not READY)
- [ ] Output explains that new manifest rules may apply, and the `Fix:` says to review the changed rules, update the story if needed, then set its `Manifest Version:` to current

---

### Case 5: Director Gate — QL-STORY-READY behavior across review modes
**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- Story file exists and passes every checklist item
- Review mode comes from `modes.review_mode` (legacy mirror `production/review-mode.txt`) or `--review`

**Case 5a — full mode:** `$gs-story-readiness production/epics/core/story-light-pickup.md --review full`

**Domain checks (5a):**
- [ ] Skill uses the resolved review mode before deciding whether to consult QL-STORY-READY
- [ ] QL-STORY-READY is consulted only after the checklist verdict exists
- [ ] A GAPS result produces the three-option `host input tool`
- [ ] An INADEQUATE result overrides the checklist's READY: the final verdict is NEEDS WORK, restated with the gate's specific gaps
- [ ] If the user proceeds anyway, the verdict stays NEEDS WORK and the output states the override ("proceeding despite QL-STORY-READY: INADEQUATE (user override)") — never a silent READY
- [ ] A NOT ASSESSED answer from the gate names the missing input and never leaves READY standing: unless the input is supplied and the gate re-run, the verdict is NOT ASSESSED

**Case 5b — lean or solo mode:** `--review lean` or `--review solo`

**Domain checks (5b):**
- [ ] QL-STORY-READY does NOT consult in lean or solo mode
- [ ] The skip is noted in the output with the mode named
- [ ] Verdict is based on the checklist alone

---

### Case 6: UI story at `qa.level: minimal` — the screenshot plan is never waived

**Fixture:**
- `project.yaml` sets `modes.workflow: standard` and `qa.level: minimal` (set on
  its own, so only the test-evidence axis is at `minimal` and every checklist
  group is evaluated)
- No `docs/architecture/control-manifest.md` and no `tr-registry.yaml` yet
- Story `production/epics/ui/story-003-shop-panel.md` has `Type: UI`, a
  `GDD: design/gdd/shop.md` reference quoting the requirement it implements, two
  testable acceptance criteria naming what the shop panel shows, "No ADR applies —
  pure layout", engine notes, an estimate, an Out of Scope statement,
  `Dependencies: None` and a performance note — and no `## Test Evidence` section,
  nor any other mention of where a screenshot will go
- No TBD / UNRESOLVED markers and no asset paths

**Input:** `$gs-story-readiness production/epics/ui/story-003-shop-panel.md`

**Domain checks:**
- [ ] Verdict is NEEDS WORK, not READY — the evidence item does not auto-pass for a UI story at `qa.level: minimal`
- [ ] The gap names the missing screenshot plan, and its `Fix:` points at `production/qa/evidence/`
- [ ] The missing screenshot plan is the only gap — no ADR, TR-ID or manifest gap is flagged
- [ ] Variant — a `Type: Logic` story with three testable criteria and no `## Test Evidence` section, same config: the evidence item auto-passes at `qa.level: minimal`, so the missing section alone does not make it NEEDS WORK

---

### Case 7: NOT ASSESSED — nothing to evaluate, or an ADR nobody can read

**Case 7a — zero stories in scope:**
- `production/epics/` holds only `EPIC.md` index files, no story files
- **Input:** `$gs-story-readiness all`

**Domain checks (7a):**
- [ ] Output is `NOT ASSESSED — no stories in scope`, naming `production/epics/**/*.md` as the path searched
- [ ] It routes to `$gs-create-epics [layer]` then `$gs-create-stories [epic-slug]`
- [ ] No `Ready: 0 / Needs Work: 0 / Blocked: 0` summary is printed over an empty list

**Case 7b — a referenced ADR with no readable status:**
- `project.yaml` sets `modes.workflow: full`
- Story `production/epics/core/story-save-slots.md` passes every other item and
  references `ADR-0007`; `docs/architecture/adr-0007-save-format.md` exists but has
  no `## Status` section
- **Input:** `$gs-story-readiness production/epics/core/story-save-slots.md`

**Domain checks (7b):**
- [ ] The ADR check is NOT ASSESSED — the status is unknown, not failed — and the verdict is NOT ASSESSED: not BLOCKED, not READY
- [ ] Output names `docs/architecture/adr-0007-save-format.md` and routes to `$gs-architecture-decision retrofit docs/architecture/adr-0007-save-format.md`

**Case 7c — referenced ADR file is absent:**
- As 7b, except docs/architecture/adr-0007-save-format.md does not exist; the story itself remains in scope.
- **Input:** $gs-story-readiness production/epics/core/story-save-slots.md

**Domain checks (7c):**
- [ ] Verdict is BLOCKED ("referenced ADR is missing"), not NOT ASSESSED or READY; the finding names ADR-0007 and its missing path.
- [ ] Resolve the missing referenced decision before implementation; do not report an empty story scope or a malformed existing ADR.
