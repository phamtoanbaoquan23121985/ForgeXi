# ForgeXi EVB v1

Ephemeral Verification Bridge (EVB) is the fallback verifier when a persistent runner is unavailable.

Trust chain:

1. Pin an exact Git commit SHA.
2. Build a manifest of repository paths and content SHA-256 values.
3. Materialize those exact bytes into an isolated ephemeral directory.
4. Verify every materialized file against the manifest before execution.
5. Run the standard ForgeXi hardening verifier.
6. Bind the hardening receipt to the source manifest in an EVB receipt.
7. Report only `HARDENED`, `NOT_HARDENED`, or `UNVERIFIED`.

`UNVERIFIED` dominates all other results. A missing or modified source file can never inherit a successful hardening decision.

EVB does not claim to be GitHub Actions and does not require a persistent daemon, inbound port, runner registration token, or long-lived credential. Raw credentials and authorization headers are excluded from receipts.
