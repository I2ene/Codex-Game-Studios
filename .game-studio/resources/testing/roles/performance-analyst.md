# Evaluation scenarios: gs-performance-analyst

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-performance-analyst.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Analyze this frame time data: CPU 14ms, GPU 8ms, physics 6ms, draw calls 420, scripts 3ms."
**Domain checks:**
- Identifies the primary bottleneck: the frame is CPU-bound (CPU 14ms vs GPU 8ms) — inside a 16.67ms (60fps) frame, but with under 3ms of headroom
- Breaks down contributors: physics (6ms, 43% of CPU time) is the top culprit
- Draw calls (420) flags as a secondary concern if the budget limit is lower (e.g., 200 draw calls per the project's `performance.draw_call_limit`)
- Produces a prioritized bottleneck report:
  1. Physics — 6ms, reduce simulation frequency or switch broadphase algorithm
  2. Draw calls — 420, implement batching or LOD
  3. Scripts — 3ms, profile hot paths
- Does NOT implement any of these optimizations

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Implement the batching optimization to reduce draw calls from 420 to under 200."
**Domain checks:**
- Does NOT produce implementation code for batching
- Explicitly states that implementing optimizations belongs to the owner of the system — `technical-artist`, whose rendering optimization covers batching (naming `engine-programmer` as well, for an engine-level rendering change the batching needs, is fine)
- Redirects the implementation to `technical-artist`, handing over its recommendation as the brief: the target (under 200 draw calls), estimated impact, and implementation cost

---

### Case 3: Regression identification
**Input:** "Performance dropped significantly after last week's commits. Frame time went from 10ms to 18ms."
**Domain checks:**
- Compares profiles of a build from before the window (~10ms) and after it (~18ms); if no profile exists for either build, asks for or proposes the captures instead of guessing
- Localizes the 8ms delta to the frame-time categories that grew (gameplay logic, rendering, physics, AI, audio), not to a cause guessed from commit messages or diffs alone
- Names a suspect commit or system only when a profile supports it (e.g., profiles of builds inside the commit range) — never from commit messages or diffs alone
- Reports it under "Regressions Since Last Report" with the measured delta (10ms → 18ms) and the affected category, and recommends a fix owner rather than implementing the fix

---

### Case 4: Recommendation vs. code quality trade-off
**Input:** "The fastest optimization for the script bottleneck would be to inline all calls and remove abstraction layers."
**Domain checks:**
- Surfaces the trade-off: inlining improves performance but reduces testability and violates the coding standard requiring unit-testable public methods
- Does NOT recommend the optimization without noting the code quality cost
- Escalates the trade-off to `technical-director`, the agent it reports to, for a decision
- Presents the options with their trade-offs — e.g., inlining only the hottest 2–3 methods, which keeps the public methods testable — rather than one all-or-nothing recommendation

---

### Case 5: Context pass — project performance budgets
**Input:** Performance budgets from the project config (`performance.*` in `project.yaml`) provided in context: Target 60fps, frame budget 16.67ms, draw calls max 200, memory ceiling 512MB. Request: "Review the current build profile."
**Domain checks:**
- References the specific values from the provided context: 16.67ms, 200 draw calls, 512MB
- Compares current measurements against each threshold explicitly, in its Performance Report Format (Budget / Actual / Status tables for frame time and memory)
- Labels each metric's Status as OK or OVER based on the provided numbers
- Does NOT use different budget numbers than those provided in the context
