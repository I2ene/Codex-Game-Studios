## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.



Run `python .game-studio/runtime/studio.py config --root <project-root>` explicitly; use effective values and provenance. Existing authorization covers routine scoped writes. Shell helpers emit TSV; native helpers emit JSON. Required scope decisions remain human-owned; parent expertise is valid and missing checks are NOT ASSESSED.

# Cut

Finishing a game is choosing what not to build. $gs-cut reads what exists, proposes cuts with a
reason taken from it, and keeps a polish list; the person picks every cut. For `sell`,
`early_access` and `publisher` it asks a target date and proposes a freeze date. It writes the
brief, the polish list and any cut story's Status line, and makes one commit.

It runs only when asked: `$gs-cut`, or "what should I cut?", "how do I finish this?". It works on
the game `design/game-brief.md` describes. A project with GDDs and no brief is `$gs-scope-check`'s.

Ask with the question tool. Without one, list the options numbered and end your turn to wait. The
question is the last thing in the reply. A skipped or dismissed question is not an answer: ask
again in plain text. Every ask follows `.game-studio/resources/docs/automation-modes.md`: in `collaborative` and
`guided` the cuts and the dates are asked, as scope changes are major decisions; in `autonomous`
$gs-cut writes the polish list only and leaves the proposals in its report: cuts and dates wait for
the person, and nothing is committed.

## Phase 1: Read what exists

Run `bash .game-studio/scripts/cut-read.sh` and keep its rows:

| Rows | Use |
|---|---|
| `brief`, `title` | The briefs written, both copies while they are the same text. `brief none`: say "$gs-cut works from the brief's Features list, and there is no `design/game-brief.md`", name `$gs-scope-check` when `design/gdd/` has files, and stop. `brief_differs`: the game's folder copy differs; only `design/game-brief.md` is written, said in one line |
| `goal`, `dates` | `dates asked` or `not_asked` follows the goal. `goal - unset` (or `unknown`): guess it with `$gs-start`'s goal table (`.agents/skills/gs-start/references/workflow.md`, Phase 4) from the brief's In your words, `hobby` when nothing fits, and show it *guessed* |
| `feature`, `keep`, `avoid`, `out`, `cut` | The Features list by number, with its marks; the lists the proposals check |
| `recorded`, `passed` | Dates already on the brief's Dates line, and any date already past |
| `game`, `record`, `open` | A one-shot's last check record and its fails not marked deliberate |
| `smoke` | A project's smoke command, from the engine table, or `none` with why |
| `feel` | The feel log |
| `polish`, `polish_row` | The polish list's rows and ticks. `polish other_game`: it is another game's; say so and write no polish rows |
| `story`, `stories_other` | Stories traced to a Features item by number (`cut`: one already cut); a count of stories traced elsewhere, which $gs-cut leaves alone (say so) |

Read the brief itself too: its Question, Hooks, First minute, Challenge, Goal & fail state and
Build order give the reasons.

- **Fresh first:** a `record ... stale` row means the game changed after its check record. A
  changed game gets the light check, never the small check again: the small check is the
  build's, and `one-shot-check.sh --record` records only that, so never run it here. First see
  whether a light check is newer than every game file. For each marker on disk,
  `evidence/changes.tsv` (a change's light check) and `evidence/cut-end.png` (an earlier $gs-cut's),
  run `find prototypes/<name> -type f -newer prototypes/<name>/evidence/<marker> ! -path '*/evidence/*' ! -path '*/dist/*' ! -name brief.md ! -name feel-log.md ! -name polish-list.md`.
  - **One prints nothing:** that light check is fresh, so run nothing. Errors and a bot stop on
    `changes.tsv`'s last line that the polish list lacks become rows.
  - **Otherwise,** run the light check once, as `.agents/skills/gs-prototype/references/one-shot-4-change.md` section 7 does before accept: its step 1 (keep) and step 2 (play it once), the shot
    `prototypes/<name>/evidence/cut-end.png`. A `not_assessed` row: say "not checked: <why>"
    in one line. Fix nothing: each error, bot stop and `changed` or `gone` keep row becomes a
    polish row.

  These rows end `· from: light check of <date>`. The stale `record` row stays; its `open` rows
  still count.
- **A project:** the `smoke` row is advisory. Resolve `commands.smoke` from native config, inspect its explicit argv array and authorization, and run that exact argv once with a 900-second bound. Never evaluate a TSV or table shell string. If no configured argv is available, report smoke NOT ASSESSED. A failure is a polish row
  (`from: smoke run of <date>`); a pass adds none. `record none` with no smoke command to run:
  say in one line that the polish rows come from the feel log and the person.

## Phase 2: Propose

**Cuts,** in this order, each with a reason from what exists:

1. A `not_yet` item that Out of scope or Avoid already rules out.
2. A `built` item whose check fails (`open`), offered as cut it or polish it.
3. A `not_yet` item that no Question, Hook, First minute, Challenge, Goal & fail state or Keep
   line names.

For a selling goal, every `not_yet` item left also shows "build it before <freeze date>, or cut
it". **Never propose an item a Keep line names.** The person can still name any item.

