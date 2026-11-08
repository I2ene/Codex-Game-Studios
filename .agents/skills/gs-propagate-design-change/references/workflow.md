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

# Propagate Design Change

Every `ask the user` call follows `.game-studio/resources/docs/automation-modes.md`
(collaborative resolves open choices · guided resolves major choices · autonomous records in-scope choices;
`automation_always_ask` categories require input only outside existing authorization — ADR/schema impacts here fall
under `schema_changes` and `architecture_decisions`).

**Workflow tier**: resolve for the **changed GDD's system** (per
`.game-studio/resources/docs/workflow-modes.md`): use the
`system_overrides` row for that system if the block lists one, else the
project value. (A system pinned `minimal` has no ADRs even on a `standard`
project — so its change is N/A.) It scopes the cascade: `full` cascades across all
ADRs; `standard` checks only critical (Foundation-layer) ADRs plus any ADR
referencing the changed GDD; `minimal` is **not applicable** — no ADRs to cascade.
See Step 4.

Asks follow `.game-studio/resources/docs/automation-modes.md` (collaborative resolves open decisions, guided
asks on major choices, autonomous logs and goes on; `automation_always_ask`
categories always ask: an ADR impact here is `schema_changes` and
`architecture_decisions`).

**Tier.** `workflow` for the changed GDD's system: its `system_overrides` row if
there is one, else the project value. A system pinned `minimal` has no ADRs even on
a `standard` project. `full` checks every ADR; `standard` checks the critical
(Foundation-layer) ADRs and any ADR that names the changed GDD; `minimal` has
nothing to check (Phase 4).

## Phase 1: The GDD path

The text typed after the skill name, with any `--review <mode>` pair removed, is the
changed GDD. It is required. Missing: "Usage: `$gs-propagate-design-change
design/gdd/[system].md` — give the path to the GDD that changed." Not a file:
"[path] not found. Check the path and try again."

## Phase 2: What changed

Ask git, never compare two whole documents by eye:

```bash
git diff HEAD -- design/gdd/[filename].md
```

Empty: the change may be committed already, so widen to the last commit that
touched it: `git diff HEAD~1 HEAD -- design/gdd/[filename].md`.

- No history at all (`git log --oneline -1 -- design/gdd/[filename].md` prints
  nothing): "No previous version in git — this is a new GDD, not a revision.
  Nothing to propagate." Stop.
- History, but both diffs empty: report "no uncommitted or last-commit changes to
  `[file]`" and ask which revision to propagate. An empty diff means nothing changed
  *here*, not that nothing is affected.

From the hunks: the `@@` headers name the section each change sits in, so the
changed-section list comes from the diff itself. A section with no hunk is unchanged
by construction. Read the surrounding section only when a hunk cannot be understood
alone (a changed number whose meaning depends on the rule above it), and then only
that section: `python .game-studio/runtime/studio.py markdown --root <project-root> extract design/gdd/[file].md "[Section]"`.

## Phase 3: The change summary

```
## Change Summary: [GDD filename]
Date of revision: [today]

Changed sections:
- [Section]: [what changed — new rule, removed rule, formula modified, …]

Unchanged sections:
- [Section]

Key changes affecting architecture:
- [change likely to affect ADRs]
```

**Downstream GDD impact via the registry.** If `design/registry/entities.yaml`
exists, it already records which other GDDs depend on this system's facts —
compute the affected set from it rather than re-reading every GDD:
```
Grep pattern="source: design/gdd/[filename]" path="design/registry/entities.yaml" output_mode="content" -A 6
```
For each entity/constant/formula this GDD **owns** whose value the diff changed,
its `referenced_by:` list is the set of downstream GDDs that may now be
inconsistent — report them under "Downstream GDDs to re-check". **If
`design/registry/entities.yaml` does not exist or has no entries** (it ships as
an empty stub until `$gs-design-system` populates it), skip this — the ADR cascade
below still runs.

---

## 4. Load Architecture Inputs

Read ADRs in `docs/architecture/` **per the resolved tier**:
- **`full`** — read **all** ADRs.
- **`standard`** — read only **critical (Foundation-layer) ADRs** plus any ADR
  that references the changed GDD. An ADR is critical when the `**Layer**` row of
  its `## Engine Compatibility` table says `Foundation`, or when it has no
  `**Layer**` row — when in doubt, treat it as critical
  (`.game-studio/resources/docs/workflow-modes.md`). Read every row in one call:
  `Grep pattern="\*\*Layer\*\*" glob="docs/architecture/adr-*.md" output_mode="content"`,
  and count an ADR that Grep does not list as critical.
