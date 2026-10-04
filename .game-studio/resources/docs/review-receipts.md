# Linked native review receipts

Markdown carries human findings/verdicts; a separate JSON companion carries input
SHA-256 hashes plus report path/hash. First review, missing companion, legacy embedded
SHA-1/Markdown or a changed/missing linked report requires a fresh review. Never pass
Markdown to --receipt or parse old hash lines as native JSON.

| Workflow | Report | Latest companion |
|---|---|---|
| design-review | design/gdd/reviews/<stem>-review-log.md | design/gdd/reviews/<stem>-review-receipt.json |
| architecture-review | docs/architecture/architecture-review-YYYY-MM-DD.md | same stem + .receipt.json |
| review-all-gdds | design/gdd/gdd-cross-review-YYYY-MM-DD.md | same stem + .receipt.json |

Choose the actual latest report/companion pair explicitly; ISO date order is useful
but the helper never automatically chooses a baseline. Record which pair was used.
For design-review pass the target GDD and any actual registry/dependency inputs read.
For architecture-review pass actual scoped ADR/GDD/architecture/registry inputs read.
For cross-review include actual GDDs and context/registry/pillar inputs read. Do not
hash unread documents and imply review coverage. Changed scope/mode/context invalidates
reuse even when input bytes match. Required unavailable inputs remain NOT ASSESSED.

Before review snapshot actual inputs; recheck before publication. If they changed
while reviewed, reconcile/re-review rather than stamping the new unread contents.
After the actual report/log is written, generate its linked companion:

`python .game-studio/runtime/studio.py receipts hash <reviewed-patterns...> --root <project-root> --report <report.md> --output <companion.json>`

On re-review use identical input patterns and read the actual report/verdict:

`python .game-studio/runtime/studio.py receipts check <reviewed-patterns...> --root <project-root> --receipt <companion.json>`

Consume JSON baseline_status, report_status, unchanged_inputs, observations, hashes,
patterns and unresolved/previous_unresolved. Only unchanged_inputs=true, linked report
UNCHANGED, unchanged scope/mode and complete required coverage permits offering the
actual prior verdict. A prior failure remains a failure; helper hashes do not approve it.
Changed/new/removed inputs, report drift or unresolved required patterns need review.
Optional inputs absent in both snapshots are named; new/deleted optional inputs change
the snapshot. Do not read an empty observation set as unchanged.

For since-last-review cross-review explicitly run review-scope --receipt <companion.json>.
Use changed/scope/missing/unresolved_dependencies JSON. No baseline means conservative
full scope. Dependency additions/content changes/deletions are visible; unresolved
declarations widen scope. Apply professional consistency/design checks to that set,
and name covered/unread documents. Section receipts require # free filenames;
whole-file receipts support #. Hashes certify observed bytes, not judgment quality.
