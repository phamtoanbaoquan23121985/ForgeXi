# ForgeXi

Evidence-driven coding agent for the Nebius × NVIDIA Global AI Hackathon — Coding and Agentic Engineering track.

**Plan → Act → Test → Diagnose → Repair → Verify → Evidence**

ForgeXi places NVIDIA Nemotron on the engineering decision path and keeps repository execution, authentication, verification, and evidence behind explicit security boundaries.

## What is implemented

- Capability-driven authentication negotiation with short-lived Nebius AI Cloud IAM support and separate Token Factory credential handling.
- Authenticated read-only `/v1/models` probe before inference.
- Provider-neutral Nemotron decision contract with bounded retry.
- Workspace-confined command execution with an allowlist and sanitized child environment.
- Bounded repair loop with an explicit repair budget.
- SHA-256 tamper-evident event chain.
- Secret-free inference receipts: model, measured latency, input/output token counts, and response digest.
- Native WebMCP producer surface for `probe_models`, `run_nemotron_decision`, `run_forgexi_task`, `get_run_status`, and `get_evidence_receipt`.
- Paired benchmark result schema for baseline vs ForgeXi.

## Security boundary

Credentials are resolved server-side. Browser/WebMCP schemas do not accept credentials, headers, arbitrary URLs, or arbitrary shell commands. Child repository processes do not inherit Nebius credentials. Evidence rejects credential-bearing fields while allowing non-secret usage metrics such as `input_tokens` and `output_tokens`.

## Setup

Requires Python 3.11+.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Configure Nebius credentials outside source control. Never commit `.env` or paste credentials into benchmark artifacts. See `docs/AUTHENTICATION.md`.

## Verification status

Architecture and contract tests are implemented. Live Nemotron/Nebius inference, benchmark measurements, hosted-demo verification, and native-browser WebMCP invocation are **not claimed complete until observed run artifacts exist**.

## Evidence policy

No benchmark, quality, latency, cost, reliability, or competition-performance claim is accepted without a reproducible run artifact. Unmeasured values remain absent/null rather than estimated.

## License

Apache-2.0.
