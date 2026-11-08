# $gs-architecture-review — Phase 1: Load Everything

> Part of `$gs-architecture-review`. [workflow.md](workflow.md) names when to read this file; the settings it
> resolved and the rules under its later headings still apply here.

## Phase 1: Load Everything

**In this file:**

- Phase 1a — L0: Summary Scan (fast, low tokens)
- Phase 1b — L1/L2: Targeted Section Load
- Design Documents
- Architecture Documents
- Engine Reference
- Project Standards

### Phase 1a — L0: Summary Scan (fast, low tokens)

**Freshness check before any scan.** A prior report can stand in for this run
only if nothing it rests on has changed: the documents, the engine reference,
the project config, this skill, and the kind of review that produced it.

In `rtm` mode, skip the check and say so — *"Freshness check: not run — rtm
builds the matrix fresh, because stories and tests change without any review
input changing."*

Choose the actual latest Markdown report and its JSON companion explicitly; read
[the native receipt contract](../../../../.game-studio/resources/docs/review-receipts.md).
Build the input patterns from actual review scope: scoped ADRs/GDDs, registry,
architecture, project-owned engine records, effective configuration sources,
consistency failures and the native skill entry plus all loaded phase files.
Snapshot these inputs before review. Required missing classes are NOT ASSESSED;
only inputs explicitly optional at the resolved tier may be optional patterns.

```text
python .game-studio/runtime/studio.py receipts check <reviewed-patterns...> --receipt <companion.json> --root <project-root>
```

Read JSON baseline_status, report_status, unchanged_inputs, observations,
required_unresolved and optional_unresolved; do not pass Markdown as --receipt.
Missing/legacy companions, report drift or unresolved required inputs require a
fresh review, never a no-report stop. Name stable absent optional inputs.

Read Mode and Workflow from the actual report. Prior-verdict reuse requires the
same mode, system scope and applicable coverage, unchanged context, linked report
UNCHANGED and unchanged_inputs=true. No Mode/Workflow means no reusable baseline.
A prior failure remains a failure. A full report can evidence a gate item it really
checked, but is not automatically a reusable verdict for a different review mode.

Only changed existing GDDs/ADRs may justify a proposed single-gdd follow-up, with
its narrower coverage clearly stated. New ADRs, deleted inputs, registry/config/
engine/skill changes or unresolved dependencies require the requested wider review.
The user may always request a fresh full review. In rtm mode build the matrix
fresh, including current stories and tests, rather than reusing an older result.

Before reading any full document, use Grep to extract `## Summary` sections
from all GDDs and ADRs:

```
Grep pattern="## Summary" glob="design/gdd/*.md" output_mode="content" -A 4
Grep pattern="## Summary" glob="docs/architecture/adr-*.md" output_mode="content" -A 3
```

**Fail open on a missing Summary.** Establish the denominator: glob
`design/gdd/*.md` and count **N**. A scan matching fewer than N means those GDDs
predate `## Summary` (`$gs-design-system` emits it, but older GDDs lack it) — never
treat an absent Summary as a system out of scope. A zero-match scan means "no GDD
carries a Summary yet", not "nothing to review": full-read the unmatched set.

For `single-gdd [path]` mode: use the target GDD's summary to identify which
ADRs reference the same system (Grep ADRs for the system name), then load only
those ADRs' sections per Phase 1b. Skip unrelated GDDs entirely.

For `engine` mode: load ADR sections only — GDDs are not needed for engine checks.
In practice this is the `## Engine Compatibility` scan alone.

For `coverage` or `full` mode: proceed to Phase 1b for the full in-scope set.
**This is a section load, not a full-file load** — see below for why, and for the
narrow cases that still justify escalating to a whole document.

### Phase 1b — L1/L2: Targeted Section Load

Load the sections the later phases actually consume — **not whole files**. This
skill reads the two largest document sets in the project (every GDD *and* every
ADR); at realistic sizes a full load of both exhausts the context window before
Phase 2 starts, and most of what it loads is narrative this skill never uses.

**Establish the denominator first.** Glob `design/gdd/*.md` and count **N_gdd**;
glob `docs/architecture/adr-*.md` and count **N_adr**. Report both. A section
scan matching fewer than the denominator means those documents lack the section —
**never treat an absent section as an absent document.** The scan narrows the
*read* set; it never shrinks the *in-scope* set.

### Design Documents

Phase 2 extracts *technical requirements* — data structures, performance
constraints, engine capabilities, cross-system communication, persistence,
threading, platform needs. Those live in a known set of sections; Overview and
Player Fantasy are narrative and yield none.

```
Grep pattern="^## (Detailed Rules|Detailed Design|Formulas|Dependencies|Tuning Knobs|Acceptance Criteria)" glob="design/gdd/*.md" output_mode="content" -A 40
```

Accept **either** `## Detailed Rules` or `## Detailed Design` — the design
standard and the GDD template disagree on the name and they denote the same
required section. Full-read a single GDD only when a scanned section
cross-references material outside itself, or when a GDD matched zero sections
(it predates the template — read it whole and say so).

- `design/gdd/systems-index.md` — the authoritative list of systems; read whole (small, and it is an index)

### Architecture Documents

Phases 3–5 need the traceability table, the decision itself, engine claims, and
the dependency edges — not Context, Consequences, Alternatives, Migration Plan or
Validation Criteria, which explain *why* a decision was made.

```
Grep pattern="^## (Status|Decision|GDD Requirements Addressed|Engine Compatibility|ADR Dependencies|Performance Implications)" glob="docs/architecture/adr-*.md" output_mode="content" -A 30
```

Interpret against **N_adr**, and distinguish the two zero-match cases — they are
not the same finding:

| Result | Meaning | Action |
|---|---|---|
| N_adr matches | Normal. | Proceed on the scanned sections. |
| Some ADRs match, some do not | Those ADRs are missing sections. | Record each as a **structural gap** in the Phase 7 report — a missing `## GDD Requirements Addressed` is itself a traceability finding. |
| **0 matches, N_adr > 0** | **Malformed ADRs**, not "no architecture". | "[N_adr] ADRs found, none carries a scannable section — run `$gs-architecture-decision retrofit [file]` on each." Do **not** report zero coverage; that would read as a design failure when it is a format failure. |

Escalate to a full read of one ADR only when judging a conflict needs its
reasoning (Phase 4) — that is a per-ADR decision, not a blanket load.

- `docs/architecture/architecture.md` if it exists

### Engine Reference
- `<project-engine-reference>/VERSION.md`
- `<project-engine-reference>/breaking-changes.md`
- `<project-engine-reference>/deprecated-apis.md`
- **Only the module docs the in-scope ADRs actually name** — take the union of
  each ADR's `References Consulted` and `Post-Cutoff APIs Used` fields (already
  captured by the `## Engine Compatibility` scan above) and read those files.
  Reading the whole `modules/` directory loads engine subsystems the project may
  not use at all. If no ADR names any module, read none and note it: Phase 5
  cannot cross-check engine claims that were never made.

### Project Standards
- `project.yaml` — `naming.*` and `performance.*`; plus `.game-studio/resources/docs/technical-preferences.md` for those keys when absent and for forbidden patterns / allowed libraries

Report a count: "Loaded [N] GDDs, [M] ADRs, engine: [name + version]."

**Also read `docs/consistency-failures.md`** if it exists. Extract entries with
Domain matching the systems under review (Architecture, Engine, or any GDD domain
being covered). Surface recurring patterns as a "Known conflict-prone areas" note
at the top of the Phase 4 conflict detection output.

---
