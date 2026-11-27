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


Explicitly resolved — use as-is; `--review` overrides `review_mode`. No block →
defaults in `.game-studio/resources/docs/config-resolution.md`.

## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.


## Native phase execution

Every referenced phase inherits the native contracts above. Role or agent wording
describes a professional responsibility: apply it in the parent when delegation is
unavailable or unauthorized, read its gate file yourself, and label parent work.
Only actual delegated participants count as independent reviews. Existing task
authorization covers in-scope writes and implementation; later example approval
questions are for unresolved choices, not a requirement to ask again per file.
Bash helpers under .game-studio/scripts require a compatible shell and the consumer
root as working directory; inspect their TSV output. Native studio.py commands use
--root explicitly and emit JSON; never parse them as historical colon-prefixed rows.

# Guided Onboarding

The entry point for a new user. It assumes no game idea, no engine and no experience: it reads
the project, asks where the user is starting from, shows what it assumes about the project, and
names the one next step. Continue into it when the user already authorized the
end-to-end work; a request for a game goes straight to `$gs-prototype` (One-shot 1).

The main path leads: make a game (`$gs-prototype`), change it after play, grow it into a project.
The design documents, the agents and the `team-*` pipelines are studio mode, the path at rigor
`standard` and `full` (Phase 6).

This workflow may write `project.stage`, `project.goal`, `modes.rigor`
and `modes.automation`. It never writes `modes.review_mode` or `production/review-mode.txt`, and none
of the other knobs rigor fronts (`modes.workflow`, `docs.density`, `qa.level`,
`modes.story_granularity`, `team.size`): a written value pins that knob over the rigor expansion,
and a mirror file outranks it. The make-me-a-game route writes nothing: `$gs-prototype`'s card is
that route's assumptions card.

Ask with the question tool. Without one, list the options numbered and end your turn to wait. The
question is the last thing in the reply: no path, note or advice after it. A skipped or dismissed
question is not an answer: ask again in plain text.

The questions in Phases 2, 4 and 5 shape the project, so they are asked in every automation mode.
The engine is not one of them: `$gs-setup-engine` chooses it. Phase 6's last question follows a
`modes.automation` already in `project.yaml`, per `.game-studio/resources/docs/automation-modes.md`; with none
set, ask it.

## Phase 1: Read the project

**A game already asked for.** When the message that started this skill asks for a game itself
("make me a game", or a description of one: "a game where you herd sheep with a dog") and the
person did not type `$gs-start`, ask nothing and read nothing. Say in one line that you are taking
them straight to the build, then start `$gs-prototype` by reading its native entry with the original user request: it
reads their message as their words and asks only what is missing. Use actual inherited
model and permissions; native skill invocation does not switch models.

**A game brought.** When that message brings a game the person already has (a path to an
`.html` file or a folder, or "bring in my game"), do the same with `$gs-prototype --from <path>`.

Run `python .game-studio/runtime/studio.py project-state --root <project-root>` and read its JSON facts dictionary (each fact has value/source). Do not show them yet; they check
the user's answer in Phase 2.

| Fact | Use |
|---|---|
| `engine`, `code_root`, `source_files` | Is an engine set, and how much code is there. `source_files` of `unknown` means the code root could not be found: say that, never "no code" |
| `concept` | `design/gdd/game-concept.md` or `design/game-brief.md` exists |
| `gdd_files`, `adr` | Design documents and architecture decisions on disk (they set the stage in Phase 4) |
| `prototype`, `sprint`, `milestone`, `story` | Other existing work |
| `origin_url` | Contains `donchitos/claude-code-game-studios`, matched case-insensitively: the clone still points at the template repo, so a push or pull request would go there. A fork under another owner is the user's own |
| `stage` | The stage already recorded, if any |