- **`minimal`** — **not applicable**: there are no ADRs to cascade. Report "No ADR
  cascade at minimal workflow — design change recorded; no architecture impact
  analysis." and stop here.

**Establish the denominator first.** Glob the in-scope ADRs (per the tier above).
Call the count **N**. If N is 0: "No ADRs found in `docs/architecture/` — nothing
to cascade." Stop.

**Scan the requirement tables — do not full-read the ADRs at this step:**
```
Grep pattern="## GDD Requirements Addressed" glob="docs/architecture/adr-*.md" output_mode="content" -A 15
```
**Recall net — an ADR may cite the changed GDD in prose without tabling it:**
```
Grep pattern="[changed-gdd-basename]" glob="docs/architecture/adr-*.md" output_mode="files_with_matches"
```
Take the **union** of the two results as the affected set **M**. This turns
N × ~200 lines into N × ~15 lines; `5 full-reads only the M.

## Phase 4: The ADRs in scope

`bash .game-studio/scripts/adr-status.sh` lists every ADR with its status, layer and
missing sections.

- **`full`:** every ADR.
- **`standard`:** the critical ones (the `layer` column reads Foundation, or holds
  no layer: when in doubt, critical) and any ADR that names the changed GDD.
- **`minimal`:** report "No ADR check at minimal workflow — design change recorded;
  no architecture impact analysis." Stop.

Establish the denominator first: their count is **N**. N is 0: "No ADRs found in `docs/architecture/` — nothing to
check." Stop.

**Which ones reference this GDD.** Without reading whole ADRs:

1. each ADR's GDD Requirements Addressed section
   (`python .game-studio/runtime/studio.py markdown --root <project-root> extract <adr> "GDD Requirements Addressed"`),
   for rows naming the changed GDD;
2. a search of the ADRs for the changed GDD's file name, which catches an ADR that
   cites it in prose without a table row.

The union of the two is the affected set **M**.

| Result | Meaning | Action |
|---|---|---|
| **M ≥ 1** | Normal. | Go on. The N − M others are out of scope for this check: never describe them as verified unaffected. |
| **M = 0**, and every in-scope ADR lacks GDD Requirements Addressed (`missing` column) | Traceability cannot be computed. | "[N] ADRs found, none has a 'GDD Requirements Addressed' section — traceability cannot be computed (a pre-production gate blocker). Run `$gs-architecture-decision retrofit [adr]`." Stop. |
| **M = 0**, the sections exist | No ADR references this GDD. | "No ADR references [gdd] — no architecture impact." Stop. |

Read `docs/architecture/requirements-traceability.md` when it exists.

Report: "Checked [N] ADRs. [M] reference [gdd filename] ([X] in a requirements
table, [Y] in prose only)."

## Phase 5: Impact analysis

For each ADR in **M**, read its Context, Decision and Consequences sections with
`md-section.sh extract`: whether a decision still holds needs its reasoning, never
only its table row. Then, for each requirement it lists from the changed GDD:

1. Does the requirement still exist in the current GDD?
2. What did the GDD say when the ADR was written, and what does it say now?
3. Does the decision still hold?

Classify each ADR:

| Status | Meaning |
|--------|---------|
| ✅ **Still Valid** | The change does not touch what this ADR decided |
| ⚠️ **Needs Review** | The change may affect it; human judgement needed |
| 🔴 **Likely Superseded** | The change contradicts what this ADR assumed |

```
### ADR-NNNN: [title]
Status: [Still Valid | Needs Review | Likely Superseded]

What the ADR assumed about this GDD:
  "[quote from its GDD Requirements Addressed or Context]"

What the GDD now says:
  "[quote from the current GDD]"

Assessment:
  [whether the decision still holds, and why]

Recommended action:
  [Keep as-is | Review and update | Mark Superseded and write a new ADR]
