# Evaluation scenarios: gs-changelog

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-changelog/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Multiple sprints since last release tag

**Fixture:**
- Git history has a tag `v0.3.0`; it is the newest tag in the injected tag list
- Since that tag: 12 commits across sprints 006, 007, 008 — all Game commits
  (mechanics, content, bug fixes) naming systems that appear in `design/`
- `production/sprints/sprint-006.md` through `sprint-008.md` exist and list the
  stories whose task IDs appear in the commit messages
- `docs/CHANGELOG.md` does not yet exist

**Input:** `$gs-changelog`

**Domain checks:**
- [ ] Changelog covers the commits in `v0.3.0..HEAD`, and the output states how many of how many injected commits it used
- [ ] Entries use the skill's section set — New Features, Improvements, Bug Fixes, Balance Changes, Technical Debt / Refactoring, Known Issues, Miscellaneous — not a generic Features/Fixes split
- [ ] Sprint plans in `production/sprints/` for the covered sprints are read for context before categorizing
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is CHANGELOG WRITTEN after the write

---

### Case 2: No Git Tags Found — Bounded range used

**Fixture:**
- Git repository has 20 commits and no tags; all 20 are Game commits
- The injected tag list is empty
- `docs/CHANGELOG.md` does not exist

**Input:** `$gs-changelog`

**Domain checks:**
- [ ] Skill does not error when no git tags exist
- [ ] The range is read with the bounded `git log --oneline -n 100`, never an unbounded full log
- [ ] All 20 commits are covered, and the skill does not ask for a start ref (the bound reaches the first commit)
- [ ] Output states how many of the 20 commits were used
- [ ] Changelog is still organized into sections despite the missing tag

---

### Case 3: Commit Messages Without Task IDs — Categorized by content, counted in Metrics

**Fixture:**
- Git log since the last tag has 8 Game commits
- 3 commits reference task IDs (e.g. `[STORY-012]`) matching sprint stories
- 5 commits have no task ID: "tweak dash cooldown 0.8 -> 0.6",
  "fix player clipping through ledge", "add footstep sounds", "level tweaks",
  "combat cleanup"

**Input:** `$gs-changelog`

**Domain checks:**
- [ ] Commits are categorized by content with or without a task ID — the untagged "tweak dash cooldown 0.8 -> 0.6" lands in Balance Changes, not in a separate no-ID group
- [ ] "combat cleanup" is listed under Technical Debt / Refactoring in the internal changelog and does not appear in the player-facing changelog
- [ ] "level tweaks", too vague to classify, is listed under Miscellaneous
- [ ] Metrics section contains `Commits without task reference: 5`
- [ ] No commits are silently dropped — all 8 appear in a section

---

### Case 4: Existing CHANGELOG.md — New entry at the top, old entries preserved

**Fixture:**
- `docs/CHANGELOG.md` already exists with sections for `v0.2.0` and `v0.3.0`
- New Game commits exist since the `v0.3.0` tag

**Input:** `$gs-changelog`

**Domain checks:**
- [ ] Skill checks whether `docs/CHANGELOG.md` exists before asking, and recommends [A] append because it does
- [ ] The prompt offers append, overwrite and decline as distinct options
- [ ] On [A], the new entry is placed at the top of the file (newest first), not at the bottom and not replacing the file
- [ ] Existing `v0.2.0` and `v0.3.0` entries are preserved in the written file

---

### Case 5: Gate Compliance — No gate; declined write ends COMPLETE

**Fixture:**
- Git history has Game commits since the last tag
- `project.yaml` sets `modes.review_mode: full`

**Input:** `$gs-changelog`

**Domain checks:**
- [ ] No director gate is invoked regardless of review mode
- [ ] Output does not reference any gate result
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] On [C], no file is written and the verdict is COMPLETE, not CHANGELOG WRITTEN

---

### Case 6: Provenance Stop — Zero Game commits

**Fixture:**
- The 30 injected commits all touch the framework or tooling — subjects such as
  "fix: session-start hook timeout", "docs: skill catalog", "ci: cache the test
  runner" — and none names a game system in `design/` or the code root
- `docs/CHANGELOG.md` does not exist

**Input:** `$gs-changelog`

**Domain checks:**
- [ ] Output names the classification result — 0 of 30 commits are Game commits
- [ ] Output contains the "does not appear to belong to" stop, not a changelog built from framework commits (no "Fixed an issue where …" copy from a hook fix)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is BLOCKED — not COMPLETE and not CHANGELOG WRITTEN

---

### Case 7: No History — Not a git repository

**Fixture:**
- The project directory is not a git repository, so both injected history
  blocks are empty
- `docs/CHANGELOG.md` does not exist

**Input:** `$gs-changelog`

**Domain checks:**
- [ ] The "does not appear to belong to" provenance stop is NOT shown — an empty history is not a wrong history
- [ ] Output says no git history was found and offers committing the work or supplying the change list directly
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is BLOCKED
