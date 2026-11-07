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


Resolve settings explicitly with the native config command; retain its values and provenance.


`--review` overrides `review_mode`; store it for all gate spawns this run. See
`.game-studio/resources/docs/director-gates.md` for the full check pattern. Individual gate definitions live in `.game-studio/resources/docs/director-gates/[gate-id].md` — the actual reviewer reads its gate file; read it in the parent when applying the role yourself.

Every `ask the user` call follows `.game-studio/resources/docs/automation-modes.md`
(collaborative resolves open choices · guided resolves major choices · autonomous records in-scope choices;
`automation_always_ask` categories require input only outside existing authorization).

**`docs.density`** — it controls per-section *depth*, where `workflow`
controls which sections exist. `modes.rigor` sets both together; set
`docs.density` explicitly to vary depth alone: `terse` (the default, via `rigor: minimal`) = pillar bullets + concept bullets;
`balanced` = pillars + concept with brief rationale (`rigor: standard`); `thorough` =
pillars + concept + extensive rationale + alternatives. Apply it to every section
you author.

---

## Resolve this run's settings

Run `python .game-studio/runtime/studio.py config --root <project-root>` explicitly. Use effective values and provenance. If duplicate keys are reported, inspect the merged values to repair configuration before dependent writes or commands.


(`workflow: minimal`, `review_mode: solo`, `automation: collaborative`, `docs.density: terse`), and
say that the settings were not read.

# Brainstorm

Turns no idea, or a rough one, into a written design the next step builds from. How much it writes
depends on `workflow`:

- **`minimal`:** the Lean Brief flow below: a one-page `design/game-brief.md`, then stop. No
  discovery questions, pillars, director gates or `game-concept.md`, and do not load
  `.agents/skills/gs-brainstorm/references/full-concept.md`.
- **`standard` or `full`:** read `.agents/skills/gs-brainstorm/references/full-concept.md` and follow it. It writes
  `design/gdd/game-concept.md` from `.game-studio/resources/docs/templates/game-concept.md`. Its gates follow
  `.game-studio/resources/docs/director-gates.md`; each director agent is given its own gate file,
  `.game-studio/resources/docs/director-gates/<gate-id in lower case>.md` (`cd-pillars.md`,
  `ad-concept-visual.md`, `td-feasibility.md`, `pr-scope.md`), and you do not read those files
  yourself.

`--review` in the text typed after the skill name overrides `review_mode` for this run.
`docs.density` sets each section's depth: `terse` = bullets; `balanced` = with brief rationale;
`thorough` = rationale and alternatives. Questions follow `.game-studio/resources/docs/automation-modes.md`
(collaborative asks, guided asks only for major decisions, autonomous logs and proceeds; the
always-ask categories always ask).

Ask with the question tool. Without one, list the options numbered and end your turn to wait. The
question is the last thing in the reply: no advice or lean after it. A skipped or dismissed
question is not an answer: ask again in plain text.

## Lean Brief flow (`workflow: minimal`)

A few exchanges, not fifteen: capture the thinking that carries the game on one page, then get to
code. Write from the template `.game-studio/resources/docs/templates/game-brief.md` (six required fields, three
one-liners). If `design/game-brief.md` exists, read it and refine it instead of starting over.

1. **Concept.** From the hint typed after the skill name (or one quick open question if there is
   none), propose **2 or 3 one-line concepts** (verb-first or a mashup of genre and theme), not
   full concept cards. Ask the user to pick or combine them. This is the one creative question
   every run asks.
2. **Fill the brief** in conversation, several fields per exchange:
   - **Working title:** the brief's title line. Offer one from the chosen concept and let the user
     change it; `$gs-create-stories` names the epic folder after it.
   - **Pitch:** the excited one-liner.
   - **Core loop:** the 2 to 4 steps the player repeats.
   - **Player goal & fail state**: what the player tries to do, and how they lose.
     `$gs-create-stories` turns it into acceptance criteria.
   - **MVP:** the short list that makes it the game; each item becomes a story. **More than 7
     items: push back.** Say it is too long for an MVP, propose which items to cut (the ones the
     core loop works without), and keep the brief to 7 or fewer.
   - **Out of scope:** what they are deliberately not building (the cut items go here).
   - **Build order:** the riskiest or least proven part first.
   - **Who it's for and what they feel**, **Art & audio direction**, **Reference game** (the
     closest shipped game, and the part of it the MVP keeps): one line each; offer, don't force.
3. **Show the filled brief in full.** Then ask, as its own question: "Brief is ready. May I write it
   to `design/game-brief.md`?" `Yes — write it` / `Revise a field first`. Write only on an explicit
   yes to this question; agreeing to a cut or saying "go on" is not a yes to the write. On a
   revision, change the named field, show it before and after, and ask again. Then write
   `design/game-brief.md`, creating folders as needed. Never write `design/gdd/game-concept.md`
   at this tier.
4. **Next steps.** Read `engine.name` in `project.yaml`:
   1. `$gs-setup-engine`: configure the engine. List it **only** when `engine.name` is absent or
      empty: on the minimal path it usually ran before this skill.
   2. `$gs-create-stories`: turn the MVP list into stories. At `minimal` there is no separate
      `$gs-create-epics` or `$gs-sprint-plan`; the build order is the plan.
   3. `$gs-dev-story`: the first line of game code.

   Then one summary line: the pitch, the number of MVP items, and `design/game-brief.md`. End with
   the line `Verdict: COMPLETE — game brief written; next stop is code.`

If the user stops before the write, say the brief was not written, so it lives only in this
conversation.
