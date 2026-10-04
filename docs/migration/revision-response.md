# Astra round 1 response — 2026-10-05

Baseline reviewed: `11c8d24569e7666bb5f9d461bf9fe62e55d300df`.
Six P2 findings were accepted and repaired. Implementation remains Sol/xhigh;
the user-assigned original Astra/high chat performs independent candidate review.

| Finding | Concrete repair | Evidence |
|---|---|---|
| R1: review Markdown passed as hash baseline / absent lifecycle | Three review workflows use explicit companion JSON, link actual report bytes, cover first/legacy/unchanged/change/deletion/dependency/context cases and preserve earlier failing verdicts. Scope is conservative on missing/drift/unresolved context. | `runtime/checks.py`, shared `review-receipts.md`; linked design/cross/architecture outputs and freshness observations in [native-sample](native-sample/execution.json) |
| R2: old host interfaces survived native wrappers | Reviewed interface pass covers all 74 workflows, 49 profiles, coordination/roster, effects-map, templates, gates and rules. Explicit helper JSON replaces injected text. Roles inherit session settings; parent fallback is labeled; an agent path/message never creates human authorization. Professional checks remain in procedures. | `tools/revise_interfaces.py`, `tools/native_content.py`, new format guards in `tools/validate.py`; restored upstream gate adequacy/smoke/test/performance checks are retained |
| R3: Status parsing/count/routing incomplete | Five formatting variants, exact leading completion words, real complete/count/category fields, priority ordering and next-action/path JSON; help/sprint/story procedures consume these fields. | New regression cases; actual route before 0/1 → story-done, after 1/1 → COMPLETE |
| R4: coherence lost original comparisons | Project-first engine resolver; declared/project VERSION/installed-at-pin/project version, Godot rendering/2D-Jolt, runner files and export presets; explicit reviewed binary probe only; absent data remains NOT ASSESSED. | Local contradiction/probe/Windows path/patch-pin/UTF-8/absent-render regressions; final fixture coherence has 2 MATCH, 8 NOT ASSESSED, 2 OBSERVED, not an overall pass |
| R5: packaged engine examples used as current facts | Shared resolver contract routes native workflows/roles/rules/gates to exact project reference root; historical engine resources are marked background. Missing project VERSION never falls back to packaged version. | Fixture configured Godot 4.3 at custom `records/toolchain/godot`; ADR/gate use 4.3, package 4.6 stays historical; removed project VERSION observation stays unknown |
| R6: tests imported a separate copied implementation | Tests prepend delivered `src`, helper fixture copies only one implementation. Damaging delivered source fails even when an old same-named test copy exists. | Red symptom reproduced, new regression asserts failure, corrected helper fixture tests/package actually executed |

New interface regressions plus existing checks: 21 targeted tests executed successfully.
Final format/inventory/release and the new six-environment CI are tracked in
[verification](verification.md); prior CI remains evidence for its exact earlier head.

The fixture builder authors only synthetic inputs. Actual outputs were written by
the current model parent after reading installed entries/procedures and actual input
documents, running tools and applying the relevant branch. Ten selected workflows
were exercised: help, sprint status, conditional story closure, three reviews,
ADR, target gate, release checklist and release-team Phase 0 guard. All professional
perspectives were parent-only; no invented independent participant or sign-off.

Actual outcomes include an initial blocked story despite passing copied tests,
then four acceptance tests and authorized closure; standard review failing on real
input gaps; unchanged hashes preserving the failure; full re-review detecting
maximum 5 versus 3; a Proposed ADR; failing architecture/gate; unchanged Technical
Setup stage; blocked release guard; and a configured checkpoint handoff. These are
synthetic negative exercises, not validation of a game or all 74 workflows.

The separate headless Codex call reached its model, but Windows native sandbox
initialization failed before tool reads/commands. Its final report is retained as
NOT ASSESSED. No sandbox, user rules, model defaults or hook trust was weakened to
force completion. Manual installed-procedure execution is reported as a distinct
method; autonomous headless completion remains unverified.

No main merge, private game install, engine install, certification, deployment,
notification or global configuration change occurred. [Draft PR #2](https://github.com/I2ene/Codex-Game-Studios/pull/2)
remains the reviewable delivery. Independent re-review is pending.
