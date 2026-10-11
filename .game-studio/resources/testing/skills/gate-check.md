# Evaluation scenarios: gs-gate-check

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-gate-check/SKILL.md` and its current procedure first.
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

### Case 1: Happy Path — All Concept artifacts present, advancing to Systems Design

**Fixture:**
- `project.yaml` sets `modes.workflow: full` and `modes.review_mode: solo`
- `design/gdd/game-concept.md` exists with real content: core loop, target
  audience, a pillars section, and a Visual Identity Anchor section holding a
  one-line visual rule and 2 supporting visual principles
- No systems index and no art bible yet. `<runtime> artifacts --phase concept`
  reports those catalog steps (`required=true`) as ABSENT, but neither is an item
  in the Concept → Systems Design gate file, and the loaded gate file decides what
  this gate requires
- No `$gs-design-review` record for the concept

**Input:** `$gs-gate-check systems-design`

**Domain checks:**
- [ ] The authorized PASS transition sets `project.stage` to Systems Design and synchronizes `production/stage.txt`; the re-read confirms the target value, not merely that two old values agree.
- [ ] Existence is resolved via `<runtime> artifacts --phase concept`, not by opening files to see what exists
- [ ] The ABSENT systems-index and art-bible catalog steps are not reported as blockers — the catalog's `required=` flag is an observation; the gate file's checklist is what this gate requires
- [ ] `design/gdd/game-concept.md` is spot-read for real content before it is marked `[x]`
- [ ] Output includes a "Required Artifacts: [X/Y present]" section and a "Quality Checks: [X/Y passing]" section
- [ ] The unconfirmed review item is asked about, not assumed PASS
- [ ] Output includes a `### Verdict:` line with one of PASS / NOT ASSESSED / CONCERNS / FAIL
- [ ] Output includes `Chain-of-Verification: [N] questions checked — verdict [unchanged | revised from X to Y]`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] After writing, skill re-reads both files and reports any divergence instead of continuing
- [ ] The next-step recommendation is `$gs-map-systems` (no systems index exists yet), not `$gs-create-architecture`
- [ ] Variant: with `design/gdd/systems-index.md` already written (the catalog orders `$gs-map-systems` in Concept), option [A] is `$gs-design-system` for the first system in its design order instead

---

### Case 2: Failure Path — Missing required artifacts for Concept → Systems Design

**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- `design/gdd/game-concept.md` does NOT exist
- No game pillars document exists
- `design/gdd/` directory is empty or absent

**Input:** `$gs-gate-check systems-design`

**Domain checks:**
- [ ] Verdict is FAIL (not PASS, CONCERNS or NOT ASSESSED) — FAIL is evaluated first in the precedence order
- [ ] Output explicitly names `design/gdd/game-concept.md` as missing
- [ ] Output includes a "Blockers" section with at least 1 item
- [ ] Output recommends `$gs-brainstorm` as the remediation action
- [ ] Skill does NOT write `project.yaml` or `production/stage.txt` when the verdict is FAIL
- [ ] Skill does NOT create `design/gdd/game-concept.md` or any other missing artifact to manufacture a PASS

---

### Case 3: No Argument — Auto-detect current stage

**Fixture:**
- `project.yaml` sets `modes.workflow: full` and has no `project:` block;
  `production/stage.txt` contains `Concept`, so the config block reports
  `project.stage: Concept (production/stage.txt)` from the legacy mirror (with no
  `project.yaml` at all the tier would resolve to `minimal`, whose gate target is
  `design/game-brief.md`, not the concept doc below)
- `design/gdd/game-concept.md` exists with content
- No systems index yet

**Input:** `$gs-gate-check` (no argument)

**Domain checks:**
- [ ] Current stage comes from `production/stage.txt` (via the resolved config block) or project-stage-detect heuristics
- [ ] Skill confirms the detected transition with `host input tool` before running checks — this step is never skipped when no argument is given
- [ ] The full list of six gates is shown only if the user picks `[B] No — pick a different gate`
- [ ] Output header names both phases: "Gate Check: Concept → Systems Design"

---