Treat the inferred `phase` as a hint only: it guesses from file counts, and a project with code but no design
documents is not in Production. If the helper fails, say so and read the same facts by hand
(engine in `project.yaml`, the two concept files, the code root's files, `design/gdd/`).

The helper does not report rigor, automation or the goal. Read `project.yaml`, if it exists, and
note whether `modes.rigor`, `modes.automation` and `project.goal` are set: a set value is kept,
and it is neither guessed nor asked again (Phases 4 and 5).

**Returning user** (an engine is set and `concept` is present): ask nothing. Say the engine, the
`modes.rigor` implies (`minimal` → `solo`, `standard` → `lean`, `full` → `full`). Suggest `$gs-next-step` for the next step, add the
template-remote note if it applies, and stop.

## Phase 2: Ask where the user is

Ask with the question tool: "Welcome! Where are you starting from with your game?" Options:
- `A) Make me a game (playable in your browser)`: a browser game built from a few quick answers, any
  of which can be "you pick".
- `B) An idea, or none yet`: nothing yet, or a theme, feeling or genre ("something with space",
  "a cozy farming game").
- `C) Clear concept`: the core idea and genre are known, nothing is written down yet.
- `D) Existing work`: design documents, prototypes, code or plans already exist.

With `engine.name` set to an engine other than `web`, A reads `A) Make me a game`: a throwaway
prototype of one mechanic in that engine, with a browser sketch as one option.

Wait for the answer. If it contradicts Phase 1, say what you found once and ask again: D on an
empty project ("this looks like a fresh template; would A or B fit better?"), or B with code on
disk ("I found code in `[code_root]`; did you mean D?"). D on an empty project with no game
found (Phase 3) asks first, in plain text, where their game is: a path, or drop it in this
folder; an answer with no game in it gets the A-or-B question. If no option fits, let the user
describe their situation and route from that.

## Phase 3: Route

Name the immediate next step only. The full path waits for Phase 6, after the rigor is known.

- **A, make me a game:** ask nothing more. `$gs-prototype` asks the quick questions and shows a card
  of what it will build before it builds anything. Skip Phases 4 to 6: that card is this route's
  assumptions card, and this route writes no setting (a rigor left unset reads as `minimal`). Go
  to Phase 7 with `$gs-prototype`.
- **B, an idea or none yet:** ask in plain text: "What's the idea, in a few words? A theme,
  feeling or genre is enough, or say none." None: `$gs-brainstorm open`, which explores freely. A
  hint: `$gs-brainstorm [their words]`, taken as it is. A hint, with no engine set: ask "How would
  you like to go on?" with `Build it now (Recommended)` (`$gs-prototype [their words]`: pitches
  from the idea, then a playable browser game) / `Shape the idea first`
  (`$gs-brainstorm [their words]`). `Build it now` goes on as route A. Describe it as "turns an idea, or none, into
  a written design the next step builds from"; how long that design is depends on the rigor, so
  leave that for Phase 6.
- **C, clear concept:** ask for the concept in one sentence (genre and core mechanic), as plain
  text. Then ask: "How would you like to proceed?" With no engine set and none named in the
  sentence, the options are `Build it now (Recommended)` (`$gs-prototype` makes it a playable
  browser game) / `Formalize it first` (`$gs-brainstorm [concept]` writes it down) /
  `Jump straight in` (`$gs-setup-engine` now, write the design after). With an engine set or named:
  `Formalize it first` / `Jump straight in` / `Browser sketch first` (`$gs-prototype --path html`, a
  throwaway in the browser; not recommended, since the game is rebuilt in the engine). The next
  step is their pick. `Build it now` goes on as route A, and so does `Browser sketch first`, with
  `$gs-prototype --path html` as the skill to type.
- **D, existing work, a game first:** look for a game they made elsewhere: an `.html` file up to
  two folders deep, outside `prototypes/`, `.agents/`, `.codex/`, `.game-studio/`, `docs/`, `design/`, `production/`,
  `references/`, `node_modules/`, `dist/` and `build/`, whose page has a `<script>` and a
  `<canvas>`, `requestAnimationFrame` or an engine loader; or a folder holding such an
  `index.html` (Glob, then Grep). One to three found: offer each by name, plus "Something else".
  A pick ends on "Type `$gs-prototype --from <path>` to begin: it brings a copy in exactly as it
  is." Skip Phases 4 to 6, as on route A. A folder with a `package.json` at its top is not one of
  these: it is a web project with its own build (`$gs-setup-engine web`). A page with no script is
  not offered.
