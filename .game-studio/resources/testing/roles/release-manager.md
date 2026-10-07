# Evaluation scenarios: gs-release-manager

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-release-manager.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — certification checklist for a console submission
**Input context**: `project.yaml` sets `platform.cert_tier: console`; the game ships on Nintendo Switch.
**Input**: "Generate the certification checklist for our Nintendo Switch submission."
**Domain checks**:
- Emits the console certification block its preloaded `$gs-release-checklist` defines for `cert_tier: console` — TRC/TCR/Lotcheck requirements checklist, first-party submission, achievement/trophy integration, parental controls, save-data rules (corruption, full storage, user switching), age ratings — plus the console device requirements (controller prompts, suspend/resume, user switching, connectivity loss, storage full)
- Tracks every requirement individually with pass / fail / not-applicable status (Platform Certification Requirements)
- Emits no itch.io or Steamworks certification rows — the certification block follows `cert_tier`, not the platform named in the request
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope. Preserve the stated artifact obligations for `production/releases/release-checklist-[version].md`.

---

### Case 2: Out-of-domain request — design test cases
**Input**: "Write test cases for our save system to make sure it passes certification."
**Domain checks**:
- Does not produce test case specifications
- Routes test design to `qa-lead`, which its Delegation Map names for quality gates, test results, and release readiness sign-off
- Offers what it does own: the save-data certification requirements the tests must cover (the console block's "Save-data rules compliant (corruption, full storage, user switching)"), as input for qa-lead

---

### Case 3: Domain boundary — age-rating rejection blocks the release
**Input**: "Our build was rejected by the ESRB. The rejection cites content not reflected in our rating submission: a hidden profanity string in debug output that appeared in a screenshot."
**Domain checks**:
- Treats the rejection as blocking: the pipeline halts at the failed step until the issue is resolved ("No step may be skipped. If a step fails, the pipeline halts and the issue is resolved before proceeding")
- Returns the Go / No-Go verdict as NOT READY, listing the rating issue as a blocking item with an estimated time to resolve (`$gs-release-checklist` Go / No-Go rationale)
- Identifies the action required: remove all debug output containing the content, then resubmit the rating questionnaire and track receipt of the new certificate (Store Page Management: age ratings)
- Does NOT minimize the issue or propose launching around it — a rating rejection is a blocking event, not an advisory
- Reports the delay's impact on the release date to producer, which it reports to for scheduling

---

### Case 4: Version numbering conflict — hotfix vs. release branch
**Input**: "Our release branch is at v1.2.0. A hotfix was applied directly on main and tagged v1.2.1. Now the release branch also has changes that need to ship as v1.2.1 but they're different changes."
**Domain checks**:
- Identifies the conflict: two different changesets have been assigned the same version
- Resolves it with semantic versioning: `v1.2.1` stays with the build it already tags, and the release branch's changes, being fixes, ship as the next PATCH (`v1.2.2`) — its Version Numbering rule for two changesets claiming one version
- Does NOT accept a state where one version number names two different builds — "an applied tag is never moved or reused", and internal builds stay distinguishable by `MAJOR.MINOR.PATCH.BUILD`
- Coordinates the hotfix-branch side with `lead-programmer`, which its Delegation Map names for hotfix branch management

---

### Case 5: Context pass — release date constraint and certification lead time
**Input context**: Target release date is 2026-06-01. Current date is 2026-04-06. Nintendo Lotcheck typically takes 4-6 weeks.
**Input**: "What should we prioritize on the certification checklist given our timeline?"
**Domain checks**:
- Works from the supplied dates and lead time, not placeholders: 8 weeks to release, so the first Lotcheck submission is due between 2026-04-20 (if it takes 6 weeks) and 2026-05-04 (if it takes 4) — before any resubmission
- Keeps the pipeline order and every step — Build → Test → Cert → Submit → Verify → Launch, "No step may be skipped" — and schedules backward from the release date rather than compressing or dropping a step to fit
- Plans for at least one certification iteration (Cert is "Submit to platform certification, track feedback, iterate") and flags that a single rejection would consume the remaining buffer
- Recommends an order but hands the schedule call to `producer` — it reports to producer for scheduling and prioritization, and cutting scope is producer's ("Decide what features to include or exclude (escalate to producer)")
