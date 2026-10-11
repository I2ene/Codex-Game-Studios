## Native review evidence contract

Read .game-studio/resources/docs/review-receipts.md before freshness/scope decisions. It replaces old text-line
or embedded-hash consumption below. Choose a real report/companion pair explicitly;
first/missing/legacy JSON means fresh full review. Consume baseline_status,
report_status and unchanged_inputs plus observations/required_unresolved/optional_unresolved. Prior failures stay
failures. After actual review, write the human report then generate a linked JSON
with receipts hash --report <report> --output <companion> for inputs actually read.
Declare applicable optional inputs when generating the snapshot with repeated
--optional-pattern <pattern>; check inherits the saved classification. Required
unavailable inputs still block verdict reuse; stable absent optional inputs stay named.
Scope/mode/required coverage must be the same before prior-verdict reuse.

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


Explicitly resolved — use as-is; `--review` overrides `review_mode`. `--depth` is
the pre-1.1 name for the same flag: treat `--depth <mode>` exactly as
`--review <mode>`, and say once that it was renamed. Given both, `--review`
wins and `--depth` is ignored — say so. No block → defaults in
`.game-studio/resources/docs/config-resolution.md`.


## Phase 0: Parse Arguments


See `.game-studio/resources/docs/director-gates.md` for the full check pattern. Individual gate definitions live in `.game-studio/resources/docs/director-gates/[gate-id].md` — the actual reviewer reads its gate file; read it in the parent when applying the role yourself.


Every `ask the user` call follows `.game-studio/resources/docs/automation-modes.md`
(collaborative resolves open choices · guided resolves major choices · autonomous records in-scope choices;
`automation_always_ask` categories require input only outside existing authorization).

**`workflow`** for the GDD under review — use the `system_overrides` row for `<system>` if the block lists one, else the project value. Validation scope follows the tier:
- `full` — all 8 sections validated; any missing section blocks approval.
- `standard` — the 5 required sections (Overview, Detailed Rules, Edge Cases,
  Dependencies, Acceptance Criteria) block if missing; Formulas blocks only when
  the system defines numeric rules (rates, curves, thresholds, costs — the
  category is a hint, not the test); Player Fantasy and
  Tuning Knobs are advisory (warn, never block) unless `workflow_overrides`
  require them.
- `minimal` — no GDD is expected; if one exists, validate the 5 standard
  sections advisorily.

Resolved mode controls how thorough this review is:

- **`full`**: Complete review — all phases + specialist expertise (Phase 3b, delegated only when authorized/available)
- **`lean`**: All phases, no specialist agents — faster, single-session analysis
- **`solo`**: Phases 1-4 only, no delegation, no Phase 5 next-step prompt — use when called from within another skill

---

## Phase 1: Load Documents

Select the actual report/JSON companion pair explicitly. Read the prior report,
including verdict, mode and covered inputs. Run receipts check with that companion
and exactly the input patterns previously reviewed, including dependencies/context
actually read. Use .game-studio/resources/docs/review-receipts.md.

- baseline_status=MISSING, legacy/non-native JSON, report_status=UNLINKED/ABSENT/
  CHANGED, changed scope/mode, or unavailable required input: fresh review. A legacy
  JSON error is a baseline problem; retain the old report and create a native pair.
- unchanged_inputs=true with report_status=UNCHANGED and complete required coverage:
  surface the actual prior date/verdict. A failed verdict still fails. Reuse an
  approved verdict only within the requested scope; an explicit request to re-review
  takes precedence. Do not ask again when that choice was already authorized.
- observations NEW/CHANGED/REMOVED or changed unresolved: read/review affected inputs.
  For design-review read the target fully; registry-only changes require rechecking
  all registry-sourced facts and full review if conflicts appear. For architecture
  review reconcile affected systems/dependencies; structural/deleted ADR changes need
  full coverage analysis. Report unresolved required inputs as NOT ASSESSED, never
  silently reduce the denominator or offer an unsupported unchanged verdict.
- Optional inputs absent in both snapshots are named, rather than silently omitted.
  Their appearance/deletion changes freshness. Empty observations never prove reuse.

Snapshot the actual inputs before reviewing and reconcile any input drift before
publication. After writing the real Markdown report/log, generate its companion with
receipts hash <actual-reviewed-patterns...> --root <project-root> --report <report.md>
--output <companion.json>. Re-run check to confirm the link and input snapshot. Hashes
record bytes; they never supply a professional approval or independent participant.


Companion: design/gdd/reviews/[doc-name]-review-receipt.json.
Report: design/gdd/reviews/[doc-name]-review-log.md.

