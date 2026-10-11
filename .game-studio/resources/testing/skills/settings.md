# Evaluation scenarios: gs-settings

Use the [evaluation policy](../README.md), current native skill and configuration contract.

### Case 1: Inspect actual configuration

Fixture: project YAML selects full rigor but explicitly overrides QA. Resolve per-leaf
values and sources; report the explicit override rather than inferring it from rigor.

### Case 2: Local scope

Fixture: local settings contain a permitted testing leaf and an engine override.
Apply only whitelisted leaves and report the ignored override; preserve unrelated YAML.

### Case 3: Malformed configuration

Fixture: duplicate keys or invalid YAML. Surface the error and preserve the file;
never silently reset it to defaults or borrow a neighboring project's configuration.

### Case 4: Authorized edit and dry run

Fixture: a supported assignment, with an existing human request to edit it. Dry run
reports the intended change without writes. An authorized actual edit updates only
the selected scope and preserves other project facts; no global Codex changes.
