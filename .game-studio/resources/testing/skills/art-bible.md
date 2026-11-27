# Evaluation scenarios: gs-art-bible

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-art-bible/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Full mode, full workflow, all nine sections, AD-ART-BIBLE approves

**Fixture:**
- No `design/art/art-bible.md`
- `design/gdd/game-concept.md` exists with pillars and a Visual Identity Anchor section
- `project.yaml` has `modes.review_mode: full` and `modes.workflow: full`
- AD-ART-BIBLE returns APPROVE

**Input:** `$gs-art-bible`

**Domain checks:**
- [ ] The Scope tab marks "Full bible — all 9 sections" as Recommended and says why
- [ ] Every section applies its owning expertise and records actual contributors: sections 1–4 and 9 may use an authorized art-director helper or labeled parent fallback; sections 5–8 stay in conversation.
- [ ] In collaborative mode with delegation unavailable, the parent drafts the required section bodies and records their specialist basis; Phase 2, the art-bible effects-map note and the Collaborative Protocol all permit that work, with each section's approval and write, without requiring calls or inventing independent review.
- [ ] Section 1 is approved and written before drafting Sections 2–4; an already complete locked foundation is reused without rewriting.
- [ ] Sections 2–4 form one coherent art-director draft, applied by the parent or requested in a single authorized delegated brief; they are presented, approved and written one section at a time.
- [ ] Sections 5–6 share the completed sections 1–4, keep characters and environments legible against each other, and retain separate approval and write steps.
- [ ] For sections 1–4 and 9 only, any helper brief requires user authorization, actual tools and capacity; sections 5–8 never launch helpers. No calls are required on the parent path.
- [ ] Section 7 covers art direction and UX, Section 8 art direction and technical constraints, Section 9 reference direction, and the full-mode AD-ART-BIBLE assessment remains required in conversation through parent expertise; authorship and review sources are accurate.
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] AD-ART-BIBLE runs only after all nine sections are written, applying the art-director gate definition through a labelled parent assessment.
- [ ] AD-ART-BIBLE is passed all four context items: the art bible path, the pillars and core fantasy, the platform and performance constraints, and the visual identity anchor
- [ ] The APPROVE verdict is recorded in the art bible's status header line
- [ ] The closing options include `$gs-create-architecture` and "Stop here"
- [ ] Sections 1–4 and 9 retain art-director expertise (parent fallback when necessary); sections 5–8 use the in-conversation lenses, with separate art/UX or art/technical blocks for 7/8 and no extra helpers.
- [ ] AD-ART-BIBLE runs in conversation against the written artifact and all four inputs; print the actual verdict first. One section's approval/write is not batched with another's.

---

### Case 2: AD-ART-BIBLE Returns CONCERNS or NOT ASSESSED

**Fixture:**
- All nine sections have been written to `design/art/art-bible.md`
- `project.yaml` has `modes.review_mode: full` and `modes.workflow: full`
- Scenario (a): AD-ART-BIBLE returns CONCERNS: "Color System does not match the Mood & Atmosphere targets for combat"
- Scenario (b): AD-ART-BIBLE returns NOT ASSESSED — no platform or performance constraints were available to check the asset standards against

**Input:** `$gs-art-bible` (reaching Phase 5)

**Domain checks:**
- [ ] (a) CONCERNS are shown to the user with the three standard options, not auto-accepted
- [ ] (a) "Accept and proceed" records `CONCERNS (accepted) [date]` in the status header
- [ ] (a) The flagged section is re-drafted with its owning lens (an authorized art-director helper is optional for sections 1–4/9; sections 5–8 stay in conversation), and approved before it is written; the header records `REVISED [date]`.
- [ ] (b) NOT ASSESSED is recorded as such, naming the missing input — not as an approval
- [ ] Phase 6 next steps are not presented before the verdict is recorded
- [ ] Redraft flagged sections using their owning lens. Missing inputs stay NOT ASSESSED; accepted concerns and revised status remain distinct.

---

### Case 3: Lean Mode, Standard Workflow — Core sections only, gate skipped

**Fixture:**
- No existing art bible
- `design/gdd/game-concept.md` exists
- `project.yaml` has `modes.review_mode: lean` and `modes.workflow: standard`
- User picks the Recommended scope

**Input:** `$gs-art-bible`

**Domain checks:**
- [ ] The Scope recommendation is sections 1–4, with the `standard` explanation
- [ ] Only sections 1–4 are authored
- [ ] The close names sections 5–9 as not authored and says why, so the four-section bible does not read as complete
- [ ] AD-ART-BIBLE is not consulted in lean mode, and the skip note reads "AD-ART-BIBLE skipped — Lean mode."
- [ ] Per-section user approval is still required before each write

---

### Case 4: Existing Art Bible — Retrofit of incomplete sections only

**Fixture:**
- `design/art/art-bible.md` exists with sections 1–4 fully written
- Section 5's heading is followed by `[To be designed]`
- Sections 6–9 have headings with nothing between them
- `design/gdd/game-concept.md` exists; `project.yaml` has `modes.workflow: full` and `modes.review_mode: full`
- At the Scope tab the user picks `Resume — fill in missing sections`
- AD-ART-BIBLE returns APPROVE

**Input:** `$gs-art-bible`

**Domain checks:**
- [ ] Section status comes from the two Greps, not from a full read of the file
- [ ] The retrofit message states the complete and incomplete counts and that existing content will not be touched
- [ ] Only Empty and Placeholder sections are authored; Complete sections are left unchanged
- [ ] The status table rows use the section names the skill authors (e.g., `Mood & Atmosphere`, `Shape Language`, `Reference Direction`)
- [ ] AD-ART-BIBLE runs after the retrofitted sections are written, as it does after a fresh run

---

### Case 5: Solo Mode and Missing Concept

**Fixture:**
- Scenario (a): no `design/gdd/game-concept.md`; `design/game-brief.md` exists; `project.yaml` has `modes.review_mode: solo` and `modes.workflow: minimal`
- Scenario (b): neither `design/gdd/game-concept.md` nor `design/game-brief.md` exists

**Input:** `$gs-art-bible`

**Domain checks:**
- [ ] (a) The game brief is used when the game concept is absent
- [ ] (a) The skill states no art bible is required at `minimal` before asking the Scope question
- [ ] (a) Art-director expertise still covers the chosen sections in solo mode, through parent work or an authorized delegate; skipping the final gate does not skip authoring expertise.
- [ ] (a) AD-ART-BIBLE is not consulted; the skip note reads "AD-ART-BIBLE skipped — Solo mode.", and the header records the SKIPPED sign-off line with the mode and date
- [ ] (a) The Phase 6 option pool is the `workflow: minimal` set, not the `standard`/`full` GDD pool
- [ ] (b) The skill stops with the `$gs-brainstorm` message and writes nothing
- [ ] Read Look and references from a new brief, or Label/Art & audio direction from an older one; minimal scope and missing-concept stops remain unchanged.

## Applicable domain checks

- [ ] Surface conflicting discipline recommendations to the user before choosing a direction; do not silently select a winner.
