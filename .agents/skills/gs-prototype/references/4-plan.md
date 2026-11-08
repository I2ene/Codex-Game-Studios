# $gs-prototype — Phase 4: Plan the Prototype

> Part of `$gs-prototype`. `.agents/skills/gs-prototype/references/workflow.md` names when to read this file; the settings it
> resolved and the rules under its later headings still apply here.

## Phase 4: Plan the Prototype

Define in 3–5 bullet points the minimum viable prototype:

- What is the falsifiable hypothesis?
- What is the riskiest assumption — and how does this prototype test it first?
- What is the absolute minimum needed to answer the question?
- What is explicitly cut? (menus, save systems, error handling, polish, architecture — all of it)

**Scope constraint:** A concept prototype tests ONE mechanic — not the whole game.
If scope covers more than one mechanic, cut it down. When in doubt, cut more.

Present this plan to the user before building. Get confirmation before proceeding.

Once confirmed, if checkpoint recovery is enabled, save the plan to
`<resolved-checkpoint>` via `checkpoint --save <authored-file> --root <project-root>`.
Include the concept name, hypothesis, path chosen, scope, and current phase
("Phase 5 — Implement") so a resumed session can continue the approved plan.
If DISABLED, skip the state write and continue with the confirmed plan.

---
