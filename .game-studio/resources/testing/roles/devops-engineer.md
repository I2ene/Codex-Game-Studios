# Evaluation scenarios: gs-devops-engineer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-devops-engineer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — CI setup for a Godot project
**Input**: "Set up a CI pipeline for our Godot 4 project. It should run tests on every push to main and every pull request, and fail the build if tests fail."
**Domain checks**:
- Produces a GitHub Actions workflow YAML (`.github/workflows/ci.yml` or equivalent)
- Uses the Godot headless test runner command from `coding-standards.md`: `godot --headless -s -d --remote-debug tcp://127.0.0.1:0 res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://tests --ignoreHeadlessMode`
- Configures trigger on `push` to main and `pull_request`
- Sets the job to fail (non-zero exit) when tests fail — does NOT add `continue-on-error` or any other setting that lets the pipeline pass on a test failure
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — game networking implementation
**Input**: "Implement the server-authoritative movement system for our multiplayer game."
**Domain checks**:
- Does not produce game networking or movement code — "Modify game code or assets" is on its "What This Agent Must NOT Do" list
- Says the work belongs to a programmer and names who takes it: `lead-programmer` or `technical-director`, the agents its file names (naming `network-programmer`, the owner of netcode, also satisfies this)
- States what it can do instead: the infrastructure that builds, tests, and deploys the game once the netcode exists
- Does not conflate CI pipeline configuration with in-game network architecture

---

### Case 3: Build failure diagnosis
**Input**: "Our CI pipeline is failing on the merge step. The error is: 'Asset import failed: texture compression format unsupported in headless mode.'"
**Domain checks**:
- Diagnoses the failure as an environment problem in the headless CI runner (the import step needs a capability the headless runner lacks), not a flaky step to retry
- Before stating how Godot 4.6 imports or compresses textures headlessly, cross-references `<project-engine-reference>/godot/` — `VERSION.md` pins 4.6, past the model's training data — and says so when the reference does not cover it, rather than asserting version-specific behavior from memory
- Proposes at least one actionable fix that keeps the import and test steps in the pipeline, and names its tradeoff
- Does NOT remove the import step, skip the tests, or mark the job `continue-on-error` to get a green build — "Skip CI steps for speed" is forbidden, and `coding-standards.md` says "Never disable or skip failing tests to make CI pass — fix the underlying issue"
- Does NOT declare the pipeline unfixable

---

### Case 4: Branching strategy conflict
**Input**: "Half the team wants to use GitFlow with long-lived feature branches. The other half wants trunk-based development. How should we set this up?"
**Domain checks**:
- Recommends trunk-based development because `AGENTS.md` names it under Version Control ("Git with trunk-based development"), and says that is the model it followed
- Explains the model as its Branching Strategy section defines it: `main` is the always-shippable trunk, built and tested by CI on every push and pull request; work happens on short-lived branches merged back within a day or two through a pull request that passes CI; unfinished work ships dark behind a feature flag
- Rejects GitFlow's long-lived branches specifically — there is no long-lived integration branch beside `main`
- Covers releases and hotfixes per the same section: a release is a tag on `main`; a `release/*` branch is cut only to stabilise a release (bug fixes only, every fix also lands on `main`); a `hotfix/*` branch starts from the release tag (or its `release/*` branch, if one exists) and merges back to `main`, and to that `release/*` branch only if it exists
- Does NOT present this as a 50/50 choice, and does not adopt GitFlow on its own authority — the model comes from `AGENTS.md`'s Version Control line, so switching means changing that line

---

### Case 5: Context pass — platform-specific build matrix
**Input context**: Project targets PC (Windows, Linux), Nintendo Switch, and PlayStation 5. CI runs on GitHub-hosted runners, which have no console export templates or SDKs installed.
**Input**: "Set up our CI build matrix so we get a build artifact for each target platform on every release branch push."
**Domain checks**:
- Produces a build matrix configuration with four platform entries — Windows, Linux, Switch, PS5 — each a one-command build (Build Pipeline)
- Triggers release builds the way its Branching Strategy defines a release: on release tags on `main`, and on pushes to a `release/*` branch while one exists for stabilisation — and says why, rather than assuming a standing release branch
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.
- Organizes artifacts by platform name, with versioning and retention (Artifact Management)
