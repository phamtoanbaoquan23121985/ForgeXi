"""Bounded Plan → Act → Test → Diagnose → Repair → Verify loop."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Verification:
    ok: bool
    summary: str


@dataclass(frozen=True)
class RunResult:
    status: str
    repairs: int
    verification: str


class ClosedLoop:
    def __init__(self, decisions, work, *, max_repairs: int = 2):
        if not 0 <= max_repairs <= 5:
            raise ValueError("max_repairs must be between 0 and 5")
        self.decisions = decisions
        self.work = work
        self.max_repairs = max_repairs

    def run(self, task: str) -> RunResult:
        plan = self.decisions.decide("plan", task)
        self.work.act(plan)
        repairs = 0
        test = self.work.test()
        while not test.ok:
            if repairs >= self.max_repairs:
                return RunResult("failed", repairs, test.summary)
            diagnosis = self.decisions.decide("diagnose", task, failure=test.summary)
            repair = self.decisions.decide("repair", task, failure=diagnosis)
            self.work.repair(repair)
            repairs += 1
            test = self.work.test()
        final = self.work.verify()
        return RunResult("verified" if final.ok else "failed", repairs, final.summary)
