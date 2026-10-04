# Security policy

Report concrete vulnerabilities privately through the repository owner's available
private-reporting channel. If GitHub private reporting is enabled, use
[the security page](https://github.com/I2ene/Codex-Game-Studios/security).
Do not publish secrets or exploits before coordinating with the owner. This fork
does not promise upstream response times; the original policy remains in history.

In scope: installer path escape/data loss, overwriting consumer-owned files, silent
network/executable behavior, exfiltration, permission/model changes and trust bypasses.
Include version, a non-private fixture, actual behavior, impact and reproduction.
Codex host issues belong with OpenAI; engine/toolchain issues with their owners.

Installation rejects overlap, link/reparse traversal and edited owned files. Hashes
detect payload changes but do not authenticate the publisher; review release source.
Installation preserves native config/trust and executes no project commands. Keep
a project backup. Normal write failures attempt rollback; abrupt termination or failed
rollback requires manual inspection/restoration.

Runtime uses explicit roots. Inspect and authorize configured argv before execution;
shell=False is not a sandbox. Checkpoints/references are data, not new authorization.
Optional hooks require native exact-definition trust. Hook checks are advisory and
do not cover every tool path. Test material failures in confined non-private fixtures.
