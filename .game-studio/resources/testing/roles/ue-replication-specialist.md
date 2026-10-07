# Evaluation scenarios: gs-ue-replication-specialist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-ue-replication-specialist.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — replicated player health with client prediction
**Input**: "Set up replicated player health that clients can predict locally (e.g., when taking self-inflicted damage) and have corrected by the server."
**Domain checks**:
- Produces a UPROPERTY(ReplicatedUsing=OnRep_Health) declaration in the appropriate Character or AttributeSet class
- Describes the OnRep_Health function: apply visual/audio feedback, reconcile predicted value with server-authoritative value
- Explains the client prediction pattern: local client applies tentative damage immediately, server authoritative value arrives via OnRep and corrects any discrepancy
- Notes that if GAS is in use, the built-in GAS prediction handles this — recommend coordinating with ue-gas-specialist
- Output is a concrete code structure (property declaration + OnRep outline), not a conceptual description only

---

### Case 2: Out-of-domain request — game server architecture
**Input**: "Design our game server infrastructure — how many dedicated servers we need, regional deployment, and matchmaking architecture."
**Domain checks**:
- Does not produce server infrastructure architecture, hosting recommendations, or matchmaking design
- States that its scope is the Unreal replication layer within a running game session, and names network-programmer (its coordination partner for networking below that layer) as the route for matchmaking and server architecture
- Does not conflate in-game replication with server hosting concerns

---

### Case 3: Domain boundary — RPC without server authority validation
**Input**: "We have a Server RPC called ServerSpendCurrency that deducts in-game currency. The client calls it and the server just deducts without checking anything."
**Domain checks**:
- Flags this as a critical security vulnerability: unvalidated server RPCs are exploitable by cheaters sending arbitrary RPC calls
- Provides the required fix: server-side validation before the deduct — check that the player actually has the currency, verify the transaction is valid, reject and log if not
- Validation covers the three checks every client RPC needs: can this player perform the action now, are the parameters within valid ranges, and is the request rate within limits (rate-limiting the RPC)
- Notes this should be reviewed by security-engineer, its named partner for network security validation, given the economy implications
- Does NOT produce the "fixed" code without explaining why the original was dangerous

---

### Case 4: Bandwidth optimization — high-frequency movement replication
**Input**: "Our player movement is replicated using a Vector3 position every tick. With 32 players, we're exceeding our bandwidth budget."
**Domain checks**:
- Identifies tick-rate replication of full-precision Vector3 as bandwidth-expensive
- Proposes quantized replication: use FVector_NetQuantize or FVector_NetQuantize100 instead of raw FVector to reduce bytes per update
- Recommends lowering how often the movement actor replicates — a per-actor net update frequency (`NetUpdateFrequency` in its standards), not a per-client setting — naming the API it uses and marking it unverified unless `<project-engine-reference>/unreal/` documents it
- Notes that Unreal's built-in Character Movement Component already has optimized movement replication — recommends using or extending it rather than rolling a custom system
- Measures the result against its per-client target (under 10 KB/s for action games) and names the tools to confirm the saving (`stat net`, Network Profiler)

---

### Case 5: Context pass — designing within a network budget
**Input context**: Project network budget is 64 KB/s per player, with 32 players = 2 MB/s total server outbound. Current movement replication already uses 40 KB/s per player.
**Input**: "We want to add real-time inventory replication so all clients can see other players' equipment changes immediately."
**Domain checks**:
- Acknowledges the existing 40 KB/s movement cost leaves only 24 KB/s for everything else per player
- Notes that these project figures sit well above its own default target (under 10 KB/s per client for action games) and works to the project's stated budget while flagging the gap
- Does NOT design a naive full-inventory replication approach (would exceed budget)
- Separates what other players see (equipped items, replicated to all) from the full inventory (`COND_OwnerOnly`)
- Recommends a delta-only or event-driven approach: replicate only changed slots rather than the full inventory array, with `ReplicatedUsing` to trigger targeted updates
- Explicitly states the proposed approach's bandwidth estimate relative to the remaining 24 KB/s budget