```

## Phase 6: The impact report, then the review

Show the whole report before asking for any action:

```
## Design Change Impact Report
GDD: [filename]
Date: [today]
Changes detected: [N sections changed]
ADRs referencing this GDD: [M]

### Not Affected
[ADRs whose decisions still hold]

### Needs Review ([count])
[ADRs that may need updating]

### Likely Superseded ([count])
[ADRs whose assumptions the change contradicts]
```

---

## 6b. Director Gate — Technical Impact Review

**Review mode check** — apply before spawning TD-CHANGE-IMPACT:
- `solo` → skip. Note: "TD-CHANGE-IMPACT skipped — Solo mode." Proceed to Phase 7.
- `lean` → skip. Note: "TD-CHANGE-IMPACT skipped — Lean mode." Proceed to Phase 7.
- `full` → spawn as normal.

Spawn `technical-director` via native delegation when authorized using gate **TD-CHANGE-IMPACT** (`.game-studio/resources/docs/director-gates/td-change-impact.md`).

Pass: the full Design Change Impact Report from Phase 6 (change summary, all affected ADRs with their Still Valid / Needs Review / Likely Superseded classifications, and recommended actions).

The technical-director reviews whether:
- The impact classifications are correct (no ADRs under-classified)
- The recommended actions are architecturally sound
- Any cascading effects on other ADRs or systems were missed

Apply the verdict:
- **APPROVE** → proceed to Phase 7 resolution workflow
- **CONCERNS** → surface the specific ADRs or recommendations flagged; use `ask the user` with options: `Revise the impact assessment` / `Accept with noted concerns` / `Discuss further`
- **REJECT** → do not proceed to resolution; re-analyze the impact before continuing
- **NOT ASSESSED** [missing input] → not an approval (`.game-studio/resources/docs/director-gates.md`): name what was missing, then supply it and re-run the gate — or, if the user chooses to go on without it, proceed to Phase 7 and state `TD-CHANGE-IMPACT: NOT ASSESSED — [input]` in the change impact report and the final Verdict line

---

## 7. Resolution Workflow

For each ADR marked "Needs Review" or "Likely Superseded", ask the user what to do:

Ask for each ADR in turn:
> "ADR-NNNN ([title]) — [status]. What would you like to do?"
> Options:
> - "Mark Superseded (I'll write a new ADR)" — updates ADR status line to `Superseded by: [pending]`
> - "Update in place (minor revision)" — opens the ADR for editing; note what to revise
> - "Keep as-is (the change doesn't actually affect this decision)"
> - "Skip for now (revisit later)"

```
python .game-studio/runtime/studio.py markdown --root <project-root> replace docs/architecture/[adr-file].md "Status" <<'EOF'
Superseded — replacement pending (see docs/architecture/change-impact-[date]-[system-slug].md)
EOF
```

This is the one form this skill writes. `adr-status.sh` reads it as Superseded, so
`$gs-dev-story` and `$gs-create-stories` block the stories that still point at it. The
new ADR, once written, records which one it replaces. Change nothing else in the
ADR: its content stays.

## Phase 8: The traceability index

When `docs/architecture/requirements-traceability.md` exists, ask "May I add the
changed requirements to the traceability index?" On yes, add a row per changed
requirement:

```markdown
## Superseded Requirements
| Date | GDD | Requirement | Changed To | ADRs Affected | Resolution |
|------|-----|-------------|------------|---------------|------------|
| [date] | [gdd] | [old requirement text] | [new requirement text] | ADR-NNNN | [Superseded/Updated/Valid] |
```

## Phase 9: The change impact document

Ask "May I write the change impact report to
`docs/architecture/change-impact-[date]-[system-slug].md`?" It holds the change
summary, the impact analysis, the resolution chosen for each ADR, and the ADRs that
need writing or updating.

## Phase 10: Follow-up

From the resolutions:

**Applies in `collaborative` mode (the default).** For `guided` and
`autonomous` modes, see `.game-studio/resources/docs/automation-modes.md` — the rules below
describe what collaborative mode requires, not universal behavior.

End with `Verdict: COMPLETE — change impact report saved` after the Phase 9 write,
or `Verdict: BLOCKED — user declined the write` when declined.
