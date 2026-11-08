## Native checkpoint interface

Read .game-studio/resources/docs/context-management.md. Explicitly run recover
--root <project-root> and use checkpoint.path as <resolved-checkpoint>. If DISABLED,
skip checkpoint reads/writes; do not create a fixed fallback. Otherwise write the
current concise authored state to a temporary repository-local Markdown file and
run checkpoint --save <authored-file> --root <project-root>. Preserve useful fields
from the prior snapshot, reconcile current facts and replace stale state; the helper
keeps a hash-named backup. Do not append unbounded history or infer unseen work.
Existing task authorization covers routine state writes; state never grants consent.

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


Explicitly resolved — use as-is; `--review` overrides `review_mode`. No block →
defaults in `.game-studio/resources/docs/config-resolution.md`.

## Resolve this run's settings

Run `python .game-studio/runtime/studio.py config --root <project-root>` explicitly. Use effective values and provenance. Duplicate keys or malformed YAML are errors: inspect and repair the source configuration before dependent writes or commands; no merged values are authoritative after an error.



Ask with the question tool. Without one, list the options numbered and end your turn
to wait. A skipped question grants no approval. For optional questions continue with a stated reasonable assumption; keep genuinely required unresolved decisions pending.

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

# Story Done

Closes a finished story. Every acceptance criterion is checked against evidence,
deviations from the GDD, the ADRs and the story's own scope are reported as facts,
and the story is marked Complete only on the user's yes.

**Writes, after the user's yes:** the story file (`Status`, `Last Updated`, a
`## Completion Notes` section) and its `production/sprint-status.yaml` entry;
`docs/tech-debt-register.md` only when the user picks that option. The session
checkpoint is written at the end of every run, whatever the verdict.
**Next:** the next story (Phase 8).

Asks follow `.game-studio/resources/docs/automation-modes.md` (collaborative resolves open decisions, guided
asks on major choices, autonomous logs and goes on; `automation_always_ask`
categories require input only for decisions outside existing authorization).

Checklist (copy it and tick as you go):

```
- [ ] Phase 1: story found, facts and settings read
- [ ] Phase 2: what the story is checked against, loaded for its tier
- [ ] Phase 3: each criterion verified, traceability table built
- [ ] Phase 4: test evidence and run result checked
- [ ] Phase 5: deviations and scope checked
- [ ] Phase 6: review gates run, or their skip noted
- [ ] Phase 7: report and verdict shown; close asked
- [ ] Phase 8: next story named, checkpoint written, closing block printed
```

## Phase 1: The story and its settings

**Which story.** The text typed after the skill name, with any `--review <mode>`
pair removed, is the story path. With nothing typed:

1. The checkpoint in `<resolved-checkpoint>`: its **Current task**
   line, when it names a story.
2. Else the stories in progress: `bash .game-studio/scripts/story-facts.sh --all`, rows
   whose state is `IN_REVIEW` or `IN_PROGRESS`. Several: ask "Which story are we
   closing?" with one option per story.
3. None: ask for the path. When `production/epics/` holds no story file at all,
   stop:
   "No stories found in `production/epics/` — run `$gs-create-stories [epic-slug]` to make them (at `standard` and `full`, run `$gs-create-epics` first if there is no epic yet)."

**Its facts.** `bash .game-studio/scripts/story-facts.sh <story-path>` gives the status,
type, layer, TR-IDs, ADRs, criteria count, test-evidence status and dependencies.
Then read the story in full: the criteria text, the Test Evidence path, `## Files`,
Out of Scope.

**Tier.** `workflow` for the story's system, keyed on the GDD filename stem of its
`GDD:` path (`design/gdd/<stem>.md` → `<stem>`; the `[system]` of its TR-ID only
when there is no GDD path): that system's `system_overrides` row if there is one,
else the project value.

**What `qa.level` requires** (the evidence rows of `.game-studio/resources/docs/coding-standards.md`).
Take the value from the `qa.level` line above, never from `workflow` or `rigor`: the
two are set apart, so `workflow: minimal` with `qa.level: standard` still requires a
Logic story's unit test.

| Check | `qa.level: minimal` | `qa.level: standard` | `qa.level: full` |
|---|---|---|---|
| Logic, Integration test | waived | required | required |
| Config/Data smoke report | waived | required, advisory by default | required, **blocking** by default |
| Visual/Feel, UI retained screenshot | required | required | required |
| Untested criteria (Phase 3) | never escalate | more than half block | **any** blocks |

The look is never waived: a Visual/Feel or UI story needs its screenshot at every
level. **Gate level** per type is the `gate_level` line above. At `full`, a
Config/Data default (`config=advisory(default…)`) becomes blocking; an explicit
`testing.strict.config: false` still makes it advisory.

