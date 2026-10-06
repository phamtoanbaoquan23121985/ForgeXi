"""Evidence-safe paired benchmark aggregation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RunResult:
    arm: str
    task_id: str
    base_sha: str
    seed: int
    wall_time_seconds: int
    verified: bool
    latency_ms: int | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None

    @property
    def pair_key(self) -> tuple[str, str, int, int]:
        return (self.task_id, self.base_sha, self.seed, self.wall_time_seconds)


def paired_results(results: Iterable[RunResult]) -> list[tuple[RunResult, RunResult]]:
    buckets: dict[tuple[str, str, int, int], dict[str, RunResult]] = {}
    for result in results:
        arms = buckets.setdefault(result.pair_key, {})
        if result.arm in arms:
            raise ValueError(f"duplicate arm {result.arm!r} for pair {result.pair_key}")
        arms[result.arm] = result

    pairs: list[tuple[RunResult, RunResult]] = []
    for key, arms in sorted(buckets.items()):
        if set(arms) != {"baseline", "forgexi"}:
            raise ValueError(f"incomplete benchmark pair {key}: {sorted(arms)}")
        pairs.append((arms["baseline"], arms["forgexi"]))
    return pairs
