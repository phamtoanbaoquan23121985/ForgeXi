"""Runtime configuration loaded without embedding credentials in artifacts."""

from __future__ import annotations

import os
from dataclasses import dataclass

from .nebius_client import DEFAULT_BASE_URL


@dataclass(frozen=True)
class ModelConfig:
    model: str = "nvidia/nemotron-3-super-120b-a12b"
    base_url: str = DEFAULT_BASE_URL
    timeout_seconds: float = 60.0
    max_retries: int = 2

    @classmethod
    def from_env(cls) -> "ModelConfig":
        return cls(
            model=os.getenv("FORGEXI_MODEL", cls.model),
            base_url=os.getenv("FORGEXI_BASE_URL", cls.base_url),
            timeout_seconds=float(os.getenv("FORGEXI_REQUEST_TIMEOUT_SECONDS", "60")),
            max_retries=int(os.getenv("FORGEXI_MAX_RETRIES", "2")),
        )
