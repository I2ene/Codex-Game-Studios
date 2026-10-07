# Evaluation scenarios: gs-architecture-decision

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-architecture-decision/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — New rendering ADR, full mode, TD-ADR approves

**Fixture:**
- `project.yaml` has `engine.name: Godot` and `modes.review_mode: full`
- `<project-engine-reference>/godot/VERSION.md` exists and marks the pinned version HIGH risk; `breaking-changes.md` lists a Rendering change
- `docs/architecture/` contains `adr-0001-*.md` and `adr-0002-*.md`; none covers rendering
- `docs/registry/architecture.yaml` exists with no stance touching rendering
- `design/gdd/visual-effects.md` exists; the user confirms it as the GDD driving the decision, and its names match the ADR's Key Interfaces
- The engine specialist finds only minor notes; TD-ADR returns APPROVE

**Input:** `$gs-architecture-decision rendering-approach`

**Domain checks:**
- [ ] `VERSION.md` is read before any other step, and the knowledge-gap warning is shown for the HIGH-risk domain
- [ ] Assumptions are confirmed via `host input tool` before the ADR is generated; Status is shown as `Proposed`, never asked
- [ ] The engine specialist validation runs before TD-ADR (sequential, not parallel)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The written ADR has `Status: Proposed` even though TD-ADR returned APPROVE
- [ ] The GDD sync check reports the clean result for `visual-effects.md` in one line
- [ ] The registry update has its own approval prompt, separate from the ADR write
- [ ] Closing output contains the fresh-session `$gs-architecture-review` notice and the `accept ADR-0003` command

---

### Case 2: Failure Path — TD-ADR returns CONCERNS

**Fixture:**
- Same as Case 1, but TD-ADR returns CONCERNS: "Alternatives do not address the mobile renderer"
- One point stays unresolved after revision (which renderer to target on mobile)

**Input:** `$gs-architecture-decision rendering-approach`

**Domain checks:**
- [ ] TD-ADR receives the ADR draft/path, engine version and domain as context
- [ ] The CONCERNS are shown verbatim and the user chooses Revise / Accept / Discuss — the draft is not revised before that choice
- [ ] Each unresolved decision is a separate `host input tool` with a free-text escape option
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 3: Lean and Solo Modes — TD-ADR skipped; checks that cannot run say so

**Fixture:**
- Scenario (a): `project.yaml` has `modes.review_mode: lean` and `engine.name: Godot`
- Scenario (b): same project, invoked with `--review solo`
- Scenario (c): invoked with `--review solo` on a project with no engine configured — `engine.name` unset and `.game-studio/resources/docs/technical-preferences.md` still `[TO BE CONFIGURED]`; at Step 1's prompt the user carries on without running `$gs-setup-engine`
- `design/gdd/` holds no GDD, so the ADR's GDD Requirements Addressed names none

**Input:** (a) `$gs-architecture-decision save-format` (b) and (c) `$gs-architecture-decision save-format --review solo`

**Domain checks:**
- [ ] `technical-director` is not consulted in lean or solo mode
- [ ] The skip note names the gate and the mode ("TD-ADR skipped — Lean mode." / "— Solo mode.")
- [ ] The `--review solo` argument overrides the resolved `review_mode` for the run
- [ ] (a) and (b): the engine specialist validation still runs
- [ ] (c) With no engine configured, the output says engine validation was NOT ASSESSED instead of passing silently
- [ ] With no GDD named, the GDD sync check reports NOT ASSESSED, not a clean result
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 4: Edge Case — Proposed decision contradicts a registered stance

**Fixture:**
- `docs/registry/architecture.yaml` records an interface contract: `damage_delivery → signal pattern (ADR-0003)`
- ADR-0003 is Accepted
- The user states the proposal when invoking the skill, before Step 1: the decision is to deliver damage by direct method calls

**Input:** `$gs-architecture-decision damage-pipeline`, with that description in the same message

**Domain checks:**
- [ ] The registry is read before any existing ADR file
- [ ] The conflict warning names ADR-0003 and offers exactly the three options above
- [ ] The confirm/adjust assumptions prompt (Step 4) does not appear until the conflict is resolved
- [ ] On supersede, the old registry entry is marked `superseded_by`, not edited or deleted

---

### Case 5: Acceptance Mode — Status moves to Accepted only through `accept`

**Fixture:**
- `docs/architecture/adr-0005-physics-layers.md` exists with `Status: Proposed`
- Scenario (a): its `## ADR Dependencies` lists `Depends On: ADR-0002`, and ADR-0002 is `Proposed`
- Scenario (b): its only dependency is ADR-0001, which is `Accepted`; three files under `production/epics/*/story-*.md` name `ADR-0005` and are Blocked — two in the header form `$gs-create-stories` writes (`> **Status**: Blocked`), one as `**Status:** Blocked`
- `modes.automation` is `autonomous`

**Input:** `$gs-architecture-decision accept ADR-0005`

**Domain checks:**
- [ ] (a) Acceptance is refused when a dependency is not `Accepted`, naming ADR-0002; nothing is written
- [ ] (b) The confirmation prompt states how many stories will become Ready
- [ ] (b) The confirmation prompt appears in `autonomous` automation mode
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Stories are matched only under `production/epics/`
- [ ] (b) All three stories are found — the Blocked grep matches `> **Status**: Blocked` and `**Status:** Blocked`, not only the literal `Status: Blocked`

---

### Case 6: Retrofit — Missing Status answered `Accepted`

**Fixture:**
- `docs/architecture/adr-0004-input-mapping.md` exists with Context, Decision, Consequences, Engine Compatibility and GDD Requirements Addressed, but no `## Status` and no `## ADR Dependencies`
- ADR-0001 is `Accepted`
- One file under `production/epics/*/story-*.md` names `ADR-0004` and has `> **Status**: Blocked`

**Input:** `$gs-architecture-decision retrofit docs/architecture/adr-0004-input-mapping.md`

**Domain checks:**
- [ ] Only the missing sections are appended; existing sections are untouched
- [ ] The retrofit answer `Accepted` is never written straight into `## Status`; `Accepted` appears only after acceptance mode's dependency check and confirmation
- [ ] The confirmation prompt names the story count, as in Case 5
- [ ] Variant — the user declines "Shall I add the 3 missing sections?": no section is written, `## Date` included
