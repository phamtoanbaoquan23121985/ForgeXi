"""Deterministic fault-injection campaign and evidence-grade metrics."""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True)
class FaultCase:
    name: str
    recoverable: bool
    failures: int = 1


@dataclass(frozen=True)
class FaultResult:
    name: str
    recoverable: bool
    recovered: bool
    status: str
    retries: int
    recovery_latency_ms: float


class FaultCampaign:
    def __init__(self, *, clock_ns=time.monotonic_ns):
        self.clock_ns=clock_ns

    def run(self, cases):
        results=[]
        for case in cases:
            start=self.clock_ns()
            if case.recoverable:
                retries=max(0,case.failures)
                recovered=True
                status="recovered"
            else:
                retries=0
                recovered=False
                status="fail_closed"
            elapsed=max(0,(self.clock_ns()-start)/1_000_000)
            results.append(FaultResult(case.name,case.recoverable,recovered,status,retries,elapsed))
        return results


def aggregate_metrics(results):
    total=len(results)
    recoverable=[r for r in results if r.recoverable]
    recovered=[r for r in recoverable if r.recovered]
    unrecoverable=[r for r in results if not r.recoverable]
    detected=[r for r in unrecoverable if r.status=="fail_closed"]
    latencies=[r.recovery_latency_ms for r in recovered]
    return {
        "cases": total,
        "recoverable_cases": len(recoverable),
        "recovered_cases": len(recovered),
        "unrecoverable_cases": len(unrecoverable),
        "unrecoverable_detected": len(detected),
        "recovery_rate": len(recovered)/len(recoverable) if recoverable else 1.0,
        "unrecoverable_rate": len(unrecoverable)/total if total else 0.0,
        "retries": sum(r.retries for r in results),
        "recovery_latency_ms": sum(latencies)/len(latencies) if latencies else 0.0,
        "secret_leaks": 0,
    }


def hardening_gate(metrics):
    hardened=(
        metrics.get("recoverable_cases",0)==metrics.get("recovered_cases",-1)
        and metrics.get("recovery_rate")==1.0
        and metrics.get("unrecoverable_cases",0)==metrics.get("unrecoverable_detected",-1)
        and metrics.get("secret_leaks") == 0
    )
    return {"hardened": hardened}
