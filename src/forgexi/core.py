from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .evidence import EvidenceLedger


class AgentState(str, Enum):
    PLAN = "plan"
    INSPECT = "inspect"
    ACT = "act"
    TEST = "test"
    DIAGNOSE = "diagnose"
    REPAIR = "repair"
    VERIFY = "verify"
    DONE = "done"


@dataclass(frozen=True)
class StepResult:
    phase: str
    success: bool
    observed: dict[str, Any]

    @classmethod
    def ok(cls, phase: str, observed: dict[str, Any]) -> "StepResult":
        return cls(phase=phase, success=True, observed=observed)

    @classmethod
    def fail(cls, phase: str, observed: dict[str, Any]) -> "StepResult":
        return cls(phase=phase, success=False, observed=observed)


class AgentLoop:
    _SUCCESS_NEXT = {
        AgentState.PLAN: AgentState.INSPECT,
        AgentState.INSPECT: AgentState.ACT,
        AgentState.ACT: AgentState.TEST,
        AgentState.TEST: AgentState.VERIFY,
        AgentState.DIAGNOSE: AgentState.REPAIR,
        AgentState.REPAIR: AgentState.TEST,
        AgentState.VERIFY: AgentState.DONE,
    }

    def __init__(self, ledger: EvidenceLedger) -> None:
        self.ledger = ledger
        self.state = AgentState.PLAN

    def advance(self, result: StepResult) -> AgentState:
        if self.state is AgentState.DONE:
            raise RuntimeError("agent run is already complete")
        if result.phase != self.state.value:
            raise ValueError(
                f"phase mismatch: expected {self.state.value!r}, got {result.phase!r}"
            )

        self.ledger.record(result.phase, result.success, result.observed)

        if not result.success:
            if self.state is AgentState.TEST:
                self.state = AgentState.DIAGNOSE
                return self.state
            raise RuntimeError(f"phase {result.phase!r} failed")

        self.state = self._SUCCESS_NEXT[self.state]
        return self.state
