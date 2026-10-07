# Evaluation scenarios: gs-team-ui

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-team-ui/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

## Execution path variants

Run the relevant success and blocking cases through both paths; preserve each
case's inputs, professional scope, artifact destinations and expected verdict.

**Parent execution path:**
- Fixture: delegation is unavailable or unauthorized; routine task work is authorized.
- [ ] The parent performs each required discipline and labels the work as parent work; it never invents independent participants or sign-off.
- [ ] All required results and blockers are summarized, and dependent phases wait for their prerequisites even when independent work is performed sequentially.

**Authorized delegation path:**
- Fixture: explicit user authorization, an exposed host tool and sufficient capacity for the independent tasks are confirmed.
- [ ] Independent tasks may run concurrently with distinct ownership; do not serialize genuinely independent delegated work when the fixture provides sufficient capacity.
- [ ] Dependent phases wait for all required results; blocks preserve completed work and surface before dependent action.
- [ ] Actual delegated participants are recorded with scope, result, artifacts and blockers; parent contributions remain labeled as parent work.
- [ ] Repeat with capacity below the full roster: queue independent work or apply the parent fallback without inventing concurrency or dropping disciplines.

### Case 1: Happy Path — Full pipeline from UX spec through polish succeeds

**Fixture:**
- Resolved config block: `review_mode: full`, `team.size: studio`, `automation: collaborative`
- `design/gdd/game-concept.md` exists with platform targets and intended audience
- `design/player-journey.md` exists
- `design/ux/interaction-patterns.md` exists with relevant patterns
- `design/accessibility-requirements.md` exists with committed tier (e.g., Standard)
- `engine.name` in `project.yaml` is Godot and `specialists.ui` is `godot-specialist`

**Input:** `$gs-team-ui inventory screen`

**Domain checks:**
- [ ] Active-set line naming `team.size: studio` appears before the first agent is consulted
- [ ] Phase 1a reads all five sources and lists each as present or ABSENT before briefing ux-designer
- [ ] UX Review Gate checked before Phase 2 — Phase 2 does NOT begin until APPROVED
- [ ] Art-director in Phase 2 reviews full spec, not just wireframe images
- [ ] Engine UI specialist is taken from `specialists.ui` and consulted before ui-programmer in Phase 3
- [ ] ui-programmer lists the files it will create or change, and writes none before the one ask for that set is answered yes
- [ ] Phase 4 covers UX, visual and accessibility reviews independently before final polish
- [ ] At `team.size: studio`, Phase 4's prompts are adversarial and the summary report says the adversarial pass ran
- [ ] The parent or authorized participants write their assigned artifacts under existing user authorization and label actual authorship
- [ ] Verdict COMPLETE in final summary report
- [ ] Next steps include `$gs-ux-review`, `$gs-code-review`, `$gs-team-polish`

---

### Case 2: UX Review Gate — Spec fails review; skill halts before implementation

**Fixture:**
- Resolved config block: `automation: collaborative` (any `team.size` — ux-designer is active at every size)
- `design/ux/inventory-screen.md` produced by Phase 1b
- `$gs-ux-review` returns verdict NEEDS REVISION with specific concerns flagged (e.g., gamepad navigation flow incomplete, contrast ratio below minimum)

**Input:** `$gs-team-ui inventory screen`

**Domain checks:**
- [ ] Phase 2 does NOT begin while UX review verdict is NEEDS REVISION
- [ ] `host input tool` presents the specific flagged concerns before offering options
- [ ] User must make a conscious choice to override — skill does not assume override
- [ ] If user accepts risk, the final report records the override: the NEEDS REVISION verdict, the concerns left open, and that the user chose to proceed
- [ ] Revision-and-re-review loop is offered (not just a one-shot failure)
- [ ] Skill does NOT discard the produced UX spec on review failure
- [ ] Phase 2 does NOT begin on NOT ASSESSED without an explicit user decision — it blocks like NEEDS REVISION
- [ ] The prompt names the dimension `$gs-ux-review` could not assess and the input that would make it checkable, not spec revisions
- [ ] The skill does not re-run `$gs-ux-review` against the same missing input and treat the result as new
- [ ] An override is recorded in the final report with the NOT ASSESSED verdict and the unassessed dimension

---

### Case 3: No Argument — Usage guidance shown

**Fixture:**
- Any project state

**Input:** `$gs-team-ui` (no argument)

**Domain checks:**
- [ ] Skill does NOT consults any specialist disciplines when no argument is given
- [ ] Usage message shows the full argument-hint: `$gs-team-ui [UI feature description] [--review full|lean|solo]`
- [ ] At least one example of a valid invocation is shown
- [ ] No UX spec files or GDDs read before failing
- [ ] Verdict is NOT shown (pipeline never starts)

---

### Case 4: Accessibility Parallel Review — Phase 4 independent review streams

**Fixture:**
- Resolved config block: `review_mode: full`, `team.size: small`, `automation: collaborative`
- `design/ux/inventory-screen.md` exists (APPROVED)
- Visual design spec complete
- Implementation complete
- `design/accessibility-requirements.md` committed tier: Standard

**Input:** `$gs-team-ui inventory screen` (resuming from Phase 3 complete)

**Domain checks:**
- [ ] The three review disciplines use the same implementation and specs independently; Phase 5 waits for all results
- [ ] Phase 5 does NOT begin until all three Phase 4 agents have returned
- [ ] Accessibility-specialist explicitly reads `design/accessibility-requirements.md` for the committed tier
- [ ] Accessibility violations flagged as BLOCKING (not merely advisory)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] No Phase 4 agent's output is used as input for another Phase 4 agent

---

### Case 5: Missing Interaction Pattern Library — Skill notes the gap rather than inventing patterns

**Fixture:**
- Resolved config block: `automation: collaborative` (any `team.size`)
- `design/ux/interaction-patterns.md` does NOT exist
- All other required files present

**Input:** `$gs-team-ui settings menu`

**Domain checks:**
- [ ] Skill does NOT silently ignore the missing pattern library
- [ ] Skill does NOT invent patterns by guessing from the feature name or GDD alone
- [ ] `host input tool` offers a "create pattern library first" option (referencing `$gs-ux-design patterns`)
- [ ] If user proceeds without the library, ui-programmer is told to treat all patterns as new
- [ ] Final report documents pattern library status (created / absent / updated)
- [ ] Skill does NOT fail entirely — the gap is noted and user is given a choice


## Applicable domain checks

- [ ] Before professional work starts, resolve and announce team-size scope, parent coverage and any actual participants. At `team.size: individual`: ui-programmer and ux-designer; art, accessibility and engine-UI perspectives follow the documented team-size scope. Name inactive perspectives and unassessed work accurately.
- [ ] Absent committed accessibility requirements make that review NOT ASSESSED; absent engine configuration makes engine validation NOT ASSESSED. Name each unassessed dimension in the qualified completion verdict.
- [ ] Missing named artifacts fail their phase; error recovery surfaces the block, offers options and preserves the partial report.
- [ ] UX review checks keyboard-only and gamepad-only navigation; visual review checks minimum and maximum supported resolutions against the art bible.
