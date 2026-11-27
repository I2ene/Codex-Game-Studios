# Evaluation scenarios: gs-setup-engine

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-setup-engine/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Godot 4 + GDScript — Full engine configuration

**Fixture:**
- `project.yaml` has no `engine` block; `technical-preferences.md` holds only placeholders
- No `design/gdd/game-concept.md` and no `design/game-brief.md`
- `<project-engine-reference>/godot/VERSION.md` already pins 4.7
- No `project.godot` at the repo root; the user approves every write

**Input:** `$gs-setup-engine godot 4.7`

**Domain checks:**
- [ ] `engine.name` is Godot and `engine.language` is GDScript in `project.yaml`
- [ ] `naming.variables` and `naming.files` are `snake_case`
- [ ] Routing table includes `.gd`, `.gdshader`, and `.tscn` entries; `specialists.code` is `godot-gdscript-specialist`
- [ ] The rendering/physics shape is asked, not inferred from the engine name
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Knowledge Risk is HIGH for this historical fixture relative to its recorded reference baseline; the active model's knowledge is not asserted by the packaged May 2025 snapshot
- [ ] Verdict is COMPLETE

---

### Case 2: Unity + C# — Unity-specific configuration

**Fixture:**
- Placeholders only in `technical-preferences.md`; no `engine` block in `project.yaml`
- The user supplies the version and the build target when asked

**Input:** `$gs-setup-engine unity`

**Domain checks:**
- [ ] Engine field is set to Unity and Language to C#
- [ ] Naming conventions reflect C# conventions
- [ ] Routing table includes `.cs` and `.unity` entries
- [ ] No project-shape question is asked for Unity
- [ ] No Unity project files are written
- [ ] Verdict is COMPLETE

---

### Case 3: Unreal — C++ primary, Blueprint routed to its specialist

**Fixture:**
- Placeholders only; the user never states that the project is Blueprint-primary
- The session runs on Windows (`uname -s` is neither `Linux` nor `Darwin`), so the Windows `commands` block applies

**Input:** `$gs-setup-engine unreal 5.8`

**Domain checks:**
- [ ] In the baseline fixture, Engine is Unreal Engine 5.8 and `engine.language` is `C++`; no `.uproject` is scaffolded
- [ ] Routing table includes `.uasset` and `.umap` entries
- [ ] ue-blueprint-specialist is assigned for Blueprint graphs
- [ ] `commands` carry the `# TODO: confirm these` comment
- [ ] Verdict is COMPLETE

**Variant — explicit Blueprint-primary choice:**
- Same project, but the user explicitly selects Blueprint as the primary language.
- Input: `$gs-setup-engine unreal 5.8`, with the Blueprint-primary answer.

**Domain checks (Blueprint-primary):**
- [ ] Records Blueprint as `engine.language` and the primary language, with C++ where needed; the baseline C++-primary expectation does not apply.
- [ ] No `.uproject` is scaffolded; engine routing and command-verification requirements still apply.

---

### Case 4: Re-run on a Configured Project — blocks edited in place

**Fixture:**
- `project.yaml` already has `engine` (Godot 4.7), `specialists`, `naming`, a
  `modes` block, and a `commands` block missing its `smoke` key
- `project.godot` exists at the repo root
- `<project-engine-reference>/godot/VERSION.md` pins 4.7

**Input:** `$gs-setup-engine godot 4.7`

**Domain checks:**
- [ ] No block is duplicated in `project.yaml`, and the missing `commands.smoke` key is added
- [ ] `modes` (and all other non-engine content) is unchanged
- [ ] `project.godot` is not overwritten
- [ ] For a same-version pin, Engine Version, Project Pinned and Last Docs Verified are untouched and `Installed at pin time` is written
- [ ] Verdict is COMPLETE

---

### Case 5: Director Gate Check — No gate; setup-engine is a utility skill

**Fixture:**
- Fresh project with no engine configured

**Input:** `$gs-setup-engine godot`

