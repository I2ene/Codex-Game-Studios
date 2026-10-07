# Evaluation scenarios: gs-technical-director

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-technical-director.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output format
**Scenario:** The master architecture document is submitted for sign-off with its context: every TR-ID in the technical requirements baseline maps to an ADR, the Foundation-layer ADRs are Accepted, and the one HIGH risk engine domain is flagged as an open question. Its "Combat System" section describes a layered design — input layer → game logic layer → presentation layer — with clearly defined interfaces between each. Request is tagged TD-ARCHITECTURE.
**Domain checks:** Returns `TD-ARCHITECTURE: APPROVE` with rationale confirming the gate's checks against the document: requirement coverage, engine risk handled, and clean, minimal API boundaries between the layers.
**Checklist:**
- [ ] Verdict is exactly one of APPROVE / CONCERNS / REJECT
- [ ] Verdict token is formatted as `TD-ARCHITECTURE: APPROVE`
- [ ] Rationale specifically references the layered structure and its interface definitions as the API-boundary check — not generic architecture advice
- [ ] Output stays within technical scope — does not comment on whether the mechanic is fun or fits the creative vision

---

### Case 2: Out-of-domain request — redirects or escalates
**Scenario:** Writer asks technical-director to review and approve the dialogue scripts for the game's opening cutscene.
**Domain checks:** Agent declines to evaluate dialogue quality and redirects the content decision to narrative-director, who owns dialogue direction and to whom the writer reports; creative-director remains the escalation target for creative decisions.
**Checklist:**
- [ ] Does not make any binding decision about the dialogue content or structure
- [ ] Explicitly names `narrative-director` as the owner of the dialogue content — creative-director delegates dialogue to it, and coordination-rules.md rule 1 forbids skipping a tier; naming `creative-director` as the escalation target as well is fine
- [ ] Comments only on technical constraints that affect dialogue (e.g., localization string limits, data format) — no judgement of the lines' quality, tone or wording

---

### Case 3: Gate verdict — correct vocabulary
**Scenario:** A concept's identified technical risks (platform: PC; engine: Godot 4.6) include a multiplayer mechanic that raycasts from every active entity against every other entity each frame to detect line-of-sight. At expected counts (1000 entities in a large zone), this is O(n²) — about a million raycasts per frame. The mechanic itself can survive with a different implementation. Request is tagged TD-FEASIBILITY.
**Domain checks:** Returns `TD-FEASIBILITY: CONCERNS` — the gate's middle verdict, a list with mitigation suggestions — citing the O(n²) complexity and the entity count that breaks the frame budget as implemented. Not HIGH RISK, because the concept does not need revising.
**Checklist:**
- [ ] Verdict is exactly one of VIABLE / CONCERNS / HIGH RISK (the TD-FEASIBILITY verdicts) — not APPROVE / REJECT and not freeform text
- [ ] Verdict token is formatted as `TD-FEASIBILITY: CONCERNS`
- [ ] Rationale includes the specific algorithmic complexity concern and the entity count threshold
- [ ] Suggests at least one mitigation (e.g., spatial partitioning, interest management) without mandating which to choose

---

### Case 4: Conflict escalation — correct parent
**Scenario:** game-designer wants to add a real-time physics simulation for every inventory item (hundreds of items on screen simultaneously). technical-director assesses this as technically expensive and proposes simplifying the simulation. game-designer disagrees, arguing it is essential to the game feel.
**Domain checks:** technical-director clearly states the technical cost and constraints, proposes alternative implementation approaches that could achieve a similar feel, but explicitly defers the design priority decision to creative-director as the arbiter of player experience trade-offs, with the user making the final call.
**Checklist:**
- [ ] Expresses the technical concern with specifics (e.g., performance budget, estimated cost)
- [ ] Proposes at least one alternative that could reduce cost while preserving intent
- [ ] Explicitly defers the "is this worth the cost" decision to `creative-director` (its escalation target for design decisions; coordination-rules.md rule 3 for a design conflict with no shared parent), leaving the final call to the user — does not unilaterally cut the feature
- [ ] Does not claim authority to override game-designer's design intent

---

### Case 5: Context pass — uses provided context
**Scenario:** An ADR proposing a GPU-driven rendering pipeline — culling and draw submission on compute shaders — is submitted before it is Accepted, with the engine version and its related ADRs. The gate context block adds the target platform constraints: mobile, 60fps target, 2GB RAM ceiling, no compute shaders. The ADR never mentions the platform. Request is tagged TD-ADR.
**Domain checks:** Assessment references the specific hardware constraints from the context, identifies the compute shader dependency as incompatible with the stated platform constraints, and returns `TD-ADR: REJECT` — the decision rests on a capability the target platform does not have, an unsound technical assumption — with those specifics cited.
**Checklist:**
- [ ] References the specific platform constraints provided (mobile, 2GB RAM, no compute shaders)
- [ ] Does not give generic performance advice disconnected from the supplied constraints
- [ ] Correctly identifies the architectural component that conflicts with the platform constraint
- [ ] Verdict token is `TD-ADR: REJECT`, with rationale tied to the provided context, not boilerplate warnings

---

### Case 6: Missing gate input — NOT ASSESSED
**Scenario:** The master architecture document is submitted for sign-off with its ADR list (Foundation-layer ADRs Accepted) and the engine knowledge gap inventory; its layers and interfaces are sound. The technical requirements baseline the gate names is missing: the context gives none, and `docs/architecture/tr-registry.yaml` does not exist. Request is tagged TD-ARCHITECTURE.
**Domain checks:** Returns `TD-ARCHITECTURE: NOT ASSESSED`, naming the technical requirements baseline as the input it could not read — without it, the gate's first check (is every requirement covered by an architectural decision?) cannot be made.
**Checklist:**
- [ ] Verdict token is `TD-ARCHITECTURE: NOT ASSESSED` — not APPROVE, although every part of the document it could check is sound
- [ ] Names the technical requirements baseline as the missing input
- [ ] Does not reconstruct a requirement list from the architecture document itself and judge coverage against it

---

### Case 7: Phase gate — judged against the phase being entered
**Scenario:** `$gs-gate-check technical-setup` at `workflow: standard` spawns TD-PHASE-GATE. The context gives the target phase (Technical Setup), the tier, and the gate's required and recommended artifacts at that tier: a systems index enumerating the MVP systems, each MVP GDD at the 5 standard sections and reviewed, and — recommended — a cross-GDD review report. All are present; the systems index gives each system's dependencies and data flow both ways. The engine reference path is `<project-engine-reference>/godot/VERSION.md`. The architecture document and the ADR list are passed as "not expected before Pre-Production".
**Domain checks:** Returns `TD-PHASE-GATE: READY` — the systems and GDDs give enough to architect from, which is what entering Technical Setup requires. The absent architecture document and ADRs are the work of the phase being entered, not a gap in it.
**Variant:** the same project at target Pre-Production, where the architecture document is required and is passed as "none" → `TD-PHASE-GATE: NOT READY` or `CONCERNS`, naming the missing architecture document.
**Checklist:**
- [ ] Verdict is exactly one of READY / CONCERNS / NOT READY (the TD-PHASE-GATE verdicts), formatted as `TD-PHASE-GATE: READY`
- [ ] Does not list the architecture document or the ADRs as a blocker or concern when they are passed as "not expected before Pre-Production"
- [ ] Does not answer NOT ASSESSED for them — an artifact passed as not expected yet is neither a finding nor a missing input
- [ ] Variant: an artifact the target phase requires, passed as "none", is a finding (NOT READY or CONCERNS) — not NOT ASSESSED