Read the target design document in full. Read AGENTS.md to understand project context and standards.

**For cross-document facts, prefer the registry over sibling GDDs.** If
`design/registry/entities.yaml` exists **and lists entries for this system**,
grep it — these are the established facts this GDD must not contradict, and they
replace reading sibling GDDs to rediscover them:
```
Grep pattern="source: design/gdd/[system].md" path="design/registry/entities.yaml" output_mode="content" -A 6
Grep pattern="design/gdd/[system].md" path="design/registry/entities.yaml" output_mode="content" -B 8
```
The first finds entries this system **owns** — the `-A 6` context includes their
`referenced_by:` block. The second finds entries that **reference** this system —
`referenced_by:` is a block sequence (the key and its paths are on separate
lines), so match the path with `-B 8` context to see the owning entry, not a
`referenced_by.*name` one-liner (which never matches the block form).

**If `design/registry/entities.yaml` does not exist, or lists no entry for this
system** — the file ships as an empty stub, so this is the default until
`$gs-design-system` has populated it — fall back to reading the related GDDs the
target doc names in its Dependencies section. Bound the read to those, not to
everything "implied". Do not glob-read all of `design/gdd/`.

**Dependency graph validation:** For every system listed in the Dependencies section, use Glob to check whether its GDD file exists in `design/gdd/`. Flag any that don't exist yet — these are broken references that downstream authors will hit.

**Lore/narrative alignment:** If `design/gdd/game-concept.md` (or, at `rigor: minimal`, the one-page brief `design/game-brief.md`) or any file in `design/narrative/` exists, read it. Note any mechanical choices in this GDD that contradict established world rules, tone, or design pillars. Pass this context to `game-designer` in Phase 3b.

**Prior review check:** Check whether `design/gdd/reviews/[doc-name]-review-log.md` exists. If it does, read the most recent entry — note what verdict was given and what blocking items were listed. This session is a re-review; track whether prior items were addressed.

---

## Phase 2: Completeness Check

**Step 2a — gather section presence deterministically (no document read):**

```
Bash: python .game-studio/runtime/studio.py gdd-structure --root <project-root> [target-doc-path]
```

It returns documents JSON with present/absent section-name arrays and a document count. It reports
**presence only** and makes no REQUIRED/ADVISORY judgment — that is Step 2b's
job. It already accepts `## Detailed Design` as satisfying the `Detailed Rules`
requirement, so do not flag that as missing.

**Step 2b — apply the tier.** Using the Step 2a lists, evaluate against the
Design Document Standard checklist below. **Mark each section REQUIRED or
ADVISORY per the resolved workflow tier (Phase 0).** A missing REQUIRED section
blocks approval; a missing ADVISORY section is surfaced as a recommendation but
does not block.

A section reported PRESENT can still fail review if it is an empty heading —
spot-read any section the verdict actually turns on.

- [ ] Has Overview section (one-paragraph summary) — REQUIRED at all tiers
- [ ] Has Player Fantasy section (intended feeling) — REQUIRED at `full`; ADVISORY at `standard`
- [ ] Has Detailed Rules section (unambiguous mechanics) — REQUIRED at `full`/`standard`. The GDD template titles this section `## Detailed Design` (it carries Core Rules / States / Interactions sub-headings); accept **either** heading as satisfying this requirement — do not flag "Detailed Rules" as missing when a `## Detailed Design` section is present.
- [ ] Has Formulas section (all math defined with variables) — REQUIRED at `full`; at `standard` REQUIRED whenever the system defines numeric rules (rates, curves, thresholds, costs, damage, drop weights), else ADVISORY. The system's `Category` is a hint, not the test — do not clear this on a category token alone
- [ ] Has Edge Cases section (unusual situations handled) — REQUIRED at `full`/`standard`
- [ ] Has Dependencies section (other systems listed) — REQUIRED at `full`/`standard`
- [ ] Has Tuning Knobs section (configurable values identified) — REQUIRED at `full`; ADVISORY at `standard` unless `workflow_overrides.tuning_knobs`
- [ ] Has Acceptance Criteria section (testable success conditions) — REQUIRED at `full`/`standard`

---

## Phase 3: Consistency and Implementability

**Internal consistency:**
- Do the formulas produce values that match the described behavior?
- Do edge cases contradict the main rules?
- Are dependencies bidirectional (does the other system know about this one)?

