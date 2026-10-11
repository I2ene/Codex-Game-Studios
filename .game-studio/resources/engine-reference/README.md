# Historical engine reference library

These upstream snapshots preserve professional engine knowledge for Godot, Unity
and Unreal. Their version pins and verification dates are historical. They do not
identify the consumer's installed engine or establish current API correctness.
Read [project reference resolution](../docs/engine-reference-resolution.md) first.

## Reference structure

Each engine directory contains version records, breaking changes, deprecated APIs,
best practices and subsystem modules. Consult the relevant knowledge when reviewing
architecture or implementation, then verify APIs against current official sources
and the consumer's actual engine version.

## Project maintenance

`$gs-setup-engine` records project-owned toolchain facts and references. Update those
records after an engine upgrade or verified API change; preserve packaged snapshots
so ownership-based framework upgrades remain safe. Record the engine version, actual
probe evidence where available, source URLs and verification dates. Keep subsystem
notes focused, with correct/incorrect code examples and migration risks.

Model knowledge may lag engine releases. Unknown or unverified facts remain unknown;
a packaged example is not evidence that an engine build, test or export succeeded.
