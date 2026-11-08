# Upstream compatibility

Codex Game Studios adapts [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios).
Use the upstream release as the baseline for professional behavior and reusable
implementation. The installed native entry points govern actual execution. See
[attribution](../NOTICE.md) and the [MIT license](../LICENSE).

| Role in the comparison | Version | Commit |
| --- | --- | --- |
| Previous upstream source | 1.1.2 | `b21fa0f7f289fc3e726cf36fb12b9bc1e7a51e4d` |
| Integrated upstream source | 1.2.0 (includes 1.1.3) | `05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418` |
| Previous Codex distribution | 2.0.1 | `4889c2b1fa938073670dc855c76072fe742c307a` |

The [upstream file map](upstream-file-map.tsv) accounts for every entry in the
[fixed Git comparison](https://github.com/Donchitos/Claude-Code-Game-Studios/compare/b21fa0f7f289fc3e726cf36fb12b9bc1e7a51e4d...05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418).
It records source and native paths before/after, rename/delete status, disposition
and a contract category. A split section's earlier native location is the
monolithic workflow. The map tracks maintenance provenance, not model test
results. Source paths in the map are Git references, not installed entry points.

## Workflow

| Contract | Previous native behavior | Integrated behavior and verification |
| --- | --- | --- |
| Main path and continuation | Long entry references included later phases inline. | Follow upstream's staged references and focused story/onboarding main paths. Load the needed phase and re-read it on resume. Read and validate actual resources, then inspect relevant branches; metadata, gates and recovery evidence remain separate. |
| Architecture and IDs | Existing reviews used linked receipts, but local writes did not consistently delimit single-system scope and the dependency graph used filename stems. | Keep active and retired IDs, coordinate provisional IDs, write only the selected system's rows, quote status values containing a colon and record Layer in ADRs. Resolve actual numbered ADR filenames and distinguish dependency gaps, cycle membership and blocked consumers. See `test_upstream_alignment.py` and `test_upstream_workflows.py`. |
| Gate coverage and advancement | A summary CONCERNS could hide an unexecuted required item. | Cover only the dimensions established by the report's mode and scope. Partial smoke/design/architecture reports cannot substitute for required dimensions; keep an independent no-advance condition for any unexecuted required check. Keep actual human decision and stage readback. |
| Story pipeline | Generation and readiness used inconsistent AC limits; scope and test evidence could drift. | Match generation/readiness by granularity, preserve actual ADR dependencies and estimates, protect planned vs actual Files scope, and use actual playtest records and code freshness stamps. Keep known failing tests visible; existence alone cannot verify success. |
| Input and delegation | Native roles were already optional delegates; original host had fixed tools and stricter per-file prompting. | Preserve roles, inputs, mode-dependent reviews, necessary human decisions and no-answer stops. A delegate returns its question to the caller; the parent may perform required expertise and report that source. An authorized brief does not grant new permissions or establish independent sign-off. |

## Helpers

| Contract | Compared behavior and disposition |
| --- | --- |
| Upstream Bash utilities | Directly reuse the data algorithms for ADR status, story facts, registry observations, input checks, planning math, bug/debt/asset/content/code/flakiness observations. Adapt asset/content lookup to take the effective project engine explicitly rather than honoring a disallowed local engine override. Bash/awk is optional; see [native helper interfaces](../.game-studio/resources/docs/native-runtime.md). |
| YAML and settings | Keep the native parsed YAML and per-leaf sources. Read-only resolution merges repeated mapping blocks, applies later overlapping leaves and reports locations. Writes and configured commands require clean settings; dotted collisions are ambiguous. Use explicit preview/readback and confined atomic writes. |
| Receipt formats | Reuse upstream coverage checks while retaining native SHA-256 JSON companions and report hashes. Compare every previously stamped input, and disqualify required misses. An explicitly optional absence can be stable. Old unlinked/text receipts are not equivalent evidence. |
| Markdown and registry writes | Read complete sections and expose safe explicit edits. Scope guards are observations. Preserve exact ID boundaries, canonical dependencies, unfilled vs absent data, existing entries and previously assigned IDs. |
| Project state | Use configured project values and observations with provenance. Legacy text is a read fallback; stage writes update `project.stage` only. Keep configured checkpoint, previous snapshots and disabled state; no silent rotation or legacy config finalization. |
| Tests and scaffolds | Reuse test scaffolding layouts with preview and exclusive creation. The installer does not create or enable game CI. Run approved configured argv with actual exit/output/timeout; shell command strings and automatic discovery/launch of game tools are not interchangeable. |

## Hooks

Upstream event payloads, tool pre-approval, status lines, model pins, automatic
worktree-local configuration copies, update caches and shell interception do not
ship. The native hook definitions are optional and require real host trust.
Use the explicit input, read, write and registry checks for the associated
professional observations. A runtime callback or a role launch is NOT ASSESSED
until observed in the actual host. No automatic background update or vendor
filing follows a framework command.

## Engine

Packaged source references reflect upstream's documentation snapshots, including
[Godot 4.7.2](https://godotengine.org/download/archive/4.7.2-stable/),
[Unreal Engine 5.8](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes)
and [Unity 6.3 LTS](https://unity.com/releases/unity-6/support). Do not interpret
upstream dates, examples or release-note/Editor discrepancies as observations
of the user's installation. Prefer the project's pinned engine and resolved
records, then confirm the applicable API and tooling. Godot's production import
exclusion is an explicit setup template; ownership installation never rewrites
game engine assets or project configuration.

## Evaluation

Merge the upstream guidance and new cases into the native catalog. Preserve
fixture boundaries, mutually exclusive branches, professional checks, mode
applicability and the native distinctions between absence and missing evidence.
Upstream scenarios, even ones recorded as tested in the original host, are
guidance for Codex. FORMAT covers static and branch-contract checks. EXECUTED
requires a real local command or fixture with an observed result. NOT ASSESSED
covers model behavior, real engines, game quality and unavailable host callbacks.

## Distribution

The source commit is an ancestor of the integration. Keep its second-parent
history when integrating the synchronization into the main branch. The MIT
license and Donchitos notice accompany the original source and installed
payload. The [ownership upgrade](../UPGRADING.md) replaces unchanged managed
files and protects consumer edits, configuration and checkpoints. Historical
host entry points are available through Git only.