**Implementability:**
- Are the rules precise enough for a programmer to implement without guessing?
- Are there any "hand-wave" sections where details are missing?
- Are performance implications considered?
- Is every acceptance criterion independently testable? Flag each one that is
  not, quoting it — "feels balanced", "works correctly", "performs well" are not
  criteria — with a measurable rewrite. In `full` mode `qa-lead` also checks them
  (Phase 3b); in `lean` and `solo` no specialist runs, so this main-review check
  is the only one.

**Cross-system consistency:**
- Does this conflict with any existing mechanic?
- Does this create unintended interactions with other systems?
- Is this consistent with the game's established tone and pillars?

---

## Phase 3b: Adversarial Specialist Review (full mode only)

**Skip this phase in `lean` or `solo` mode.**

**This phase is MANDATORY in full mode.** Do not skip it.

State the actual review method before the domain pass: parent-only or authorized
participants with real IDs. Professional adversarial checks are required in full;
they do not require unavailable or unauthorized delegation, guessed durations or
independent sign-off. Read relevant role instructions and apply their checks here
when the parent performs them.

### Step 1 — Identify all domains the GDD touches

Using the GDD **already loaded in Phase 1** — do not re-read it — identify every domain present. A GDD can touch multiple domains simultaneously — be thorough. Common signals:

| If the GDD contains... | Spawn these agents |
|------------------------|-------------------|
| Costs, prices, drops, rewards, economy | `economy-designer` |
| Combat stats, damage, health, DPS | `game-designer`, `systems-designer` |
| AI behaviour, pathfinding, targeting | `ai-programmer` |
| Level layout, spawning, wave structure | `level-designer` |
| Player progression, XP, unlocks | `economy-designer`, `game-designer` |
| UI, HUD, menus, player-facing displays | `ux-designer`, `ui-programmer` |
| Dialogue, quests, story, lore | `narrative-director` |
| Animation, feel, timing, juice | `gameplay-programmer` |
| Multiplayer, sync, replication | `network-programmer` |
| Audio cues, music triggers | `audio-director` |
| Performance, draw calls, memory | `performance-analyst` |
| Engine-specific patterns or APIs | Primary engine specialist (`<engine>-specialist` from `engine.name` — Godot→`godot-specialist`, Unity→`unity-specialist`, Unreal→`unreal-specialist`; fall back to the Primary line of `## Engine Specialists` in `technical-preferences.md`) |
| Acceptance criteria, test coverage | `qa-lead` |
| Data schema, resource structure | `systems-designer` |
| Any gameplay system | `game-designer` (always) |

Spawn `game-designer` for all GDDs that describe gameplay mechanics or player-facing rules.
Spawn `systems-designer` for all GDDs that contain formulas or system interaction rules.
These are the most common baselines — but not required for pure UI specs, audio specs, or lore documents. Use the domain table above to determine which specialists are truly relevant.

### Step 2 — Spawn all relevant specialists in parallel

Use actual host delegation tools only when authorized and available. Give bounded
independent tasks and track real participants/artifacts/results. Otherwise the parent
reads the relevant gs-* expertise profile, performs its adversarial checks and labels
each finding [parent applying role]. Never describe parent analysis as an independent
specialist review. Parallelism is optional for independent work; dependent work waits.

**Prompt each specialist adversarially:**
> "Here is the GDD for [system] and the main review's structural findings so far.
> Your job is NOT to validate this design — your job is to find problems.
> Challenge the design choices from your domain expertise. What is wrong,
> underspecified, likely to cause problems, or missing entirely?
> Be specific and critical. Disagreement with the main review is welcome."

**Additional instructions per agent type:**

- **`game-designer`**: Anchor your review to the Player Fantasy stated in Section B of this GDD. Does this design actually deliver that fantasy? Would a player feel the intended experience? Flag any rules that serve implementability but undermine the stated feeling.

- **`systems-designer`**: For every formula in the GDD, plug in boundary values (minimum and maximum plausible inputs). Report whether any outputs go degenerate — negative values, division by zero, infinity, or nonsensical results at the extremes.

- **`qa-lead`**: Review every acceptance criterion. Flag any that are not independently testable — phrases like "feels balanced", "works correctly", "performs well" are not ACs. Suggest concrete rewrites for any that fail this test.

### Step 3 — Senior lead review

After all required specialist findings are available, apply `creative-director` expertise as the **senior reviewer** in the parent, or delegate when authorized with available host tools. Label parent synthesis accurately:
- Provide: the GDD, all specialist findings, any disagreements between them
- Ask: "Synthesise these findings. What are the most important issues? Do you agree with the specialists? What is your overall verdict on this design — APPROVED, NEEDS REVISION or MAJOR REVISION NEEDED?"
- The creative-director's synthesis becomes the **final verdict** in Phase 4, in this skill's verdict words — never a director-gate word such as READY or REJECT.

