"""Canonical paired-benchmark task definitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkTask:
    task_id: str
    repo_url: str
    base_sha: str
    instruction: str
    seed: int
    wall_time_seconds: int

    def __post_init__(self) -> None:
        for name in ("task_id", "repo_url", "base_sha", "instruction"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.wall_time_seconds <= 0:
            raise ValueError("wall_time_seconds must be positive")

    @property
    def pair_key(self) -> tuple[str, str, int, int]:
        return (self.task_id, self.base_sha, self.seed, self.wall_time_seconds)
