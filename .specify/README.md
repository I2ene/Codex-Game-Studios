# Maintainer SDD tooling

This change uses [GitHub Spec Kit](https://github.com/github/spec-kit) v1.4.5,
source commit `6ba8beefff8d6408cadd62038e92d459093e33a8`. It is a development tool,
not part of the installed game framework. The [constitution](memory/constitution.md)
records existing AGENTS.md and CONTRIBUTING.md rules. Feature artifacts live in specs/.

Use an isolated uv tool environment pinned to the official tag. Initialize an empty
ignored staging directory with Codex integration, Python scripts and integration
options `--skills --events false`. Review its generated file list before adopting
project infrastructure. Keep generated Codex skills in that tool staging directory;
read and execute their instructions in the development agent. Never overwrite
existing AGENTS, framework skills or Codex configuration. Runtime events are disabled.

The official commands are agent instructions: constitution, specify, plan, tasks,
analyze, implement and converge. Run the generated setup/template/prerequisite
scripts as directed; terminal commands alone do not execute the agent workflow.
Generated templates/scripts and per-checkout feature pointers are ignored. Only
generic constitution and feature artifacts are retained for review. The framework
installer's managed-file predicate excludes `.specify` and `speckit-*` skills.
