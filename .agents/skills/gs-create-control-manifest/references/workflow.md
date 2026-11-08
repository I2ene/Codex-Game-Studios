## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

## Native execution contract

Use current project instructions, user authorization and inherited model/permissions.
Read `.game-studio/resources/docs/native-runtime.md` for platform mechanics and only
the domain references needed for this task. Config is an explicit command, not shell
preprocessing. Workflow inputs come from the user's request, not injected variables.
Tool-shaped examples below are procedural briefs; use tools actually exposed by the
host. They do not declare APIs or grant permissions. Existing task authorization
satisfies routine writes already in scope; do not repeat per-file approval questions.

Roles describe expertise. Delegate only when authorized and useful; otherwise apply
the role yourself and label the review as performed by the parent. Never fabricate
participant IDs, independent reviews or sign-off. Record real delegated participants.
Missing evidence means NOT ASSESSED — NO DATA. Resolve engine/version from this
project; engine reference versions are examples and require current verification.


Explicitly resolved — use as-is; `--review` overrides `review_mode` for this run. No
block → defaults in `.game-studio/resources/docs/config-resolution.md`.

Ask with the question tool. Without one, list the options numbered and end your turn
to wait. A skipped or dismissed question is not an answer: ask again in plain text.

# Create Control Manifest

The control manifest is a flat rules sheet for programmers: what to do and what
never to do, by architectural layer, taken from the Accepted ADRs, the project's
technical preferences and the engine reference docs. The ADRs say *why*; the
manifest says *what*.

**Writes:** `docs/architecture/control-manifest.md`, after the user's yes.
**When:** after `$gs-architecture-review` passes and the ADRs are Accepted. Run it
again whenever an ADR is accepted or revised.

Asks follow `.game-studio/resources/docs/automation-modes.md` (collaborative resolves open decisions, guided
asks on major choices, autonomous logs and goes on; `automation_always_ask`
categories always ask).

Every `ask the user` call follows `.game-studio/resources/docs/automation-modes.md`
(collaborative resolves open choices · guided resolves major choices · autonomous records in-scope choices;
`automation_always_ask` categories require input only outside existing authorization).

## 1. Load All Inputs

### ADRs

`bash .game-studio/scripts/adr-status.sh` reads every `docs/architecture/adr-*.md` in one
pass: the counts first (`adrs`, then `accepted`, `proposed`, `deprecated`,
`superseded`, `unfilled`, `other`, `no_status`), then one row per ADR with its
status and layer. Establish the denominator first: decide from the counts, before
reading any ADR:

| Counts | Meaning | Action |
|---|---|---|
| **N matches, some read `Accepted`** | Normal. | The Accepted set is **A**; proceed with A. Name every ADR left out, with its status, in the Phase 4 preview — the user approves a manifest knowing what it does not cover. |
| **N matches, none `Accepted`** | Genuinely no Accepted ADRs. | "[N] ADRs found, none Accepted. A manifest built from Proposed ADRs would encode decisions that may still change." Ask whether to proceed with Proposed or stop. **Do not silently emit an empty manifest.** |
| **0 matches, N > 0** | **Malformed ADRs — not an empty Accepted set.** `## Status` is BLOCKING-if-missing. | "[N] ADRs found, none has a `## Status` section — acceptance cannot be determined. Run `$gs-architecture-decision retrofit [file]` on each." **Stop.** Do not treat all ADRs as Accepted; do not emit a manifest. |

- Note the ADR number and title for every rule sourced.

### Project Config
- Read `naming.*` and `performance.*` from `project.yaml`; for any key absent or
  empty, fall back to `docs/project-reference/technical-preferences.md`
- Read approved libraries/addons and forbidden patterns from
  `docs/project-reference/technical-preferences.md` (not migrated to project.yaml)

### Engine Reference
- Read `<project-engine-reference>/VERSION.md` for engine + version
- Read `<project-engine-reference>/deprecated-apis.md` — these become
  forbidden API entries
- Read `<project-engine-reference>/current-best-practices.md` if it exists

### Existing Artifacts
- Glob `docs/architecture/control-manifest.md` (present → this run is a
  regeneration; Read it before the Phase 5 write, which overwrites it) and
  `production/epics/*/EPIC.md` (present → epics exist). Phase 6 picks its next
  step from both.

