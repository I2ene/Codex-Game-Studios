# Validation and supported boundaries

Evidence uses three separate labels:

| Label | Meaning |
|---|---|
| **FORMAT** | Metadata, resource links, schemas, catalog coverage or release hashes were checked; no task-quality claim |
| **EXECUTED** | The named helper, test, discovery call or consumer command actually ran, with its result and scope |
| **NOT ASSESSED** | Required input, tool, authorization or execution evidence is unavailable; never a clean pass |

## Reproducible framework checks

[CI](../.github/workflows/framework.yml) runs `tools/validate.py`, unittest discovery
and `tools/integration_sample.py` on Windows, macOS and Linux with Python 3.11/3.12.
Inspect the checks for the specific commit being reviewed; a CI definition alone is
not execution evidence. Tests cover installer safety/ownership/rollback, configuration,
context, receipts, dependencies, engine facts and command execution with confined fixtures.

The integration sample installs into a temporary existing consumer with spaces in its
path, preserves its instructions/configuration, tests a pure counter function,
packages source, recovers a checkpoint and reinstalls. Source packaging is not an
engine build. Optional `--native-discovery` exercises actual installed skill discovery
when Codex CLI is available. It does not call a model, launch roles or trust hooks.

The [evaluation catalog](../.game-studio/resources/testing/README.md) preserves
professional scenario inputs and domain assertions for skills and roles. These are
human/model evaluation guidance, not executable tests or proof of passing behavior.
Record actual host, scope, participants and outputs when using them.

## Limits requiring separate evidence

- Exhaustive inference behavior of all 74 skills and 49 roles is not established by metadata or discovery checks.
- Custom role loading/launch and trusted hook callback delivery need actual host capability tests. Direct handler fixtures only check handler I/O.
- Engine APIs and packaged version examples need current official verification and project toolchain records. Unknown facts remain unknown.
- Game balance, visuals, accessibility outcomes, playtests, performance, engine builds, platform certification and deployment need real consumer inputs and execution.
- Permission availability and native APIs vary with the Codex host. Roles inherit session settings; no model, permission or concurrency policy is installed.
- Normal installation failures attempt rollback. Abrupt termination or failed rollback needs manual inspection; integrity hashes are not publisher signatures.

Professional gates retain their missing-input, mode applicability and strictest-verdict
rules. A report must name skipped/unavailable checks, actual execution failures and
remaining risks. Synthetic game-shaped documents cannot establish game quality or
release readiness.