### Case 4: Edge Case — Manual check items: "I don't know" is not "not yet"
**Fixture:**
- `project.yaml` sets `modes.workflow: full` and `modes.review_mode: solo`
- All required artifacts for Concept → Systems Design are present, and every
  other check passes: `design/gdd/game-concept.md` holds real content with a
  pillars section, a core loop, a target audience, and a Visual Identity Anchor
  with a one-line visual rule and 2 supporting principles
- No review record exists (the "Game concept has been reviewed" check cannot be auto-verified)

**Input:** `$gs-gate-check systems-design`

**Case 4a — the user answers "I don't know":** the item stays unresolved, so the
verdict is NOT ASSESSED, not PASS.

**Case 4b — the user answers "Not yet":** the check has an answer — the concept
was not reviewed — so it ran and failed. Nothing is unknown: the verdict is
CONCERNS or FAIL (FAIL and CONCERNS are evaluated before NOT ASSESSED), with
`$gs-design-review` named as the fix.

**Domain checks:**
- [ ] Items that cannot be auto-verified are marked `[?] MANUAL CHECK NEEDED` rather than assumed PASS
- [ ] Skill uses a question to the user for at least one unverifiable quality item
- [ ] Skill does not mark unverifiable items as PASS by default
- [ ] 4a: a `MANUAL CHECK NEEDED` item the user never resolved yields NOT ASSESSED (it outranks PASS), naming the item and why in the Blockers section
- [ ] 4b: a "not yet" answer is a failed check, never an unknown — the verdict is CONCERNS or FAIL, not NOT ASSESSED and not PASS, and the output names `$gs-design-review` (the one exception is the Production gate's play questions, where "not yet" means nobody has played it — Case 8)
- [ ] Skill does not write the stage on a NOT ASSESSED or FAIL verdict, nor on CONCERNS unless the user explicitly accepts the listed risks (Case 7)

---

### Case 5: Director Gate — panel existence (`review_mode`) vs panel width (`workflow`)
**Fixture (all sub-cases):**
- All required artifacts for Concept → Systems Design are present
- `design/gdd/game-concept.md` exists
- Review mode comes from `modes.review_mode` in `project.yaml` (legacy mirror:
  `production/review-mode.txt`) or an inline `--review` flag

**Case 5a — full panel:** `modes.review_mode: full`, `modes.workflow: full`

**Input:** `$gs-gate-check systems-design`

**Domain checks (5a):**
- [ ] Skill reads the resolved `review_mode` before deciding whether the panel runs
- [ ] All 4 PHASE-GATE directors are consulted (panel width comes from `workflow: full`)
- [ ] Directors cover the applicable disciplines, with optional authorized parallel delegation (independent authorized delegated work may run concurrently; parent work is labeled accurately)
- [ ] A CONCERNS verdict from any one director propagates to at least CONCERNS overall
- [ ] A NOT READY verdict from any director makes the overall verdict at least FAIL — never auto-PASS
- [ ] A director's NOT ASSESSED is never counted as READY: with no NOT READY or CONCERNS alongside it, the overall verdict is NOT ASSESSED, and the Director Panel summary shows it for that director

**Case 5b — solo mode:** `modes.review_mode: solo` (or `--review solo`)

**Domain checks (5b):**
- [ ] No director gates are consulted in solo mode
- [ ] The skip is stated in the output ("Director Panel skipped — Solo mode"), not silent
- [ ] Verdict is based on artifact and quality checks only
- [ ] The narrowed/skipped panel alone does not make the verdict NOT ASSESSED

**Case 5c — width follows `workflow`, not `review_mode`:** `modes.review_mode: full`, `modes.workflow: standard`

**Domain checks (5c):**
- [ ] Exactly TD-PHASE-GATE and PR-PHASE-GATE are consulted — `review_mode: full` does not widen the panel
- [ ] Output names the perspectives that did not run and how to get them: `modes.workflow: full`, the source the config block shows for `workflow`
- [ ] Output never suggests `--review full` to widen the panel — `--review` decides whether the panel runs, not its width
- [ ] The deliberately narrow panel does not by itself produce NOT ASSESSED

**Case 5d — lean mode, width from rigor:** the panel runs in `lean` (phase gates
are what lean mode keeps); its width still follows `workflow`.

- (i) `project.yaml` sets only `modes.rigor: standard` → the block resolves
  `review_mode: lean` and `workflow: standard`, both from `rigor:standard`
- (ii) `project.yaml` sets `modes.rigor: minimal` and `modes.review_mode: lean`
  (explicit — `rigor: minimal` alone would resolve `solo` and skip the panel), plus
  a filled `design/game-brief.md` → `workflow: minimal`

**Domain checks (5d):**
- [ ] (i): exactly TD-PHASE-GATE and PR-PHASE-GATE are consulted, and the output reads "Panel: 2 of 4" and points to raising `modes.rigor` to `full` (that is where `workflow` came from)
- [ ] (ii): only PR-PHASE-GATE is consulted, and the output reads "Panel: 1 of 4", naming the three perspectives that did not run
- [ ] In both, lean mode does not skip the panel, and the narrow panel alone does not produce NOT ASSESSED

---

### Case 6: Director context — a later phase's artifact is "not expected", never "none"

**Fixture:**
- `project.yaml` sets only `modes.rigor: standard` → `workflow: standard`,
  `review_mode: lean`, so the panel is `technical-director` + `producer`
- The engine is configured; `design/gdd/systems-index.md` enumerates 3 MVP
  systems, each with a GDD holding the 5 standard sections, each reviewed, and a
  `$gs-review-all-gdds` report with verdict PASS; the systems index maps
  dependencies both ways and defines the MVP tier
- No `docs/architecture/` at all (no architecture document, no ADRs), no
  `production/sprints/`, no stories

**Input:** `$gs-gate-check technical-setup`

**Domain checks:**
- [ ] Each director receives the target gate's required and recommended artifacts at the resolved tier, not only the phase name
- [ ] No director context passes "none" for an artifact the target gate does not require at this tier — it reads "not expected before [phase]" (or "not required at `workflow: [tier]`")
- [ ] With every director READY and every check passing, the verdict is PASS — the absent architecture document and sprint plan do not turn it into CONCERNS
- [ ] Variant (ii): an artifact the target gate requires and that does not exist is passed as "none", never "not expected", and the verdict is not PASS

---

### Case 7: CONCERNS override — the user accepts the risks; a FAIL is never overridden

**Fixture:**
- `project.yaml` sets `modes.workflow: standard` and `modes.review_mode: solo`
- `design/gdd/game-concept.md` holds a core loop and a target audience, and the
  user confirms it was reviewed; it has no pillars section and no Visual Identity
  Anchor — both recommended at `standard`, so absent → CONCERNS

**Input:** `$gs-gate-check systems-design`, then, after the CONCERNS verdict, the
user says "advance anyway"

**Domain checks:**
- [ ] On CONCERNS the stage is written only after the user explicitly accepts the listed risks, never by default
- [ ] The report records the accepted risks under `### Accepted Risks`
- [ ] Variant: on FAIL the stage is never written, whatever the user asks; the same holds for NOT ASSESSED

---

### Case 8: `$gs-gate-check production` at `workflow: minimal` — the slice items drop

**Fixture:**
- `project.yaml` sets only `modes.rigor: minimal` → `workflow: minimal`,
  `qa.level: minimal`, `review_mode: solo`
- `design/game-brief.md` is filled, with a Build order of three MVP features
- Three story files under `production/epics/core/`, one per feature
- No `prototypes/`, no Vertical Slice, no sprint plan, no playtest report

**Input:** `$gs-gate-check production`; the user answers yes to both current-build
questions (the core loop is fun; one start → challenge → resolution cycle runs
end to end)

**Domain checks:**
- [ ] No Vertical Slice item is listed as missing or turned into CONCERNS at `minimal`
- [ ] The two current-build checks are asked and carry the verdict: both yes → PASS; a "no" → FAIL; "not yet" on the fun question → NOT ASSESSED
- [ ] The floor is read from `<runtime> artifacts --path minimal`, not by opening files to see what exists

---

### Case 9: A gate its tier file marks "not applicable"

**Fixture:** `project.yaml` sets `modes.rigor: minimal` and `modes.review_mode:
lean` (so a panel would otherwise run); a filled `design/game-brief.md`; no GDDs

**Input:** `$gs-gate-check technical-setup`

**Domain checks:**
- [ ] Verdict is PASS, not NOT ASSESSED — the not-applicable gate is the named exception to "a gate with no required artifacts left may not PASS"
- [ ] The gate file's note is printed, and no director is consulted
- [ ] Absent GDDs are not reported as blockers
