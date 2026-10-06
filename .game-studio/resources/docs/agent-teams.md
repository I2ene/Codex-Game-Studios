# Role collaboration

49 expertise profiles live in .codex/agents/gs-*.toml. Their required fields are name,
description and developer_instructions. Model, effort, permissions and concurrency
are intentionally omitted so they inherit the current session settings.

A team workflow supplies disciplines, dependencies and review gates. It does not
require concurrent execution. Delegate only when authorized, useful and supported by
the actual host. Keep dependent decisions sequential; share bounded read-only context
and distinct output ownership for independent work. Never launch a roster automatically.

Use native spawn/wait/message tools actually present. Role names are gs-<upstream-role>.
If custom-role selection is unavailable, pass the chosen role's instructions in a
bounded brief. If delegation is unavailable, the parent applies role knowledge and
reports a parent review. Independent director sign-off cannot be claimed in that case.

Record actual participant ID, expertise, task, returned result and artifacts reviewed.
Only name participants who truly worked. The project task board/checkpoint is the
generic coordination interface; no team service, external chat or personal skill is
required. In-progress work and failed delegation remain visible in the handoff.
See director-gates.md for professional gate responsibilities and review modes.
