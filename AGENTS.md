# Framework contributor instructions

This repository distributes Codex Game Studios; it is not a game project. Preserve
MIT/Donchitos attribution, professional lifecycle procedures, templates and contracts.
Native content is authoritative. Retired host sources are available in Git history;
do not restore runtime entries or regenerate reviewed content from historical files.

Use Python 3.11+ with requirements.txt in a local environment. Validate changed
runtime behavior with targeted unittest checks. Run tools/validate.py for content,
document links, evaluation catalog and release integrity. After reviewed payload
changes, run tools/build_release.py, then validate again. See CONTRIBUTING.md.

Consumer packaging consists of .agents/skills/gs-*, .codex/agents/gs-* and .game-studio.
Installer changes must preserve user files, reject unsafe paths and record ownership.
Never ship model/permission pins, global configuration changes or hook-trust bypasses.
Record FORMAT, EXECUTED and NOT ASSESSED evidence separately. Scope validation to new
risks; synthetic samples are framework checks, not game-quality evidence.
