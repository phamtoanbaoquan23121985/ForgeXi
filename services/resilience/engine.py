"""Central bounded recovery engine."""

from __future__ import annotations

import time


class RecoveryEngine:
    def __init__(self, policy, retry_budget, *, sleeper=time.sleep):
        self.policy=policy
        self.retry_budget=retry_budget
        self.sleeper=sleeper

    def run(self, operation, *, classify):
        attempt=0
        while True:
            try:
                return operation()
            except Exception as exc:
                action=self.policy.action_for(classify(exc))
                if action.kind != "retry":
                    raise
                if attempt >= action.max_attempts or not self.retry_budget.take():
                    raise
                delay=min(0.25*(2**attempt),4.0)
                attempt += 1
                self.sleeper(delay)