## Phase 2: What the story is checked against

By the tier. Read every document by section, never whole.

- **`full`:** the current requirement text of each TR-ID: in
  `docs/architecture/tr-registry.yaml`, the lines matching `id: <TR-ID>\s*$` and the
  entry's text below (the anchor keeps `TR-combat-001` from matching
  `TR-combat-0010`; `\s*` takes a Windows line ending). Never use text quoted in the
  story; the GDD's Acceptance Criteria and Detailed Design
  (`python .game-studio/runtime/studio.py markdown --root <project-root> extract design/gdd/<file>.md "Acceptance Criteria"`,
  then the same for `"Detailed Design"`; if its JSON status says absent, try `"Detailed Rules"`, the design
  standard's name for the same section);
  each ADR's status with `bash .game-studio/scripts/adr-status.sh <ADR ids>`, then its
  Decision and Consequences sections.
- **`standard`:** the same GDD sections; the ADR sections only for a critical ADR
  (`adr-status.sh`'s layer column reads Foundation, or has no layer).
- **`minimal`:** none. The story's criteria are the spec.

At every tier, when `docs/architecture/control-manifest.md` exists, note its
`Manifest Version` line.

Known failing tests are actual evidence: apply the resolved testing.strict level and the affected criteria; never label failure as NOT ASSESSED or pass. File existence alone proves no behavioral criterion.

## Phase 3: Verify each criterion

Take each acceptance criterion in turn:

- **Checked by looking:** a file the criterion names exists; a test file it names
  exists (report "test file present", never "test passes": nothing here runs it);
  numeric literals in gameplay code that belong in data files; player-facing
  strings in the code root that belong in localization files (resolve the root
  per `.game-studio/resources/docs/code-root-resolution.md`; unresolved, report `NOT ASSESSED —
  code root unresolved`, never zero hits).
- **Asked:** behaviour ("the player takes damage when…"), feel, and performance
  criteria. Never mark one passed from reading the code: the code says what should
  happen, not what the build does. Up to four per ask: "Does [criterion]?" Options:
  Yes — passes / No — fails / Not tested yet. `Not tested yet` is UNTESTED, and
  keeps the verdict at best NOT ASSESSED until someone checks it.
- **Seen on screen:** a criterion about something visible is covered by a retained
  image under `production/qa/evidence/[story-slug]/` (`[story-slug]`: the story
  file's name without `.md`) that you opened and saw it in.
  Never describe an image you have not opened; a checkpoint's `Run result:
  OBSERVED — <text>` is `$gs-dev-story`'s description, to quote as such.
- **Needs a full playtest:** `DEFERRED — requires playtest session`. It does not
  block.

Then map each criterion to what covers it: a test under the test root, a
"Yes — passes", or a retained image.

```
| Criterion | Covered by | Status |
|-----------|------------|--------|
| AC-1: [text] | tests/unit/[system]/[file]::[test] | COVERED |
| AC-2: [text] | production/qa/evidence/[slug]/01-[what].png | COVERED |
| AC-3: [text] | — | UNTESTED |
```

Untested criteria escalate by the Phase 1 table: blocking above the line; below it,
advisory, listed in the Completion Notes as "Untested criteria: [AC-N list]".

## Phase 4: Test evidence and the run result

By the story's type, at the Phase 1 gate level. Skip a check `qa.level` waives, and
say so: `Test evidence: waived at qa.level minimal`.

- **Logic:** the exact path in the story's Test Evidence section, else anywhere
  under `tests/unit/[system]/`.
- **Integration:** the same under `tests/integration/[system]/`, else a playtest
  record naming this story in `production/qa/playtests/` (`$gs-playtest-report`
  writes them there).
- **UI:** a UI story is satisfied by the retained screenshot of each screen touched,
  under `production/qa/evidence/`. No evidence doc or sign-off needed.
- **Visual/Feel:** the screenshot, and a Visual/Feel story also needs the sign-off:
  `production/qa/evidence/[story-slug]-evidence.md` with every sign-off row
  `[x] Approved` (one person may sign every role).
- **Config/Data:** a `production/qa/smoke-*.md` report; none: "No smoke check
  report found. Run `$gs-smoke-check`."
- **No Type:** advisory: "Story Type not declared. Add `Type:` to the story header."

A missing item is a gap at the gate level: BLOCKING stops COMPLETE, ADVISORY goes
in the notes. Name what is missing and where it goes. An evidence doc with no image
beside it is not evidence: a described check is an assertion.

**Is the evidence older than its code?** For retained visual evidence, locate the
actual report/companion pair per [story capture receipts](.game-studio/resources/docs/review-receipts.md#story-capture-receipts). If found, run
`python .game-studio/runtime/studio.py receipts check <source-and-image-patterns...> --receipt <evidence.receipt.json> --root <project-root>`
with the companion's saved patterns. Report freshness separately; apply the
existing evidence gate only when the required evidence itself is missing,
unreadable or inadequate. No companion means freshness is NOT ASSESSED, not a
failed criterion.

**Run result, every other type.** Take the `Run result:` line from the `$gs-dev-story`
checkpoint (only when its **Current task** names this story) or the story's Completion Notes.
`OBSERVED` with a path: note it. `N/A — <reason>`: accept only a reason that says
why nothing is observable ("it's a Logic story" is not one). `NOT VERIFIED` on a
story whose criteria name something on screen: a gap at the gate level. No line:
advisory, "confirm the build was launched and looked at". A user's "Yes — passes"
to an on-screen criterion with no retained image is an assertion, not an
observation: a gap at the gate level.

## Phase 5: Deviations and scope

Run, by tier (`minimal` skips 1 and 3):

1. **GDD rules** (`full`; `standard` on its required sections): search the changed
   files for the names the current GDD text and TR requirement use.
2. **Manifest:** the story's `Manifest Version` older than the manifest's: ADVISORY,
   "written against manifest v[story]; current is v[current] — run
   `$gs-story-readiness` to check". No manifest: skip. A `Manifest-Note:` line in the
   story is carried into the deviations as written.
3. **ADR constraints** (`full`; `standard` for a critical ADR): search for the
   patterns the ADR's Decision or the manifest forbids.
4. **Hardcoded values** in the changed files.
5. **Scope:** compare the confirmed changes attributable to this story against
   `### Planned` and explicit accepted scope changes in `## Files`, and reconcile
   `### Actual` with the observed changes. An actual list is evidence of work,
   not authorization for it. Changes outside the approved scope are OUT OF SCOPE.
   For a legacy unlabelled list, establish its provenance using the pre-work
   story or actual checkpoint. If a clean tree, unrelated edits or missing
   history prevent a comparison, record `Scope: NOT ASSESSED` and why; do not
   claim a clean scope from an empty diff.

Each deviation is **BLOCKING** (contradicts the GDD or ADR), **ADVISORY** (drifts
but works the same; the user decides) or **OUT OF SCOPE** (for awareness). State
them as facts; the user judges them.

## Phase 6: Review gates

Read the `review_gate` line above.

- **`skill-gates=skip`:** no agent. Note `QL-TEST-COVERAGE skipped — [Solo | Lean]
  mode` and `LP-CODE-REVIEW skipped — [Solo | Lean] mode`. In `lean` mode, ask: "Did
  you run `$gs-code-review` on the implemented files?" Options: Yes — it passed or was
  approved with suggestions / No — skipping review for this story / No — I'll run
  it before the sprint close-out. The answer sets Reviewed by.
- **`skill-gates=run`:** read [review-gates.md](review-gates.md) and
  `.game-studio/resources/docs/director-gates.md`, and run both gates now. On a skip, do not load
  it.

**Reviewed by** is never blank: `lead-programmer` when LP-CODE-REVIEW ran;
`$gs-code-review (you said you ran it; not verified here)` for the lean Yes; `self, no
independent review` in solo mode, for either No, and when no implementation file
exists yet.

## Phase 7: Report, verdict, and the close

```markdown
## Story Done: [title]
**Story**: [path] · **Type**: [type] · **Date**: [today]

### Acceptance Criteria: [X/Y passing]
- [x] [criterion] — [how verified]
- [ ] [criterion] — FAILS: [reason]
- [?] [criterion] — DEFERRED: requires playtest

### Traceability
[the Phase 3 table]

### Test Evidence
**Required**: [what the type needs at this qa.level, or "waived at qa.level minimal"]
**Found**: [YES — path | NO — BLOCKING | NO — ADVISORY]

### Deviations
[NONE, or each: BLOCKING / ADVISORY / OUT OF SCOPE — description — reference]

### Review
**Reviewed by**: [value]

### Verdict: [COMPLETE | COMPLETE WITH NOTES | NOT ASSESSED | BLOCKED]
```

**Verdicts, the first that matches wins:**

1. **BLOCKED:** a criterion fails, or a BLOCKING gap or deviation stands.
2. **NOT ASSESSED:** a criterion could not be evaluated: it names no observable
   outcome, the user answered "Not tested yet", a review gate returned NOT ASSESSED
   and its input was not supplied, evidence exists but cannot be read, or the GDD
   or ADR a deviation would be judged against is missing. Name each one and what
   would settle it. It outranks the two passes and never hides a failure.
3. **COMPLETE WITH NOTES:** every criterion passes or is DEFERRED, with advisory
   items listed. An absent sprint file and capture freshness alone are informational.
   Known criterion failures and actual required evidence gaps still use their
   applicable gate; do not infer either from a freshness observation.
4. **COMPLETE:** every criterion passes, nothing advisory.

**Then ask, before writing anything:** "How do you want to proceed?" Options:
Close the story — mark it Complete and log notes (Recommended) / Close and log the
advisory deviations as tech debt / Don't close yet — I'll fix things first / Close
anyway, accepting the deviations. On BLOCKED or NOT ASSESSED, recommend "Don't close
yet" and list what must change. Closing such a story is a `scope_changes` decision:
when the `automation_always_ask` line lists it, ask in every automation mode, even
when the user's own request is what got here. Write only on an explicit choice to
close.

**On close:**

1. `python .game-studio/runtime/studio.py markdown --root <project-root> set-field <story> Status Complete`, then
   `python .game-studio/runtime/studio.py markdown set-field <story> "Last Updated" <YYYY-MM-DD> --after Status --root <project-root>`.
2. Add at the end of the story, with a file edit, never a shell command (a shell
   write skips the project's write checks):
   ```markdown
   ## Completion Notes
   **Completed**: [date]
   **Criteria**: [X/Y passing] ([deferred items])
   **Deviations**: [None, or the advisory ones]
   **Test Evidence**: [path, or "waived at qa.level minimal", or "none required"]
   **Reviewed by**: [value]
   ```
3. "Close and log as tech debt": read [tech-debt-row.md](tech-debt-row.md) and add one
   row per advisory deviation.
4. `production/sprint-status.yaml`, when it exists: this story's entry gets
   `status: done` and `completed: [date]`, and the top-level `updated` gets today.
   The close answer covers it.
5. Print a suggested commit: `git add [the changed code and test files] [story path]`
   and `git commit -m "feat: [story title] ([TR-ID])"`.

**On "Don't close yet":** change no story file. List what the user flagged. Never
fix a failing criterion yourself: report it and ask what to do.

## Phase 8: Next story, checkpoint, close

**The next story.** With no sprint plan in `production/sprints/` (always at
`workflow: minimal`): Run `python .game-studio/runtime/studio.py stories --root <project-root>` after the close, so
this story's new status is in it. Read the JSON stories/unfinished arrays, counts and next object. Categories are
IN_REVIEW, IN_PROGRESS, TODO, BLOCKED, OTHER/NO_STATUS and COMPLETE. Preserve the
helper's ordering and inspect dependencies before recommending its candidate; a
TODO candidate is not proof its prerequisites are met. next.action, next.skill and
next.path identify the proposed route:

```
### Next Up
**[Story NNN: title]** — [one line]
Run `$gs-story-done [path]` to close it (In Review) — else `$gs-dev-story [path]` to implement it.
```

When the `workflow` line above reads `minimal`, print no `$gs-story-readiness` line at
all, not even as an option: it is not on that path. With no sprint plan at
`workflow: standard` or `full`, add "Run `$gs-story-readiness [path]` first."

- A nonempty story set with counts.COMPLETE equal to its total: every story is recorded complete; that does not prove game quality. Offer: play the build and note what
  feels wrong; add stories from the brief with `$gs-create-stories`; or `$gs-settings` to
  raise `modes.rigor` if the game has outgrown its brief.
- Only BLOCKED, OTHER or NO_STATUS categories remain: there is no Next Up, and the
  build order is **not** done. Name each story with its blocker, `Draft` or `no
  status`.
- Never print the Sprint Close-Out Sequence on this branch: there is no sprint.

With a sprint plan: read [sprint-next.md](sprint-next.md).

**The checkpoint**, on every verdict, closed or not. When recovery enables a checkpoint, author the block in a temporary repository-local Markdown file and save it with
`python .game-studio/runtime/studio.py checkpoint --save <authored-file> --root <project-root>`, which replaces the resolved snapshot and keeps its hash backup:

```
**Updated:** [date]
**Branch:** `[current git branch]`
**Current task:** $gs-story-done — [story path]: [verdict], [closed | left open]
**Next step:** [the Next Up command, or the fix the verdict named]
**Blocked on:** [nothing, or what blocked the verdict]
**Files in progress:** none
**Open questions:** [tech debt logged: N items, or none]
```

**The run's last reply ends with this block** (repeat it if you showed it earlier):

```
Verdict: [COMPLETE | COMPLETE WITH NOTES | NOT ASSESSED | BLOCKED] — [story path]
Story: [closed — Status: Complete | left open — Status: [status]]
Review: [Reviewed by value; the gates' skip notes]
Next step: [$gs-dev-story [path] | $gs-story-done [path] | the fix | play the build]
```
