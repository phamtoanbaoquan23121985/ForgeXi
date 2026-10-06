from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EvidenceEvent:
    sequence: int
    phase: str
    success: bool
    observed: dict[str, Any]


class EvidenceLedger:
    def __init__(self, run_id: str) -> None:
        if not run_id.strip():
            raise ValueError("run_id must be non-empty")
        self.run_id = run_id
        self.events: list[EvidenceEvent] = []

    def record(self, phase: str, success: bool, observed: dict[str, Any]) -> None:
        self.events.append(EvidenceEvent(
            sequence=len(self.events),
            phase=phase,
            success=success,
            observed=dict(sorted(observed.items())),
        ))

    def scorecard(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "run_id": self.run_id,
            "events": [
                {
                    "sequence": event.sequence,
                    "phase": event.phase,
                    "success": event.success,
                    "observed": event.observed,
                }
                for event in self.events
            ],
        }
