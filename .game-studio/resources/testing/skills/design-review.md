# Evaluation scenarios: gs-design-review

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-design-review/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
`<runtime>` abbreviates `<runtime-python> <project-root>/.game-studio/runtime/studio.py`;
append `--root <project-root>` and use the current command's `--help`.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Complete GDD, all 8 sections present

**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- `design/gdd/light-manipulation.md` exists with all 8 sections populated with
  substantive content (the Detailed Rules section is titled `## Detailed Design`)
- Formulas section defines at least one formula with named variables
- Acceptance Criteria section contains at least 3 testable criteria
- Every system named in its Dependencies section has a GDD in `design/gdd/`
- No prior review log exists for this document

**Input:** `$gs-design-review design/gdd/light-manipulation.md --review lean`

**Domain checks:**
- [ ] Skill reads the target file before producing any output
- [ ] Section presence comes from `<runtime> gdd-structure`, and `## Detailed Design` is accepted as the Detailed Rules section (not flagged missing)
- [ ] Output includes "Completeness: 8/8" (N is 8 because the tier is `full`)
- [ ] Output includes a "Dependency Graph" section listing each declared dependency with whether its GDD exists
- [ ] Output includes "Required Before Implementation", "Recommended Revisions" and "Scope Signal" sections, and "Re-review: No — first review"
- [ ] Output ends with `### Verdict:` APPROVED when all REQUIRED sections are present and no blocking issue is found
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] If the review-report option is selected, the actual report has a linked SHA-256 JSON companion covering the document and required context

---

### Case 2: Failure Path — Incomplete GDD (4/8 sections at `full`)

**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- `design/gdd/light-manipulation.md` has Overview, Player Fantasy, Detailed
  Rules and Dependencies only; Formulas, Edge Cases, Tuning Knobs and
  Acceptance Criteria are absent

**Input:** `$gs-design-review design/gdd/light-manipulation.md --review lean`

**Domain checks:**
- [ ] Output shows "4/8" in the completeness section (not a higher number)
- [ ] Output explicitly names each missing section (Formulas, Edge Cases, Tuning Knobs, Acceptance Criteria) as REQUIRED
- [ ] Verdict is NEEDS REVISION or MAJOR REVISION NEEDED — never APPROVED while a REQUIRED section is missing, and not NOT ASSESSED (the document was read)
- [ ] Output does not suggest the document is implementation-ready
- [ ] "Accept as-is and move on" is not offered, because the missing sections are blocking
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The systems-index prompt offers `Needs Revision` or `In Review` — never `Approved` on this revision verdict — and the linked review report/JSON receipt records the revision verdict, not an approval

---

### Case 3: Partial Path — `standard` tier, numeric rules with no Formulas section

**Fixture:**
- `project.yaml` sets `modes.workflow: standard`
- GDD has Overview, Player Fantasy, `## Detailed Design`, Edge Cases,
  Dependencies, Tuning Knobs and Acceptance Criteria; no Formulas section
- Detailed Design states numeric rules ("drain 2 oxygen per second", "refill
  costs 50 credits") but no formula defines them
- Acceptance Criteria are vague ("feels good" rather than measurable)

**Input:** `$gs-design-review design/gdd/oxygen.md --review lean`

**Domain checks:**
- [ ] Output identifies the missing Formulas section as REQUIRED (not advisory) because numeric rules are present
- [ ] Completeness is reported against the `standard` count ("5/6"), not "7/8"
- [ ] Output flags the vague acceptance criteria as an implementability gap, quoting each one — the main review does this itself, since no `qa-lead` runs in `lean`
- [ ] Verdict is NEEDS REVISION or MAJOR REVISION NEEDED, never APPROVED

---

### Case 4: Edge Case — File not found

**Fixture:**
- The path provided does not exist in the project

**Input:** `$gs-design-review design/gdd/nonexistent.md --review lean`

(`lean`, so Phase 5 runs. In `solo` — what the review mode resolves to when
`project.yaml` sets neither `modes.review_mode` nor `modes.rigor` — Phase 5 never
runs and the last assertion below would test nothing.)

**Domain checks:**
- [ ] Verdict is NOT ASSESSED — not APPROVED, NEEDS REVISION or MAJOR REVISION NEEDED
- [ ] Output names the missing file and which skill produces it
- [ ] Phase 5 runs, and offers neither a `systems-index.md` status update nor a linked review report/JSON receipt — in particular it never offers to mark the system Approved

---

### Case 5: Review mode — specialist coverage in `full`, main review in `lean` / `solo`
**Fixture (all sub-cases):**
- `project.yaml` sets `modes.workflow: full`
- `design/gdd/light-manipulation.md` exists with all 8 sections, including
  formulas and combat stats

**Case 5a — full:** `$gs-design-review design/gdd/light-manipulation.md --review full`

**Domain checks (5a):**
- [ ] The notice is printed before any discipline review begins
- [ ] Specialists cover the applicable disciplines, using explicitly labeled parent work or optional authorized parallel delegation
- [ ] `creative-director` is consulted only after the specialists respond, and output has a "Senior Verdict [creative-director]" section
- [ ] "Specialists consulted:" lists the agents actually consulted, and every finding carries a source tag such as `[game-designer]`
- [ ] Specialist disagreements appear under "Specialist Disagreements"
- [ ] The `### Verdict:` line carries exactly one of this skill's words — APPROVED, NEEDS REVISION or MAJOR REVISION NEEDED — taken from the creative-director's synthesis; never a director-gate word such as READY, CONCERNS, NOT READY, APPROVE or REJECT
- [ ] No director-gate IDs appear ("Gate: CD-…" etc.) — the senior review is a direct consultation, not a gate from `director-gates.md`

**Case 5b — lean via the legacy flag:** `$gs-design-review design/gdd/light-manipulation.md --depth lean`

**Domain checks (5b):**
- [ ] `--depth lean` is treated as `--review lean`, and the skill says once that the flag was renamed
- [ ] No delegation is required; the work is performed by the parent; the review is performed by the parent
- [ ] Phase 5's next-step widgets still run

**Case 5c — solo:** `$gs-design-review design/gdd/light-manipulation.md --review solo`

**Domain checks (5c):**
- [ ] No delegation is required; the work is performed by the parent
- [ ] Only Phases 1–4 run: no Phase 5 next-step prompt, so no systems-index or linked review report/JSON write is offered

---

### Case 6: Review mode from the resolved config — no flag

**Fixture:**
- `project.yaml` sets `modes.workflow: full` and `modes.review_mode: lean`
- `design/gdd/light-manipulation.md` exists with all 8 sections

**Input:** `$gs-design-review design/gdd/light-manipulation.md`

**Domain checks:**
- [ ] The review mode comes from the resolved config block when no flag is given (`review_mode: lean (project.yaml)`)
- [ ] No delegated participant is required, and Phase 5's next-step widgets run — so the run is `lean`, not the `solo` default
- [ ] Variant — the same fixture with `--review solo` on the input: the flag wins over the config, and no Phase 5 widget runs
