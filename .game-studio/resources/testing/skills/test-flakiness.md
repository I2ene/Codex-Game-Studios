# Evaluation scenarios: gs-test-flakiness

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-test-flakiness/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — High flakiness from JUnit history, quarantined on approval

**Fixture:**
- `project.yaml`: `engine.name: godot`; `modes.automation` unset (collaborative)
- `test-results/` holds 6 gdUnit4 JUnit XML files from 6 runs of the same commit
- `test_loot_drop_rolls_rare_item` fails in 2 of the 6 runs (33%); the other 40 tests pass in all 6
- `tests/unit/loot/loot_drop_test.gd` calls `randf()` with no seed
- `tests/regression-suite.md` has a Quarantined Tests table with 1 existing entry

**Input:** `$gs-test-flakiness scan`

**Domain checks:**
- [ ] JUnit XML results in `test-results/` are parsed per test across all 6 runs
- [ ] The flaky test is named with its fail rate, Confidence confirmed, and classified High → quarantine
- [ ] The skip mechanism named is gdUnit4's `_do_skip` / `_skip_reason` parameter pair, not an invented flag
- [ ] The likely cause is Random seed, with the explicit-seed fix direction
- [ ] The two writes are asked about separately, each before it happens
- [ ] The quarantine entry is appended and the existing entry is not removed
- [ ] Verdict is COMPLETE

---

### Case 2: Moderate Flakiness — Fix directly, do not quarantine

**Fixture:**
- `project.yaml`: `engine.name: godot`
- `test-results/` holds 20 JUnit XML files from 20 runs of the same commit
- `test_physics_bounce_height_matches_spec` fails in 3 of 20 runs (15%)
- The test asserts `bounce_height == 0.5`

**Input:** `$gs-test-flakiness scan`

**Domain checks:**
- [ ] A 15% fail rate is classified Moderate
- [ ] The recommendation is to fix directly, not to quarantine
- [ ] The cause is Floating point and the fix names an epsilon comparison such as `is_equal_approx`

---

### Case 3: No Result Data — List options and stop

**Fixture:**
- No `test-results/` directory, no `.github/` directory, no `Saved/Logs/`
- No log path is given

**Input:** `$gs-test-flakiness scan`

**Domain checks:**
- [ ] Output states no CI log data was found
- [ ] All three options are listed, including `$gs-test-flakiness registry`
- [ ] Skill stops to ask instead of reporting a clean result
- [ ] No files are written

---

### Case 4: Too Few Runs — Suspected, not confirmed

**Fixture:**
- `project.yaml`: `engine.name: godot`
- `test-results/` holds only 2 JUnit XML files, from 2 runs of the same commit
- `test_save_roundtrip_preserves_inventory` passes in one run and fails in the other

**Input:** `$gs-test-flakiness scan`

**Domain checks:**
- [ ] The finding is labelled suspected, not confirmed, in the summary table's Confidence column
- [ ] The 50% fail rate does not trigger quarantine — no skip is recommended, and any regression-suite note marks the test suspected
- [ ] Skill asks whether more run data is available
- [ ] Data Limitations states that fewer than 5 runs were analysed

---

### Case 5: Registry Mode in Full Review Mode — Guidance for known quarantined tests, no gates

**Fixture:**
- `project.yaml`: `modes.review_mode: full`
- `tests/regression-suite.md` Quarantined Tests table lists `test_ai_path_recalc_avoids_blocked_tile` (reason: timing) and `test_scene_load_spawns_player` (reason: scene not ready)

**Input:** `$gs-test-flakiness registry`

**Domain checks:**
- [ ] The quarantine section of `tests/regression-suite.md` is the input
- [ ] Each quarantined test gets a fix direction matching its cause
- [ ] No director gate is invoked in any review mode
- [ ] No quarantine entry is removed and no test file is deleted