### Step 4 — Surface disagreements

If specialists disagree with each other or with the creative-director, do NOT silently pick one view. Present the disagreement explicitly in Phase 4 so the user can adjudicate.

Mark every finding with its source: `[game-designer]`, `[economy-designer]`, `[creative-director]` etc.

---

## Phase 4: Output Review

```
## Design Review: [Document Title]
Specialists consulted: [list agents spawned]
Re-review: [Yes — prior verdict was X on YYYY-MM-DD / No — first review]

### Completeness: [X/N sections present, where N is the count REQUIRED at this project's `modes.workflow`]
[List only sections missing that are REQUIRED at this tier. Mark ADVISORY gaps
separately as "advisory at `standard`" — do not list them as missing.]

> **N is not 8 unless `workflow: full`.** The tier table earlier in this skill is
> authoritative: 8 required at `full`, 5 at `standard` (+ Formulas when the system
> defines numeric rules), 0 at `minimal`. Hardcoding `/8` here
> reintroduces the tier confusion in the presentation layer after the logic
> layer already handles it — reporting a `standard` project as "5/8 missing Player
> Fantasy, Formulas, Tuning Knobs" warns about three sections that project's own
> configuration says it does not need, which trains the reader to ignore the
> review.

### Dependency Graph
[List each declared dependency and whether its GDD file exists on disk]
- ✓ enemy-definition-data.md — exists
- ✗ loot-system.md — NOT FOUND (file does not exist yet)

### Required Before Implementation
[Numbered list — blocking issues only. Each item tagged with source agent.]

### Recommended Revisions
[Numbered list — important but not blocking. Source-tagged.]

### Specialist Disagreements
[Any cases where agents disagreed with each other or with the main review.
Present both sides — do not silently resolve.]

### Nice-to-Have
[Minor improvements, low priority.]

### Senior Verdict [creative-director]
[Creative director's synthesis and overall assessment.]

### Scope Signal
Estimate implementation scope based on: dependency count, formula count,
systems touched, and whether new ADRs are required.
- **S** — single system, no formulas, no new ADRs, <3 dependencies
- **M** — moderate complexity, 1-2 formulas, 3-6 dependencies
- **L** — multi-system integration, 3+ formulas, may require new ADR
- **XL** — cross-cutting concern, 5+ dependencies, multiple new ADRs likely
Label clearly: "Rough scope signal: M (producer should verify before sprint planning)"

### Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED / NOT ASSESSED]

> **`NOT ASSESSED` when the review could not actually be performed.**
> The other three verdicts are all claims about the design's quality, so each one
> asserts that the document was read and judged. Use `NOT ASSESSED` instead when
> the target document is absent, unreadable, or empty of the sections being
> reviewed, or when a document it depends on is missing so the criteria cannot be
> applied. **Name what was unavailable and which skill produces it.**
>
> `APPROVED` is the dangerous default here: a review that could not find its
> input has not approved anything, and this verdict is consumed downstream as a
> sign-off. `NOT ASSESSED` outranks `APPROVED` in any aggregate — it does not
> outrank the two revision verdicts, because a known problem is more actionable
> than an unknown one.
```

This skill is read-only — no files are written during Phase 4.

---

## Phase 5: Next Steps

Use `ask the user` for ALL closing interactions. Never plain text.

**First widget — what to do next:**

If APPROVED (first-pass, no revision needed), proceed directly to the systems-index widget, review-log widget, then the final closing widget. Do not show a separate "what to do" widget — the final closing widget covers next steps.

If NOT ASSESSED, nothing was reviewed: offer no tracking update and go straight
to the final closing widget, leading with the skill that produces the missing
input (e.g. `$gs-design-system [system]` for a GDD that does not exist).

If NEEDS REVISION or MAJOR REVISION NEEDED, build the options from the findings:
- `[A] Revise the GDD now — address blocking items together`
- `[B] Stop here — revise in a separate session`
- `[C] Accept as-is and move on` — include only when every finding is advisory
  (Required Before Implementation is empty). With any blocking item, offer [A]
  and [B] only.

**If user selects [A] — Revise now:**

Work through all blocking items, asking for design decisions only where you cannot resolve the issue from the GDD and existing docs alone. Group all design-decision questions into a single multi-tab `ask the user` before making any edits — do not interrupt mid-revision for each blocker individually.

