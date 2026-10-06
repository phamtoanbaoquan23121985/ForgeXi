"""Credential sources kept outside ForgeXi evidence and configuration."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Callable, Protocol


@dataclass(frozen=True, repr=False)
class BearerCredential:
    value: str = field(repr=False)
    expires_at: float | None = None

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("credential must be non-empty")

    def __repr__(self) -> str:
        return f"BearerCredential(value=<redacted>, expires_at={self.expires_at!r})"


class CredentialProvider(Protocol):
    def get(self) -> BearerCredential: ...


class EnvironmentCredentialProvider:
    def __init__(self, variable: str):
        self.variable = variable

    def get(self) -> BearerCredential:
        value = os.getenv(self.variable)
        if not value:
            raise RuntimeError(f"required credential environment variable is not set: {self.variable}")
        return BearerCredential(value)


class ExpiringCredentialProvider:
    def __init__(
        self,
        mint: Callable[[], BearerCredential],
        *,
        refresh_skew_seconds: float = 30.0,
        clock: Callable[[], float] = time.time,
    ):
        self._mint = mint
        self._skew = refresh_skew_seconds
        self._clock = clock
        self._cached: BearerCredential | None = None

    def get(self) -> BearerCredential:
        current = self._cached
        if current is None or (
            current.expires_at is not None
            and self._clock() >= current.expires_at - self._skew
        ):
            current = self._mint()
            if current.expires_at is not None and current.expires_at <= self._clock():
                raise RuntimeError("credential provider returned an expired credential")
            self._cached = current
        return current
