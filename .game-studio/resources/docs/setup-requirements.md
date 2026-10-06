# Requirements

Codex with repository skill discovery (.agents/skills), Python 3.11+ and PyYAML 6.x.
Install Python dependencies into a project-owned virtual environment after reviewing
requirements.txt. The installer itself does not install packages, engines or plugins.
Custom roles and trusted hooks depend on host support; the parent can apply role
expertise and explicit helper commands provide recovery/checks without hooks.

No engine is required to install the framework. Real game tests/builds/profiles need
the consumer's chosen engine, SDKs, assets and configured argv commands. Verify current
engine documentation for the project's pinned version. Framework fixtures only test
the framework. Native CLI 0.160.0 was the local audit environment, not a promise that
every older or future host supports the same APIs. Check capability evidence on upgrade.
