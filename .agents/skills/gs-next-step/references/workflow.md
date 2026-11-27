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


Run `python .game-studio/runtime/studio.py config --root <project-root>` explicitly before dependent work. Shell helpers under `.game-studio/scripts` emit TSV and require Bash in the consumer root. Native commands emit JSON. Inspect actual argv and existing authorization before commands, installs, downloads or Git operations.


# Next Step — What Do I Do Next?

This skill is read-only — it reports findings but writes no files.

This skill figures out where the project is and tells you the one thing to do
next. The main path comes first: make a game (`$gs-prototype`), change it after you
play it, then grow it into a project you keep building. The stages below, with
their design documents, agents, `team-*` pipelines and stage gates, are **studio
mode**, the path at `workflow` `standard` or `full`. It is **lightweight** — not a full
audit. For a full gap analysis, use `$gs-project-stage-detect`.

## Live Project State
Run `python .game-studio/runtime/studio.py config --root <project-root>` and
`python .game-studio/runtime/studio.py project-state --root <project-root>`.
Use effective values and provenance; errors do not authorize writes or commands.
`project.stage` is the configured stage, and `derived.workflow` the tier; missing
facts remain unknown. Do not infer a quality gate passed from artifact presence.

## Step 1: Read the Catalog

Read `.game-studio/resources/docs/workflow-catalog.yaml`. This is the authoritative list of all
phases, their steps (in order), whether each step is required or optional, and
the artifact globs that indicate completion.

---

## Step 1b: Find Skills Not in the Catalog

After reading the catalog, list `.agents/skills/gs-*/SKILL.md` to get the full list
of installed skills. For each file, extract the `name:` field from its frontmatter.

Compare against the `command:` values in the catalog. Any skill whose name does
not appear as a catalog command is an **uncataloged skill** — still usable but not
part of the phase-gated workflow.

Collect these for the output in Step 7 — show them as a footer block:

```
### Also installed (not in workflow)
- `/skill-name` — [description from SKILL.md frontmatter]
- `/skill-name` — [description]
```

Only show this block if at least one uncataloged skill exists. Limit to the 10
most relevant based on the project's stage (QA skills in production, team
skills in production/polish, etc.).

---

## Step 2: Determine the Current Stage

**First, take `workflow` from the config block above.** If it is `minimal`, the
project is on the minimal path, not the phase ladder: skip the rest of this step,
read the session context (**Step 3**), then go to **Step 4m**. At that tier, do
not map `project.stage` — nothing on the minimal path runs `$gs-gate-check`, so
the stage reads Concept however far the
project has got, and walking the Concept stage would send a project that already
has stories back to the concept doc, art bible and systems map.

Otherwise, check in this order:

1. **Take `project.stage` from the config block above** — it is already resolved. Map its value to a catalog phase key:
   - "Concept" → `concept`
   - "Systems Design" → `systems-design`
   - "Technical Setup" → `technical-setup`
   - "Pre-Production" → `pre-production`
   - "Production" → `production`
   - "Polish" → `polish`
   - "Release" → `release`

2. **If neither is set**, infer phase from artifacts (most-advanced match wins):
   - code root has 10+ source files → `production`
   - `production/epics/**/story-*.md` exists → `pre-production`
   - `docs/architecture/adr-*.md` exists → `technical-setup`
   - `design/gdd/systems-index.md` exists → `systems-design`
   - `design/gdd/game-concept.md` (or `design/game-brief.md`) exists → `concept`
   - Nothing → `concept` (fresh project)

3. **`workflow`** was taken at the top of this step (per
   `.game-studio/resources/docs/workflow-modes.md`). It controls whether optional docs are
   surfaced as next steps (Step 5).

---

## Step 3: Read Session Context
Run `python .game-studio/runtime/studio.py recover --root <project-root>` and use
its `checkpoint.path`. DISABLED means skip checkpoint reads; never use a fixed fallback.
Read the actual recovered STATUS/CHECKPOINT or concise authored state, preserving
its provenance: current work, open questions, completed artifacts and next action.
Do not infer unseen work or authorization. At minimal continue with Step 4m.

## Step 4: Check Step Completion for the Current Stage

For each step in the current stage (from the catalog):

### Artifact-based checks

**Resolve these deterministically — one call, not a glob per step:**

```
python .game-studio/runtime/studio.py artifacts --phase [current-phase] --root <project-root>
```

It evaluates every `glob`, `pattern`, `min_count` and `any_of` in the catalog
against the working tree and returns JSON observations per step. Map its statuses:

