# Evaluation scenarios: gs-security-engineer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-security-engineer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Review the save data system for security issues."
**Domain checks:**
- Audits the save data handling against its Save Data Security rules: encryption with a per-user key, integrity checksums for tamper detection, save versioning with a backup before migration, validation on load that rejects corrupt or tampered files gracefully, and no sensitive credentials stored in save files
- Flags unencrypted player stats with a severity level (e.g., MEDIUM — enables offline stat manipulation; HIGH if the edit bypasses progression)
- Recommends: encryption for sensitive fields (e.g., AES-256) and a keyed integrity checksum (e.g., HMAC) for tamper detection
- Produces a prioritized finding list (CRITICAL / HIGH / MEDIUM / LOW)
- Gives each finding the `$gs-security-audit` per-finding fields its Findings Format names: ID and title, category, `file:line`, description, attack scenario, remediation, effort
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Design the matchmaking algorithm to pair players by skill rating."
**Domain checks:**
- Does NOT produce matchmaking algorithm design — it is not among its Core Responsibilities, and the project coordination rules bar binding decisions outside an agent's domain
- Explicitly states that matchmaking design belongs to `network-programmer` — the partner its Coordination section names for multiplayer work
- Redirects the request to `network-programmer`
- Anything it offers in place of the design is from its own domain — e.g., a security review of the matchmaking system (rating manipulation) once the design exists — never a matchmaking algorithm

---

### Case 3: Critical vulnerability — SQL injection
**Input:** (Hypothetical) "Review this server-side query handler: `query = 'SELECT * FROM users WHERE id=' + user_input`"
**Domain checks:**
- Flags this as a CRITICAL vulnerability (SQL injection via unsanitized user input — a data-breach class flaw)
- Provides immediate remediation: parameterized queries / prepared statements, consistent with its rule to validate all client input server-side
- Recommends a security review of all other query-construction code in the codebase (its Core Responsibility: "Review all networked code for security vulnerabilities")
- Escalates to `technical-director` immediately — its Coordination rule: "Report CRITICAL findings (and HIGH in a multiplayer game) to **Technical Director** immediately" — and does not leave the finding unescalated

---

### Case 4: Security vs. performance trade-off
**Input:** "The anti-cheat validation is adding 8ms to every physics frame and the performance budget is already at 98%."
**Domain checks:**
- Surfaces the trade-off clearly: removing/reducing validation creates exploit surface; keeping it blows the performance budget
- Does NOT unilaterally drop the security measure
- Escalates to `technical-director` as a technical conflict (its Coordination rule for security trade-offs it cannot settle, and coordination rule 3: technical conflicts with no shared parent go to technical-director), with both the security risk level and the 8ms performance impact stated
- Presents 2-4 options, each with its security cost and its frame-time cost — e.g., async validation (reduces frame impact, adds latency), sampling-based checks (reduces frequency, accepts some cheating), moving the check server-side (its server-authoritative game state rule), or budget renegotiation — and leaves the choice to the user or technical-director

---

### Case 5: Context pass — OWASP guidelines
**Input:** OWASP Top 10 (2021) provided in context by the invoking skill or agent. Request: "Audit the game's login and account system."
**Domain checks:**
- Uses the supplied OWASP list rather than asking which standard to apply or substituting a different one
- Audits against its own authentication and network rules: TLS for all network communication, session tokens with expiration and refresh, rate-limited client-to-server calls, replay and spoofing protection, no sensitive data in logs or error messages, no hardcoded secrets or credentials
- Flags each finding with the matching supplied category by ID and name (e.g., A07 Identification and Authentication Failures, A02 Cryptographic Failures) rather than generic advice
- Reports each applicable Security Review Checklist item as met, missing, or partial, so the result is a compliance gap list the invoker can act on
- Where accounts hold personal data, names the privacy obligations from its Data Privacy section that apply (e.g., GDPR data export and deletion, COPPA age-gate)
