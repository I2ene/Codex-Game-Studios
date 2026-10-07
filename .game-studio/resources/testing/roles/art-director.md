# Evaluation scenarios: gs-art-director

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-art-director.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output format
**Scenario:** A complete art bible is submitted for sign-off with the pillars and core fantasy, the platform constraints and the visual identity anchor chosen during brainstorm. Its color section defines a desaturated earth-tone primary palette with high-contrast accent colors tied to the game pillar "beauty in decay"; its shape language, asset standards and character direction are consistent with that section and within the stated platform constraints. Request is tagged AD-ART-BIBLE.
**Domain checks:** Returns `AD-ART-BIBLE: APPROVE` with rationale confirming the palette's internal consistency and that the color system matches the pillar's mood target.
**Checklist:**
- [ ] Verdict is exactly one of APPROVE / CONCERNS / REJECT
- [ ] Verdict token is formatted as `AD-ART-BIBLE: APPROVE`
- [ ] Rationale references the specific palette characteristics and how they serve the "beauty in decay" mood target (the gate's color-vs-mood check) — not generic art advice
- [ ] Output stays within visual domain — does not comment on UX interaction patterns or audio mood

---

### Case 2: Out-of-domain request — redirects or escalates
**Scenario:** Sound designer asks art-director to specify how ambient audio should layer and duck when the player enters a combat zone.
**Domain checks:** Agent declines to define audio behavior and redirects to audio-director.
**Checklist:**
- [ ] Does not make any binding decision about audio layering or ducking behavior
- [ ] Explicitly names `audio-director` as the correct handler
- [ ] Any comment it makes is about the zone's visual mood (e.g., "the audio should match the visual tension of the zone") — it specifies no layer, duck amount, fade time or trigger

---

### Case 3: Gate verdict — correct vocabulary
**Scenario:** Right after pillars are locked, the concept and pillar set are submitted for a visual identity anchor. The three pillars are "fun combat," "great story," and "lots of content"; none of their design tests says anything about mood, atmosphere, or what the world should feel like, and no visual touchstones were given. Request is tagged AD-CONCEPT-VISUAL.
**Domain checks:** Returns `AD-CONCEPT-VISUAL: CONCERNS` — the gate's verdict for pillars that don't yet give enough direction to differentiate a visual identity — naming which pillars give no visual direction and what is missing (mood, shape language, color meaning).
**Checklist:**
- [ ] Verdict is exactly one of CONCEPTS / STRONG / CONCERNS (the AD-CONCEPT-VISUAL verdicts) — not APPROVE / REJECT and not freeform text
- [ ] Verdict token is formatted as `AD-CONCEPT-VISUAL: CONCERNS`
- [ ] Rationale names the specific pillars that give no visual direction and which of the gate's four direction components (visual rule, mood, shape language, color philosophy) they leave open — not a generic "pillars are vague"
- [ ] Does not rewrite the pillars itself — pillar changes go back to the user and creative-director

---

### Case 4: Conflict escalation — correct parent
**Scenario:** ux-designer proposes using high-contrast, brightly colored icons for the HUD to improve readability. art-director believes this violates the art bible's muted visual language and would undermine the visual identity.
**Domain checks:** art-director states the visual identity concern and references the art bible, acknowledges ux-designer's readability goal as legitimate, and escalates to creative-director to arbitrate the trade-off between visual coherence and usability.
**Checklist:**
- [ ] Escalates to `creative-director` (shared parent for creative domain conflicts)
- [ ] Does not unilaterally override ux-designer's readability recommendation
- [ ] Clearly frames the conflict as a trade-off between two legitimate goals
- [ ] References the specific art bible rule being violated

---

### Case 5: Context pass — uses provided context
**Scenario:** Agent receives a gate context block that includes the existing art bible with specific palette values (primary: #8B7355, #6B6B47; accent: #C8A96E) and style rules ("no pure white, no pure black; all shadows have warm undertones"). A new asset type is submitted for review: the first enemy sprite sheet, whose body colors come from the primary palette but whose outline is pure black (#000000), highlights pure white (#FFFFFF) and shadows a cool blue-grey (#5A6A7A). Request is tagged AD-VISUAL.
**Domain checks:** Assessment references the specific hex values and style rules from the provided art bible, not generic color theory advice, and returns `AD-VISUAL: REJECT` — the sprite breaks all three style rules, a style violation to resolve before the asset type is used — with each violation tied to the rule it breaks.
**Checklist:**
- [ ] References specific palette values from the provided art bible context
- [ ] Applies the specific style rules (no pure white/black, warm shadow undertones) from the provided document, naming the outline, highlight and shadow colors that break them
- [ ] Does not generate generic art direction feedback disconnected from the supplied art bible
- [ ] Verdict token is `AD-VISUAL: REJECT`, with rationale traceable to specific lines or rules in the provided context

---

### Case 6: Missing gate input — NOT ASSESSED
**Scenario:** A complete, internally consistent art bible is submitted for sign-off with the pillars and the visual identity anchor, but no platform or performance constraints: the context gives none, `project.yaml` sets no `platform.*` or `performance.*` keys, and `.game-studio/resources/docs/technical-preferences.md` still holds only unconfigured placeholders. Request is tagged AD-ART-BIBLE.
**Domain checks:** Returns `AD-ART-BIBLE: NOT ASSESSED`, naming the platform and performance constraints as the input it could not read — without them, the gate's check that the asset standards are achievable on the platform cannot be made.
**Checklist:**
- [ ] Verdict token is `AD-ART-BIBLE: NOT ASSESSED` — not APPROVE, although every section it could check is sound
- [ ] Names the platform and performance constraints as the missing input
- [ ] Does not assume a platform or budget to complete the review