| status | Report as |
|---|---|
| `PRESENT` | **Complete** |
| `ABSENT` | **Incomplete** |
| `SHORT` | **Incomplete** — say how far short (`count=`/`min=` are given) |
| `PATTERN_MISS` | **Incomplete** — the file exists but lacks its marker; say so, since "missing" would send the user to recreate a file they already have |
| `NO_CHECK` | **MANUAL** if the step carries a `note=`, else **UNKNOWN** — completion is not trackable (e.g. repeatable implementation work) |

Do not re-derive any of this by searching the files yourself. `any_of` in particular is a list of
**alternatives** — one match is enough — and hand-evaluating it risks a false
"incomplete": `engine-setup` is satisfied by `engine.name`
in `project.yaml` **or** by the legacy `Engine:` line in
`docs/project-reference/technical-preferences.md`, and the script reports which alternative
matched (`alt=`/`match=`).

**`NO_CHECK` never means done.** The native JSON reports totals and step observations; if most of a phase is NO_CHECK, say that plainly rather than implying the
phase is nearly complete.

### Special case: the Production stage — read `sprint-status.yaml`

When the current stage is `production`, check for `production/sprint-status.yaml`
before doing any glob-based story checks. If it exists, read it directly:

- Stories with `status: in-progress` → surface as "currently active"
- Stories with `status: ready-for-dev` → surface as "next up"
- Stories with `status: done` → count as complete
- Stories with `status: blocked` → surface as blocker with the `blocker` field

This gives precise per-story status without markdown scanning. Skip the glob
artifact check for the `implement` and `story-done` steps — the YAML is authoritative.

### Special case: `repeatable: true` (non-production)

For repeatable steps outside production (e.g. "System GDDs"), the artifact
check tells you whether *any* work has been done, not whether it's finished.
Label these differently — show what's been detected, then note it may be ongoing.

---

## Step 4m: The Minimal Path (`workflow: minimal` only)

At `minimal` the route is the catalog's `paths.minimal`, not a phase: engine →
`design/game-brief.md` → stories → `$gs-dev-story` ↔ `$gs-story-done`. Resolve it in
one call:

```
python .game-studio/runtime/studio.py artifacts --path minimal --root <project-root>
```

Map the statuses exactly as in Step 4. `implement` and `story-done` are
`NO_CHECK` by design — the story status lines below are their check. The next
step is the first of these that applies:

1. `engine-setup` not PRESENT → the main path first. Look for
   `prototypes/*/index.html`:
   - a match → a game is made. Not played yet → `→ Next up` is to play it
     and ask for changes in plain words ("make the jump higher"). Once
     played (its folder has a `feel-log.md` or a `REPORT.md`, or its brief
     an `After play:` line or a line under `## Keep`) → `→ Next up` is to
     grow it: `$gs-prototype` and say grow it (its
     verdict, then one question: keep iterating, or grow it into a real web
     project), with `$gs-setup-engine` under "Coming up after that" for an
     engine instead
   - When the person asks for a change to a made game, or says they love or
     hate it, `→ Next up` is `$gs-prototype` with their words, whatever else this
     list finds: it makes a change with an accept-or-undo question and a
     checkpoint, takes a love-it as a Keep line, and on hate it it offers fix
     (recommended), pivot or kill. Never answer it with a change or a drop of
     your own
   - no match, and the code root holds fewer than 10 source files → no game
     yet: `→ Next up` is `$gs-prototype` (make a game you can play),
     with `$gs-setup-engine` under "Coming up after that" as the way to start
     on an engine instead. With design documents in `design/gdd/`, it is
     built from their concept doc, as in Step 5's **A design with nothing to play**
     (its first case)
   - no match, and 10 or more source files → `$gs-setup-engine`, as before
2. `game-brief` not PRESENT → `$gs-reverse-document design [code root]` when the
   code root already holds the game (10 or more source files, the test Step 2
   uses for `production`): at `minimal` it writes `design/game-brief.md` from
   what is built. Otherwise, with nothing under `prototypes/` yet, the main
   path first: `→ Next up` is `$gs-prototype` (say the game in one line; on Web it
   is playable, and writes the brief, on an engine it is a quick
   throwaway build), with `$gs-brainstorm` under "Coming up after that" for
   someone with no idea yet. With a prototype made, `$gs-brainstorm` (at `minimal`
   it writes the one-page brief), which on a built game would start a new idea.