**Marks brought up to date:** a `not_yet` item whose `story` row is Complete is shown built and
marked `[x]` with the other writes.

**Polish rows** come from what exists, never invented: each `open` row, each smoke failure, and what the person adds. Each row ends
`· from: <source>`: `<check> check of <date>`, `smoke run of <date>` or `you said`. The person's rows and ticks stay; a row whose
source now passes is ticked, said in one line. Rows about a cut item go with the cut.

## Phase 3: Dates, for sell, early_access and publisher only

Any other goal gets no date, asked or shown.

- **Recorded** dates are shown, not asked again ("move the dates" changes them). A `passed
  freeze` row is said in one line; a `passed target` row is asked again.
- **Target:** ask in plain words named for the goal: when to release it (`sell`), when the Early
  Access launch is (`early_access`), when the pitch or demo is (`publisher`). Turn a month or
  "next spring" into a date and show it.
- **Freeze:** run `bash .game-studio/scripts/cut-read.sh --target <date>`; its `proposed freeze` row is
  70% of the way from today to the target. Ask "Freeze on <date>?" Options: `Freeze then` /
  `Another date`. Say what it means: from then on no new features, only the polish list and
  fixes; recorded, and nothing holds you to it yet. `target_past`: ask the target again.
- **A goal changed on the screen** ("I want to sell it") is written at once with
  `python .game-studio/runtime/studio.py settings --root <project-root> project.goal=<value>`, and its dates are asked. A guessed
  goal left as it is is not written. No other `project.yaml` key is touched.

## Phase 4: The screen and the pick

```text
$gs-cut · <title> · Goal: <goal> (set | guessed)
Cut? You pick; nothing is cut without your pick.
  1. [ ] <item>
     · <reason>
Staying: <n> built features · Never offered: your <n> Keep lines
Polish: <n> rows, from <the sources>
Dates: target <date> (<what>) · freeze <date>
Writes: <the briefs>, <the polish list>, <each story> · one commit
```

Leave out the Dates line for a goal that gets none, and Cut? when there is nothing to propose.
Every file is named on the Writes line before writing, and nothing is written before the pick.
Then ask with the question tool, multi-select, up to four proposals ("Cut which? Pick none to cut
nothing"); more are numbered in text and picked by number. The reason is the person's words if
they gave any, else the proposal's. With dates to ask, ask the target in the same call, then the
freeze as Phase 3 says.

## Phase 5: Write and commit

Run `bash .game-studio/scripts/cut-apply.sh` with `--brief <path>` for each `brief` row and:

- `--cut <n> "<reason>"` for each picked item: it leaves Features for the end of Out of scope as
  `- [-] <item> · cut: <reason> (<date>)`, plus ` · was built` when it was `[x]`; its story's
  Status becomes `Blocked — BLOCKED: cut by /cut <date>: <reason>` (the persisted marker; also recognize native `cut by $gs-cut` records), a status `$gs-dev-story` stops on
  (a Complete story keeps its status: `story moved`).
- `--mark <n>` for each mark brought up to date.
- `--dates <target> <freeze> "<what>"` when dates were given.
- `--polish "<row>"`, `--tick "<row>"` and `--drop "<row>"` for the polish list.

Moving an item renumbers the Features after it, so the stories traced to them are renumbered too
(`story renumbered`); the Writes line names every story a proposed cut can touch. `bad` rows mean
nothing was written: fix the arguments and run it again. A cut built item stays in the game until
it is taken out, an ordinary change: say "say 'take out <item>' to remove it".

Commit when `git rev-parse --is-inside-work-tree` succeeds, the pick being the commit instruction:
`git add -- <each wrote path, design/ ones first>`, then `git commit -m "docs: cut <items> · dates ·
polish list (<n> rows)" -m "Brief: design/game-brief.md" -- <the same paths>`. Leave out
`cut <items> · ` when nothing was cut, and `dates · ` when the Dates line did not change. No git:
"Not committed: this project has no git." Say in one line what was written.

Next step: build what is left before the freeze (`$gs-create-stories` writes a story for each
not-yet item in a project), and work down the polish list.

## Afterwards

- **"Bring back <item>":** use existing scope authorization when it explicitly
  restores this item; otherwise ask for that scope choice before writing. Identify
  the exact item and authoritative brief from `cut-read.sh`; run
  `bash .game-studio/scripts/cut-apply.sh --brief <path> --back "<item>" built|not_yet`
  for the applicable brief copies. Use `built` only while the feature is still in
  the game. Inspect the helper result and re-read the brief and associated story:
  the item must be back in Features, absent from its cut Out of scope entry, and
  its cut-blocked story must read `Ready`. Failure or an ambiguous mapping does not
  authorize clearing Status by hand. A successful Ready readback allows
  `$gs-dev-story` to continue its remaining prerequisites under existing work
  authorization. Commit only the actual `wrote` paths as `docs: bring back <item>`
  when that commit is authorized. Cutting a planned feature does not delete
  implemented code; removing code is a separately scoped implementation change.
- **"Move the dates":** Phase 3 again, with the recorded dates shown, then write and commit as
  Phase 5 does.
- Nothing blocks or warns on the freeze date in this version: only $gs-cut reads it back.
