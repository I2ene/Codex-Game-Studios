# Evaluation scenarios: gs-team-live-ops

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-team-live-ops/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — All 7 phases complete, season plan produced

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`
- `design/live-ops/economy-rules.md` exists with current economy configuration
- `design/live-ops/ethics-policy.md` exists with the project ethics policy
- Game concept document exists at its standard path
- No existing season documents for the new season name being planned

**Input:** `$gs-team-live-ops "Season 2: The Frozen Wastes"`

**Domain checks:**
- [ ] Active-set line naming `team.size: studio` appears before the first agent is consulted
- [ ] All 7 phases execute in order; Phase 3 and 4 are covered as independent reviews, optionally through authorized parallel delegation
- [ ] Phase 7 consolidated summary includes all six sections (season brief, narrative framing, economy design, analytics plan, content inventory, communication calendar)
- [ ] Ethics review section in Phase 7 explicitly references `design/live-ops/ethics-policy.md`
- [ ] Three output documents written to `design/live-ops/seasons/` with the `S[N]_[name].md`, `S[N]_[name]_analytics.md`, `S[N]_[name]_comms.md` naming convention
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict: COMPLETE appears in final output, only after the user approves the season plan
- [ ] Next steps reference `$gs-design-review`, `$gs-sprint-plan`, and `$gs-team-release`

---

### Case 2: Ethics Violation Found — Reward element violates ethics policy

**Fixture:**
- All standard live-ops fixtures present (economy-rules.md, ethics-policy.md)
- `design/live-ops/ethics-policy.md` contains the rule "No randomized premium rewards without published drop rates and a pity timer"
- economy-designer (Phase 3) proposes a "Mystery Chest" mechanic with randomized premium rewards, unpublished drop rates and no pity timer

**Input:** `$gs-team-live-ops "Season 3: Shadow Tournament"`

**Domain checks:**
- [ ] Phase 7 ethics review section explicitly names the violating element and the policy rule it breaks
- [ ] Skill does not auto-approve the season plan when an ethics violation is present
- [ ] host input tool is used to surface the violation and offer resolution options (revise economy design, override with documented rationale, cancel)
- [ ] Output documents are NOT written while the violation is unresolved
- [ ] If user chooses to revise: skill re-consults economy-designer to produce a corrected design before returning to Phase 7 review
- [ ] Verdict: COMPLETE is only issued after the ethics flag is cleared; Cancel ends with Verdict: BLOCKED

---

### Case 3: No Argument — Usage guidance shown

**Fixture:**
- Any project state

**Input:** `$gs-team-live-ops` (no argument)

**Domain checks:**
- [ ] Skill does NOT guess a season name or fabricate a scope
- [ ] Usage message shows the full argument-hint: `$gs-team-live-ops [season name or event description] [--review full|lean|solo]`
- [ ] No Agent calls are issued before the argument check fails
- [ ] No files are read or written

---

### Case 4: Parallel Phase Validation — Phases 3 and 4 run simultaneously

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- All standard live-ops fixtures present
- Phase 1 (season brief) and Phase 2 (narrative framing) already approved
- Phase 3 (economy-designer) and Phase 4 (analytics-engineer) inputs are independent of each other

**Input:** `$gs-team-live-ops "Season 1: The First Thaw"` (observed at Phase 3/4 transition)

**Domain checks:**
- [ ] Both Agent calls for Phase 3 and Phase 4 are issued before either result is awaited — they are not sequential
- [ ] Analytics-engineer prompt does NOT include economy-designer output as a required input (the inputs are independent)
- [ ] If economy-designer blocks but analytics-engineer succeeds, analytics output is preserved and the block is surfaced via host input tool
- [ ] Phase 5 does not begin until BOTH Phase 3 and Phase 4 results are collected
- [ ] Skill documentation explicitly states "Phases 3 and 4 can run simultaneously"

---

### Case 5: Missing Ethics Policy — `design/live-ops/ethics-policy.md` does not exist

**Fixture:**
- `design/live-ops/economy-rules.md` exists
- `design/live-ops/ethics-policy.md` does NOT exist
- All other fixtures are present

**Input:** `$gs-team-live-ops "Season 4: Desert Heat"`

**Domain checks:**
- [ ] Skill does NOT error out when the ethics policy file is missing
- [ ] Skill does NOT fabricate ethics policy rules in the absence of the file
- [ ] Phase 7 summary explicitly notes that ethics review was skipped and why
- [ ] Verdict: COMPLETE is still reachable despite the missing file
- [ ] Gap flag appears in the season design output document (not just in conversation)
- [ ] Next steps recommend creating `design/live-ops/ethics-policy.md`
