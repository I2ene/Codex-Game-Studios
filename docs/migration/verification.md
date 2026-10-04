# Candidate verification — 2026-10-05

Environment: Windows; Python 3.12.14; PyYAML 6.0.3; Codex CLI 0.160.0.
User/session model and permissions inherited. No private game project installed,
edited or used as a sample. MIT/Donchitos license unchanged.

| Check | Observed result | Boundary |
|---|---|---|
| tools/validate.py | FORMAT: 74 skills, 49 roles, 485 sources, zero errors | Metadata, links and known interface guards; not inference quality |
| tools/audit_inventory.py | 485 original SHA-256 hashes verified; 123 native/68 replace/289 retain/5 unsupported | Audited coverage and declared targets; not game outcomes |
| tools/build_release.py | FORMAT: 2.0.0; 398 managed payload files | Integrity manifest, not publisher authenticity |
| unittest tests.test_workflow_interfaces tests.test_checks | EXECUTED: 21 targeted tests passed | Concrete revision regressions and helper checks; does not imply all model workflows passed |
| R7/R8 interface/helper regressions | EXECUTED: 26 targeted tests passed after three red reproductions | Actual cwd positive/negative runs, known/unknown resource paths, explicit optional/required snapshots and CLI classification |
| corrected integration_sample.py | EXECUTED: source-import tests and source ZIP exit 0; recovery PRESENT; reinstall writes 0 | Deterministic nongame helper/artifact fixture; native discovery not requested in this corrected run |
| installed native sample, current model parent | Actual selected branches of ten workflows exercised, with reports/receipts and four acceptance tests | Manual installed-procedure execution, parent-only; distinct from automated CLI execution |
| headless Codex model attempt | Model call EXECUTED; workflow NOT ASSESSED | Windows native sandbox setup blocked reads/commands; no permissions/trust bypass |

[sample-evidence.json](sample-evidence.json) records the corrected deterministic
helper fixture. Its tests import the delivered src implementation; a new regression
proves damaged src fails even with an old same-named copy in tests. Source ZIP is
not an engine/game build or platform release.

[native-sample/execution.json](native-sample/execution.json) records retained actual
model-parent outputs. The input builder never prewrites reports or verdicts. The
parent read installed procedures and applied selected branches: minimal routing and
conditional closure; standard/full design, cross-GDD and architecture reviews;
change/re-review; project-first engine ADR/target gate; release stage guard and
missing-data handoff. Initial story BLOCKED on an actual specification mismatch,
then four tests and 3/3 criteria permitted closure. Review failure remained failure
when inputs were unchanged; changed limits exposed maximum 5 versus 3. Proposed ADR,
failing architecture/gate, unchanged Technical Setup stage, blocked release team and
unknown release/engine quality are retained. No independent sign-off is claimed.

The separate CLI invocation reached GPT-6.1 Sol/xhigh but native Windows sandbox
initialization failed before tool reads/commands; its retained final explicitly
says NOT ASSESSED. A prior restricted-network attempt never connected and its
verified fixture process was terminated. Raw CLI transcripts/global data are not
committed. Manual parent execution is not autonomous headless completion evidence.
Fixture/Python paths and CRLF line endings are normalized in retained evidence; manifest records
original and retained hashes. Linked report bytes remain unchanged. Normalized
project config copies cannot replay original config digests without original bytes.

Prior [CI run](https://github.com/I2ene/Codex-Game-Studios/actions/runs/37233711962)
passed six Windows/macOS/Linux × Python 3.11/3.12 jobs at
11c8d24569e7666bb5f9d461bf9fe62e55d300df; [ci-evidence.json](ci-evidence.json)
records actual results. Its old counter-test copy was insufficient source evidence
and is superseded by R6. Earlier local suite: 32 tests, 31 passed/1 symlink privilege
skip; normal/dangling junction rejection executed. Earlier read-only native discovery
found all 74 installed skills with zero framework/protocol errors; this was discovery,
not model execution. Revision run 37238640713 exposed an order-dependent test import:
the new test module prepended the unused tools directory, shadowing runtime studio.
Removed that import-path entry after reproducing the exact failing order; the
13-test reproduction then passed. Fresh replacement CI must be read at its actual
commit on PR #2.

[Replacement CI](https://github.com/I2ene/Codex-Game-Studios/actions/runs/37238824476)
at dd0dc4390bff6c14a73a540809016cff1a15123d passed all six environments and their
format/full 44-test suite/helper fixture steps. [ci-revision-evidence.json](ci-revision-evidence.json)
retains those results. Astra round 2 accepted the first six repairs and the declared
parent sample scope, then found two P2 boundary issues. [R7/R8 response](revision-2-response.md)
records their red reproductions, repairs and new checks. The next CI belongs to the
new boundary-fix head; earlier sample artifacts retain their exact earlier payload
hash, rather than pretending their original execution occurred at a later revision.

Runtime tests cover YAML/config precedence and validation, confined recovery,
consumer preservation, ownership/overlap/upgrade/dry-run/rollback/locking, path links,
actual success/failure commands and optional event I/O. Added tests cover linked
receipt lifecycle/report drift/dependencies/context, five story formats/routing,
engine authority, concrete coherence contradictions/probe/pins/Windows paths,
missing rendering, UTF-8 and dependency ordering/missing declarations.

NOT ASSESSED: complete inference of all 74 workflows/49 roles; custom-role launch;
trusted callbacks; game balance/performance/visuals/assets/playtests; actual engine
parse/tests/build; certification/deployment/live operations. Missing data never
became a pass; no hook was automatically registered or trusted. Abrupt process/OS
termination is nontransactional: inspect/restore before clearing an orphan install
lock. Hashes do not authenticate a publisher; reviewed argv is not a sandbox.
