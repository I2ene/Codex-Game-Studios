# Evaluation scenarios: gs-balance-check

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-balance-check/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — All balance values within their intended ranges

**Fixture:**
- `assets/data/combat-balance.json` exists with 6 stat values
- `design/registry/entities.yaml` has no entries (the shipped empty stub)
- `design/gdd/combat-system.md` gives an expected range for all 6 stats
- All 6 values fall inside their ranges; no degenerate strategy exists

**Input:** `$gs-balance-check combat`

**Domain checks:**
- [ ] Data Sources Analyzed lists every file read, including the data file and the GDD
- [ ] The empty registry is skipped and the GDD supplies the intended ranges
- [ ] The Outliers Detected table has no rows
- [ ] Health Summary is HEALTHY
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 2: Outlier — Player damage far above its intended range

**Fixture:**
- `assets/data/combat-balance.json` has `player_damage_base: 140`
- `design/gdd/combat-system.md` gives `player_damage_base` an expected range of 90–110
- All other stats are within range

**Input:** `$gs-balance-check combat`

**Domain checks:**
- [ ] `player_damage_base` appears in the Outliers Detected table with Expected Range 90–110 and Actual 140
- [ ] The Recommendations table ranks the fix with a Priority
- [ ] Health Summary is CONCERNS — not HEALTHY, and not CRITICAL ISSUES without a finding of the critical kind
- [ ] On [A], a fix to a GDD-defined value is followed by the `$gs-propagate-design-change` reminder

---

### Case 3: No Design Targets — Data exists but no GDD or registry defines the ranges

**Fixture:**
- `assets/data/economy-balance.yaml` exists with 10 plain stat values (prices and rates, no faucet/sink loop the data alone could show)
- `design/registry/entities.yaml` has no entries
- No GDD in `design/gdd/` covers the economy

**Input:** `$gs-balance-check economy`

**Domain checks:**
- [ ] Skill does not fabricate expected ranges when neither the registry nor a GDD supplies them
- [ ] The affected sections are marked `NOT ASSESSED — NO DATA` rather than shown as empty tables
- [ ] Output names the missing design source (economy GDD in `design/gdd/`, empty `design/registry/entities.yaml`) and `$gs-design-system`
- [ ] Health Summary is NOT ASSESSED — not HEALTHY, and not CONCERNS, since nothing was found wrong

---

### Case 4: Registry First — The registry value overrides a contradicting GDD

**Fixture:**
- `design/registry/entities.yaml` `constants:` lists `player_damage_base` with `value: 100`, `unit: damage`, `source: design/gdd/combat-system.md` (a registry constant carries a value, not a range)
- `design/gdd/combat-system.md` still says `player_damage_base` range 100–130 (stale)
- `assets/data/combat-balance.json` has `player_damage_base: 125`

**Input:** `$gs-balance-check combat`

**Domain checks:**
- [ ] The registry is read before the GDD
- [ ] `player_damage_base` is judged against the registry value (100), not the GDD range (100–130)
- [ ] `player_damage_base: 125` is reported as an outlier
- [ ] Data Sources Analyzed includes `design/registry/entities.yaml`

---

### Case 5: No Argument, Gate Compliance and the Save Path

**Fixture:**
- Combat data, registry and GDD exist; 1 stat is slightly outside its range
- `project.yaml`: `modes.review_mode: full`
- `modes.automation` resolves to `collaborative`

**Input:** `$gs-balance-check` (no argument)

**Domain checks:**
- [ ] With no argument, the skill asks which system to check before reading data
- [ ] No director gate is invoked in any review mode
- [ ] The report is presented before the save option, and the save option names `design/balance/balance-check-[system]-[date].md`
- [ ] Option [B] writes to that path with the date in YYYY-MM-DD form; option [C] writes nothing
- [ ] Both [B] and [C] end with "Re-run `$gs-balance-check` after fixes to verify."

---

### Case 6: Orphan Stat — A data value no GDD or registry defines

**Fixture:**
- `assets/data/combat-balance.json` holds 6 stats plus `legacy_armor_mult: 1.5`
- `design/registry/entities.yaml` has no entries
- `design/gdd/combat-system.md` gives a range for the 6 stats and nothing for `legacy_armor_mult`
- The 6 stats are inside their ranges; no degenerate strategy exists

**Input:** `$gs-balance-check combat`

**Domain checks:**
- [ ] `legacy_armor_mult` is reported as `no stated range — not judged`, apart from any outlier
- [ ] The orphan stat is not skipped silently and not judged against a range inferred from the data
- [ ] Health Summary is NOT ASSESSED, not HEALTHY, naming the unjudged value
