# Framework contributor instructions

This repository distributes Codex Game Studios; it is not a game project. Preserve
MIT/Donchitos attribution, professional lifecycle procedures, templates and contracts.
`.claude/` and `CCGS Skill Testing Framework/` are archived upstream reference sources,
excluded from installation. Never treat them as Codex runtime instructions.

Run Python 3.11+ with requirements.txt in a local environment. Validate changed runtime
behavior with targeted unittest checks; run tools/validate.py for native content changes.
Do not regenerate migrated content blindly: tools/migrate_upstream.py is a one-time
baseline adapter and subsequent reviewed native edits are authoritative.

Consumer packaging consists of .agents/skills/gs-*, .codex/agents/gs-* and .game-studio.
Installer changes must preserve user files, reject unsafe paths and record ownership.
Never ship model/permission pins, global configuration changes or hook-trust bypasses.
Record FORMAT, EXECUTED and NOT ASSESSED evidence separately. Scope validation to new
risks; synthetic samples are framework checks, not game-quality evidence.