Each stop above ends with `Verdict: BLOCKED — [the reason]`. Note the number and
title of every ADR a rule comes from.

---

## 2. Extract Rules from Each ADR

Read **only these four sections** per Accepted ADR — not the whole file. Context,
Consequences, Migration Plan and Validation Criteria explain *why* a decision was
made; the manifest records *what to do*, so they are not needed here:
```
Grep pattern="^## (Decision|Alternatives Considered|Performance Implications|Engine Compatibility)" glob="docs/architecture/adr-*.md" output_mode="content" -A 30
```
Filter the results to the Accepted set **A** explicitly resolved. If a section is
absent for a given ADR, note it per ADR and continue; if a section is absent
across **all** of A, report "No Accepted ADR contains a `[section]` section — the
manifest's [category] rules will be empty. Verify this is intended." Escalate to
a full read of one ADR only when its scanned sections cross-reference material
outside them (e.g. a Decision that says "subject to the constraints in Context").

For each Accepted ADR, extract:

### Required Patterns (from the `## Decision` section)
- Every "must", "should", "required to", "always" statement in the Decision body
  — including any `### Implementation Guidelines` sub-heading when the ADR has one
  (newer ADRs emit it; older ones state mandates directly in `## Decision`). Never
  scan for `### Implementation Guidelines` alone — it is absent from many
  skill-authored ADRs, and scanning for it yields an empty Required Patterns
  section on a manifest that should have been full.
- Every specific pattern or approach mandated

### Forbidden Approaches (from "Alternatives Considered" sections)
- Every alternative that was explicitly rejected — *why* it was rejected becomes
  the rule ("never use X because Y")
- Any anti-patterns explicitly called out

### Performance Guardrails (from "Performance Implications" section)
- Budget constraints: "max N ms per frame for this system"
- Memory limits: "this system must not exceed N MB"

### Engine API Constraints (from "Engine Compatibility" section)
- Post-cutoff APIs that require verification
- Verified behaviours that differ from default LLM assumptions
- API fields or methods that behave differently in the pinned engine version

### Layer Classification
Classify each rule by the architectural layer of the system it governs:
- **Foundation**: Scene management, event architecture, save/load, engine init
- **Core**: Core gameplay loops, main player systems, physics/collision
- **Feature**: Secondary systems, secondary mechanics, AI
- **Presentation**: Rendering, audio, UI, VFX, shaders

If an ADR spans multiple layers, duplicate the rule into each relevant layer.

- `naming.*` and `performance.*` from `project.yaml`; for any key absent or empty,
  `.game-studio/resources/docs/technical-preferences.md`.
- Approved libraries and forbidden patterns from
  `.game-studio/resources/docs/technical-preferences.md` (not migrated to `project.yaml`).

### Engine reference

- `.game-studio/resources/engine-reference/[engine]/VERSION.md` for the engine and version.
- `.game-studio/resources/engine-reference/[engine]/deprecated-apis.md`: these become forbidden APIs.
- `.game-studio/resources/engine-reference/[engine]/current-best-practices.md`, when it exists.

### What exists already

`docs/architecture/control-manifest.md` present: this run regenerates it; read it
before the Phase 5 write, which replaces it. `production/epics/*/EPIC.md` present:
epics exist. Phase 6 picks its next step from both.

Report: "Loaded [A] Accepted ADRs of [N], engine: [name + version]."

## Phase 2: Extract the rules from each ADR

For each ADR in **A**, read only four sections, never the whole file:

```
python .game-studio/runtime/studio.py markdown --root <project-root> extract docs/architecture/[adr-file].md "Decision"
```

and the same for `Alternatives Considered`, `Performance Implications` and `Engine
Compatibility`. Context, Consequences, Migration Plan and Validation Criteria say why
a decision was made; the manifest records what to do. A section an ADR lacks: note
it for that ADR and go on. A section missing from **every** ADR in A: report "No
Accepted ADR has a `[section]` section — the manifest's [category] rules will be
empty. Verify this is intended." Read beyond the four only when a section points
outside itself ("subject to the constraints in Context"), and then that one section.

From each ADR:

