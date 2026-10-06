"""Secret-free capability probe evidence."""

from __future__ import annotations

from dataclasses import dataclass

from .auth_negotiation import AuthMode


@dataclass(frozen=True)
class ProbeResult:
    auth_mode: AuthMode
    model: str
    endpoint_capability: str
    status: str
    latency_ms: int

    def __post_init__(self):
        if not self.model.strip() or not self.endpoint_capability.strip() or not self.status.strip():
            raise ValueError("probe fields must be non-empty")
        if self.latency_ms < 0:
            raise ValueError("latency_ms must be nonnegative")


def evidence_fields(result: ProbeResult) -> dict[str, object]:
    # Explicit allowlist: adding fields to ProbeResult cannot silently add them to evidence.
    return {
        "auth_mode": result.auth_mode.value,
        "model": result.model,
        "endpoint_capability": result.endpoint_capability,
        "status": result.status,
        "latency_ms": result.latency_ms,
    }


def record_probe(chain, result: ProbeResult) -> dict:
    return chain.append("capability_probe", evidence_fields(result))
