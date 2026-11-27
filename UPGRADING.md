# Upgrading Codex Game Studios

## 2.1.0 to 2.2.0

Preview and run the ownership-based upgrade below. Native skills, roles, genre/
engine data, templates and helpers change; the installer does not grow or change
your game, install Web dependencies, run a browser, trust hooks or upgrade an
engine. Existing configuration and instructions remain yours.

New canonical entries are `$gs-next-step`, `$gs-project-settings` and
`$gs-write-changelog`. `$gs-help`, `$gs-settings` and `$gs-changelog` forward the
original arguments with one rename notice. `$gs-cut` adds the upstream finishing
workflow. Aliases share evaluation guidance rather than duplicate scenarios.

Shared `engine.code_root` and `engine.test_root` take priority over old shared
`code_root` and `test_root`; old keys remain supported. Invalid explicit paths
are diagnosed without scanning fallback directories. Root `.` means the project
root with framework/generated trees excluded. Explicit argv and pins retain
priority over engine-table suggestions.

One-shot evidence and native SHA-256 report receipts retain distinct consumers.
Old native receipts and checkpoints need no conversion. Grow copies the prototype
and preserves the original. Accept replay/feature differences based on actual
observations. Spec Kit development tooling is never an upgrade prerequisite.


## 2.0.0 or 2.0.1 to 2.1.0

Use the same installer and preview with --dry-run. Review the list of updated
and retired managed references; nested copies of moved phase files are retired.
If an edited managed path or unowned destination conflicts, reconcile it before
retrying. Keep your original configuration, context, engine pin, and design records.
No automatic engine upgrade or native hook trust is performed.

Read-only config inspection now exposes duplicate-key diagnostics. Fix the named
keys before writing settings or running a configured command. Bash and awk are
needed only for the optional upstream data utilities. See
[upstream compatibility](docs/upstream-compatibility.md).


For native 2.x projects, review the new release and run the same ownership-based
installer using its source and a separate consumer target:

```text
<python-with-PyYAML> tools/studio.py upgrade --target <absolute-project-root> --dry-run
<python-with-PyYAML> tools/studio.py upgrade --target <absolute-project-root>
```

The release manifest validates source integrity. The consumer's
.game-studio/install-state.json records installed hashes and version. Existing
project.yaml metadata is preserved, so the ledger is authoritative for the framework
version. Exact identical reinstallation writes nothing. Changed release files replace
only unedited owned files. Removed files are pruned only when owned and unchanged;
unmanaged files are never pruned. Instructions outside the managed AGENTS.md block,
Codex config/hooks/trust, local context/preferences and game records remain yours.

If a managed file/block was edited, preflight fails before file writes and lists the
conflict. Preserve your edit, compare old/new release content and reconcile deliberately;
move project-specific extensions into project-owned files or a differently named skill
where practical. Do not delete ownership state to force an upgrade. A corrupt ledger
is an error and requires inspection. Keep a project backup or commit before upgrading.

A normal write failure restores file snapshots; empty directories may remain.
An abrupt process/OS termination is not transactional: the install.lock remains and
blocks another installation. Inspect affected files and restore from your backup
before removing the lock and retrying. Do not run concurrent installers or edit the
managed payload during installation. Dry run never writes or creates the target.

## From upstream 1.x

From upstream 1.x, use a normal native install followed by gs-adopt. Old .claude
settings, @ imports and permission grants are not Codex configuration. Preserve
professional records and map applicable preferences explicitly to project.yaml.
Legacy review/stage text is a read-only fallback. Automatic legacy Markdown conversion
and finalization are unsupported. Old SHA-1 review logs need a fresh reviewed SHA-256
JSON baseline.

See [install](docs/install.md), [integration](docs/integration.md) and
[validation boundaries](docs/validation.md).

## 2.0.0 to 2.0.1

The skill names, role names, runtime commands, configuration schema and ownership
ledger remain compatible. This release removes retired host sources and process
records from the distribution repository; those were never installed into consumers.
It adds native professional evaluation scenarios and registry templates, and updates
managed documentation. Local instruction guidance now uses the native filename
`.game-studio/resources/docs/local-guidance.md`; the old owned filename is removed
only when unchanged. Installation seeds absent configuration with the actual
release version. Existing project.yaml version text is preserved; install-state.json
remains authoritative. Review managed-file conflicts using the normal upgrade flow.