- **Required patterns** (Decision): every "must", "should", "required to",
  "always", and every pattern or approach it mandates, including any `### Implementation
  Guidelines` inside it. Never look for that sub-heading alone: many ADRs state
  their mandates directly under Decision, and a scan for the sub-heading alone
  yields an empty section.
- **Forbidden approaches** (Alternatives Considered): every rejected alternative,
  with why it was rejected as the rule ("never use X because Y"), and any named
  anti-pattern.
- **Performance guardrails** (Performance Implications): budgets ("max N ms per
  frame for this system") and memory limits.
- **Engine API constraints** (Engine Compatibility): post-cutoff APIs that need
  verifying, behaviour that differs from what a model would assume, fields or
  methods that changed in the pinned version.

**Layer.** Each rule goes under the layer of the system it governs, the ADR's
`layer` column where it has one:

- **Foundation:** scene management, event architecture, save/load, engine start-up
- **Core:** core gameplay loop, main player systems, physics and collision
- **Feature:** secondary systems and mechanics, AI
- **Presentation:** rendering, audio, UI, VFX, shaders

An ADR that spans layers puts its rule in each one.

## Phase 3: Add the global rules

Rules for every layer, each with its source (the `project.yaml` key,
`technical-preferences.md`, or the engine-reference file), as a layer rule has:

- **Naming** from `naming.*`: classes, variables, signals and events, files,
  constants.
- **Performance budgets** from `performance.*`: target frame rate, frame budget,
  draw calls, memory ceiling.
- **Forbidden APIs** from `deprecated-apis.md`, **only those that apply to what this
  project builds.** Never copy the table whole: its `GodotPhysics3D → Jolt Physics
  3D` row is 3D-only, and a 2D project does not use that engine. When you cannot
  tell whether an entry applies (2D or 3D, a module the project may not include),
  scope the rule ("when using 3D physics: …") or leave it out and list it as
  unresolved. `$gs-create-stories` reads this file, and rules that do not apply are
  rules nobody reads.
- **Required patterns** from `current-best-practices.md`, when it exists.
- **Forbidden patterns** from `technical-preferences.md`, copied as written.

## Phase 4: Show the summary, then the review

```
## Control Manifest Preview
Engine: [name + version]
ADRs covered: [ADR numbers]
ADRs left out: [ADR-NNNN ([status]), … — every ADR not in A, or "None"]
Rules extracted:
  - Foundation layer: [N] required, [M] forbidden, [P] guardrails
  - Core layer: [N] required, [M] forbidden, [P] guardrails
  - Feature layer: …
  - Presentation layer: …
  - Global: [N] naming conventions, [M] forbidden APIs, [P] approved libraries
Unresolved: [engine entries left out because whether they apply is unclear, or "None"]
```

Use `ask the user`:
- Prompt: "Does this rule summary look complete?"
- Options:
  - `[A] Yes — looks good, run the director review and write the manifest`
  - `[B] Add rules — I have additional rules to include before writing`
  - `[C] Remove rules — some extracted rules should be dropped`
  - `[D] Stop here — I need to review the ADRs first`

---

## 4b. Director Gate — Technical Review

**Review mode check** — apply before spawning TD-MANIFEST:
- `solo` → skip. Note: "TD-MANIFEST skipped — Solo mode." Proceed to Phase 5.
- `lean` → skip. Note: "TD-MANIFEST skipped — Lean mode." Proceed to Phase 5.
- `full` → spawn as normal.

Spawn `technical-director` via native delegation when authorized using gate **TD-MANIFEST** (`.game-studio/resources/docs/director-gates/td-manifest.md`).

Pass: the Control Manifest Preview from Phase 4 (rule counts per layer, full extracted rule list), the list of ADRs covered, engine version, and any rules sourced from technical-preferences.md or engine reference docs.

The technical-director reviews whether:
- All mandatory ADR patterns are captured and accurately stated
- Forbidden approaches are complete and correctly attributed
- No rules were added that lack a source ADR or preference document
- Performance guardrails are consistent with the ADR constraints

Apply the verdict:
- **APPROVE** → proceed to Phase 5
- **CONCERNS** → surface via `ask the user` with options: `Revise flagged rules` / `Accept and proceed` / `Discuss further`
- **REJECT** → do not write the manifest; fix the flagged rules and re-present the summary
- **NOT ASSESSED** [missing input] → not an approval (`.game-studio/resources/docs/director-gates.md`): name what was missing, then supply it and re-run the gate — or, if the user chooses to go on without it, continue to Phase 5 and state `TD-MANIFEST: NOT ASSESSED — [input]` in the output and the final Verdict line

---

## 5. Write the Control Manifest

Use `ask the user`:
- Prompt: "May I write the Control Manifest?"
- Options:
  - `[A] Yes — write to docs/architecture/control-manifest.md`
  - `[B] Show me the full draft first, then ask again`
  - `[C] Not yet — I want to make more changes`

Format:

```markdown
# Control Manifest

> **Engine**: [name + version]
> **Last Updated**: [date]
> **Manifest Version**: [date]
> **ADRs Covered**: [ADR-NNNN, ADR-MMMM, ...]
> **Status**: Active — regenerate with `$gs-create-control-manifest update` when ADRs change

`Manifest Version` is the date this manifest was generated. Stories embed it when
they are written, and `$gs-story-readiness` compares a story's version with this one
to find stories written against old rules. It always equals `Last Updated`: the
same date, for different readers.

This manifest is a programmer's quick reference taken from the Accepted ADRs, the
technical preferences and the engine reference docs. For the reason behind a rule,
read its ADR.

---

## Foundation Layer Rules

*Applies to: scene management, event architecture, save/load, engine start-up*

### Required Patterns
- **[rule]** — source: [ADR-NNNN]

### Forbidden Approaches
- **Never [anti-pattern]** — [brief reason] — source: [ADR-NNNN]

### Performance Guardrails
- **[system]**: max [N]ms/frame — source: [ADR-NNNN]

---

## Core Layer Rules

*Applies to: core gameplay loop, main player systems, physics, collision*

### Required Patterns
...

### Forbidden Approaches
...

### Performance Guardrails
...

---

## Feature Layer Rules

*Applies to: secondary mechanics, AI systems, secondary features*

### Required Patterns
...

### Forbidden Approaches
...

---

## Presentation Layer Rules

*Applies to: rendering, audio, UI, VFX, shaders, animations*

### Required Patterns
...

### Forbidden Approaches
...

---

## Global Rules (All Layers)

### Naming Conventions
| Element | Convention | Example | Source |
|---------|-----------|---------|--------|
| Classes | [convention] | [example] | [`naming.classes` in project.yaml, or technical-preferences.md] |
| Variables | [convention] | [example] | [`naming.variables` in project.yaml, or technical-preferences.md] |
| Signals/Events | [convention] | [example] | [`naming.signals` in project.yaml, or technical-preferences.md] |
| Files | [convention] | [example] | [`naming.files` in project.yaml, or technical-preferences.md] |
| Constants | [convention] | [example] | [`naming.constants` in project.yaml, or technical-preferences.md] |

### Performance Budgets
| Target | Value | Source |
|--------|-------|--------|
| Framerate | [value] | [`performance.target_framerate` in project.yaml, or technical-preferences.md] |
| Frame budget | [value] | [`performance.frame_budget_ms` in project.yaml, or technical-preferences.md] |
| Draw calls | [value] | [`performance.draw_call_limit` in project.yaml, or technical-preferences.md] |
| Memory ceiling | [value] | [`performance.memory_ceiling_mb` in project.yaml, or technical-preferences.md] |

### Approved Libraries / Addons
- [library] — approved for [purpose] — source: technical-preferences.md

### Forbidden APIs ([engine version])
These APIs are deprecated or unverified for [engine + version]:
- `[api name]` — deprecated since [version] / unverified post-cutoff
- Source: `<project-engine-reference>/deprecated-apis.md`

### Cross-Cutting Constraints
- [constraint that applies in every layer] — source: [ADR-NNNN, preference key or engine-reference file]
```

## Phase 6: Next steps

**Applies in `collaborative` mode (the default).** For `guided` and
`autonomous` modes, see `.game-studio/resources/docs/automation-modes.md` — the rules below
describe what collaborative mode requires, not universal behavior.

Every rule traces to an ADR, a technical preference or an engine reference doc;
none is invented, and none is paraphrased in a way that changes its meaning. End
with `Verdict: COMPLETE — control manifest written` after the write, or `Verdict:
BLOCKED — user declined the write` when declined.
