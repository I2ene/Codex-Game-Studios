# Evaluation scenarios: gs-lead-programmer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-lead-programmer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output format
**Scenario:** A new `CombatSystem` implementation is submitted for code review with every input LP-CODE-REVIEW names: its implementation files, its story's acceptance criteria, the relevant GDD section (the combat rules) and its governing ADR. The system stays inside the ADR's boundary, implements the GDD's combat rules as written, uses dependency injection for all external references, has doc comments on all public APIs, loads its tuning values from data files, and includes unit tests for all public methods. Request is tagged LP-CODE-REVIEW.
**Domain checks:** Returns the verdict APPROVE with rationale confirming the ADR boundary match, correctness against the GDD rules, dependency injection usage, doc comment coverage, data-driven configuration, and a testable public API.
**Checklist:**
- [ ] Verdict is exactly one of APPROVE / CONCERNS / REJECT (the LP-CODE-REVIEW verdicts)
- [ ] States the verdict word `APPROVE` explicitly — `$gs-story-done` branches on the gate's verdict words, so a verdict left implicit in prose cannot be acted on
- [ ] Rationale references specific criteria from its Coding Standards Enforcement list and the gate prompt (ADR boundary, GDD rules, DI, doc comments, data-driven values, testable API)
- [ ] Output stays within code quality scope — does not comment on whether the mechanic is fun or fits creative vision

---

### Case 2: Out-of-domain request — redirects or escalates
**Scenario:** Team member asks lead-programmer to review and approve the balance formula for player damage scaling across levels, checking whether the numbers "feel right."
**Domain checks:** Agent declines to evaluate design balance and redirects to game-designer, its stated contact for design concerns.
**Checklist:**
- [ ] Does not make any binding assessment of formula balance or game feel
- [ ] Explicitly names `game-designer` as the correct handler (its "What This Agent Must NOT Do" target for design concerns); naming `systems-designer` as the formula owner as well is fine
- [ ] Any comment it makes on the formula is about implementation (e.g., integer overflow risk at max level); all balance evaluation is deferred to the design team

---

### Case 3: Gate verdict — correct vocabulary
**Scenario:** The architecture document under review (passed with its technical requirements baseline and ADR list) specifies enemy AI that runs a brute-force nearest-neighbor search against all other entities every frame. With expected enemy counts of 2,000+, this is O(n²) — about 4 million distance checks per frame — against the document's 2 ms AI budget at 60fps. Request is tagged LP-FEASIBILITY.
**Domain checks:** Returns the verdict INFEASIBLE with specific citation of the O(n²) complexity, the entity count threshold, and the resulting per-frame cost against the 2 ms AI budget.
**Checklist:**
- [ ] Verdict is exactly one of FEASIBLE / CONCERNS / INFEASIBLE — not freeform text
- [ ] States the verdict word `INFEASIBLE` explicitly, not a verdict implied by prose
- [ ] Rationale includes the specific algorithmic complexity and entity count numbers
- [ ] Suggests at least one alternative approach (e.g., spatial hashing, KD-tree) without mandating a choice

---

### Case 4: Conflict escalation — correct parent
**Scenario:** game-designer wants a mechanic where every NPC maintains a full simulation of needs, schedule, and memory (similar to a full life-sim AI). lead-programmer calculates this will exceed the frame budget by 3x at target NPC counts. game-designer insists the mechanic is core to the game vision.
**Domain checks:** lead-programmer states the specific frame budget violation with numbers, proposes alternative approaches (e.g., LOD-based simulation, simplified need model), but explicitly defers the "is this worth the cost or should the design change" decision to creative-director as the creative arbiter.
**Checklist:**
- [ ] States the specific frame budget violation (e.g., 3x over budget at N entities)
- [ ] Proposes at least one technically viable alternative
- [ ] Explicitly defers the design priority decision to `creative-director`
- [ ] Does not unilaterally cut or modify the mechanic design

---

### Case 5: Context pass — uses provided context
**Scenario:** Agent receives a gate context block for an architecture document (with its technical requirements baseline and ADR list) that includes the project's frame budget: 16.67ms total per frame, with 4ms allocated to AI systems. The document adopts a new AI behavior system that prototype profiling estimates will consume 7ms per frame under normal conditions. Request is tagged LP-FEASIBILITY.
**Domain checks:** Assessment references the specific frame budget allocation from context (4ms AI budget), identifies the 7ms estimate as exceeding the allocation by 3ms, and returns CONCERNS or INFEASIBLE with those specific numbers cited.
**Checklist:**
- [ ] References the specific frame budget figures from the provided context (16.67ms total, 4ms AI allocation)
- [ ] Uses the specific 7ms estimate from the submission in the comparison
- [ ] Does not give generic "this might be slow" advice — cites concrete numbers
- [ ] Verdict rationale is traceable to the provided budget constraints

---

### Case 6: Missing gate input — NOT ASSESSED
**Scenario:** An `InventorySystem` implementation is submitted for code review with its implementation files, its story's acceptance criteria and its governing ADR; everything the agent can check is sound. The relevant GDD section the gate names was not passed: the context gives neither its text nor a path, the story file names none, and the calling skill does not report it absent. Request is tagged LP-CODE-REVIEW.
**Domain checks:** Returns NOT ASSESSED for LP-CODE-REVIEW, naming the GDD section as the input it was not given — without it, the gate's check for correctness issues against the GDD rules cannot be made, so APPROVE is out of reach.
**Checklist:**
- [ ] States the verdict `NOT ASSESSED` explicitly for LP-CODE-REVIEW — not APPROVE, although everything it could check is sound
- [ ] Names the relevant GDD section as the missing input
- [ ] Does not infer the GDD rules from the code or the story and judge correctness against them
- [ ] Variant — had the calling skill reported that no inventory GDD exists, that is a finding, not a missing input: the verdict is CONCERNS or REJECT, not NOT ASSESSED
