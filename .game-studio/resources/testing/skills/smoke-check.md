# Evaluation scenarios: gs-smoke-check

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-smoke-check/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Automated tests pass, manual items confirmed, PASS

**Fixture:**
- `project.yaml` has `engine.name: Godot` and `commands.test` set to the gdUnit4 command
- `addons/gdUnit4/bin/GdUnitCmdTool.gd` exists; game tests exist under
  `tests/unit/` and `tests/integration/`
- `production/qa/qa-plan-sprint-005.md` exists
- The runner exits 0 with 12 tests, 12 passing
- The developer says the build was launched this session and selects no FAILED item in Batch 1, Batch 2 or Batch 3
- Every sprint story is COVERED or EXPECTED (no MISSING, no UNKNOWN)

**Input:** `$gs-smoke-check`

**Domain checks:**
- [ ] Automated test runner is invoked via Bash, after the Godot import
- [ ] `host input tool` is used for manual smoke check batches
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Report is written to `production/qa/smoke-[date].md`
- [ ] Verdict is PASS

---

### Case 2: Failure Path — Automated test fails, blocking FAIL

**Fixture:**
- As Case 1, but `project.yaml` sets `modes.rigor: standard` (so `qa.level`
  resolves to `standard`) and leaves `testing.strict` unset
- The runner exits 100: 10 tests run, 8 passing, 2 failing —
  `test_health_clamp_at_zero`, `test_damage_calculation_negative`

**Input:** `$gs-smoke-check`

**Domain checks:**
- [ ] Failing test names are listed in the report
- [ ] Verdict is FAIL
- [ ] The blocking message directs the developer to fix failures before QA hand-off
- [ ] `$gs-smoke-check` re-run is suggested after fixing

---

### Case 3: Manual Confirmation — MISSING coverage, PASS WITH WARNINGS

**Fixture:**
- As Case 1: runner exits 0 with 8/8 passing
- One Logic story has no matching test file (MISSING coverage); no UNKNOWN rows
- The developer selects no FAILED item in Batch 1, Batch 2 or Batch 3

**Input:** `$gs-smoke-check`

**Domain checks:**
- [ ] `host input tool` is used for manual smoke check batches (not inline text prompts)
- [ ] MISSING test coverage entry appears in the report
- [ ] Verdict is PASS WITH WARNINGS (not PASS, not FAIL)
- [ ] Advisory note says the MISSING entry must be resolved before `$gs-story-done`
- [ ] Report file is written to `production/qa/smoke-[date].md`

---

### Case 4: Scaffold Without Game Tests — NOT ASSESSED, then stop

**Fixture:**
- `project.yaml` sets `modes.rigor: standard` (so `qa.level` resolves to `standard`)
- Engine is Godot; `tests/unit/` and `tests/integration/` exist but hold only
  the `.gdignore_placeholder` files `$gs-test-setup` creates
- No `tests/smoke/` directory

**Input:** `$gs-smoke-check`

**Domain checks:**
- [ ] The presence of `tests/` and its subdirectories is not treated as tests existing
- [ ] Verdict is NOT ASSESSED — the skill does not stop without a verdict
- [ ] `$gs-test-setup` is suggested as the remediation step
- [ ] No further phases run and no report file is written

---

### Case 4b: No Game Tests at `qa.level: minimal` — WAIVED, the build carries the verdict

**Fixture:**
- No `modes.rigor` set (the default, `minimal`, so `qa.level` resolves to `minimal`)
- Engine is Godot; no game test files under `tests/unit/`, `tests/integration/` or `tests/smoke/`
- `commands.smoke` is `godot --headless --quit-after 5`; it exits 0 with no `SCRIPT ERROR` line
- The user says the build was launched this session and confirms every Batch 1, Batch 2 and Batch 3 check

**Input:** `$gs-smoke-check`

**Domain checks:**
- [ ] The missing tests are WAIVED, not NOT ASSESSED, because `qa.level` is `minimal`
- [ ] The skipped test run and Phase 3 are announced, not silent
- [ ] The build check runs `commands.smoke` and its result is in the report
- [ ] Batch 1 and Batch 2 still run — PASS is never given without them
- [ ] Verdict is PASS and the report's Automated Tests row reads WAIVED
- [ ] A Batch 1 or Batch 2 check that could not be executed (no build) makes the verdict NOT ASSESSED, as at any level
- [ ] Variant — the user answers that the build was not launched this session: Batches 2 and 3 are not asked (the skip is said), the Batch 1 checks read `NOT RUN — build not launched this session`, and the verdict is NOT ASSESSED — never PASS from an empty failure list
- [ ] Variant — `commands.smoke` prints `SCRIPT ERROR` (Godot's boot check exits 0 on it): the build check is FAIL and so is the verdict

---

### Case 5: Director Gate Check — No gate; smoke-check is a QA pre-check utility

**Fixture:**
- Valid test setup, automated tests pass, manual smoke checks confirmed

**Input:** `$gs-smoke-check`

**Domain checks:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is PASS, PASS WITH WARNINGS, NOT ASSESSED, or FAIL — no gate verdict involved

---

### Case 6: gdUnit4 Lookalikes — exit 0 over zero tests, and exit 101

**Fixture:**
- As Case 1, with every story COVERED or EXPECTED and nothing selected in
  Batch 1, Batch 2 or Batch 3
- Run A: the suites under `tests/unit/` declare no test functions; the runner
  prints `No test cases found` and exits 0
- Run B: the runner exits 101 — 12 tests, 12 passing, 2 orphan nodes leaked

**Input:** `$gs-smoke-check`

**Domain checks:**
- [ ] Run A's verdict is NOT ASSESSED — not PASS
- [ ] Run B's Status line is PASS WITH WARNINGS with the orphan count
- [ ] Run B's verdict is PASS WITH WARNINGS — not PASS, and not FAIL

---

### Case 7: Timeout — the suite never completed, FAIL

**Fixture:**
- As Case 2 (`qa.level: standard`, `testing.strict` unset)
- The runner hangs; `timeout 900` ends it with exit 124 and no summary printed

**Input:** `$gs-smoke-check`

**Domain checks:**
- [ ] A timeout is FAIL — not NOT ASSESSED and not NOT RUN
- [ ] The report names the timeout as the reason
- [ ] The blocking message is delivered

---

### Case 8: Batch 3 Skipped — NOT ASSESSED, not PASS

**Fixture:**
- As Case 1: runner exits 0 with 12/12 passing, no MISSING or UNKNOWN rows
- In Batch 3 the developer selects only "Performance not checked this session"

**Input:** `$gs-smoke-check`

**Domain checks:**
- [ ] Verdict is NOT ASSESSED — not PASS, not FAIL
- [ ] The unchecked performance item is named in the report

---

### Case 9: Unity — Play Mode is a second run

**Fixture:**
- `engine.name: Unity`; `com.unity.test-framework` is in `Packages/manifest.json`
- `commands.test` is the Edit Mode command `$gs-setup-engine` writes
- `Assets/Tests/EditMode/` and `Assets/Tests/PlayMode/` both hold test files
- Edit Mode exits 0 with 8/8 passing; Play Mode exits 2 with 1 of 3 failing

**Input:** `$gs-smoke-check`

**Domain checks:**
- [ ] Play Mode is run as a second run with its own results file
- [ ] Each platform is reported on its own line
- [ ] The Play Mode failure makes the verdict FAIL — the Edit Mode pass does not cover it