- **D, existing work:** say what Phase 1 found ("N source files under `[code_root]`, N design
  documents, engine [X / not set]"). When `gdd_files` is 1 or more and Glob finds no
  `prototypes/*/index.html`, the design is written but there is nothing to play yet:
  - No engine set, or `web`: the next step is a playable first, `$gs-prototype` built from their
    concept doc (`$gs-prototype design/gdd/game-concept.md`; with no concept doc, the GDD that
    describes the whole game). Say in one line: "Your design documents stay the source of truth;
    the brief `$gs-prototype` writes is only a summary for the build."
  - An engine other than `web`: the next step stays `$gs-project-stage-detect`. Say in one line that
    `$gs-prototype --path html` is the fast option: a browser sketch of the core game,
    thrown away when the engine build starts.

  Otherwise: `$gs-setup-engine` when no engine is set and there is no more than a concept; else
  `$gs-project-stage-detect`.

Then, except on route A, say: "I'll lay out the full path in a moment."

## Phase 4: Show what you assume, then save it

Work out three values.

**Stage.** Paths B and C: `Concept`. Path D, from the Phase 1 rows:

| On disk | Stage |
|---|---|
| no engine, or nothing beyond a concept (`gdd_files` 0) | `Concept` |
| `gdd_files` 1 or more, `adr` 0 | `Systems Design` |
| `adr` 1 or more | `Technical Setup` |

**Rigor.** If `modes.rigor` is already set in `project.yaml`, keep it and say so. Otherwise infer
it from what the user said in Phases 2 and 3, using the signals in
`.game-studio/resources/docs/settings-guidance.md` `3:

| The user's words mention | Rigor |
|---|---|
| open world, RPG, sim, sandbox, factions, crafting, economy, MMO, multiplayer, many systems | `full` |
| release, commercial, Steam, one clear core loop | `standard` |
| jam, weekend, prototype, first game, small, just trying | `minimal` |
| nothing above, or no idea yet | `minimal` (the default) |

A path B hint is still a description: "some kind of open-world survival sim" is `full`.

On path D, count the system GDDs: `gdd_files` less `game-concept.md` and `systems-index.md`
when they exist. About 9 or more (`.game-studio/resources/docs/settings-guidance.md` §4) proposes `standard`,
with the reason "[N] system design documents; most projects this size run `standard`", unless
the words above point to `full`. A `modes.rigor` already set is still kept.

**Goal.** If `project.goal` is already set, keep it and say so. Otherwise guess it from what the
user said in Phases 2 and 3; it is never a question of its own:

| The user's words mention | Goal |
|---|---|
| a game jam, or a theme with a deadline | `jam` |
| learning, a first game, practice, a course or class | `learn` |
| a portfolio, a job, showing their work | `portfolio` |
| selling it, Steam, a price, commercial, wishlists | `sell` |
| early access | `early_access` |
| a publisher, a pitch, funding | `publisher` |
| mobile, a phone, iOS, Android, an app store | `mobile` |
| a purpose none of the rows above fits | `other` |
| fun, themselves or friends, or nothing above | `hobby` (the default) |

When two fit, a selling goal wins over the others, and `early_access` or `publisher` over `sell`.

Show the card:

```
What I'll set up
  Stage:  [stage]  ([why, from what was found or picked])
  Rigor:  [value]  ([why, in the user's words] | [N] system design documents | already set)
          minimal: short brief, coarse stories, tests optional; about 4 steps to code
          standard: studio mode; about 8 design documents before code; standard QA evidence
          full: studio mode; standard plus validation builds; evidence everywhere
  Goal:   [value]  ([why, in the user's words] | guessed | already set)
          jam, learn, hobby, portfolio, sell, early_access, publisher, mobile or other
  $gs-project-settings changes any of these any time.
```

Ask only when not already authorized: "Save these settings to `project.yaml`?" Options: `Save them` / `Change something` / `Don't save`. Ask no
question about the rigor or the goal itself: the card shows them, and the user changes them there
or later with `$gs-project-settings`.

- **Change something:** ask what to change, starting with a *guessed* goal, then show the card
  again with the new value and "you said" as its reason, and ask the save question again. A value
  changed here is saved even when it was already set.
- **Save them:** run `python .game-studio/runtime/studio.py settings "project.stage=[stage]" --root <project-root>`, then
  `python .game-studio/runtime/studio.py settings modes.rigor=[value] --root <project-root>` and
  `python .game-studio/runtime/studio.py settings project.goal=[value] --root <project-root>`, each only when that key was not
  already set or was changed on the card. Read config JSON again and verify values/provenance. Say: "Saved. Rigor
  `[value]` sets six other settings; `$gs-project-settings` shows them and changes any of them."
- **Don't save**, or anything other than an explicit yes: write nothing, keep the values for this
  run, and say they were not saved.

If a helper exits non-zero, show its output, say which setting was not written, and go on with the
value for this run.

## Phase 5: Ask how much to confirm

If `modes.automation` is already set, say "Automation is `[value]`" and go on. Otherwise ask:
"Last one: how much should I confirm with you as we work?" Options:
- `Guided (Recommended)`: I decide small things and still stop for big ones (scope changes,
  deletions, schema changes).
- `Collaborative`: I ask before each significant step and show drafts before writing.
- `Autonomous`: I proceed and log decisions, stopping only for the always-ask categories. Fastest,
  most tokens.

Mapping: `Guided` → `guided`, `Collaborative` → `collaborative`, `Autonomous` → `autonomous`. The
pick is the consent to write it: run `python .game-studio/runtime/studio.py settings modes.automation=[value] --root <project-root>`,
unless the Phase 4 save was declined (then say it was not saved).

## Phase 6: Show the path

Say: "Here's your path at rigor `[value]`. Every skill still runs at any rigor; rigor changes
what's required, not what's allowed."

Except on path D, lead with the main path, in one line: "The main path: make a game
(`$gs-prototype`), change it after you play it (ask in plain words), then grow it into a project
with the steps below." At `standard` or `full`, add one line after the path: "This is studio
mode: the design documents, agents and `team-*` pipelines. It fits a team, a long project, or
someone who wants the paperwork."

The path starts with the step Phase 3 named. When that was `$gs-brainstorm` (path B and C's
`Formalize it first`), list `$gs-brainstorm` first and `$gs-setup-engine` after it: each runs without
the other. With no engine set, `$gs-prototype` goes between them.

**`minimal`: 4 steps to running code**
1. `$gs-setup-engine`: choose and configure the engine (web, unless you name another)
2. `$gs-brainstorm`: write the one-page `design/game-brief.md`
3. `$gs-create-stories`: turn the brief's Features list into stories (no epics or sprint plan needed)
4. `$gs-dev-story`: the first line of game code

With no engine set, `$gs-prototype` builds the brief as a playable browser game: list it
straight after `$gs-brainstorm`, as the recommended next step, and `$gs-setup-engine` after it.

**`standard`** (studio mode)
- Concept: `$gs-setup-engine` → `$gs-brainstorm` → `$gs-prototype` → `$gs-art-bible` → `$gs-map-systems` →
  `$gs-gate-check`. With no engine set, `$gs-setup-engine` moves after `$gs-prototype`: the playable
  first, the engine last
- Systems Design: `$gs-design-system` (once per system) → `$gs-review-all-gdds` → `$gs-gate-check`
- Architecture: `$gs-create-architecture` → `$gs-architecture-decision` (once per decision) →
  `$gs-architecture-review` → `$gs-create-control-manifest` → `$gs-ux-design` (accessibility and
  interaction patterns) → `$gs-test-setup` → `$gs-gate-check`
- Pre-Production: `$gs-ux-design` (HUD and key screens) → `$gs-create-epics` → `$gs-create-stories` →
  `$gs-sprint-plan` → `$gs-gate-check`
- Production: `$gs-dev-story`

Each `$gs-gate-check` moves the project one stage, and only when it passes.

**`full`** (studio mode): everything in `standard`, plus `$gs-vertical-slice` and `$gs-playtest-report`
in Pre-Production and `$gs-design-review` after each GDD.

**Path D with existing work** (stage `Systems Design` or later, or code on disk) gets this instead.
Print only the steps that apply, and for the brief only the one source that applies. When Phase 3
named `$gs-prototype` from their design documents, list it first, before the numbered steps; with an
engine other than `web`, add `$gs-prototype --path html` after step 1 as the fast option. At
`minimal`:
1. `$gs-project-stage-detect`: what stage the project is at and what is missing
2. `$gs-adopt`: whether the existing files are in the format the skills read
3. `$gs-setup-engine`: only when no engine is set; leave it out when `engine` names one
4. The brief, only if `concept` is absent: `$gs-reverse-document design [code_root]` when the code
   root holds 10 or more source files (it writes the brief from the game), and then do not mention
   `$gs-brainstorm` at all; `$gs-brainstorm` only when it holds fewer

At `standard` and `full`, steps 1 to 3, then `$gs-design-system retrofit [path]`,
`$gs-architecture-decision retrofit [path]`, `$gs-architecture-review` and `$gs-gate-check`.

Present `minimal` as the documented floor, not a lesser mode, and name its trade once: no GDDs, so
design problems show up in code.

Ask: "Would you like to start with [first step]?" Options: `Yes, start with [first step]` /
`Something else first`. Use Phase 7 to hand off or continue within existing end-to-end authorization.

## Phase 7: Hand off

Name the selected next skill and its purpose. Continue by reading its native entry
when the user has authorized that work; preserve the original request and answers.
Otherwise offer the command to begin it. Route A uses `$gs-prototype`; Browser sketch
first uses `$gs-prototype --path html`. Never require a typed reinvocation for model
selection, and never claim a skill changed the inherited model.

Verdict: **COMPLETE**, the user is oriented and handed off. A game already asked for (Phase 1)
gives no verdict: `$gs-prototype` takes over. If the user stopped before Phase 7, say which settings
were saved and which were not.
