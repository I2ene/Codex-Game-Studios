# Evaluation scenarios: gs-hotfix

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-hotfix/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — S1 crash fixed with record, branch, approvals and backport

**Fixture:**
- Git repository; the live build is the release tag `v1.2.0` on `main`, and no
  `release/*` branch exists (the trunk default)
- Bug in `src/gameplay/arena.gd` (crash on boss arena entry);
  `production/qa/bugs/BUG-0031.md` exists with `**Status**: Open`
- All three sign-offs return APPROVE; `qa-lead` picks a smoke check, which returns PASS

**Input:** `$gs-hotfix BUG-0031`

**Domain checks:**
- [ ] The hotfix record is written before the branch is created
- [ ] The branch starts from the release tag `v1.2.0`, not from the head of `main`
- [ ] The branch is created only after the user picks `[A]`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The three sign-off agents cover the applicable disciplines, with optional authorized parallel delegation
- [ ] No merge happens before the Phase 6 deploy question is answered
- [ ] No `release/*` branch is created or merged; the patch release is tagged
- [ ] The summary's Backport line states presence on `main`
- [ ] `BUG-0031.md` Status becomes `Fixed — Pending Verification`

---

### Case 2: Sign-off REJECT — Deployment blocked

**Fixture:**
- Fix implemented for an S1 bug
- `qa-tester` returns REJECT: "Player health clamping regression detected";
  `lead-programmer` and `producer` return APPROVE

**Input:** `$gs-hotfix`

**Domain checks:**
- [ ] The qa-tester's REJECT and its regression are shown to the user
- [ ] Skill does not proceed to deployment with a REJECT outstanding
- [ ] The deploy `host input tool` is not issued while the REJECT stands
- [ ] No merge is performed

---

### Case 3: Release Branch — Deploy approval holds even in autonomous mode

**Fixture:**
- `project.yaml` sets `modes.automation: autonomous`
- The live release `v1.3.0` has a `release/1.3` branch, cut to stabilise it for
  certification; the hotfix branch was started from `release/1.3`
- An S2 fix has all three APPROVE sign-offs and a smoke check PASS

**Input:** `$gs-hotfix`

**Domain checks:**
- [ ] The deploy question is asked even though `modes.automation` is `autonomous`
- [ ] The question names `release/1.3`, because this release has one
- [ ] All three options are offered
- [ ] With `[B]`, `release/1.3` is not merged, no tag is created and nothing is deployed
- [ ] With `[B]`, `main` receives the fix
- [ ] With `[B]`, the summary does not say "Deployed" and names no tag

---

### Case 4: Not an Emergency — a cosmetic S4 redirected before any work

**Fixture:**
- User reports a typo on the credits screen

**Input:** `$gs-hotfix typo in the credits screen`

**Domain checks:**
- [ ] Severity is confirmed via `host input tool` with S1 / S2 / S3-or-lower options
- [ ] Verdict is REDIRECTED
- [ ] No hotfix record is written and no branch is created
- [ ] No code is modified and no agents are consulted

---

### Case 5: Director Gate Check — Producer sign-off, and NOT ASSESSED QA is not a pass

**Fixture:**
- `project.yaml`: `modes.rigor: standard` (so a project with no game tests gets NOT ASSESSED, not WAIVED)
- S1 fix implemented; all three sign-offs APPROVE
- `qa-lead` picks a smoke check; `$gs-smoke-check` returns `NOT ASSESSED — no game tests found`

**Input:** `$gs-hotfix`

**Domain checks:**
- [ ] No gate IDs (CD-*, TD-*, AD-*, PR-*) appear in output
- [ ] NOT ASSESSED does not advance to Phase 6 as if the QA gate passed
- [ ] Deployment goes ahead only with the three APPROVE sign-offs plus an explicit producer decision to deploy unverified
- [ ] That decision is logged in the hotfix record
- [ ] The summary records the QA gate as NOT ASSESSED with the reason and whose decision it was

---

### Case 6: Smoke Check FAIL — back to Phase 4, and a CONCERNS sign-off still blocks

**Fixture:**
- S1 fix implemented; all three sign-offs APPROVE; `qa-lead` picks a smoke check
- `$gs-smoke-check` returns FAIL: "Player health clamping regression detected"
- On the revised fix, `lead-programmer` returns CONCERNS ("the clamp now runs on
  the save path too"); `qa-tester` and `producer` return APPROVE

**Input:** `$gs-hotfix`

**Domain checks:**
- [ ] A smoke-check FAIL never reaches the deploy question
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] All three sign-offs and the QA step are re-run for the revised fix
- [ ] CONCERNS from a sign-off blocks deployment until resolved; it is not treated as an approval
- [ ] No merge, tag or deploy occurs while the FAIL or the CONCERNS stands
