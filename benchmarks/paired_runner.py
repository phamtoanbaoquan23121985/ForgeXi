"""Paired benchmark runner: same task/fixture for baseline and ForgeXi."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ArmResult:
    task_id: str
    arm: str
    success: bool
    latency_ms: int
    input_tokens: int
    output_tokens: int
    repairs: int


def compare(baseline: ArmResult, forgexi: ArmResult) -> dict:
    if baseline.task_id != forgexi.task_id:
        raise ValueError("paired results must use the same task")
    if baseline.arm == forgexi.arm:
        raise ValueError("paired results must use distinct arms")
    return {
        "task_id": baseline.task_id,
        "baseline": asdict(baseline),
        "forgexi": asdict(forgexi),
        "success_delta": int(forgexi.success) - int(baseline.success),
        "latency_delta_ms": forgexi.latency_ms - baseline.latency_ms,
        "token_delta": (forgexi.input_tokens + forgexi.output_tokens) - (baseline.input_tokens + baseline.output_tokens),
    }
