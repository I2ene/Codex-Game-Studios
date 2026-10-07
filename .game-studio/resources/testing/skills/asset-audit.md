# Evaluation scenarios: gs-asset-audit

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-asset-audit/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — All assets follow naming conventions

**Fixture:**
- `project.yaml`: `engine.name: godot`, so the asset root is `assets/` and the code root `src/`
- `design/art/art-bible.md` Asset Standards: textures PNG, power-of-two, ≤2MB; SFX OGG, 44.1 kHz, ≤500KB (no duration budget)
- `assets/art/characters/` contains: `char_grunt_idle_512.png`, `char_sniper_run_512.png` (512×512 PNG, 300KB each)
- `assets/audio/sfx/` contains: `sfx_player_jump_01.ogg`, `sfx_item_pickup_01.ogg` (OGG, 44.1 kHz, 80KB and under 1 s each)
- `src/` references all four files

**Input:** `$gs-asset-audit`

**Domain checks:**
- [ ] Audit covers both art and audio asset directories
- [ ] Each file is checked against the Phase 3 naming pattern and the size budget from the art bible
- [ ] Summary reports `Total assets scanned: 4` with zero naming, size, format, orphaned and missing counts, and `Sections not assessed: none`
- [ ] Verdict is COMPLIANT
- [ ] No files are written

---

### Case 2: Non-Compliant — Textures exceed size budget

**Fixture:**
- `project.yaml`: `engine.name: godot`
- `design/art/art-bible.md` asset standards: textures PNG, power-of-two, ≤2MB
- `assets/art/environment/` contains 5 correctly named power-of-two PNG textures, all referenced from code
- 3 of them are 4096×4096 at 4MB each; 2 are 1024×1024 at 1MB each

**Input:** `$gs-asset-audit`

**Domain checks:**
- [ ] All 3 oversized files appear in the Size Violations table with Budget (2MB), Actual (4MB) and Overage
- [ ] Sizes come from a measuring command (`stat`/`du`), not an estimate
- [ ] Verdict is NON-COMPLIANT when any file exceeds its budget
- [ ] Each oversized file has a recommendation that names its target resolution or compression, not only "reduce size"
- [ ] The 2 within-budget files are counted in `Total assets scanned` but are not listed as violations

---

### Case 3: Format Issue — Music in wrong format

**Fixture:**
- `project.yaml`: `engine.name: godot`
- `design/art/art-bible.md` asset standards: SFX OGG ≤500KB; music OGG or MP3 ≤8MB
- `assets/audio/music/music_menu_theme_01.wav` exists (WAV format, 6MB), referenced from code
- `assets/audio/sfx/sfx_player_footstep_01.ogg` exists (OGG format, 40KB), referenced from code

**Input:** `$gs-asset-audit`

**Domain checks:**
- [ ] `music_menu_theme_01.wav` appears in the Format Violations table with Expected Format OGG/MP3 and Actual Format WAV
- [ ] The recommendation for the WAV file names OGG or MP3 as its target format
- [ ] Verdict is WARNINGS (not NON-COMPLIANT) for a format issue alone
- [ ] `sfx_player_footstep_01.ogg` is not listed in any violation table
- [ ] Skill does not modify or convert any asset files

---

### Case 4: Missing Asset — Referenced by code but absent from assets/

**Fixture:**
- `project.yaml`: `engine.name: godot`; `design/art/art-bible.md` sets texture budgets
- `assets/art/characters/` holds 3 other correctly named textures, within budget and referenced from code
- `src/enemies/boss.gd` loads `res://assets/art/characters/boss/char_boss_idle_512.png`
- `assets/art/characters/boss/` is empty — the file does not exist
- `design/gdd/enemies.md` also names `char_boss_roar_512.png`, which no code references

**Input:** `$gs-asset-audit`

**Domain checks:**
- [ ] The Missing Assets table lists `src/enemies/boss.gd` as the reference location and `assets/art/characters/boss/char_boss_idle_512.png` as the expected path
- [ ] The GDD-only asset name is not reported as missing
- [ ] Verdict is NON-COMPLIANT when a code-referenced asset is missing
- [ ] Next steps name `$gs-content-audit` for GDD-vs-asset completeness
- [ ] Skill does not create or add placeholder assets

---

### Case 5: No Data — No assets and no asset standards

**Fixture:**
- `project.yaml`: `engine.name: godot`, `modes.review_mode: full`
- `assets/` does not exist
- `design/art/art-bible.md` does not exist; no design doc defines asset standards

**Input:** `$gs-asset-audit`

**Domain checks:**
- [ ] Inputs are listed as FOUND / ABSENT before any report section
- [ ] Verdict is `NOT ASSESSED — NO DATA`, not COMPLIANT
- [ ] The report names the missing inputs (`assets/`, asset standards) and the skill that produces the standards (`$gs-art-bible`)
- [ ] No director gate is invoked, even with review mode `full`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 6: Zero Assets — Standards exist, nothing to audit

**Fixture:**
- `project.yaml`: `engine.name: godot`
- `design/art/art-bible.md` asset standards: textures PNG ≤2MB; SFX OGG ≤500KB
- `assets/` does not exist; `src/` holds gameplay code that loads no asset yet

**Input:** `$gs-asset-audit`

**Domain checks:**
- [ ] `Total assets scanned` is 0 and the four file checks are NOT ASSESSED with that reason
- [ ] Verdict is NOT ASSESSED, not COMPLIANT
- [ ] No file is written

---

### Case 7: No Standards — Assets exist, no size budget anywhere

**Fixture:**
- `project.yaml`: `engine.name: godot`
- `design/art/art-bible.md` does not exist; no design doc states asset standards
- `assets/art/ui/` holds 3 correctly named power-of-two PNGs; `src/` references all three

**Input:** `$gs-asset-audit`

**Domain checks:**
- [ ] No size is judged against an invented budget
- [ ] The Size section is `NOT ASSESSED — no size budget set` and `$gs-art-bible` is named
- [ ] Verdict is NOT ASSESSED, not COMPLIANT

---

### Case 8: Unreal Project — Assets under `Content/`

**Fixture:**
- `project.yaml`: `engine.name: unreal`, so the code root is `Source/<Module>/`
- `design/art/art-bible.md` asset standards: textures ≤4MB; no naming convention stated
- `Content/Characters/Grunt/` holds `T_Grunt_D.uasset` (2.5MB) and `T_Grunt_N.uasset` (2.1MB)
- `assets/` does not exist
- `Source/Arena/Private/GruntCharacter.cpp` loads `/Game/Characters/Grunt/T_Grunt_D`

**Input:** `$gs-asset-audit`

**Domain checks:**
- [ ] The scan covers `Content/` and counts 2 assets, not 0
- [ ] No naming violation is raised from the Godot lowercase patterns
- [ ] Naming, Format and Orphaned are each listed as NOT ASSESSED with a reason
- [ ] Verdict is NOT ASSESSED, never COMPLIANT and never a report of zero assets

---

### Case 9: Engine Unresolved — Stop before scanning

**Fixture:**
- `project.yaml` has no `engine.name`; `.game-studio/resources/docs/technical-preferences.md` reads `[TO BE CONFIGURED]`
- Both `src/` and `Source/` exist, so the tree does not decide the engine
- `design/art/art-bible.md` has asset standards; `assets/art/` holds PNG files

**Input:** `$gs-asset-audit`

**Domain checks:**
- [ ] Verdict is `NOT ASSESSED — engine unresolved`, not COMPLIANT
- [ ] Output names `$gs-setup-engine`
- [ ] No violation table is filled from an assumed `assets/` layout
