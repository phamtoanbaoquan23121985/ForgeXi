# ForgeXi WebMCP

ForgeXi registers five bounded browser tools using the current native producer contract: `document.modelContext.registerTool`.

| Tool | Effect |
| --- | --- |
| `probe_models` | Read-only model availability probe; no inference. |
| `run_nemotron_decision` | One bounded decision through the configured runtime. |
| `run_forgexi_task` | Starts a bounded Plan → Act → Test → Repair → Verify run. |
| `get_run_status` | Read-only run state. |
| `get_evidence_receipt` | Read-only secret-free evidence receipt. |

The browser module receives no Nebius credentials. Authentication remains server-side behind the runtime credential provider. The dispatcher exposes no arbitrary shell, URL, fetch, header, or credential operation, and rejects unsafe result fields.

Registration is owned by an AbortSignal so the page/component lifecycle can remove only ForgeXi-owned registrations. Ordinary UI behavior must remain usable when WebMCP is unsupported.

## Verification status

Source integration and contract tests are implemented. Native browser discovery/invocation remains unverified until ForgeXi is served in a browser/client exposing the current WebMCP producer/consumer capabilities.