3. `create-stories` not PRESENT:
   - **a grown game** (a `production/qa/evidence/grow-*/replay.args` file) → `→ Next up` is one feature a sitting:
     say the next feature in your own words to `$gs-prototype` (the brief's first
     `[ ]` Features line is the suggestion, when there is one); it is built,
     checked and committed in one sitting. `$gs-cut` goes under "Coming up after
     that". Stories, epics and gates only when the person asks for them (then
     `$gs-create-stories`, as below)
   - otherwise `$gs-create-stories` with no argument (at `minimal` it builds the
     stories straight from the brief's Features list). When the brief has no
     `[ ]` Features item and its `## Your systems` list has no `thin stand-in`
     or `later` system, `→ Next up` is: every feature in the brief is built, so
     say what to add next, in your own words, and `$gs-create-stories` adds it to
     the brief's Features (with your yes) and makes its stories. `$gs-cut` goes
     under "Coming up after that"
4. Stories exist → run `python .game-studio/runtime/studio.py stories --root <project-root>`.
   Read `.game-studio/resources/docs/story-routing.md`; consume JSON `next.action/path/skill`,
   counts and unfinished categories, never imaginary pre-injected TSV. IN_REVIEW goes to
   `$gs-story-done`; IN_PROGRESS uses actual checkpoint/files to distinguish written work
   from work to resume; TODO goes to `$gs-dev-story`. BLOCKED/OTHER/NO_STATUS never mean done.
   Empty stories means NO STORIES; only a nonempty complete/count match means the build
   order is recorded complete, not that game quality is proven.
   A TODO or unstarted IN_PROGRESS `Build step: deepen — <system>` first needs
   `design/gdd/<system>.md`; if missing, `$gs-design-system <system>` is Next up and the
   story follows. Use the user's system identity (lowercase slug, leading a/an/the removed).
   If all stories are complete, offer play, next feature (grown: `$gs-prototype`),
   new brief features/stories, or `$gs-project-settings` to increase rigor.

   **A game past the light path's size.** With stories, read the brief's Features
   list (count its `[x]` and `[ ]` items, not a cut `[-]`) and its Skeleton line, if
   it has one. The game has outgrown the light path when the total story count is 9 or more, the Features list has 9 or more items, or the Skeleton line
   names four or more systems. Nine is `.game-studio/resources/docs/settings-guidance.md` § 4's
   "about 9 systems"; four systems is the brief's own mark for a systemic game.
   Then add the **Studio mode** line to the `minimal` shape in Step 7, naming the
   count that passed. It is a suggestion: Next up stays the story, and nothing
   waits on it. Show it once: only while the completed story count is zero (no
   story built yet, when switching costs least), and never twice in one
   conversation. Once it shows, leave out Step 9's rigor line.

**At `minimal`, never present any of these as required or as a blocker:** the
game concept doc, art bible, systems map, GDDs, `$gs-create-epics`, a sprint plan,
`$gs-gate-check`, or sprint close-out (`$gs-smoke-check`, `$gs-team-qa`,
`$gs-retrospective`). The brief replaces the design documents and its build order
replaces the sprint plan (`.game-studio/resources/docs/workflow-modes.md` — `minimal` floor).
Every one of them still runs if the user asks for it; mention one only when the
user's argument asks about it. The one exception is a deepen story's design doc
above: one system's, named before that story only.

Then skip Steps 5 and 8, and present with the `minimal` shape in Step 7.

---

## Step 5: Find Position and Identify Next Steps

From the completion data, determine:

1. **Last confirmed complete step** — the furthest completed required step
2. **Current blocker** — the first incomplete *required* step (this is what the
   user must do next)
3. **Optional opportunities** — incomplete *optional* steps that can be done
   before or alongside the blocker. **Surface these per the workflow tier**: at
   `full`, list all of them; at `standard`, list an optional doc only if it is
   required for the current system/phase (do not flag genuinely-optional docs as
   gaps). At `minimal` this step does not run — Step 4m replaces it
4. **Upcoming required steps** — required steps after the current blocker
   (show as "coming up" so user can plan ahead)

If the user provided an argument (e.g. "just finished design-review"), use that
to advance past the step they named even if the artifact check is ambiguous.

**A design with nothing to play.** When `design/gdd/` holds a `.md` file and
Glob finds no `prototypes/*/index.html`, check `engine.name` in `project.yaml`:

- No engine set, or `web`: `→ Next up` is a playable first, `$gs-prototype` built
  from their concept doc (`$gs-prototype design/gdd/game-concept.md`; with no
  concept doc, the GDD that describes the whole game). Say in one line: "Your
  design documents stay the source of truth; the brief `$gs-prototype` writes is
  only a summary for the build." The blocker found above goes first under
  "Coming up after that", with `$gs-project-stage-detect` and `$gs-adopt` after it.
- An engine other than `web`: the blocker stays `→ Next up`. Add under "Also
  available" that `$gs-prototype --path html` is the fast option: a browser sketch
  of the core game, thrown away when the engine build starts.

---

## Step 6: Check for In-Progress Work

If `active.md` shows an active task or epic:
- Surface it prominently at the top: "It looks like you were working on [X]"
- Suggest continuing it or confirm if it's done

---

## Step 7: Present Output

Keep it **short and direct**. This is a quick orientation, not a report.

```
## Where You Are: [Phase Label]
Studio mode (`workflow: [value]`): the design documents, agents and `team-*` pipelines. It fits a team, a long project, or someone who wants the paperwork.

**In progress:** [from active.md, if any]

### ✓ Done
- [completed step name]
- [completed step name]

### → Next up (REQUIRED)
**[Step name]** — [description]
Command: `[/command]`

### ~ Also available (OPTIONAL)
- **[Step name]** — [description] → `/command`
- **[Step name]** — [description] → `/command`

### Coming up after that
- [Next required step name] (`/command`)
- [Next required step name] (`/command`)

---
Approaching the **[next stage]** stage gate → run `$gs-gate-check` when ready.
```

The studio-mode line under the heading labels the path and changes no step.

**At `minimal`** use this shape instead — no phase label, no gate line. `N`
counts only stories whose status line says `Complete` or `Done`, and only those
go under ✓ Done. `N` and `M` are the two numbers on the `COMPLETE` line; it
names no finished story, so ✓ Done gives their count, not their titles:

```
## Where You Are: Minimal path — [N] of [M] stories complete

**In progress:** [from active.md, if any]

### ✓ Done
- Engine: [engine] · Game brief · [N] stories

### → Next up
**[Story NNN: title]** — [what it delivers]
Command: `$gs-story-done [story-path]` for an In Review story, or an In Progress one whose work is written; otherwise `$gs-dev-story [story-path]`, or `$gs-design-system <system>` first for a deepen story whose system has no design doc (Step 4m), with its one line of why

### Coming up after that
- [the next Ready stories in build order, at most 3]

### ~ Studio mode (only when Step 4m's size check passed)
[M stories / N features / N systems]: past the size one brief fits. Studio mode adds a design doc per system and architecture decisions; `$gs-project-settings` switches it on. Optional: the stories build as they are either way.
```

A grown game with no stories: the heading reads `Minimal path — grown game, [N] of [M] Features
built` (the brief's `[x]` and `[ ]` lines), ✓ Done names the grow, and Next up is the next
feature, with `$gs-prototype` as its command.

**Formatting rules:**
- `✓` for confirmed complete
- `→` for the current required next step (only one — the first blocker)
- `~` for optional steps available now
- Show commands inline as backtick code
- If a step has no command (e.g. "Implement Stories"), explain what to do instead of showing a slash command
- For MANUAL steps, ask the user: "I can't tell if [step] is done — has it been completed?"

Verdict: **COMPLETE** — next steps identified.

---

## Step 8: Gate Warning (if close)

Skip this step at `minimal` — the minimal path has no stage gates.

After the current stage's steps, check if the user is likely approaching a gate:
- If all required steps in the current stage are complete (or nearly complete),
  add: "You're close to the **[Current] → [Next]** gate. Run `$gs-gate-check` when ready."
- If multiple required steps remain, skip the gate warning — it's not relevant yet.

---

## Step 9: Escalation Paths

After the recommendations, if the user seems stuck or confused, add:

```
---
Need more detail?
- `$gs-project-stage-detect` — full gap analysis with all missing artifacts listed
- `$gs-gate-check` — formal readiness check for your next stage
- `$gs-start` — re-orient from scratch
- `$gs-project-settings` — if the process feels mismatched to your project, adjust
  `modes.rigor`. Apply the change-triggers in
  `.game-studio/resources/docs/settings-guidance.md § 4`: a **lower** tier when the user sounds
  overwhelmed by process (and rigor isn't already `minimal`), or a **higher** tier
  when the project has outgrown it (many systems, or in Production on
  `workflow: minimal`)
```

Only show this if the user's input suggested confusion (e.g. "I don't know", "stuck",
"lost", "not sure"). Don't show it for simple "what's next?" queries. Show the
`$gs-project-settings` rigor line only when a `settings-guidance.md § 4` trigger actually
fires — the user sounds overwhelmed (and rigor isn't already `minimal`), or the
project has outgrown its tier — not on every confused query. At `minimal`, leave
out the `$gs-gate-check` line: the minimal path has no stage gates (Step 4m).

---

## Collaborative Protocol

- **Never auto-run the next skill.** Recommend it, let the user invoke it.
- **Ask about MANUAL steps** rather than assuming complete or incomplete.
- **Match the user's tone** — if they sound stressed ("I'm totally lost"), be
  reassuring and give one action, not a list of six.
- **One primary recommendation** — the user should leave knowing exactly one thing
  to do next. Optional steps and "coming up" are secondary context.
