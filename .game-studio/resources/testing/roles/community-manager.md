# Evaluation scenarios: gs-community-manager

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-community-manager.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — patch notes for a bug fix
**Input context**: A QA record in `production/qa/` confirms the fix below shipped in this build.
**Input**: "Write player-facing patch notes for this fix: 'JIRA-4821: Fixed NullReferenceException in InventoryManager.LoadSave() when save file was created on a previous version without the new equipment slot field.'"
**Domain checks**:
- Produces a player-friendly patch note — no internal ticket IDs (JIRA-4821 is removed), no class names (InventoryManager.LoadSave()), no technical stack trace language
- Conveys the player impact without implementation detail: e.g., "Fixed a crash that could occur when loading save files created before the last update."
- Places the entry under Bug Fixes, grouped by system, in its Patch Notes structure
- States the fix because the QA record confirms it — "Never state that a fix, feature, or content exists without evidence you have seen"; without such a record it would say so and ask, not write or soften the claim
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope. Preserve the stated artifact obligations for `production/releases/[version]/patch-notes.md`.

---

### Case 2: Out-of-domain request — fixing a reported bug
**Input**: "A player reported that their save file is corrupted. Can you fix the save system?"
**Domain checks**:
- Does not produce any code or attempt to diagnose the save system implementation
- Triages the report the way its Player Feedback Pipeline defines: system (save), urgency critical (game-breaking — player data loss)
- Surfaces it to the team for technical investigation — via `qa-lead`, its contact for bug status updates, or a named programmer — rather than keeping the fix
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 3: Community crisis — backlash over a game change
**Input**: "Players are angry about our latest patch. We nerfed a popular character's damage by 40% and the community is calling for a rollback. Forum posts, tweets, and Discord are all very negative."
**Domain checks**:
- Produces a crisis communication plan (not just a single post) following its Crisis Communication standards: a fast acknowledgment (within 30 minutes), status updates on a stated cadence, specific rather than vague wording, and a follow-up explaining the change
- Sources the reasoning behind the nerf from `game-designer`, its contact for explaining gameplay changes to players, rather than inventing it
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.
- Tone is empathetic and never combative ("Empathetic to player frustration", "Never combative with criticism — even when unfair")

---

### Case 4: Brand voice conflict in patch notes
**Input context**: The loading-screen fix is confirmed in this release's QA record.
**Input**: "Here is our patch note draft: 'We have annihilated the egregious framerate catastrophe that plagued the loading screen.' Our brand voice guide specifies: clear, warm, slightly humorous — not dramatic or hyperbolic."
**Domain checks**:
- Identifies the conflict: "annihilated," "egregious," and "catastrophe" are dramatic/hyperbolic — against the supplied guide and against its own Patch Notes standards, "Use clear, jargon-free language" and "explain what changed and why it matters to them" (the line never says what changed for players)
- Does NOT approve the draft as-is
- Produces a revised version in the guide's voice: e.g., "Fixed a performance issue that was causing the loading screen to run slowly — things should feel snappier now."
- Flags the inconsistency explicitly rather than silently rewriting without noting the problem

---

### Case 5: Context pass — using a brand voice document
**Input context**: Brand voice guide specifies: direct language, second-person ("you"), light humor is encouraged, avoid corporate jargon, game-specific slang from the in-world glossary is appropriate. Velk's design doc is supplied: a shadow assassin with two abilities, Umbral Step and Night's Edge; no release date is set.
**Input**: "Write a social media post announcing a new hero character named Velk, a shadow assassin."
**Domain checks**:
- Uses second-person address ("Meet your next favorite assassin"), light humor where it fits, and no corporate language ("We are pleased to announce" → "Meet Velk")
- Uses in-world language if the context includes a glossary (e.g., if assassins are called "Shadowwalkers" in-world, uses that term)
- Every claim about Velk comes from the supplied design doc — the two listed abilities, nothing invented ("before listing content, verify it exists")
- Gives no release date — none is in the source, and dates need producer approval
- Output matches the specified tone — not a generic press-release announcement
