# Framework architecture

## Distribution

The consumer payload consists of `.agents/skills/gs-*`, `.codex/agents/gs-*` and
`.game-studio`. Each skill has a native `SKILL.md` entry with name/description and a
complete referenced procedure; role TOML files contain name, description and
`developer_instructions`. Settings inherit the current session. Professional templates,
gates, rules, historical engine knowledge and evaluation scenarios are shared resources.

The repository's `tools/`, `tests/`, `fixtures/` and contributor documentation are
maintenance assets. They are not installed into game projects. Root `project.yaml`
is an engine-neutral configuration example, not a game design or runtime prerequisite.
The installer seeds only absent consumer configuration and a bounded `AGENTS.md` block.

## Runtime

Python 3.11+ and PyYAML 6.x implement explicit-root configuration, context recovery,
artifact/story/dependency observations, engine reference resolution, review receipts
and reviewed argv execution. Helpers report observations; workflows apply domain
judgments. See [tooling](tooling.md) and the
[native interface contract](../.game-studio/resources/docs/native-runtime.md).

Context and checkpoints are optional confined project data. They do not authorize
work. Hooks expose optional JSON handlers and definitions, with registration/trust
left to the Codex host. They never grant permissions or silently intercept all tools.

## Ownership and updates

`release.json` records the full payload's SHA-256 hashes. The consumer's
`install-state.json` records ownership, installed version and instruction block hash.
Installation preflights conflicts, rejects unsafe/link paths and overlapping roots,
serializes writes, preserves user-owned files and prunes only unchanged owned files.
Normal failures attempt rollback; abrupt termination needs manual recovery. Integrity
hashes detect modification but do not authenticate a publisher. See [upgrading](../UPGRADING.md).

Framework checks separate format integrity, executed fixture behavior and unassessed
host/game capabilities. See [validation](validation.md). Attribution and original
source links are in [NOTICE](../NOTICE.md); historical sources remain in Git history.
