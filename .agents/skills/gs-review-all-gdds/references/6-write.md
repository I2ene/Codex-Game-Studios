# $gs-review-all-gdds — Phase 6: Write Report and Flag GDDs

> Part of `$gs-review-all-gdds`. `.agents/skills/gs-review-all-gdds/references/workflow.md` names when to read this file; the settings it
> resolved and the rules under its later headings still apply here.


## Phase 6: Write Report and Flag GDDs

Use existing authorization to write the report. If not authorized, ask:
- Prompt: "May I write this review to `design/gdd/gdd-cross-review-[date].md`?"
- Options: `[A] Yes — write the report` / `[B] No — skip`

Use ISO YYYY-MM-DD report names and explicit companion selection. After the actual
report is written, run `receipts hash --root <project-root> --report <report>
--output <companion> <inputs>` for the scope actually read, including relevant
registry, GDD and configuration paths and the phase files used. Recheck any drift
since the review's input snapshot; no reuse when required inputs are unresolved.
Record Focus and skipped phases in the report. A partial report never stands for
a full review. See `.game-studio/resources/docs/review-receipts.md`.

If any GDDs are flagged for revision and the index update is outside authorized scope, ask:
- Prompt: "Should I update the systems index to mark these GDDs as needing revision? ([list of flagged GDDs])"
- Options: `[A] Yes — update systems index` / `[B] No — leave as-is`
- If yes: update each flagged GDD's Status field in systems-index.md to "Needs Revision".
  (Do NOT append parentheticals to the status value — other skills match "Needs Revision"
  as an exact string and parentheticals break that match.)

### Session State Update

After writing the report and any authorized index updates, resolve the checkpoint.
If it is enabled, append the authored summary through `checkpoint --append`:

    ## Session Extract — $gs-review-all-gdds [date]
    - Verdict: [PASS / NOT ASSESSED / CONCERNS / FAIL]
    - GDDs reviewed: [N of M present]
    - Phases not run: [names, or "None"]
    - Flagged for revision: [comma-separated list, or "None"]
    - Blocking issues: [N — brief one-line descriptions, or "None"]
    - Recommended next: [the Phase 7 handoff action, condensed to one line]
    - Report: design/gdd/gdd-cross-review-[date].md   ← only if user approved the write
    - Report: (not written — user declined at [date])  ← only if user declined the write

Use the appropriate line based on the user's response to the write-permission widget in Phase 6.

If the configured checkpoint does not exist and is enabled, use this block as its initial content. Never write a disabled checkpoint.
Confirm in conversation: "Session state updated."

---
