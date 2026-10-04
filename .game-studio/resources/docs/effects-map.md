# project.yaml — Effects Map

> ## READ ONE SECTION, NEVER THIS WHOLE FILE
>
> This document is **a large policy reference** — Read only the requested setting section; token budgets belong to the actual host. It is organised as **36 sections of
> ~900 tokens each**, one per setting, headed `## <key>`.
>
> **So opening it costs 36× what you need.** To look up a setting:
>
> ```
> Grep pattern="^## modes.review_mode" path=".game-studio/resources/docs/effects-map.md" -A 40
> ```
>
> Read the section for your key and stop. The same rule the skills already apply
> to their own reference files — `$gs-gate-check` loads only the row for the target
> phase and says "never load the others" — applies here, and this is the largest
> file in the framework by a factor of seven.
>
> This banner exists because six skills cite this document and **none of them
> scoped the citation**. None instructed a full read either, so
> nothing was actually loading 31k — but "see effects-map.md for full schema" in
> front of a file this size is an invitation, and the cost of accepting it is
> silent.

This document defines what each `project.yaml` setting actually does across
every skill that reads it. It is the tracked, authoritative reference.

**Purpose:** When a skill reads a setting, this document is the authoritative
source for what each value means for that skill's behavior. Implementers update
this file when adding a new setting or changing how a skill responds to one.

**Format per setting:**
- Priority chain — which source wins when multiple are present
- Per-value intent — what the value means in plain terms
- Skill behavior table — exactly what changes per skill per value

**Coverage scope:** This document covers the skills most affected by each setting.
Skills not listed (e.g. `ux-review`, `balance-check`, `test-flakiness`, `test-helpers`,
`test-setup`, `soak-test`, `perf-profile`, `launch-checklist`, `release-checklist`,
`skill-test`, `skill-improve`, `vertical-slice`) are not meaningfully affected by
`project.yaml` settings and do not need entries here. Add a skill only when its
behavior genuinely branches on a setting value.

**Local override pattern:** `project.yaml` is committed to git as the shared team
config. Per-developer overrides live in `project.local.yaml` (gitignored). Priority
chain across all settings: `project.local.yaml` → `project.yaml` → legacy mirror →
`modes.rigor` expansion → hardcoded default. The expansion step applies only to the
six knobs `rigor` fronts (`modes.workflow`, `docs.density`, `qa.level`,
`modes.story_granularity`, `modes.review_mode`, `team.size`), which for that reason have **no** hardcoded default —
see the `modes.rigor` section.
**Secrets do NOT belong in either file — use environment variables.** See the
"Local Override Pattern" section below for full design including the whitelist of
which settings can be locally overridden.

---

## Local Override Pattern — `project.local.yaml`

The `project.local.yaml` file lets each developer override specific settings for
their own use without affecting the team. The file is gitignored and never
committed.

### How it works

Priority chain (every setting): `project.local.yaml` → `project.yaml` → hardcoded default

If a setting is present in `project.local.yaml`, that value wins. If absent, the
value from `project.yaml` is used. If absent there too, the hardcoded default
takes over.

---

### Deep merge semantics

When both files set a nested value, only the explicitly-set key is overridden.
Sibling keys in the same block are preserved.

Example:

`project.yaml`:
```yaml
testing:
  strict:
    logic: true
    integration: true
    visual: false
```

`project.local.yaml` (sparse override):
```yaml
testing:
  strict:
    logic: false
```

Effective config seen by skills: `logic: false, integration: true, visual: false`.
Only the explicitly-set `logic` key is overridden; sibling keys come through from
`project.yaml`.

---

### Whitelist — which settings can be locally overridden

