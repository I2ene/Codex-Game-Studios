# Evaluation scenarios: gs-security-audit

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-security-audit/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Single-player Godot project, no findings

**Fixture:**
- `project.yaml`: `engine.name: godot`, `engine.language: gdscript`, `platform.multiplayer: false`, `platform.online: false`, `modes.rigor: standard` (so `workflow` resolves to `standard`); `modes.automation` unset (collaborative)
- `src/` holds the implemented game: 42 `.gd` files across core, gameplay, UI and save systems
- `src/core/save_system.gd` opens saves with `FileAccess`, verifies a checksum, and bounds-checks every loaded value before use
- No API keys, secrets, passwords or tokens anywhere in `src/` or `assets/`
- `addons/gdUnit4/` is the only third-party dependency

**Input:** `$gs-security-audit`

**Domain checks:**
- [ ] `security-engineer` is consulted with the fixed brief template — scope, engine/language, the `platform.*` values and a source manifest rooted at `src/` — and the brief adds no severity and no remark on the game's type
- [ ] Save handling is checked with Godot 4 names (`FileAccess`), not only the Godot 3 `File.open`
- [ ] Hardcoded-credential patterns (`api_key`, `secret`, `password`, `token`, `private_key`) are scanned
- [ ] The Executive Summary says Category 2 was skipped because `platform.multiplayer` and `platform.online` are `false` — the skip is not silent
- [ ] Release recommendation is CLEAR TO SHIP
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 1b: Single-player, One HIGH Finding — FIX BEFORE SHIPPING

**Fixture:**
- Same as Case 1, except `src/core/save_system.gd` loads save values with no
  checksum or bounds check, so an edited save file unlocks late-game progression
- No other findings

**Input:** `$gs-security-audit`

**Domain checks:**
- [ ] The brief sent to `security-engineer` is the fixed template: it does not call the save finding HIGH (or any severity), and does not say a single-player game lowers the bar — the agent rates it from its own table
- [ ] The finding is HIGH, not CRITICAL, in a single-player game
- [ ] Release recommendation is FIX BEFORE SHIPPING — never CLEAR TO SHIP with a HIGH open, and not DO NOT SHIP without a CRITICAL
- [ ] The ⚠️ HIGH message names the release gate's security audit item as the requirement, and names `$gs-security-audit quick` and `$gs-gate-check release`
- [ ] Variant — at `modes.rigor: minimal` the recommendation is still FIX BEFORE SHIPPING, and the message says the `minimal` release gate does not read this report instead of naming the gate item

---

### Case 2: Multiplayer Critical — Client-authoritative RPC and a hardcoded key

**Fixture:**
- `project.yaml`: `engine.name: godot`, `platform.multiplayer: true`, `platform.online: true`
- `src/net/combat_sync.gd` line 42: `@rpc("any_peer") func apply_damage(target_id, amount)` applies `amount` with no sender or range validation
- `src/online/leaderboard_client.gd` line 8: `const API_KEY = "sk_live_..."`

**Input:** `$gs-security-audit full`

**Domain checks:**
- [ ] The RPC finding cites `src/net/combat_sync.gd` with its line and an attack scenario
- [ ] The hardcoded key is raised to CRITICAL in the multiplayer context
- [ ] Every finding carries a specific remediation
- [ ] Release recommendation is DO NOT SHIP (open CRITICAL findings) — never FIX BEFORE SHIPPING or CLEAR TO SHIP
- [ ] The ⛔ message is shown and `$gs-launch-checklist` is held back

---

### Case 3: Multiplayer Scope Unset — Absent is not `false`

**Fixture:**
- `project.yaml`: `engine.name: godot`; no `platform` block at all
- `src/networking/lobby.gd` defines `@rpc` functions `join_lobby()` and `send_chat()`
- `modes.automation` unset (collaborative)

**Input:** `$gs-security-audit`

**Domain checks:**
- [ ] Absent `platform.multiplayer` / `platform.online` are not treated as `false`
- [ ] Skill asks the user whether the game has multiplayer or online features
- [ ] Category 2 is not skipped on the absent keys
- [ ] Unvalidated `@rpc` entry points in `lobby.gd` are checked and any gap is reported with a remediation
- [ ] Variant — with `modes.automation: autonomous` the question cannot be asked: Category 2 still runs, is marked `NOT ASSESSED — multiplayer scope unconfirmed`, and the recommendation is never CLEAR TO SHIP

---

### Case 4: No Implemented Surface — NOT ASSESSED — INSUFFICIENT IMPLEMENTATION

**Fixture:**
- `project.yaml`: `engine.name: godot`, `platform.multiplayer: false`, `platform.online: false`
- `src/` exists but contains no source files; `assets/data/` is empty

**Input:** `$gs-security-audit`

**Domain checks:**
- [ ] The empty code root leaves every code-scanning category NOT ASSESSED; none is reported clean or as zero findings
- [ ] Release recommendation is NOT ASSESSED — INSUFFICIENT IMPLEMENTATION
- [ ] Output names what was missing and which skill produces it
- [ ] CLEAR TO SHIP is not reachable from a scan with nothing to look at
- [ ] Variant — with no `engine.name`, `technical-preferences.md` at `[TO BE CONFIGURED]`, and both `src/` and `Source/` present, the code root is unresolved: no root is guessed, the code categories read `NOT ASSESSED — code root unresolved`, and the recommendation is never CLEAR TO SHIP

---

### Case 5: Unity Project in Full Review Mode — NOT SOURCEABLE category, no gates

**Fixture:**
- `project.yaml`: `engine.name: unity`, `engine.language: csharp`, `platform.multiplayer: true`, `platform.online: true`, `modes.review_mode: full`
- `Assets/Scripts/Save/SaveManager.cs` reads and writes save data
- `Assets/Scripts/Net/PlayerNet.cs` has `[ServerRpc]` methods that validate their inputs
- No findings in the categories that can run

**Input:** `$gs-security-audit`

**Domain checks:**
- [ ] The source manifest uses the Unity code root `Assets/`
- [ ] Category 1 is NOT ASSESSED for Unity and no save-API pattern list is invented
- [ ] Category 2 uses the Unity network names, not the Godot list
- [ ] CLEAR TO SHIP is unreachable; the recommendation names the unsourced category
- [ ] The NOT ASSESSED message points at a serialization module under `<project-engine-reference>/unity/modules/` as the fix
- [ ] No director gate is invoked in any review mode

---

### Case 5b: Ranking — An open HIGH outranks an unsourced category

**Fixture:**
- `project.yaml`: `engine.name: unity`, `engine.language: csharp`, `platform.multiplayer: false`, `platform.online: false`
- `Assets/Scripts/` holds the implemented game (35 `.cs` files), including `Assets/Scripts/Save/SaveManager.cs`
- `Assets/Scripts/Analytics/Telemetry.cs` line 12: `const string ApiKey = "sk_live_...";`
- No other findings

**Input:** `$gs-security-audit`

**Domain checks:**
- [ ] Release recommendation is FIX BEFORE SHIPPING, not NOT ASSESSED — a known failure is not buried behind an unscanned category
- [ ] Category 1 is still reported NOT ASSESSED in the Executive Summary
- [ ] CLEAR TO SHIP is not reported