After all revisions are complete, show a summary table (blocker → fix applied) and use `ask the user` for a **post-revision closing widget**:

- Prompt: "Revisions complete — [N] blockers resolved. What next?"
- Note current context usage: if context is above ~50%, add: "(Recommended: /clear before re-review — this session has used X% context. A full re-review applies five professional review responsibilities; delegation is optional and needs clean context.)"
- Options:
  - `[A] Re-review in a new session — run $gs-design-review [doc-path] after /clear`
  - `[B] Accept revisions for now — mark In Review in the systems index; a re-review decides Approved`
  - `[C] Move to next system — $gs-design-system [next-system] (#N in design order)`
  - `[D] Stop here`

In collaborative and guided modes, never end the revision flow with plain text —
always close with this widget. In autonomous mode, summarize the outcome and
record via an authored decision record (not a tool or shell function).

**Second widget — tracking records (combined, for APPROVED path):**

When the verdict is APPROVED, use a single `ask the user` with `multiSelect: true` to batch the two tracking updates:
- Prompt: "Verdict: APPROVED. I can update the tracking records now. Select any you'd like me to complete:"
- Options:
  - `Update systems-index.md status to 'Approved' for [system]`
  - `Append approval entry to design/gdd/reviews/[doc-name]-review-log.md`

If the review-log option is selected, append the same format as below. Execute both selected actions before showing the final closing widget.

When the verdict is NEEDS REVISION or MAJOR REVISION NEEDED, use separate widgets as before:

Use a second `ask the user`:
- Prompt: "May I update `design/gdd/systems-index.md` to mark [system] as [Needs Revision / In Review]?" — `Needs Revision` (that exact string) while the revisions are outstanding, `In Review` once they are applied and await re-review. This prompt never offers `Approved`: a revision verdict is not an approval.
- Options: `[A] Yes — update it` / `[B] No — leave it as-is`

Use a third `ask the user`:
- Prompt: "May I append this review summary to `design/gdd/reviews/[doc-name]-review-log.md`? This creates a revision history so future re-reviews can track what changed."
- Options: `[A] Yes — append to review log` / `[B] No — skip`

If yes, append an entry in this format:
```
## Review — [YYYY-MM-DD] — Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED]
Scope signal: [S/M/L/XL]
Specialists: [list]
Blocking items: [count] | Recommended: [count]
Summary: [2-3 sentence summary of key findings from creative-director verdict]
Prior verdict resolved: [Yes / No / First review]
Findings:
- [BLOCKING] [section]: [one-line finding]
- [RECOMMENDED] [section]: [one-line finding]
Receipt: design/gdd/reviews/[doc-name]-review-receipt.json (linked JSON generated after this log entry)
```

Findings rules: one line per finding, named by the section it lives in;
write `- none` when the verdict carried no findings. This is documentation
for a human reader of the revision history, not a mechanism the skill reads
back — a delta re-review that skipped re-analyzing unchanged sections was
tried and reverted (see Phase 1) after measuring it against a full review.

The linked JSON companion, not embedded log text, supplies the next-run hash comparison. Follow .game-studio/resources/docs/review-receipts.md, including report linkage, same scope/mode and changed/deleted/unavailable inputs.

---

**Final closing widget — always show after all file writes complete:**

Once the systems-index and review-log widgets are answered, check project state and show one final `ask the user`:

Before building options, read:
- `design/gdd/systems-index.md` — find any system with Status: In Review or Needs Revision (other than the one just reviewed)
- Count `.md` files in `design/gdd/` (excluding game-concept.md, systems-index.md) to determine if `$gs-review-all-gdds` is worth offering (≥2 GDDs)
- Find the next system with Status: Not Started in design order

Build the option list dynamically — only include options that are genuinely next:
- `[_] Run $gs-design-review [other-gdd-path] — [system name] is still [In Review / Needs Revision]` (include if another GDD needs review)
- `[_] Run $gs-consistency-check — verify this GDD's values don't conflict with existing GDDs` (always include if ≥1 other GDD exists)
- `[_] Run $gs-review-all-gdds — holistic design-theory review across all designed systems` (include if ≥2 GDDs exist)
- `[_] Run $gs-design-system [next-system] — next in design order` (always include, name the actual system)
- `[_] Stop here`

Assign letters A, B, C… only to included options. Mark the most pipeline-advancing option as `(recommended)`.

In collaborative and guided modes, never end the skill with plain text after
file writes — always close with this widget. In autonomous mode, print the next
step and record via an authored decision record (not a tool or shell function).
