"""Pre-action runtime capability gate."""

from __future__ import annotations

from services.runtime.capability_probe import ProbeResult, record_probe


class RuntimeGate:
    def __init__(self, evidence):
        self.evidence = evidence

    def require(self, probe: ProbeResult, action):
        record_probe(self.evidence, probe)
        if probe.status != "ok":
            raise RuntimeError(f"capability probe failed: {probe.endpoint_capability}")
        return action()