**Domain checks:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is COMPLETE without any gate check

---

### Case 6: Installed Editor Older Than the Chosen Version — ask, then record

**Fixture:**
- As Case 1; `<project-engine-reference>/godot/VERSION.md` pins 4.7
- `godot --version` reports `4.5.1.stable`
- The user picks "pin the newer one and upgrade later"

**Input:** `$gs-setup-engine godot 4.7`

**Domain checks:**
- [ ] Both versions are stated and all three options are offered
- [ ] The skill waits for the user's choice rather than picking silently
- [ ] `Installed at pin time` records 4.5.1 — the same-version branch does not skip it
- [ ] Engine Version, Project Pinned and Last Docs Verified are not restamped

---

### Case 7: Godot not on PATH — the probed executable goes into `commands.*`

**Fixture:**
- As Case 1, on Windows; `godot --version` fails — `godot` is not on `PATH`
- The probe finds `C:/Program Files/Godot/Godot_v4.7.2-stable_win64.exe`, which reports `4.7.2.stable`
- The user names the export preset `Windows Desktop`

**Input:** `$gs-setup-engine godot 4.7`

**Domain checks:**
- [ ] No `commands.*` value names bare `godot`
- [ ] Every Godot command value is an argv list; its executable path is one element, preserving spaces, and the remaining arguments are separate elements
- [ ] `engine.path` records the editor executable
- [ ] Variant — the probe finds nothing and the user does not know where Godot is: bare `godot` is kept under a `# TODO: godot is not on PATH here` comment, and the skill says the commands will not run until the path is set

---

### Case 8: A dismissed engine choice supplies no answer

**Fixture:** Fresh project with no configured engine. Required engine choice is dismissed; repeat in a
headless or unattended run where no answer can be supplied.

**Input:** `$gs-setup-engine`

**Domain checks:**
- [ ] Do not guess engine, version or language or infer authorization from dismissal. Restate
  the missing decision in plain text where interaction is possible; otherwise stop with the
  specific missing input.
- [ ] No project configuration, technical-preferences, engine VERSION record or project
  instructions are written while that input is missing.

---

### Case 9: Adopt an existing Web project without scaffolding over it

**Fixture:** Existing npm lockfile project: JavaScript, webpack build script, Jest test script, Phaser dependency, no hook/node_modules. Variant: package workspaces.

**Input:** $gs-setup-engine web

**Domain checks:**
- [ ] Detect and present the project's own scripts, package manager, bundler version, JavaScript, roots, test runner/library and absent hook. Preserve all game-owned files and existing lockfile.
- [ ] Write only authorized project records and argv commands, without invented rendering/physics. Dependency install and hook insertion require applicable separate scope; hook default is Not now.
- [ ] If execution is authorized, retain actual build/test outcomes and screenshot evidence; template pins do not describe this project. Workspaces variant stops before writes as unsupported.

---

### Case 10: Offer Web first only when no project engine exists

**Fixture:** Fresh project without engine markers or package. Variant: brief targets console.

**Input:** $gs-setup-engine

**Domain checks:**
- [ ] Explain engine tradeoffs before listing Web first and recommended, followed by supported engines; wait for the missing engine choice before writing.
- [ ] Console variant keeps Web visible but recommends an appropriate engine from that brief instead. Apply the chosen engine procedure, not an inferred choice.

---

### Case 11: An existing project retains its engine

**Fixture:** A: configured Godot 4.7. B: no engine config but root project.godot.

**Input:** $gs-setup-engine

**Domain checks:**
- [ ] Report the source of the detected engine and continue Godot setup without offering an unsolicited switch to Web. Preserve explicit engine facts and unrelated files.

---

## Applicable domain checks

- [ ] Use the selected Godot export preset and Unity build target; never invent a default for an unresolved preset or target.

- [ ] The closing list follows next-step order: prototype first when no game exists, retaining the studio ladder at standard/full. No setup success alone establishes a running game.