Only personal-experience settings can be locally overridden. Project-wide facts
(engine, stage, naming conventions, what's required on disk) are locked to
`project.yaml` because divergence between developers would break team coordination.

The rule for deciding which side a setting belongs on:

> **If a setting affects what artifacts exist or what they look like on disk,
> it must be locked to `project.yaml`. If a setting only changes your personal
> experience (which agents spawn for you, whether you get prompts, your local
> CI bypass), it can be locally overridden.**

**Locally overridable** (personal experience only — no effect on artifacts on disk):

| Setting | Why local override makes sense |
|---------|-------------------------------|
| `modes.review_mode` | How much AI review you personally want |
| `modes.automation` | How often the AI prompts you |
| `modes.automation_always_ask` | Your personal safety categories |
| `team.size` | Which agents spawn for your reviews (review depth differs, artifacts don't) |
| `testing.strict.*` (each type) | Whether failures block your local work (CI still enforces project.yaml defaults) |
| `performance.enforce` | Whether budget violations block your local work (CI enforces project defaults) |
| `features.session_state` | Your session tracking preference |
| `features.token_budget_warn_at` | Your personal cost threshold |

**Locked to `project.yaml`** (project-wide — would create artifact divergence if local):

| Setting | Why it must be project-wide |
|---------|----------------------------|
| `schema_version`, `framework.*` | File metadata, not preferences — **exempt from the report below**, since a `project.local.yaml` carrying `schema_version: 1` is correct as written |
| `project.name`, `version`, `genre`, `kind`, `stage` | Project identity |
| `engine.*`, `specialists.*` | Whole team must use same engine |
| `naming.*` | Code conventions must be consistent across team |
| `platform.*` | Game facts (what platforms it ships on) |
| `performance.target_framerate`, `frame_budget_ms`, `draw_call_limit`, `memory_ceiling_mb` | Game budgets, shared targets |
| `accessibility.target` | Game commitment, project-wide |
| `cadence.*` | Sprint/milestone length affects team coordination |
| `modes.rigor` | Fronts the four below — locked for the same reason they are |
| `modes.workflow` and `workflow_overrides` | Affects which sections are required in authored docs |
| `modes.story_granularity` | Affects how big stories are in repo — team must be consistent |
| `docs.density` | Affects how deep authored docs are — team must produce consistent docs |
| `qa.level` | Affects what test evidence stories must include on disk |
| `qa.coverage_minimum` | Project quality bar |
| `strict_gate_checks` | Affects whether `project.stage` advances — a project-wide write |
| `commands.*` | Build/test commands are project facts |
| `testing.framework` | Whole project uses one framework |

> **A locked key written into `project.local.yaml` by hand is reported, not
> swallowed.** `$gs-settings --local` refuses to write one, but the
> file is meant to be hand-edited and that path had no guard: `modes.rigor: full`
> there is a real key with a legal value, so enum validation passes it, and then
> resolution never consults the local file for that path — the setting vanishes
> and the user sees the default they were trying to override, with no error
> anywhere. Every check validated the **value**; nothing validated the
> `explicit config command`'s `notes:` line. It **warns and never reconciles**: it does not
> edit the file, does not begin honouring the key, and does not change
> resolution — a locked setting decides which artifacts exist on disk, so
> applying one quietly would produce exactly the divergence this table prevents.
> A clean file stays silent — you are only told when a key is actually in the
> wrong place.

---

### `$gs-settings --local` flag behavior

```
$gs-settings workflow=minimal               → writes to project.yaml (team-wide)
$gs-settings --local automation=autonomous  → writes to project.local.yaml (just you)
```

**Behavior rules:**

- Default (no flag): writes to `project.yaml`
- `--local` flag: writes to `project.local.yaml` (creates it if absent)
- `--local` on a locked setting → error:
  > *"`<setting>` cannot be locally overridden — it's a project-wide setting.
  > Use `$gs-settings <setting>=<value>` (no `--local`) to change it for the whole team."*
- Writing to `project.yaml` when the same setting is currently locally overridden → warning:
  > *"This setting is currently locally overridden in `project.local.yaml`.
  > Writing to `project.yaml` will not affect your effective value."*

---

### Schema validation on read

When skills or hooks read either file:

| Issue | Behavior |
|-------|----------|
| Unknown key (typo or stale setting) | Session-start warning: *"`project.local.yaml` has unknown key `modes.automaton` — typo? Ignored."* Does NOT block (forwards-compat with future settings). |
| Invalid value not in enum (e.g. `automation: chaotic`) | Hard error: skill exits with explanation of valid values. |
| Type mismatch (e.g. integer field set to a string) | Hard error: skill exits with type expected. |

---

### Creation and error handling

| Scenario | Behavior |
|----------|----------|
| `$gs-start` on fresh project | Creates `project.yaml` only. Does NOT create `project.local.yaml`. |
| `$gs-settings --local <x>=<y>` when local.yaml doesn't exist | Creates `project.local.yaml` containing just that setting. |
| `project.local.yaml` exists but `project.yaml` doesn't | Hard error: *"`project.yaml` missing — run `$gs-start` to create one. Local overrides require a base."* |
| Both files exist | Read `project.yaml` first, deep-merge `project.local.yaml` on top. Normal operation. |
| Both files set the same key | `project.local.yaml` wins. No prompting. |

---

### Two-developer clash scenarios — and why the whitelist prevents them

**File-level conflict (`project.yaml`):**
Standard git merge conflict. Each developer's `project.local.yaml` is gitignored
and never collides with another developer's. Normal git workflow handles team-wide
changes.

**Logical inconsistency (prevented by whitelist):**

Example of what the whitelist prevents:

> Sarah sets `modes.workflow: minimal` locally to skip GDD requirements. She
> doesn't write GDDs because her local mode doesn't require them. Mike runs
> `$gs-gate-check` with the team's `project.yaml` value, `standard`; gate-check sees missing
> GDDs and fails.

This can't happen because `modes.workflow` is locked to `project.yaml`. Same
for `qa.level`, `docs.density`, `strict_gate_checks`, `naming.*`, and every
other setting that affects what artifacts exist on disk.

Personal experience settings (`automation`, `review_mode`, `team.size`,
`testing.strict.*`, `performance.enforce`) can diverge freely without affecting
anyone else.

---

### Stricter reviewer reviewing a looser reviewer's work

A common worry: "what if my teammate has stricter review settings than me?
Will their `$gs-gate-check` or `$gs-design-review` flag things in my work?"

The answer depends on which kind of difference you're talking about:

**Different review depth, same project requirements (HEALTHY):**

- Teammate A: local `review_mode: full`, `automation: collaborative`, `testing.strict.logic: true`
- Teammate B: local `review_mode: solo`, `automation: autonomous`, `testing.strict.logic: false`
- Both bound by the same project.yaml-locked settings (e.g. `workflow: standard`, `qa.level: standard`)

B writes a GDD that meets `workflow: standard` (all 5 required sections present).
B's `$gs-design-review` runs with `review_mode: solo` — fast advisory check, no
specialists spawned. B moves on.

Later A reviews the same GDD with `review_mode: full` — spawns 5–15 specialists,
finds polish opportunities and edge cases B's lighter review missed. A files
findings as PR comments or follow-up issues. B addresses the ones that matter.

**This is normal team collaboration.** Different reviewers catching different
things is the value of having multiple reviewers. The artifacts on disk are the
same; only review depth differs. Nothing about this scenario creates project-state
divergence.

**Different requirements (PREVENTED by the whitelist):**

If `qa.level` were locally overridable:

- B sets `qa.level: minimal` locally. B's stories don't include test evidence.
- B's `$gs-story-done` accepts the story without evidence. Story marked Complete on disk.
- A pulls. A's `qa.level: standard` requires evidence. A's `$gs-story-done` would have rejected it.
- A's next `$gs-gate-check` fails because evidence is missing across multiple of B's "Complete" stories.

This is the artifact divergence problem. To prevent it, `qa.level` is locked to
`project.yaml`. The team agrees together on what's required; individuals override
only their personal experience, never the team's standards.

**The pattern to remember:**

| Difference type | Outcome |
|----------------|---------|
| Different review depth (review_mode, team.size) | Stricter reviewer surfaces more findings — healthy. Artifacts unchanged. |
| Different local strictness on failures (testing.strict.*, performance.enforce) | Stricter dev's local $gs-story-done blocks earlier — they fix it locally. CI uses project.yaml defaults so team-wide quality bar stays. |
| Different artifact requirements (workflow, qa.level, docs.density, etc.) | **Can't happen — these are locked.** Team agrees once in project.yaml. |

---

### CI behavior

CI environments have no `project.local.yaml` — the file is gitignored and never
present in a fresh clone. CI therefore always runs against `project.yaml`
defaults: strict project standards, no developer-specific overrides.

This is intentional and important:

| Setting | Local default for fast iteration | CI default (`project.yaml`) |
|---------|----------------------------------|------------------------------|
| `modes.review_mode` (locally overridable) | `solo` for one developer | `lean` (a team's usual choice — required phase checks still apply without implying delegated sign-off) |
| `testing.strict.logic` (locally overridable) | `false` for fast WIP commits | `true` (failing tests block CI) |
| `modes.automation` (locally overridable) | `autonomous` for solo flow | `collaborative` (the team's collab protocol, but CI doesn't ask questions anyway — this is mostly a no-op on CI) |

A developer can iterate locally with relaxed gates, but CI catches issues using
the strict project defaults. The team's quality bar is enforced at the CI level
regardless of any individual developer's local config.

---

### Secrets — never in either file

`project.yaml` and `project.local.yaml` are for **preferences and configuration**,
never for **secrets**. API keys, tokens, and credentials belong in:

- **Environment variables** (preferred for production/CI)
- **`.env` file** (gitignored, local dev)
- **OS keychain** (when integrating with services that support it)

When a skill needs an API key (e.g. `$gs-asset-spec` calling Midjourney), it reads
from the environment, not from `project.yaml`. `project.yaml` only stores **which**
generator is used (`art.generator: midjourney`), not the API key for it.

CI environments typically have no `project.local.yaml` (gitignored, not in the
clone) — so CI always runs against `project.yaml` defaults. This is correct
behavior: strict project defaults for CI, looser developer overrides for local work.

---

## modes.review_mode

**Controls:** How many specialist and director agents are spawned during skill execution
**Values:** `full` | `lean` | `solo`
**Default:** *none* — supplied by `modes.rigor` (`minimal`, the default, yields `solo`; `standard` yields `lean`; `full` yields `full`)
**Set by:** `$gs-settings`, or explicit reviewed legacy preference reconciliation via `$gs-adopt` when it carries over a v1.0 `production/review-mode.txt`. `$gs-start` and `$gs-adopt` never write it themselves — unset, it follows `modes.rigor`
**Read by:** See skill table below

**Priority chain (all skills):** inline argument flag → `modes.review_mode` in `project.yaml` → `production/review-mode.txt` (legacy fallback) → `modes.rigor` expansion (no terminal default; `minimal`→`solo`, `standard`→`lean`, `full`→`full`)

> **design-review follows the standard chain.** `modes.review_mode` controls
> design-review depth, its inline flag is `--review` for consistency with every
> other review-mode-aware skill, and with nothing set it follows `modes.rigor` like
> them: `solo` at `minimal` (the default), `lean` at `standard`.

> **Hotfix / day-one-patch exception:** These skills are emergency or release-critical
> pipelines. They are never gated by `review_mode` — all agents always run.

> **Known inertness — `full` and `lean` barely differ in the nine `team-*`
> orchestrators.** Each documents a three-way split: `full` spawns every director
> and lead gate, `lean` skips director gates *unless* they are PHASE-GATE type,
> `solo` skips gate spawning entirely. But the director gates the team skills name
> are the four PHASE-GATEs, which `lean` keeps — and no team pipeline spawns one
> (`$gs-gate-check` is their only spawner). Two things differ: `$gs-team-release`'s
> technical-director release sign-off runs only at `full`, and `$gs-team-narrative` at
> `team.size: small` adds `localization-lead` and `world-builder` only at `full`.
>
> `solo` genuinely differs, and outside the orchestrators (`$gs-design-review`,
> `$gs-architecture-review`) all three levels differ as documented.
>
> **This is recorded, not fixed.** Making `lean` mean something in the
> orchestrators requires deciding which non-phase-gate reviewers each of the nine
> should call at `full` — a design decision about review depth, not a wording fix,
> and one that changes how many agents a run spawns.

---

### Value intent

| Value | Intent |
|-------|--------|
| `full` | All director and specialist gates active. Best for teams, learning, or anyone who wants thorough AI feedback on every decision. |
| `lean` | Phase gates only — per-skill director sign-offs skipped. The `rigor: standard` value. Balances quality with token cost. |
| `solo` | No gates, no director spawns (a pipeline's own review, such as `$gs-team-narrative`'s ND-CONSISTENCY, still runs). Fastest. For confident solo iteration. The default, from `rigor: minimal`. |

---

### Core skills (currently review-mode aware)

| Skill | full | lean | solo |
|-------|------|------|------|
| **design-review** | 5–15 specialist agents spawned in Phase 3b | No specialist agents — single-session analysis only | Phases 1–4 only, no delegation, no next-steps prompt |
| **gate-check** | Director expertise applied by the parent, or authorized independent participants — **width set by `modes.workflow`**, not by this axis | Director expertise applied by the parent, or authorized independent participants — same width rule; required phase checks still apply without implying delegated sign-off | Artifact existence checks only, no directors spawned |
| **design-system** | All section specialists + CD-GDD-ALIGN sign-off gate | Specialists for Sections D and H only (+ G when its knobs interact, + Visual/Audio when visual feedback is central); CD-GDD-ALIGN skipped | No section specialists; CD-GDD-ALIGN skipped |
| **art-bible** | All section specialists + AD-ART-BIBLE sign-off gate | All section specialists, AD-ART-BIBLE skipped | All section specialists, AD-ART-BIBLE skipped |
| **architecture-decision** | Engine specialist + TD-ADR gate | Engine specialist; TD-ADR skipped | Engine specialist; TD-ADR skipped |
| **create-architecture** | TD-ARCHITECTURE + LP-FEASIBILITY agents, in parallel | Both skipped | Both skipped |
| **brainstorm** | CD-PILLARS, AD-CONCEPT-VISUAL, TD-FEASIBILITY, PR-SCOPE | All skipped | All skipped |
| **map-systems** | TD-SYSTEM-BOUNDARY, PR-SCOPE, CD-SYSTEMS | All skipped | All skipped |
| **story-done** | QL-TEST-COVERAGE + LP-CODE-REVIEW | Both skipped | Both skipped |
| **sprint-plan** | PR-SPRINT feasibility check | Skipped | Skipped |
| **create-epics** | PR-EPIC scope check | Skipped | Skipped |
| **create-stories** | QL-STORY-READY + test case specs | Skipped | Skipped |
| **prototype** | CD-PLAYTEST review — APPROVE keeps the recommendation; CONCERNS and REJECT go to the user, who decides | Skipped — the recommendation stands unreviewed | Skipped — the recommendation stands unreviewed |
| **milestone-review** | PR-MILESTONE feasibility check | Skipped — no producer verdict | Skipped — no producer verdict |
| **playtest-report** | CD-PLAYTEST creative assessment | Skipped | Skipped |
| **story-readiness** | QL-STORY-READY acceptance criteria check | Skipped | Skipped |
| **create-control-manifest** | TD-MANIFEST (technical-director) review | Skipped | Skipped |
| **propagate-design-change** | TD-CHANGE-IMPACT (technical-director) review | Skipped | Skipped |

---

### Skills to be made review-mode aware (currently ignore the setting)

| Skill | full | lean | solo |
|-------|------|------|------|
| **review-all-gdds** | Phase 2 consistency pass + Phase 3 design theory pass (parallel) | Phase 2 consistency pass only, Phase 3 skipped | Phase 2 only, Phase 3 skipped |
| **architecture-review** | Engine specialist + security-engineer (if online features) | Both skipped | Both skipped |
| **dev-story** | Core programmer routing always runs + engine-specialist escalation on HIGH risk stories | Core programmer routing always runs, engine-specialist escalation skipped | Core programmer routing always runs, engine-specialist escalation skipped |
| **code-review** | Language, shader, UI specialists + qa-tester | All optional specialists skipped | All optional specialists skipped |
| **security-audit** | security-engineer spawned | Skipped | Skipped |

---

### Team orchestration skills (pipeline behavior — different relationship)

Team skills are execution pipelines, not review gates. In them `review_mode` sets
only director-gate depth; `team.size` picks the agents (see `## team.size`), and a
pipeline's own review steps run in every mode.

| Skill | full | lean | solo |
|-------|------|------|------|
| **All nine `team-*`** | Every director gate the pipeline names | PHASE-GATE-type gates only | No director gates |
| **team-release** | + technical-director release sign-off before the go/no-go call | Sign-off not run — recorded as `not run (review_mode: lean)` | Sign-off not run — recorded as `not run (review_mode: solo)` |
| **team-narrative** | ND-CONSISTENCY; at `team.size: small`, + `localization-lead` and `world-builder` | ND-CONSISTENCY; at `small`, `narrative-director` + `writer` only | ND-CONSISTENCY still runs when `narrative-director` is active |

---

### Special cases and notes

- **gate-check** is the only skill where `full` and `lean` behave identically —
  required phase checks still apply without implying delegated sign-off. Only `solo` skips them. This is intentional: phase
  gates are the minimum quality bar, not optional extras. **How many directors
  run is a separate axis** — `modes.workflow` sets panel width (`minimal` → PR
  only, `standard` → TD + PR, `full` → all four), because a fixed four-director
  inherited model panel cost a two-system jam exactly what it cost a thirty-system
  commercial project. Width never softens a verdict: the strictest verdict from
  whoever ran still wins, and `$gs-gate-check` names the perspectives it skipped.
- **art-bible** always spawns its section specialists regardless of mode — only
  the final sign-off gate is controlled by `review_mode`. Specialist delegation is
  mandatory for the authoring output to be useful, and that has not changed.
  **design-system** is different: `lean` keeps the specialists for its high-risk
  sections only (D and H, plus G and Visual/Audio when they matter) and `solo`
  drafts every section without one, and each skipped spawn is announced by name.
  What sets `art-bible`'s **spawn count** is therefore not `review_mode`
  but (a) `modes.workflow`, via how many sections get authored at all — `standard`
  requires sections 1–4, not all 9, and Phase 1 recommends the tier's set — and
  (b) batching consecutive sections that call the *same* agent with the *same*
  input into one delegation (2–4, and 5–6). Unbatched, sections 5 and 6 spawn
  `art-director` twice with the identical `sections 1–4` brief. Every section is
  still specialist-authored; per-section approval and write-to-file are unchanged.
- **dev-story** core programmer routing (gameplay-programmer, ui-programmer, etc.)
  always runs regardless of mode — only the optional engine-specialist escalation
  for HIGH risk stories is gated.
- **hotfix** and **day-one-patch** are exempt — all agents always run.
- When a gate is skipped, skills emit: `"[GATE-ID] skipped — [mode] mode."` before
  proceeding. This is consistent across all skills.

---

## modes.rigor

**Controls:** How much process the project carries overall — the single question
`$gs-start` asks that sets the six knobs below
**Values:** `minimal` | `standard` | `full`
**Default:** `minimal` — see the rationale block above `_yaml_helper_defaults`
in `.game-studio/runtime/studio.py config`. Short version: the heavier tier cost several
times more to reach working code without producing a better result.
**Set by:** `$gs-start` (Phase 3d), `$gs-settings`
**Read by:** nothing directly — it is read *through* the six knobs it supplies

**Priority chain:** `modes.rigor` in `project.yaml` → hardcoded default `minimal`
(**locked** — not overridable from `project.local.yaml`, like the four *on-disk*
knobs it fronts — `modes.workflow`, `docs.density`, `qa.level`,
`modes.story_granularity` — because those five change what artifacts exist on
disk. The two personal-experience knobs it also fronts, `modes.review_mode` and
`team.size`, stay locally overridable.)

---

### Expansion table

| `modes.rigor` | `modes.workflow` | `docs.density` | `qa.level` | `modes.story_granularity` | `modes.review_mode` | `team.size` |
|---|---|---|---|---|---|---|
| `minimal` *(default)* | `minimal` | `terse` | `minimal` | `coarse` | `solo` | `individual` |
| `standard` | `standard` | `balanced` | `standard` | `balanced` | `lean` | `individual` |
| `full` | `full` | `thorough` | `full` | `fine` | `full` | `studio` |

### It fronts, it does not replace

The expansion sits **below every explicit source and above the terminal
default**:

```
project.local.yaml → project.yaml → legacy file → rigor expansion → default
```

That ordering is the back-compat guarantee, and it is what makes the migration
free. Three consequences worth stating plainly:

- **An existing `project.yaml` behaves identically.** If it already sets
  `docs.density: terse`, step 2 answers before the expansion is consulted — so
  the value and its reported source (`project.yaml`) are unchanged whether or not
  `rigor` is present. No migration, no `schema_version` bump.
- **Overrides go both ways.** Unlike the `workflow_overrides` **boolean flags** —
  which are additive and stricter-only — an explicit knob may be *looser* than
  the rigor level implies.
  (`workflow_overrides.system_overrides` is also two-directional — it replaces a tier; only the flags are stricter-only.)
  Inheriting the stricter-only rule would make "comprehensive but compact"
  inexpressible, which is the one off-diagonal the docs have always cited.
- **`modes.workflow` keeps `workflow_overrides.system_overrides`.** Per-system
  tiers still beat the rigor-derived project tier. `workflow` was fronted rather
  than folded away precisely because it drives ~5 distinct behaviors and owns the
  only per-system override mechanism.

The six fronted knobs therefore have **no entry in `_yaml_helper_defaults`**. A
terminal default there would answer before the expansion and make `rigor` a no-op
for anyone who had not also set the sub-knob.

### Provenance

Derived values report their source as `rigor:<level>`, so the vocabulary is
`{project.local.yaml, project.yaml, <legacy path>, rigor:<level>, default,
unset}`. `$gs-settings` renders this as `(derived from rigor: standard)` and
force-appends the five to its view-all list — none of them is a leaf of either
YAML file, so enumerating file leaves alone would hide exactly the settings the
user just chose.

---

## modes.workflow

**Controls:** How much design documentation is required before code can begin —
the tradeoff between token/time cost of documentation and speed of reaching
working code
**Values:** `full` | `standard` | `minimal`
**Default:** *none* — supplied by `modes.rigor` (`minimal`, the default, yields `minimal`; `standard` yields `standard`; `full` yields `full`)
**Set by:** `$gs-start` (via `modes.rigor`), `$gs-settings`
**Read by:** See skill tables below

**Priority chain:** `modes.workflow` in `project.yaml` → `modes.rigor` expansion → *(no hardcoded default)*

> **Why the middle level is `standard`, not `indie`.** A developer-type label
> would conflate "type of developer" with "level of process". `standard`
> describes the *amount of process*, not the user, and pairs cleanly with
> `minimal` and `full`.

> **Permissive, not restrictive:** `workflow` controls what is REQUIRED —
> not what is ALLOWED. Any skill can be run at any workflow level. The
> setting changes what gate-check enforces and what completeness checks
> validate, not what the user can invoke.

> **`minimal` floor:** Even in minimal mode, engine choice and a filled
> **`design/game-brief.md`** are required before code starts — the brief's
> build-order field is the plan, so there is no separate `sprint-plan` step.
> Both take minutes and prevent real problems downstream. Everything else can
> be skipped.

> **Escape hatches via `workflow_overrides`:** Users who want *almost* the
> standard set with one extra requirement (e.g. always force Edge Cases) use
> `workflow_overrides` rather than escalating to `full`. See next section.

---

### Value intent

| Value | Token/time cost | Required before code | Best for |
|-------|----------------|---------------------|----------|
| `full` | High | All 8 GDD sections per system, full architecture, all ADRs, art bible, UX specs per screen | Projects where design correctness matters more than speed — teams, commercial titles, learning the full pipeline |
| `standard` | Balanced | 5 GDD sections per system, one architecture doc, critical ADRs, game concept, systems index | Projects that have outgrown a brief — several interacting systems, or a design someone else has to implement |
| `minimal` | Low | One-page `design/game-brief.md` + engine choice (build order in the brief = the plan; no separate sprint plan) | **Default.** Get to code fast — small scope, jam projects, or the design already in your head. Raise it when the project grows |

**standard required GDD sections:** Overview, Detailed Rules, Edge Cases, Dependencies,
Acceptance Criteria.
**standard conditional:** Formulas — required when the system **defines numeric
rules**: rates, curves, thresholds, costs, damage, drop weights, or any value a
balance pass would tune. Optional only when the system defines no such value.

> **The test is what the system defines, not what it is called.** The `Category`
> column in `systems-index.md` is a *hint* — `Gameplay`, `Economy` and
> `Progression` systems almost always qualify — but it is not the test, and a
> `Core`, `UI` or `Persistence` system that defines a numeric rule qualifies too.
>
> Do not restate it as "required when system category is combat, economy,
> progression, or AI". Those four tokens are not the vocabulary `$gs-map-systems`
> writes: `templates/systems-index.md` defines the categories as `Core ·
> Gameplay · Progression · Economy · Persistence · UI · Audio · Narrative ·
> Meta`, and lists **combat and AI as example systems under `Gameplay`**. A
> combat system categorised exactly as the template instructs therefore matched
> none of the four, and Formulas was silently dropped for the system most likely
> to need it. `coding-standards.md` and `rules/design-docs.md` already stated the
> "has math" test; the skills are reconciled to them rather than the other way
> round.

> **Edge Cases is required at `standard`.** Skipping it consistently produces
> "wait, what happens if X is null?" debt during implementation. These 5
> required sections are the minimum that produces implementable code.

> **Art bible is conditional in `standard`.** It is required only if visual
> asset stories exist in the project. Code-focused projects can skip it
> entirely at `standard` level.

---

### Authoring skills

| Skill | full | standard | minimal |
|-------|------|----------|---------|
| **design-system** | All 8 sections required | 5 required sections + conditional Formulas; Player Fantasy, Tuning Knobs skipped | Not required — game brief replaces GDDs. Can still be run voluntarily. |
| **art-bible** | All 9 sections required | Required only if visual asset stories exist; sections 1–4 minimum when required | Not required. Can still be run voluntarily. |
| **create-architecture** | Full architecture — all layers, module ownership, data flow, API boundaries, full ADR audit | Simplified — system layer map + critical ADR list only | Not required. Can still be run voluntarily. |
| **ux-design** | UX spec required per screen | Core screens only (main menu, HUD, primary game loop) | Not required. Can still be run voluntarily. |
| **map-systems** | Required before design-system | Required before design-system | Not required |
| **architecture-decision** | All ADRs on required ADR list must be completed | Critical ADRs only — Foundation layer systems | Not required |

---

### Review and validation skills

| Skill | full | standard | minimal |
|-------|------|----------|---------|
| **design-review** | All 8 sections validated — any missing section blocks approval | 5 required sections validated; missing optional sections warned but do not block | Not applicable — no GDDs to review |
| **review-all-gdds** | Validates all 8 sections across all GDDs | Validates 5 required sections across all GDDs; optional sections surfaced as advisory only | Not applicable |
| **architecture-review** | Full traceability matrix — all GDDs, all ADRs | Reduced scope — architecture doc + critical ADRs only | Not applicable |
| **consistency-check** | Full entity registry cross-check against all GDD sections | Entity registry check against required sections only | Not meaningful — no GDDs to check |
| **content-audit** | Full content count audit against all GDD specs | Limited audit — only specs in required sections counted | Cannot run — no systems index exists |

---

### Phase gate enforcement (gate-check)

`gate-check` is where workflow has the most visible impact — the artifact
checklists differ per phase per mode.

| Gate | full | standard | minimal |
|------|------|----------|---------|
| Concept → Systems Design | game-concept.md, pillars, Visual Identity Anchor | game-concept.md only | `design/game-brief.md` only (content check, not section check) |
| Systems Design → Technical Setup | systems-index, all MVP GDDs reviewed (8 sections), cross-GDD review | systems-index, 5-section GDDs reviewed, cross-GDD review optional | Not applicable — no gates between brief and code; the gate PASSes with that note |
| Technical Setup → Pre-Production | engine, art bible sections 1–4+, 3+ ADRs, architecture, UX specs started | engine, art bible only if visual assets, critical ADRs, architecture | engine configured (required floor) |
| Pre-Production → Production | sprint plan, complete art bible, epics, UX specs, control manifest; Vertical Slice + its playtest recommended (absent → CONCERNS) | epics, sprint plan; complete art bible, UX specs, control manifest recommended; Vertical Slice recommended | the brief's Build order + stories under `production/epics/`; the Vertical Slice items drop — the core loop is fun and runs end to end, checked on the current build |
| Production → Polish | core mechanics, tests, smoke check, QA sign-off, 3+ playtests | core mechanics, smoke check, playable end to end, 1+ playtest, no open S1 bugs | smoke check, playable end to end, no open S1 bugs |
| Polish → Release | all features, content complete, localization (`$gs-localize qa` per locale), QA, smoke, no open S1–S3 bugs, newest `$gs-security-audit` with no open CRITICAL/HIGH | all features, smoke, no open S1 bugs, the security audit | smoke, no open S1 bugs |

<!-- gate-check reconciliation: at `full` and `standard` the Vertical Slice
     keeps its long-standing "recommended, not blocking → CONCERNS if absent;
     FAIL if built-and-broken" status — the tier table never upgrades it to a
     hard blocker. At `minimal` its items drop, and two checks on the current
     build replace them. The genuinely-required floor item at this gate is the
     sprint plan at `standard`/`full`; at `minimal` there is no separate
     sprint-plan step — the brief's Build order plus stories is the floor at
     `minimal`. -->

**Director panel width** (`$gs-gate-check` Section 4b) is workflow's second effect
here. Directors are inherited model-tier, so a fixed four-director panel charged a
two-system jam exactly what it charged a thirty-system commercial project:

| `workflow` | Panel | Directors |
|---|---|---|
| `full` | 4 | `creative-director`, `technical-director`, `producer`, `art-director` |
| `standard` | 2 | `technical-director`, `producer` |
| `minimal` | 1 | `producer` |

`review_mode` remains the axis that decides *whether* the panel runs at all
(`solo` skips it entirely); workflow decides only how wide it is. Narrowing
never softens a verdict — the strictest verdict from whoever ran still wins, and
`$gs-gate-check` names the perspectives that did not run.

---

### Planning and implementation skills

| Skill | full | standard | minimal |
|-------|------|----------|---------|
| **create-epics** | Requires all GDDs approved (8 sections) | Requires 5-section GDDs approved | **Skipped** (Option A) — no separate epic doc. `$gs-create-stories` reads `design/game-brief.md` directly and synthesizes the implicit epic container itself. |
| **create-stories** | Requires all ADRs on required list present | Requires critical ADRs present | No ADR requirement |
| **dev-story** | Requires TR registry + governing ADR — blocks without them, and on a `Proposed`, `Deprecated` or `Superseded` ADR; a missing control manifest warns | TR registry optional; blocks only on a referenced ADR that is missing, `Proposed`, `Deprecated` or `Superseded` | No TR registry or ADR required — implements against `design/game-brief.md`; a referenced ADR that is missing, `Proposed`, `Deprecated` or `Superseded` still blocks |
| **story-readiness** | Full TR registry + ADR + control manifest validation; any referenced ADR that is missing, `Proposed`, `Deprecated` or `Superseded` BLOCKS | TR registry optional; critical ADR check, and any referenced ADR that is missing, `Proposed`, `Deprecated` or `Superseded` BLOCKS | Acceptance-criteria check (the brief stands in for the GDD); any referenced ADR that is missing, `Proposed`, `Deprecated` or `Superseded` still BLOCKS |
| **story-done** | Full GDD traceability + ADR consistency check | 5-section GDD traceability check | Acceptance criteria check only |
| **qa-plan** | Full test plan derived from all 8 GDD sections | Test plan from 5 required sections | Test plan from acceptance criteria only |
| **regression-suite** | Critical paths mapped from all sections including Edge Cases | Critical paths from required sections (including Edge Cases) | Smoke test coverage only |
| **release-checklist** | Open S1, S2 or S3 bug in `production/qa/bugs/` fails its Quality Gates item | Open S1 fails; open S2/S3 listed as risks | Open S1 fails; open S2/S3 listed as risks |
| **launch-checklist** | Zero open S1–S3 bugs, no exceptions | Zero open S1; S2 or a documented exception | Zero open S1; S2 or a documented exception |
| **team-release** | qa-lead verifies no open S1–S3 bugs | qa-lead verifies no open S1 bugs | qa-lead verifies no open S1 bugs |

---

### Support skills

| Skill | full | standard | minimal |
|-------|------|----------|---------|
| **project-stage-detect** | Checks for all doc types; missing art bible or UX specs flagged as gaps | Adjusts expectations — art bible only flagged if visual-asset stories exist; non-core UX specs not flagged | `design/game-brief.md` + engine present = normal state; no gaps flagged for absent GDDs |
| **adopt** | Full format compliance audit across all doc types | Audit scope reduced to required docs only | `design/game-brief.md` format check only |
| **reverse-document** | Generates full 8-section GDD from code | Generates 5-section GDD from code | Generates `design/game-brief.md` from code |
| **propagate-design-change** | Full cascading impact analysis across all ADRs | Checks critical ADRs for references only | Not applicable |
| **help** | Full artifact detection — surfaces all missing docs as next steps | Adjusts "what's missing" to required docs only — optional docs not surfaced as gaps | `design/game-brief.md` + engine present = next step is code |

---

### Workflow change mid-project

When `workflow` changes via `$gs-settings`, the skill emits an informational note:

> "Workflow changed from [old] to [new]. Run `$gs-content-audit` to see what's now
> required or extra. No automatic migration — existing files stay in place."

No documents are auto-deleted, auto-generated, or blocked. The setting only affects
*new* enforcement going forward.

---

## workflow_overrides

**Controls:** Opt-in granular requirements that override the chosen workflow level
**Location:** **top level of `project.yaml`** — a sibling of `modes:`, *not* a child of it
**Values:** object with sub-flags (see below)
**Default:** all false / empty
**Set by:** `$gs-settings`
**Read by:** `$gs-design-system`, `$gs-design-review`, `$gs-art-bible`, `$gs-gate-check`, `$gs-review-all-gdds`, `$gs-qa-plan`

> **Why the location is called out.** `explicit config command` reads
> `workflow_overrides.system_overrides.*` from the document root
> (`native config resolver`), and all 14 consuming skill files grep the same top-level
> path. Nested under `modes:` it is still valid YAML, so nothing errors — the
> setting is simply never read. If you copied a `workflow_overrides` block from
> anywhere, check its indentation: it belongs at the document root, never under
> `modes:`.

**Priority chain:** the three `workflow_overrides` **boolean flags**
(`edge_cases`, `tuning_knobs`, `art_bible_strict`) are *additive* on top of the
chosen `workflow` level — they make things stricter, never looser. None of them
has a value that opts out of a requirement the workflow level imposes.

> **`workflow_overrides.system_overrides` is not a flag and is not additive — it replaces a tier in both directions.**
> This rule does not extend to it. On a
> `full` project, `system_overrides.inventory: minimal` really does drop that
> system's required sections to zero. Intended — see
> `.game-studio/resources/docs/workflow-modes.md § workflow_overrides`. Stating the additive
> rule over the whole key is wrong: the guarantee never held for
> `system_overrides`, so do not rely on it as a safety net.

---

### Fields

```yaml
workflow_overrides:
  edge_cases: false          # force Edge Cases section required (no-op at standard since already required; relevant at minimal)
  tuning_knobs: false        # force Tuning Knobs section required (relevant at standard, no-op at full)
  art_bible_strict: false    # force all 9 art bible sections required regardless of asset stories
  system_overrides: {}       # per-system tier overrides — see below
```

### Per-system overrides

```yaml
workflow_overrides:
  system_overrides:
    combat: full              # combat-system GDD requires full (8 sections) regardless of project workflow
    boss-encounters: full
    inventory: minimal        # inventory needs no GDD — the game brief covers it (minimal = no required sections)
```

`system_overrides` is a map of `system_name: workflow_level`. The named system uses the override; all other systems use the project-level `workflow`.

---

### Affected skills

| Skill | How workflow_overrides changes behavior |
|-------|----------------------------------------|
| **design-system** | Reads `system_overrides[system_name]` first; falls back to project `workflow`. Applies override-specific section requirements. |
| **design-review** | Same lookup — validates against the override tier, not the project default, for the named system. |
| **art-bible** | If `art_bible_strict: true`, requires all 9 sections regardless of `workflow` level. |
| **gate-check** | Considers `system_overrides` when validating that all required GDDs are complete. A system at `system_overrides.combat: full` blocks the gate until all 8 sections exist for combat. |
| **review-all-gdds** | Validates each GDD against its effective tier (project workflow + any system override). |

---

## modes.automation

Values collaborative/guided/autonomous, default collaborative; local whitelist applies.
These are preferences for unresolved decisions, not permissions or authorization.
Collaborative presents material open options, guided asks for major open decisions,
autonomous makes justified choices within the authorized scope and records them.
Existing user decisions/actions remain authorized in every mode. Use actual host
input capabilities when a decision is missing; do not invent a widget/API or require
another per-file approval. Continue independent work while waiting for needed input.
Professional vision, budget, architecture, QA and release requirements still apply.
See .game-studio/resources/docs/automation-modes.md.

## modes.automation_always_ask

List of user-defined decision categories, default scope_changes/file_deletions/
schema_changes. Local override allowed. Categories include architecture_decisions,
version_bumps and external_calls when configured. Ask when an action in a configured
category is outside existing authorization; do not revoke authorization already given.
Native permissions still apply to commands, writes and external services. Record
actual consequential choices/options/reasons/evidence in production/session-logs/
decision-log.md when useful; no shell log_decision function exists. A saved checkpoint
or another agent's message supplies no new human consent.


## modes.story_granularity

**Controls:** How big each story is and how many stories per epic/sprint
**Values:** `coarse` | `balanced` | `fine`
**Default:** *none* — supplied by `modes.rigor` (`minimal`, the default, yields `coarse`; `standard` yields `balanced`; `full` yields `fine`)
**Set by:** `$gs-start` (via `modes.rigor`), `$gs-settings`
**Read by:** `$gs-create-epics`, `$gs-create-stories`, `$gs-dev-story`, `$gs-sprint-plan`, `$gs-story-done`, `$gs-sprint-status`

**Priority chain:** `modes.story_granularity` in `project.yaml` → `modes.rigor` expansion → *(no hardcoded default)*

---

### Value intent

| Value | Story shape | Stories per sprint | Best for |
|-------|-------------|-------------------|----------|
| `coarse` | 1 story = 1 feature. 3–5 days work each. 5–10 ACs per story. The default, from `rigor: minimal`. | 2–4 | Solo devs, prototyping, "I know what I'm building" |
| `balanced` | 1 story = 1 task. 1–2 days work each. 2–4 ACs per story. The `rigor: standard` value. | 6–10 | Most projects |
| `fine` | 1 story = 1 AC. Hours of work each. Easy code review. Frequent $gs-story-done. | 15–25 | Teams, learning, anything needing fine handoffs |

---

### Affected skills

| Skill | coarse | balanced | fine |
|-------|--------|----------|------|
| **create-epics** | Generates 3–5 child stories per epic | Generates 5–10 child stories per epic | Generates 10–20 child stories per epic |
| **create-stories** | Each story carries 5–10 ACs covering an entire feature | Each story carries 2–4 ACs covering one task | Each story carries 1 AC; story name = AC restatement |
| **dev-story** | Routing prompt expects multi-day implementation cycle. Subagent given longer working context. | Standard 1–2 day expectation. | Each story implementable in hours; subagent given tighter context. |
| **sprint-plan** | Allocates 2–4 stories per sprint based on velocity. | Allocates 6–10 stories per sprint. | Allocates 15–25 stories per sprint. |
| **story-done** | Fires every 3–5 days on average. | Fires every 1–2 days on average. | Fires multiple times per day. |
| **sprint-status** | Burn-down reads in feature-sized chunks. | Burn-down reads in task-sized chunks. | Burn-down reads in AC-sized chunks. |

---

## docs.density

**Controls:** How deep each section in authored docs goes — independent of which sections are required
**Values:** `terse` | `balanced` | `thorough`
**Default:** *none* — supplied by `modes.rigor` (`minimal`, the default, yields `terse`; `standard` yields `balanced`; `full` yields `thorough`)
**Set by:** `$gs-start` (via `modes.rigor`), `$gs-settings`
**Read by:** `$gs-design-system`, `$gs-art-bible`, `$gs-create-architecture`, `$gs-ux-design`, `$gs-map-systems`, `$gs-brainstorm`

**Priority chain:** `docs.density` in `project.yaml` → `modes.rigor` expansion → *(no hardcoded default)*

> **Distinct from `workflow`, but no longer independent by default.** `workflow`
> controls which sections exist; `density` controls how deep each section goes.
> `modes.rigor` now sets both together, so the diagonal (`rigor: full` → 8
> sections *and* thorough prose) is what you get without asking. The off-diagonal
> is still reachable and is the reason `rigor` overrides both ways: `rigor: full`
> + an explicit `docs.density: terse` gives "all sections but each is compact" —
> the "comprehensive but tight" mode, which neither knob expresses alone.

---

### Value intent

| Value | Per-section output style |
|-------|--------------------------|
| `terse` | Bullet points. 2–5 lines per section. Skip rationale and narrative framing. Skip preambles like "In this game..." Just facts needed to implement. The default, from `rigor: minimal`. |
| `balanced` | Paragraphs with light rationale. Examples where helpful. The `rigor: standard` value. |
| `thorough` | Full prose. Rationale for every decision. Examples, alternatives considered, design history. |

---

### Combination matrix with workflow

|  | docs.density: terse | balanced | thorough |
|---|---|---|---|
| **workflow: minimal** | Game brief in bullets *(default)* | Game brief in prose | Game brief + rationale |
| **workflow: standard** | 5 sections, bullets | 5 sections, paragraphs | 5 sections + examples |
| **workflow: full** | 8 sections, bullets *(comprehensive but compact)* | 8 sections, paragraphs *(current full)* | 8 sections + rationale + examples |

---

### Affected skills

| Skill | terse | balanced | thorough |
|-------|-------|----------|----------|
| **design-system** | Each GDD section is 2–5 bullets. Skip Player Fantasy preambles. | Paragraphs with key decisions explained. | Full prose, decision history, alternatives considered. |
| **art-bible** | Each art bible section is a bulleted list of constraints + references. | Paragraphs explaining each visual choice. | Full prose including style explorations, references, rationale per choice. |
| **create-architecture** | Layer diagrams + decision bullets. No essays. | Diagrams + paragraph explanations of layer choices. | Full prose with rationale, trade-offs, alternatives considered per layer. |
| **ux-design** | Wireframe descriptions + interaction bullets. | Wireframes + paragraph descriptions of flows. | Full prose including user research summaries, alternative flow considerations. |
| **map-systems** | One-line system descriptions. | Brief paragraph per system + dependency notes. | Full system-by-system rationale + relationship analysis. |
| **brainstorm** | Pillar bullets + concept bullets. | Pillars + concept with brief rationale. | Pillars + concept + extensive rationale + alternatives. |

---

## testing.framework

**Controls:** Which test framework the project uses — drives test-runner commands and per-engine assumptions in CI
**Values:** engine-specific (see table)
**Default:** auto-populated by `$gs-setup-engine` based on engine choice
**Set by:** `$gs-setup-engine`, `$gs-settings`
**Read by:** `$gs-test-helpers` — the only skill that references it. `$gs-qa-plan`, `$gs-dev-story`, `$gs-regression-suite`, `$gs-test-setup` and `$gs-smoke-check` do **not** name the key, despite being plausible readers.
  *(Derived by grep. A helper-based read such as `session_state_enabled()` would not show up, so treat this list as the verified floor, not a ceiling.)*

**Priority chain:** `testing.framework` in `project.yaml` → engine default

> **Migrated from `technical-preferences.md`.**

---

### Engine defaults

| Engine | Default test framework | Alternatives |
|--------|------------------------|--------------|
| Godot | `gdunit4` | `godot-test`, `WAT` |
| Unity | `unity-test-framework` | `nunit`, custom |
| Unreal | `unreal-automation` | Google Test, custom |

---

### Affected skills

| Skill | How `testing.framework` is used |
|-------|--------------------------------|
| **qa-plan** | Test plan tailored to framework's idioms (assertion style, fixture pattern, parameterized tests) |
| **dev-story** | Test framework name passed to programmer subagent in implementation brief |
| **regression-suite** | Test file naming and discovery patterns match framework conventions |
| **test-setup** | Scaffolds the right test layout for the engine (gdUnit4 under `addons/gdUnit4/` + `tests/` for Godot; `Assets/Tests/` asmdefs for Unity; `Source/<Module>/Private/Tests/` for Unreal) |
| **smoke-check** | Invokes framework-appropriate test runner |

---

## testing.strict

**Controls:** Whether failing or missing test evidence blocks a story from
closing, or produces a warning and lets work continue — per test type
**Values:** map of `{logic, integration, visual, ui, config}` → `true | false`
**Default:** `{logic: true, integration: true, visual: true, ui: true, config: false}`
**Set by:** `$gs-settings`
**Read by:** `story-done`, `story-readiness`, `gate-check`, `smoke-check`, `dev-story`, `test-evidence-review`

> **Per-type, not a single bool.** A global `testing.strict: true|false` forces
> all-or-nothing: either all test failures block or none do. Per-type matches how
> most teams actually work — strict logic and visual gates, an advisory smoke check.

> **Composes with `qa.level`:** `qa.level` controls whether evidence is REQUIRED.
> `testing.strict` controls whether failures BLOCK when evidence exists. If
> `qa.level: minimal`, the strict map is effectively ignored (no evidence required
> means nothing to be strict about).

---

### Value intent per type

| Type | `true` | `false` |
|------|--------|---------|
| `logic` (formulas, AI, state machines) | Unit test failures BLOCK — story cannot close | Failures WARN — story can close with warning |
| `integration` (multi-system) | Integration test failures BLOCK | Failures WARN |
| `visual` (animation, VFX, feel) | Missing/failing screenshot evidence BLOCKS (default) | Advisory only — story can close |
| `ui` (menus, HUD, screens) | Missing screenshot of the screen BLOCKS (default) | Advisory only — story can close |
| `config` (balance tuning) | Failing smoke check BLOCKS | Advisory only — story can close (default) |

---

### Affected skills

| Skill | strict.[type]: true | strict.[type]: false |
|-------|---------------------|----------------------|
| **story-done** | Story of that type cannot close on test/evidence failure | Story can close; warning logged in story file |
| **story-readiness** | Validates test requirements exist before implementation — blocks if absent | Validates but does not block — surfaces as warnings |
| **gate-check** | CI failures of that type block phase transition | CI failures of that type surfaced as concerns, not blockers |
| **smoke-check** | Failing smoke (config strict) blocks QA handoff | Failing smoke flagged but handoff proceeds |
| **dev-story** | References test requirements — flags story as unverifiable if absent | References test requirements — advisory only |
| **test-evidence-review** | A gap in that type's evidence is a BLOCKING item (the run ends CONCERNS) | The gap is ADVISORY |

> **Unset-key resolution.** Each skill reads `testing.strict.<type>`; if absent
> it reads `testing.strict` as a plain boolean (legacy form); if still absent it
> falls back to a hardcoded default. For `story-done`, `story-readiness`,
> `gate-check`, and `dev-story` the hardcoded default is the per-type default map
> above (logic/integration/visual/ui strict, config advisory). **`smoke-check` is
> the exception**: it is a build-health gate, so an unset `testing.strict.config`
> defaults to *strict* (a FAIL blocks QA hand-off) — preserving its v1.0 behavior.
> Only an explicit `testing.strict.config: false` makes a failing smoke advisory.

---

## qa.level

**Controls:** What test evidence is required to mark stories Done
**Values:** `minimal` | `standard` | `full`
**Default:** *none* — supplied by `modes.rigor` (`minimal`, the default, yields `minimal`; `standard` yields `standard`; `full` yields `full`)
**Set by:** `$gs-start` (via `modes.rigor`), `$gs-settings`
**Read by:** `$gs-story-done`, `$gs-story-readiness`, `$gs-dev-story`, `$gs-smoke-check`, `$gs-gate-check`, `$gs-qa-plan`, `$gs-regression-suite`, `$gs-team-qa`, `$gs-test-evidence-review`, `$gs-create-stories`, `$gs-retrospective`, `$gs-test-setup`

**Priority chain:** `qa.level` in `project.yaml` → `modes.rigor` expansion → *(no hardcoded default)*

> **Different axis from `testing.strict`.** `qa.level` = what evidence is required.
> `testing.strict` = do failures block. A user wanting "minimal QA" sets
> `qa.level: minimal` and the strict map becomes effectively a no-op.

---

### Value intent

| Aspect | minimal | standard | full |
|--------|---------|----------|------|
| Logic stories | No test required, no gap flagged | Unit test required (strict.logic controls block) | Unit test + coverage minimum |
| Integration stories | No test required | Integration test or playtest doc required | Same + regression coverage |
| Visual stories | Screenshot + lead sign-off required — the look is never waived (strict.visual controls block) | Same | Same |
| UI stories | Screenshot of each screen touched required — never waived (strict.ui controls block) | Same | Same |
| Config/Data stories | No evidence required | Smoke check advisory | Smoke check required |
| $gs-story-done test gate | Acceptance criteria only, except the UI and Visual/Feel screenshot, which is never waived | Enforced per story type | Enforced for every story type |
| $gs-gate-check phase enforcement | No test gates | Logic + integration must pass | Full coverage + regression suite |
| $gs-dev-story routing prompt | No "Test required: ..." line | Per-type test requirement included | Per-type + coverage target included |
| Regression suite required by | Never | Polish stage | Production stage |
| Best for | Jam games, throwaway prototypes, fast iteration | Most projects | Commercial, console cert, learning, paranoid teams |

---

### Affected skills

| Skill | minimal | standard | full |
|-------|---------|----------|------|
| **story-done** | Acceptance criteria check only — no test evidence required, except the UI and Visual/Feel screenshot, which is never waived | Per-type evidence required; strictness from `testing.strict` | All types require evidence; strictness from `testing.strict` |
| **story-readiness** | No test requirement validated, except the UI and Visual/Feel screenshot requirement | Test requirement per story type validated | Test requirement + coverage target validated |
| **dev-story** | Routing prompt has no "Test required" line | Per-type test requirement passed to programmer agent | Coverage target passed to programmer agent |
| **smoke-check** | Optional; with no game tests (WAIVED), `commands.smoke` (else `commands.build`) when set and the launch and critical-path checks carry the verdict; a build nobody launched is NOT ASSESSED | Required before phase transition | Required before every commit |
| **gate-check** | No test enforcement at phase transitions | Logic + integration tests must pass | Full coverage check + regression suite |
| **qa-plan** | Skipped entirely or minimal smoke plan | Full plan per story type | Full plan + coverage targets per system |
| **regression-suite** | Not generated | Generated at Polish stage entry | Generated at Production stage entry |
| **team-qa** | A Logic, Integration or Config/Data story without a test is WAIVED; its acceptance-criteria walk in manual QA is its evidence | The automated test is the evidence for those types | Same |
| **test-evidence-review** | A story with no test evidence is WAIVED, not MISSING; gaps in existing tests are ADVISORY; screenshots never waived | Per-type evidence reviewed; BLOCKING/ADVISORY from `testing.strict` | Same |

---

## qa.coverage_minimum

**Controls:** Minimum code coverage percentage enforced at `qa.level: full`
**Values:** integer 0–100, or `null` for unset
**Default:** `null`
**Set by:** `$gs-settings`
**Read by:** `$gs-gate-check` only. `$gs-story-done` does not reference the key, and no CI runner reads it.
  *(Derived by grep. A helper-based read such as `session_state_enabled()` would not show up, so treat this list as the verified floor, not a ceiling.)*

**Priority chain:** `qa.coverage_minimum` in `project.yaml` → no enforcement if `null`

> **Only meaningful at `qa.level: full`.** Ignored at minimal and standard. A
> non-null value at standard or minimal level emits a warning at session-start:
> *"coverage_minimum is set but qa.level is not full — value will not be enforced."*

> **Implementation is engine-specific.** Coverage measurement is different per engine:
> - Godot: gdunit4 coverage report (markdown export)
> - Unity: Unity Test Framework coverage (xml export)
> - Unreal: gcov-style coverage from clang flags
> CCGS does not unify these — gate-check reads the engine-appropriate report.

---

## strict_gate_checks

> ### RESERVED - NOT IMPLEMENTED
>
> **No skill or hook reads this setting. Setting it has no effect.** Everything
> below describes the intended design, not current behaviour.
>
> The value is checked for valid spelling when you set it, and then ignored.

**Controls:** Whether phase gate failures block stage transition or just warn
**Values:** `true` | `false`
**Default:** `true`
**Set by:** `$gs-settings`
**Read by:** nothing yet (intended reader: `$gs-gate-check`)

**Priority chain:** `strict_gate_checks` in `project.yaml` → hardcoded default of `true`

> **Different from `review_mode: solo`.** `review_mode: solo` skips the gate
> *entirely* — directors don't even run. `strict_gate_checks: false` runs the
> gate normally but treats the verdict as advisory.

---

### Value intent

| Value | Behavior |
|-------|----------|
| `true` | Default. FAIL or BLOCKING-CONCERNS verdict stops the stage transition. `project.stage` is not advanced. User must address findings and re-run gate. |
| `false` | All gate verdicts are advisory. `$gs-gate-check` still runs and reports findings. `project.stage` advances on user confirmation regardless of verdict. |

---

### Affected skills

| Skill | true | false |
|-------|------|-------|
| **gate-check** | FAIL verdict stops execution before writing new stage; CONCERNS verdict prompts user but defaults to "stay at current stage." | All verdicts surfaced as informational; user is asked "advance anyway?" with default Yes. |

---

## team.size

**Controls:** Which agents are active by default — solo devs shouldn't get studio-grade gating on every change
**Values:** `individual` | `small` | `studio`
**Default:** *none* — supplied by `modes.rigor` (`minimal`/`standard` yield `individual`, `full` yields `studio`)
**Set by:** `$gs-start` (via `modes.rigor`), `$gs-settings`
**Read by:** All `team-*` skills, `$gs-gate-check`, all skills that spawn agents via native delegation when authorized

**Priority chain:** `team.size` in `project.local.yaml` → `project.yaml` → the `modes.rigor` expansion (`full` → `studio`, else `individual`) → no terminal default. Locally overridable — it is a personal-experience knob, not an on-disk artifact.

> **`individual` at `minimal`/`standard`, `studio` at `full`.** CCGS's audience is
> overwhelmingly solo indie developers, so the two lighter rigor tiers resolve
> `team.size` to `individual` — a `minimal` (default) or `standard` project gets one active agent
> per role, not 15 (directors and leads included). Only `rigor: full` opts into the
> full `studio` roster; a smaller team on a big project sets `team.size: small`
> explicitly, which wins over the rigor-derived value.

> **Different axis from `workflow`.** `workflow` controls *what docs are required.*
> `team.size` controls *which agents exist to make them.* A solo dev on
> `workflow: full` still doesn't need all 49 agents — they need the same coverage
> from a smaller active set.

---

### Active agent set per value

| Value | Active set | Notes |
|-------|-----------|-------|
| `individual` | Core 8: `producer`, `game-designer`, `gameplay-programmer`, engine-specialist (engine-driven), `technical-artist`, `sound-designer`, `qa-tester`, `writer`. **Default.** | Directors and lead-* run only on explicit invocation (e.g. via `$gs-architecture-decision`). Specialists outside the core 8 routed through their nearest core agent. Each `team-*` skill names its own set per value, which can sit outside the core 8 (`team-release` runs `release-manager`); each skill's own `team.size` list is authoritative, and the Affected skills table below mirrors it. |
| `small` | Core 15: directors (CD, TD, PR) + leads (LP, AD, QL, ND) + game-designer + systems-designer + engine-specialist + technical-artist + sound-designer + qa-tester + ux-designer + writer | `team-*` skills add their `small` set (below); most reach their full pipeline only at `studio`. |
| `studio` | All 49 agents available. Engine sub-specialists (e.g. `unity-dots-specialist` separate from `unity-specialist`) routed when relevant. The adversarial review pass in `team-combat`, `team-ui` and `team-polish`. | Commercial titles, learning the full org chart, large teams with parallel work. |

---

### Affected skills

| Skill | individual | small | studio |
|-------|------|-------|--------|
| **team-combat** | Single agent (gameplay-programmer) runs the pipeline; ai-programmer escalated only if AI work flagged | Default pipeline as documented | Default + the primary engine specialist may use its sub-specialists + adversarial review pass (Phase 5's qa-tester looks for how it breaks) |
| **team-narrative** | writer only; narrative-director invoked only on explicit pillar conflict | narrative-director + writer, + localization-lead and world-builder at `review_mode: full` | All six narrative agents, whatever the review mode |
| **team-ui** | ui-programmer + ux-designer | + accessibility-specialist + art-director | + engine UI specialist + adversarial review pass (Phase 4's reviewers look for where it fails its spec) |
| **team-audio** | sound-designer only | + audio-director + technical-artist + gameplay-programmer | + accessibility-specialist + the primary engine specialist |
| **team-level** | level-designer only | + systems-designer + art-director + qa-tester | + narrative-director + world-builder + accessibility-specialist |
| **team-qa** | qa-tester only; qa-lead invoked at phase gates only | qa-lead + qa-tester pipeline | qa-lead + per-story qa-tester spawn + sign-off |
| **team-release** | release-manager only | + producer + devops-engineer + qa-lead + community-manager | + security-engineer + analytics-engineer + localization-lead + performance-analyst, and network-programmer when the game is multiplayer |
| **team-polish** | performance-analyst + technical-artist; no programmer is active, so Phase 2's optimisation list is handed to `$gs-dev-story` | + sound-designer + qa-tester + engine-programmer (implements Phase 2's optimisation list), and tools-programmer when Phase 1 traces a cause to a content authoring tool | engine-programmer, as at small, + adversarial review pass (Phase 5's qa-tester looks for how it breaks) |
| **team-live-ops** | live-ops-designer + economy-designer | + analytics-engineer + community-manager | + writer + narrative-director |
| **gate-check** | Panel width is `modes.workflow`'s axis, not this one (gates always run) — `team.size` affects only specialist depth within each director's review | Same as individual for directors; specialists within directors' reviews use small set | Same plus engine sub-specialists |
| **architecture-decision** | TD-ADR (in `full` review mode) + the primary engine specialist | Same | Same — no sub-specialist or adversarial reviewer at any size |

---

### Special cases

- `team.size` does not decide whether directors run: `$gs-gate-check`'s panel follows `review_mode` and `modes.workflow`, and no `team-*` pipeline spawns a director phase gate. In a team skill, a "phase gate" is one of the decision points its own pipeline lists, whatever the `automation` mode.
- `individual` does not disable agents — it just changes which are active by default. Any agent can still be invoked by name.
- When `team.size: individual` and a non-core agent is needed (e.g. `network-programmer` for a multiplayer story), the skill emits an informational note and routes through the nearest active core agent.

---

## platform.multiplayer

**Controls:** Whether the project includes real-time online multiplayer — determines
which specialists are routed and which architecture sections are required
**Values:** `true` | `false`
**Default:** none — unset is not `false`
**Set by:** `$gs-settings`
**Read by:** `security-audit`, `team-release` (and the `security-engineer` agent)

**Priority chain:** `platform.multiplayer` in `project.yaml` → unset (`platform.*` is locked to `project.yaml`, so `project.local.yaml` cannot set it). Nothing writes it except `$gs-settings`, so on most projects it is unset: `$gs-security-audit` and `$gs-team-release` ask whether the game is multiplayer rather than reading unset as `false`.

> **Distinct from `platform.online`.** `multiplayer` is *real-time multiplayer
> specifically* (network specialist, netcode review, replication architecture).
> `platform.online` covers everything else online (cloud saves, leaderboards,
> telemetry). See next section.

> **This is a project attribute, not a mode.** It describes what the game is,
> not how the pipeline operates. It lives in `platform` alongside `targets`,
> `primary_input`, and `gamepad_support` — not in `modes`.

---

### Value intent

| Value | Meaning |
|-------|---------|
| `true` | Game has real-time online multiplayer. `$gs-security-audit` runs its netcode category and rates a HIGH finding as release-blocking; `$gs-team-release` adds `network-programmer`'s sign-off. |
| `false` | No real-time multiplayer. `$gs-security-audit` skips the netcode category and says so; `$gs-team-release` does not spawn `network-programmer`. |

---

### Affected skills

| Skill | multiplayer: true | multiplayer: false |
|-------|------------------|-------------------|
| **security-audit** | Includes netcode review — authentication, replication, cheat vectors | Netcode review skipped, and the report says so |
| **team-release** | `network-programmer` included in release sign-off pipeline | `network-programmer` excluded |

No other skill reads this key: `$gs-dev-story`, `$gs-create-architecture` and `$gs-gate-check`
decide networking scope from the story, GDD or architecture in front of them.

---

## platform.online

**Controls:** Whether the project has any online features (leaderboards, cloud saves, telemetry, IAP)
**Values:** `true` | `false`
**Default:** none — unset is not `false`
**Set by:** `$gs-settings`
**Read by:** `security-audit`, `team-release` (and the `security-engineer` agent)

**Priority chain:** `platform.online` in `project.yaml` → unset (`platform.*` is locked to `project.yaml`, so `project.local.yaml` cannot set it). Nothing writes it except `$gs-settings`: `$gs-security-audit` and `$gs-team-release` ask rather than reading unset as `false`.

> **Independent of `platform.multiplayer`.** A single-player game with Steam
> Cloud and leaderboards is `online: true, multiplayer: false`. The two settings
> have different specialist routing implications.

---

### Value intent

| Value | Meaning |
|-------|---------|
| `true` | Project includes online services (cloud saves, leaderboards, achievements, telemetry, IAP, anything calling external APIs at runtime). `$gs-security-audit` runs Category 2 (network and multiplayer — including a plaintext-token check) when this or `platform.multiplayer` is true or unset; `$gs-team-release` adds a `security-engineer` sign-off. |
| `false` | Project is fully offline. `$gs-security-audit` skips Category 2 only when `platform.multiplayer` is also false. |

---

### Affected skills

| Skill | online: true | online: false |
|-------|--------------|---------------|
| **security-audit** | Category 2 (network) runs — server authority, packet validation, rate limits, plaintext tokens | Category 2 skipped only when `platform.multiplayer` is also false |
| **team-release** | `security-engineer` sign-off when the game is online or stores player data | No online-driven security sign-off |

No other skill reads this key: `$gs-create-architecture`, `$gs-dev-story`, `$gs-team-live-ops`
and `$gs-gate-check` decide online scope from the documents in front of them.

---

## platform.cert_tier

> ### WIRED — this setting is live
>
> `$gs-launch-checklist` and `$gs-release-checklist` both resolve it and branch on its
> four values — `none` emits no certification section, `itch` and `steam` their
> storefront's requirements, `console` full platform certification — and ask which
> platforms are in scope when it is unset.

**Controls:** Certification target — scopes what `$gs-launch-checklist` asks for
**Values:** `none` | `itch` | `steam` | `console`
**Default:** *none* — unset stays unset, so the skills ask
**Set by:** `$gs-settings` — nothing else writes it, so it stays unset (and the skills ask) until you set it
**Read by:** `$gs-launch-checklist`, `$gs-release-checklist`

**Priority chain:** `platform.cert_tier` in `project.yaml` → unset (no default is
substituted: unset is a missing decision, `none` is a made one, and the skills
must tell them apart)

---

### Value intent

| Value | Required compliance | Best for |
|-------|---------------------|----------|
| `none` | No certification — internal release, alpha, jam game | Default |
| `itch` | itch.io upload requirements (build size, page setup, age tags) | Indie web/desktop releases |
| `steam` | Steamworks integration, store page, achievements, depot build, system requirements, common content rules | Commercial PC releases |
| `console` | Platform certification (PlayStation/Xbox/Switch) — heavy compliance: TRC/XR/Lotcheck, save data rules, controller mapping rules, age rating boards | Console releases |

---

### Affected skills

| Skill | none | itch | steam | console |
|-------|------|------|-------|---------|
| **launch-checklist** | Internal launch only — no external requirements | + itch.io page setup, butler upload, build size | + Steamworks integration, store page, achievements depot, common content checks | + Platform-specific TRC, certification submission, console save format compliance |
| **release-checklist** | Smoke pass + version bump only | + itch.io page live, build uploaded to butler | + Steam store page live, depot pushed, achievements live | + Platform submission accepted, age rating boards cleared |
| **/pre-cert** (future) | Not applicable | Lightweight readiness check | Steam common content audit | Full TRC compliance audit |

---

## accessibility.target

> ### RESERVED - NOT IMPLEMENTED
>
> **No skill or hook reads this setting. Setting it has no effect.** Everything
> below describes the intended design, not current behaviour.
>
> The value is checked for valid spelling when you set it, and then ignored.
> The accessibility-specialist routing and the Polish-stage audit described
> below **do not happen at any level** — `$gs-team-ui`, `$gs-team-level`,
> `$gs-team-polish` and `$gs-gate-check` do not read this setting, and `$gs-start`
> does not ask for it.

**Controls:** Accessibility commitment level — routes accessibility specialist and gates audit requirements
**Values:** `none` | `standard` | `aaa`
**Default:** `none`
**Set by:** `$gs-settings`
**Read by:** nothing yet (intended readers: `$gs-team-ui`, `$gs-team-level`, `$gs-team-polish`, `$gs-gate-check`)

**Priority chain:** `accessibility.target` in `project.yaml` → hardcoded default of `none`

> **Default is `none`, not `standard`.** Most CCGS users are solo devs and jam-game
> makers — defaulting to `standard` would auto-spawn the accessibility specialist
> for projects where it's overhead. `$gs-start` asks the question explicitly so users
> who care can opt into `standard` or `aaa` consciously.

---

### Value intent

| Value | Required features | Specialist routing |
|-------|-------------------|--------------------|
| `none` | None enforced | `accessibility-specialist` not spawned |
| `standard` | Colorblind-safe palette, subtitles for any voice content, key remapping | `accessibility-specialist` runs in team-ui, team-level |
| `aaa` | Full Game Accessibility Guidelines: motor, vision, hearing, cognitive categories | `accessibility-specialist` runs in all team-* skills; mandatory audit at Polish stage |

---

### Affected skills

| Skill | none | standard | aaa |
|-------|------|----------|-----|
| **team-ui** | accessibility-specialist not spawned | accessibility-specialist included for HUD/menu reviews | accessibility-specialist included for every screen + accessibility audit pass |
| **team-level** | accessibility-specialist not spawned | accessibility-specialist reviews level for colorblind safety and signposting | accessibility-specialist reviews for full mobility/audio/cognitive considerations |
| **team-polish** | No accessibility pass | Final accessibility pass added | Full accessibility audit required before completion |
| **gate-check** | No accessibility check at any stage | Polish gate checks for the standard required features | Polish gate requires full Game Accessibility Guidelines compliance audit |

---

## cadence.sprint_length and cadence.milestone_length

> ### RESERVED - NOT IMPLEMENTED
>
> **No skill or hook reads this setting. Setting it has no effect.** Everything
> below describes the intended design, not current behaviour.
>
> No reference anywhere outside this file.

**Controls:** Default sprint and milestone durations for planning
**Values:**
- `sprint_length`: `1w` | `2w` | `3w` | `4w` | `none`
- `milestone_length`: `4w` | `6w` | `8w` | `12w`
**Defaults:** `sprint_length: 2w`, `milestone_length: 8w`
**Set by:** `$gs-settings`
**Read by:** nothing yet (intended readers: `$gs-sprint-plan`, `$gs-milestone-review`, `$gs-sprint-status`, future velocity tracking)

**Priority chain:** `cadence.*` in `project.yaml` → hardcoded defaults

> **`none` for `sprint_length`** means continuous-flow / kanban-style — no sprint boundaries.
> `$gs-sprint-plan` is then invoked manually as needed. Velocity tracking
> is per-week rather than per-sprint.

---

### Affected skills

| Skill | What changes |
|-------|--------------|
| **sprint-plan** | Capacity calculated as `sprint_length × team.size velocity baseline`. `none` makes the skill emit a continuous-flow plan instead. |
| **milestone-review** | Milestone window for retrospective scope = `milestone_length`. |
| **sprint-status** | Burn-down chart x-axis spans `sprint_length`. |
| **retrospective** | Sprint retro fires at `sprint_length` cadence (or weekly when sprint_length is `none`). |

---

## performance.target_framerate and performance.frame_budget_ms

**Controls:** The frame-rate target and its per-frame millisecond budget
**Values:** integers (e.g. `60`, `16.67`)
**Default:** none — unset means no budget was ever committed to
**Set by:** the user, by hand or via `$gs-settings`
**Read by:** `$gs-perf-profile`, `$gs-gate-check`, `$gs-team-polish`

## performance.draw_call_limit and performance.memory_ceiling_mb

**Controls:** Per-frame draw-call ceiling and total memory ceiling
**Values:** integers
**Default:** none — unset means no budget was ever committed to
**Set by:** the user, by hand or via `$gs-settings`
**Read by:** `$gs-perf-profile`, `$gs-gate-check`, `$gs-team-polish`

> **Every setting needs its own `## ` heading in this file, not just a table
> row.** The dead-settings audit derives what it checks from those headings, so
> a setting mentioned only inside a table is invisible to it — it can neither be
> reported DEAD if it loses its reader, nor caught if it gains one. A setting
> outside the audit's field of view is exactly how a documented-but-dead entry,
> or a working-but-listed-as-dead one, survives unnoticed.
>
> **Unset is not zero and not a default.** A budget nobody set is not a budget
> that was met — `$gs-perf-profile` must report `NOT ASSESSED` for a metric with no
> committed target rather than measuring against a placeholder. That exact
> failure (">99% headroom against a 16.67ms budget", from zero profiler data)
> is one of the two instances that motivated `.game-studio/resources/rules/skill-authoring.md`.

## performance.enforce

**Controls:** Whether performance budget violations warn or block
**Values:** `warn` | `block` | `off`
**Default:** `warn`
**Set by:** `$gs-settings`
**Read by:** `$gs-perf-profile`, `$gs-gate-check`, CI runner

**Priority chain:** `performance.enforce` in `project.local.yaml` → `project.yaml` → hardcoded default of `warn`, resolved by `explicit config command --keys performance.enforce`

> **Read it from the resolved block, never from `project.yaml` directly.** The key is on the `$gs-settings --local` whitelist. `$gs-perf-profile` Phase 0 and `$gs-gate-check` Section 3 are the two readers the table above promises — a key that is enum-validated, accepted and displayed while nothing reads it is exactly the failure this warning guards against.

> **Mirrors the `testing.strict` pattern.** Defines what happens when a budget
> defined in `performance.target_framerate`, `frame_budget_ms`, `draw_call_limit`,
> or `memory_ceiling_mb` is exceeded.

---

### Value intent

| Value | Behavior |
|-------|----------|
| `warn` | Default. Profile runs flag violations as findings. CI logs them but doesn't fail. `$gs-gate-check` surfaces them as concerns, not blockers. |
| `block` | Profile failures block CI. `$gs-gate-check` treats violations as FAIL verdict (Polish stage onward). |
| `off` | Performance budgets are informational only — no profile runs gated, no findings surfaced. |

---

## project.stage

**Controls:** The current development phase — determines which gate-check
validates and what artifacts are expected to exist
**Values:** `Concept` | `Systems Design` | `Technical Setup` | `Pre-Production` | `Production` | `Polish` | `Release`
**Default:** `Concept`
**Set by:** `$gs-gate-check` on a PASS, or on a CONCERNS the user explicitly accepts (the accepted risks are recorded); a FAIL never advances it — never set manually
**Read by:** `gate-check`, `project-stage-detect`, `help`, `day-one-patch`, `team-release`, `launch-checklist`, `release-checklist`, `map-systems`, `team-qa`, `adopt`

> **Stage count:** This document uses the
> 7-stage reality implemented by gate-check:
> `Concept | Systems Design | Technical Setup | Pre-Production | Production | Polish | Release`

> **This is a project attribute, not a mode.** It records where the project is
> in its lifecycle. Only `$gs-start` (at onboarding) and `$gs-gate-check` write it —
> `$gs-gate-check` on a PASS verdict with user confirmation, or on a CONCERNS
> verdict whose risks the user explicitly accepts (they are recorded); a FAIL never advances it.
> Never write it manually mid-session except to correct an incorrect auto-detect.

> **Native stage resolution.** Explicit project.stage wins; legacy production/stage.txt is fallback data only. start/gate-check update the authorized project leaf, never create a new mirror. Stale mirrors are reported by config.

---

### Stage progression and gate requirements

Each row is the gate that must be passed to advance FROM that stage.

| From stage | Key artifacts required to pass | gate-check writes |
|------------|-------------------------------|-------------------|
| **Concept** | `game-concept.md`, design pillars, Visual Identity Anchor | `Systems Design` |
| **Systems Design** | `systems-index.md`, all MVP GDDs reviewed, cross-GDD consistency check | `Technical Setup` |
| **Technical Setup** | Engine configured, art bible sections 1–4 (at `standard`, only if visual stories exist), 3+ ADRs, architecture doc, traceability index, test framework, accessibility and interaction-pattern docs | `Pre-Production` |
| **Pre-Production** | Epics defined, first sprint plan, UX specs, control manifest (a Vertical Slice is recommended, not required) | `Production` |
| **Production** | Core mechanics implemented, main path playable, smoke check passes, QA sign-off | `Polish` |
| **Polish** | All features complete, content complete, localization, security audit, no open S1–S3 bugs | `Release` |

Gates adjust per `modes.workflow` — see `modes.workflow` section for what is
required at `standard` and `minimal` levels.

---

### Affected skills

| Skill | How it uses stage |
|-------|------------------|
| **gate-check** | Reads current stage to determine which gate to validate. Writes next stage on PASS, or on a CONCERNS the user explicitly accepts. |
| **project-stage-detect** | Reads `project.stage` first — if set, uses it as authoritative. Falls back to heuristic detection only if absent. |
| **help** | Uses stage to determine "where are you in the pipeline" and surfaces the correct next steps. |
| **sprint-status** | Displays current stage in status summary. |
| **day-one-patch** | Proceeds only when the stage is `Release` or `Polish`; otherwise says it is not appropriate yet. |
| **team-release** | Stops before Phase 1 unless the stage is `Release` ("run `$gs-gate-check release` first"); proceeding takes an explicit override, recorded in the go/no-go record and the report. Never writes the stage. |

---

## project.kind

> ### RESERVED - NOT IMPLEMENTED
>
> **No skill or hook reads this setting. Setting it has no effect.** Everything
> below describes the intended design, not current behaviour.
>
> No reference anywhere outside this file.

**Controls:** What type of project this is — routes skill subsets
**Values:** `game` | `tool` | `engine` | `mod` | `library`
**Default:** `game`
**Set by:** `$gs-start`, `$gs-setup-engine`
**Read by:** Many skills (advisory routing — see below)

**Priority chain:** `project.kind` in `project.yaml` → hardcoded default of `game`

---

### Value intent

| Value | Meaning | What's deactivated |
|-------|---------|-------------------|
| `game` | Default. Full CCGS framework applies. | Nothing |
| `tool` | Developer tool, not a game | Skip art bible, narrative, level design, playtesting |
| `engine` | Custom engine or library underneath games | Skip game-specific concerns entirely (narrative, art, playtest) |
| `mod` | Mod for an existing game | Skip engine setup; assume parent engine; reduce architecture scope |
| `library` | Reusable library | Emphasize tests + API design; design docs lighter; no asset pipeline |

---

### Affected skills

| Skill | game | tool | engine | mod | library |
|-------|------|------|--------|-----|---------|
| **brainstorm** | Full game-concept output | Tool concept output (user, problem, solution) | Engine concept (target use cases, scope) | Mod concept (what changes) | Library concept (API surface, target consumers) |
| **art-bible** | Required at appropriate workflow level | Skipped | Skipped | Optional (depends on visual scope) | Skipped |
| **map-systems** | Full game systems decomposition | Tool subsystems | Engine subsystems | Modified-system map | Library module map |
| **playtest-report** | Required at appropriate stages | Skipped or replaced with user testing | Skipped | Required (compatibility testing) | Skipped or replaced with API usage testing |
| **setup-engine** | Game engine setup | Skipped or replaced with build tool setup | Self-referential — engine IS the project | Parent engine assumed | Skipped or replaced with library scaffolding |

---

## engine.name and specialists

**Controls:** Which engine-specific specialist agents are routed to for code
implementation, review, and architecture validation
**Values:** any nonempty project engine name; built-in reference/specialist families: `Godot`, `Unity`, `Unreal`
**Default:** `[UNSET]` — must be configured via `$gs-setup-engine`
**Set by:** `$gs-setup-engine`
**Read by:** `dev-story`, `code-review`, `architecture-decision`, `create-architecture`, `team-combat`, `team-ui`, `team-audio`

> **Currently stored in `technical-preferences.md`**, not `project.yaml`. After
> YAML expansion, `engine.name` and the specialist routing table move to
> `project.yaml specialists` block. Skill behavior is unchanged — only the
> source file changes.

> **This is a project attribute, not a mode.** Engine choice drives specialist
> routing the same way `platform.multiplayer` drives network routing — skills
> respond to a fact about the project, not a process preference.

---

### Specialist routing by engine

| Engine | Language/code specialist | Shader specialist | UI specialist | Additional specialists |
|--------|--------------------------|-------------------|---------------|----------------------|
| **Godot** | `godot-gdscript-specialist` (GDScript) or `godot-csharp-specialist` (C#) — driven by `engine.language` | `godot-shader-specialist` | `godot-specialist` | `godot-gdextension-specialist` |
| **Unity** | `unity-specialist` | `unity-shader-specialist` | `unity-ui-specialist` | `unity-addressables-specialist`, `unity-dots-specialist` |
| **Unreal** | `unreal-specialist` | `unreal-specialist` | `ue-umg-specialist` | `ue-gas-specialist`, `ue-blueprint-specialist`, `ue-replication-specialist` |
| **[UNSET]** | No specialist spawned — warning emitted | No specialist spawned | No specialist spawned | None |

---

### Affected skills

| Skill | How engine.name is used |
|-------|------------------------|
| **dev-story** | Routes code stories to language specialist. Spawns engine specialist alongside for HIGH engine-risk stories or engine-specific API usage. |
| **code-review** | Routes review to language, shader, or UI specialist based on file type being reviewed. |
| **architecture-decision** | Loads `<project-engine-reference>/VERSION.md` before authoring. Spawns engine specialist to validate ADR for API correctness and post-cutoff compatibility. |
| **create-architecture** | Includes engine-specific constraints and patterns in architecture doc based on engine choice. |
| **team-combat / team-ui / team-audio** | Spawn the engine specialist their pipeline names: team-combat the primary engine specialist (from `team.size: small`), team-ui the engine UI specialist (`specialists.ui`, at `studio`), team-audio the primary engine specialist (at `studio`). The other six `team-*` skills spawn none. |

---

## commands

> **Live since the run-and-observe step.** This block was RESERVED — written by
> `$gs-setup-engine`, read by nothing — through most of v1.1. `test`, `smoke` and
> `build` gained readers as the parse-check and smoke gates landed; `run` gained
> its reader last, when `$gs-dev-story` Phase 6 step 4 started launching the game to
> look at it. The per-skill table at the bottom is now current behaviour, not
> intent. `validate-push.sh` was once named as a reader and never was.

**Controls:** Explicit shell commands to build, test, run, and smoke-test the project
**Values:** strings — shell-executable commands
**Default:** `[UNSET]` — populated by `$gs-setup-engine` with engine-typical defaults
**Set by:** `$gs-setup-engine`, `$gs-settings`
**Written by:** `$gs-setup-engine`, `$gs-settings`. **Read by:** `test` — `$gs-smoke-check`, `$gs-hotfix` (narrowed to the affected suite), `$gs-bug-report` (verify mode, narrowed to the affected suite), `$gs-day-one-patch` (targeted fix and, when set, the broader regression — NOT ASSESSED if unset), `$gs-dev-story` (Godot parse-check executable resolution), `$gs-test-setup` (the `<Project>.` filter root on Unreal), `coherence command`; `smoke` — `$gs-dev-story` (Unity parse check), `$gs-smoke-check` (build check when tests are WAIVED); `build` — `$gs-smoke-check` (build check when tests are WAIVED and `smoke` is unset), `coherence command`; `run` — `$gs-dev-story` (Phase 6 step 4, the run-and-observe step). `$gs-launch-checklist` and `$gs-regression-suite` name these commands but do not run them.
  *(Derived by grep. A helper-based read would not show up, so treat this list as the verified floor, not a ceiling.)*

**Priority chain:** `commands.*` in `project.yaml` → engine-typical default → no command available

> **Why explicit:** Without this block, CCGS has to guess engine-typical conventions
> for invoking the project. Better to be explicit per-project — covers cases where
> projects customize their build (e.g., a Godot project using gdunit4 for tests but
> a custom export script for builds).

---

### Fields

Each command can be a simple string (used on all OSes) or an OS-aware map:

**Simple form** (one command, used on every OS):
```yaml
commands:
  build: "godot --headless --export-debug '<PRESET>'"   # ask; see the note below
  test:  "godot --headless -s -d --remote-debug tcp://127.0.0.1:0 res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://tests --ignoreHeadlessMode"
  run:   "godot --path . --windowed --resolution 1280x720"
  smoke: "godot --headless --quit-after 5"
```

Note that `build` is the one row the simple form suits least: an export preset
names a *platform*, so a single build string is portable only for a project that
builds one platform. The other three rows are genuinely OS-independent.

**OS-aware form** (different commands per OS):
```yaml
commands:
  build:
    default: "godot --headless --export-debug 'Linux/X11'"
    windows: "godot.exe --headless --export-debug 'Windows Desktop'"
    macos:   "godot --headless --export-debug 'macOS'"
  test:
    default: "godot --headless -s -d --remote-debug tcp://127.0.0.1:0 res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://tests --ignoreHeadlessMode"
  run:
    default: "godot --path . --windowed --resolution 1280x720"
  smoke:
    default: "godot --headless --quit-after 5"
```

**Resolution rule:** if the value is a string, use it as-is on any OS. If the
value is a map, skills/hooks read the current OS and pick the matching key
(`linux`, `windows`, `macos`). Fall back to `default` if no OS-specific key
matches.

This solves the Windows/Linux/macOS path-and-binary-name differences without
breaking the whitelist (commands stays locked to project.yaml — the OS-specific
keys are inside the locked file, not a local override).

| Field | Purpose |
|-------|---------|
| `build` | Full project build for CI or release. `$gs-smoke-check` runs it only as the WAIVED-path build check when `commands.smoke` is unset; `coherence command` (which `$gs-smoke-check` runs first) checks the export preset it names, and `$gs-launch-checklist` only asks whether the build produces a valid artifact. |
| `test` | Run the full test suite. Run by `$gs-smoke-check` and, narrowed to the affected suite, by `$gs-hotfix`, `$gs-bug-report` (verify mode) and `$gs-day-one-patch`; `coherence command` checks the runner it names. `$gs-regression-suite` does **not** run it. |
| `run` | Launch the **game** windowed at a fixed resolution — not the editor. Used by `$gs-dev-story` Phase 6 step 4 to observe the feature and retain a screenshot; see `.game-studio/resources/docs/run-and-observe.md` for the per-engine capture flags that are appended to it. |
| `smoke` | Minimal "does it boot?" check. Run by `$gs-dev-story` as the Unity parse check (Phase 6 step 2), and by `$gs-smoke-check` as the build check when `qa.level: minimal` waives tests. |

---

### Engine defaults

When `$gs-setup-engine` runs, it populates `commands` based on engine choice — except
the **build** row, which it must **ask** for. The build artifact is named by a
project-defined string (a Godot export preset, a Unity build target), and no
engine reference in this repo can source it. See `$gs-setup-engine` §"The Godot
`build` row must not hardcode `'Linux/X11'`".

| Engine | build | test | run | smoke |
|--------|-------|------|-----|-------|
| Godot | `godot --headless --export-debug '<PRESET>'` | `godot --headless -s -d --remote-debug tcp://127.0.0.1:0 res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://tests --ignoreHeadlessMode` | `godot --path . --windowed --resolution 1280x720` | `godot --headless --quit-after 5` |
| Unity | `"<Unity editor>" -batchmode -quit -projectPath . -buildTarget <TARGET> -build<PLATFORM>Player Builds/<Target>/<Game>.exe` | `"<Unity editor>" -batchmode -runTests -projectPath . -testPlatform EditMode -testResults test-results/editmode.xml` | `Builds/<Target>/<Game>.exe -screen-width 1280 -screen-height 720 -screen-fullscreen 0` | `"<Unity editor>" -batchmode -quit -projectPath . -logFile -` |
| Unreal | `"<UE root>/Engine/Binaries/DotNET/AutomationTool/AutomationTool.exe" BuildCookRun -project="$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -platform=Win64 -build -cook` (confirm per project) | `"<UE root>/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -ExecCmds="Automation RunTests <project>.; Quit" -unattended -nullrhi -stdout -FullStdOutLogOutput` | `"<UE root>/Engine/Binaries/Win64/UnrealEditor.exe" "$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -game -windowed -ResX=1280 -ResY=720` | `"<UE root>/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$(pwd -W 2>/dev/null || pwd)/<project>.uproject" -game -nullrhi -unattended -stdout -ExecCmds="Quit"` |

The Unreal row is Windows'. `$gs-setup-engine` writes the Linux block (`Engine/Build/BatchFiles/RunUAT.sh`,
`Engine/Binaries/Linux/UnrealEditor`) on Linux, and on macOS only `build`, leaving `test`, `run` and
`smoke` as TODOs — see `<project-engine-reference>/current-best-practices.md`, "Command Line".

> **`<PRESET>` and `<TARGET>` are placeholders, not values to copy.** A Godot
> export preset is whatever string the operator typed into `export_presets.cfg`;
> the shipped defaults are per-platform (`Windows Desktop`, `macOS`, `Web`,
> `Linux/X11`). Copying a preset name you do not have gives you a build command
> that fails with `Unknown export preset`; copying one you *do* have, but did not
> mean, gives you a command that succeeds and builds the wrong platform. The
> second is the dangerous one. If no presets exist yet — common, since
> `$gs-setup-engine` usually runs before the project has any — write
> `[TO BE CONFIGURED]` rather than guessing a name.

Users override per-project as needed via `$gs-settings commands.<field>=<value>` or by editing `project.yaml` directly.

---

### Affected skills

| Skill | How `commands` is used |
|-------|------------------------|
| **smoke-check** | Runs `commands.test`, or the engine's default when it is unset; on Unreal it builds the editor target first. Critical path for QA hand-off. |
| **launch-checklist** | Emits a checklist **item** asking whether the build produces a valid artifact. It does **not** run `commands.build`; the verification is a human step. |
| **validate-push.sh** | Does **not** read `commands.*`. It warns on pushes to protected branches (`main`/`master`/`release/*`) and runs no build or smoke command — the block path in it is commented out, so it never fails a push. |
| **dev-story** | Phase 6 step 2 is the parse check: `<project-provided Godot parse adapter>` on Godot, `commands.smoke` on Unity, the editor-target build on Unreal. Phase 6 step 4 runs `commands.run` — the windowed game launch — to observe the feature and retain a screenshot (`.game-studio/resources/docs/run-and-observe.md`). |
| **regression-suite** | Maps coverage by **globbing test filenames**. It does **not** invoke `commands.test`, so coverage here means "a test file exists", never "a test passed". |

---

## naming

**Controls:** Code naming conventions for the project
**Values:** see field list below
**Default:** engine-specific (auto-populated by `$gs-setup-engine`)
**Set by:** `$gs-setup-engine`, `$gs-settings`
**Read by:** `$gs-adopt`, `$gs-architecture-review`, `$gs-asset-spec`,
`$gs-create-architecture`, `$gs-create-control-manifest`, `$gs-dev-story`,
`$gs-vertical-slice` — each reads `naming.*` from `project.yaml` and feeds the
conventions into a brief, manifest or spec. **NOT by `$gs-code-review` and NOT by
`validate-commit.sh`**.
  *(Reader list derived by grep, so treat it as the verified floor rather than
  a ceiling — a skill reading the value through a helper would not show up.)*

> **These conventions are guidance, not a gate.** They reach your project by
> being passed into briefs, manifests and specs for whoever writes the code.
> Nothing checks the result: `$gs-code-review` does not validate files against them
> and `validate-commit.sh` does not warn on violations — neither contains any
> naming logic. If you need enforcement, it has to be added.
>
> **Known rough edge — asset filenames.** `validate-assets.sh` warns unless files
> under Godot's `assets/` are lowercase-with-underscores, and it takes no config
> input, while `$gs-asset-spec` specifies asset names from `naming.*`. Unity's
> `Assets/` and Unreal's `Content/` are not naming-checked: those engines name
> assets in PascalCase. On Godot-C#, where `$gs-setup-engine` sets
> `naming.files: PascalCase`, the hook will warn on assets named exactly as
> `$gs-asset-spec` specified them. The two are
> measuring different things — `naming.files` describes **source** files by its
> own examples (`PlayerController.cs`), and no key currently governs asset
> filenames — so treat the hook's naming warning as advisory on those engines.

> **Moved from `technical-preferences.md`**, which is being deleted. Naming
> conventions are project-level facts shared by everyone on the project, so they
> belong in `project.yaml` alongside the rest of your structured config.

---

### Fields

| Field | Values | Godot default | Unity default | Unreal default |
|-------|--------|---------------|---------------|----------------|
| `classes` | `PascalCase` \| `snake_case` \| `camelCase` | PascalCase | PascalCase | PascalCase |
| `variables` | `snake_case` \| `camelCase` | snake_case | camelCase | camelCase |
| `constants` | `SCREAMING_SNAKE` \| `PascalCase` | SCREAMING_SNAKE | SCREAMING_SNAKE | SCREAMING_SNAKE |
| `signals` (Godot) / `events` (Unity, Unreal) | `past_tense` \| `on_event_name` | past_tense | on_event_name | OnEventName |
| `files` | `snake_case` \| `PascalCase` \| `kebab-case` | snake_case | PascalCase | PascalCase |
| `scenes` / `prefabs` | `snake_case` \| `PascalCase` | snake_case | PascalCase | PascalCase |

> **`signals` vs `events`:** Godot uses signals natively; Unity uses C# events
> or UnityEvents; Unreal uses delegates and dynamic multicast. The field stays
> named `signals` in project.yaml for consistency across engines — interpret as
> "event-like callbacks" regardless of engine.

---

### Affected skills

| Skill | How naming is used |
|-------|--------------------|
| **dev-story** | Passes the naming conventions to the programmer subagent as part of the implementation context |
| **create-control-manifest** | Emits the conventions as manifest rows (classes, variables, signals/events, files, constants) |
| **asset-spec** | Specifies asset naming per the configured convention |
| **create-architecture** / **architecture-review** | Read as project config alongside `performance.*` |
| **vertical-slice** / **adopt** | Read as project config; `$gs-adopt` audits conformance at MEDIUM severity |

No skill or hook validates code *against* these conventions — see the note above.

---

## features.session_state

on enables explicit recover/checkpoint helpers and optional trusted hook recovery.
off disables checkpoint recovery/saving. Resolve .game-studio/context.json checkpoint
and records through recover; default production/session-state/active.md. Custom paths
and bounded records are confined to the repository. Skills author current snapshots
via checkpoint --save; the runtime keeps a hash-named prior snapshot. Hooks cannot
infer work, scrape transcripts, rotate unseen state or complete a task. See
.game-studio/resources/docs/context-management.md and templates/session-state.md.


## features.token_budget_warn_at

> ### RESERVED - NOT IMPLEMENTED
>
> **No skill or hook reads this setting. Setting it has no effect.** Everything
> below describes the intended design, not current behaviour.
>
> The value is checked for valid spelling when you set it, and then ignored.
> Nothing warns at any threshold.

**Controls:** Context usage threshold at which session warnings fire
**Values:** float between 0.0 and 1.0
**Default:** `0.7` (warn at 70%)
**Set by:** `$gs-settings`
**Read by:** nothing yet (intended readers: `pre-compact.sh`, `session-start.sh`, `statusline.sh`)

**Priority chain:** `features.token_budget_warn_at` in `project.yaml` → hardcoded default of `0.7`

> Surfaces a warning when session context usage exceeds the threshold. Helps
> cost-conscious users hit `/clear` before runaway sessions. Set to `1.0` to
> disable.

---

### Behavior

| Threshold | What fires |
|-----------|-----------|
| Below `warn_at` | No warning |
| At or above `warn_at` | `statusline.sh` shows context usage in yellow; next session-start hook emits a one-line note: *"Last session reached [X]% context — consider /clear if continuing work."* |
| At 90%+ | Yellow becomes red regardless of `warn_at` value |

---

## schema_version and framework metadata

schema_version is project metadata, not an automatic migration trigger. Unknown
optional project leaves are retained by config resolution; malformed YAML is rejected.
Installer state/release manifest supplies the installed framework version. framework
version/date fields in project.yaml are informational and are never used to skip
manifest integrity/conflict checks. No skills run legacy migration or --finalize.

## Legacy preference reconciliation

Use gs-adopt to explicitly inspect old stage/review/technical-preference records,
propose a mapping to current project.yaml and review the resulting diff. Preserve
unknown/custom values for human reconciliation. Runtime supports only stage/review
text fallbacks when the current leaf is absent; an explicit project leaf wins and a
stale mirror is reported. It never converts Markdown, refuses split-brain wholesale,
deletes legacy files, or claims a conversion report was executed. Keep old files
until their contents are actually reconciled and deletion is authorized.


## Complete example `project.yaml`

A full project.yaml with every setting, showing sensible defaults for a solo
Godot project. Use this as the reference shape when authoring or migrating.

```yaml
schema_version: 1

framework:
  version: "1.1.0"
  last_upgraded: "2026-05-15"

project:
  name: "Forge Knights"
  genre: "ARPG"
  version: "0.1.0"
  stage: Concept             # Concept | Systems Design | Technical Setup | Pre-Production | Production | Polish | Release
  kind: game                 # game | tool | engine | mod | library

modes:
  review_mode: lean          # full | lean | solo
  workflow: standard         # minimal | standard | full
  automation: collaborative  # collaborative | guided | autonomous
  automation_always_ask:     # decision categories that prompt only when existing authorization does not cover the material action
    - scope_changes
    - file_deletions
    - schema_changes
  story_granularity: balanced  # coarse | balanced | fine

# TOP-LEVEL, not nested under `modes:` — explicit config command reads
# `workflow_overrides.system_overrides.*` from the document root
# (native config resolver), and every skill greps the same top-level path.
# Nesting it under `modes:` parses as valid YAML and is silently never read.
workflow_overrides:
  edge_cases: false          # force GDD Edge Cases section required
  tuning_knobs: false        # force GDD Tuning Knobs section required
  art_bible_strict: false    # force all 9 art bible sections regardless of asset stories
  system_overrides: {}       # { combat: full, inventory: minimal }

docs:
  density: balanced          # terse | balanced | thorough

testing:
  framework: gdunit4         # engine-specific — auto-populated by $gs-setup-engine
  strict:
    logic: true              # unit test failures BLOCK story closure
    integration: true        # integration test failures BLOCK
    visual: true             # missing screenshot BLOCKS
    ui: true                 # missing screenshot BLOCKS
    config: false            # advisory only

qa:
  level: standard            # minimal | standard | full
  coverage_minimum: null     # integer 0-100; only enforced at level: full

strict_gate_checks: true     # phase gate failures block stage transition

team:
  size: individual           # individual | small | studio

platform:
  multiplayer: false         # real-time multiplayer
  online: false              # any online features (leaderboards, cloud, telemetry)
  targets: [PC]              # [PC, Mobile, Web, Console]
  primary_input: "Keyboard/Mouse"
  gamepad_support: "Full"    # Full | Partial | None
  touch_support: "None"      # Full | Partial | None
  cert_tier: none            # none | itch | steam | console

engine:
  name: "Godot"              # Godot | Unity | Unreal — set by $gs-setup-engine
  version: "4.6"
  language: "GDScript"       # GDScript | C# | C++ | Blueprint
  rendering: "Forward+"
  physics: "Jolt"

specialists:                 # auto-populated by $gs-setup-engine
  code: "godot-gdscript-specialist"
  shader: "godot-shader-specialist"
  ui: "godot-specialist"
  additional: ["godot-gdextension-specialist"]

naming:
  classes: PascalCase        # PascalCase | snake_case | camelCase
  variables: snake_case
  constants: SCREAMING_SNAKE
  signals: past_tense        # past_tense | on_event_name (engine-interpreted)
  files: snake_case
  scenes: snake_case

accessibility:
  target: none               # none | standard | aaa

cadence:
  sprint_length: "2w"        # 1w | 2w | 3w | 4w | none
  milestone_length: "8w"     # 4w | 6w | 8w | 12w

performance:
  target_framerate: 60
  frame_budget_ms: 16.67
  draw_call_limit: null
  memory_ceiling_mb: null
  enforce: warn              # warn | block | off

commands:                    # simple string OR OS-aware map per command
  build: "godot --headless --export-debug '<PRESET>'"   # your export_presets.cfg name
  test: "godot --headless -s -d --remote-debug tcp://127.0.0.1:0 res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://tests --ignoreHeadlessMode"
  run: "godot --path . --windowed --resolution 1280x720"
  smoke: "godot --headless --quit-after 5"

features:
  session_state: on          # off | on
  token_budget_warn_at: 0.7  # 0.0-1.0; warn at this context % usage
```

And a minimal sparse `project.local.yaml` example — a single developer who wants autonomous mode locally:

```yaml
modes:
  automation: autonomous
features:
  session_state: on
```

Only the overridden keys are present; everything else cascades from `project.yaml`.
See "Local Override Pattern" section for full whitelist of what can/cannot be overridden locally.
