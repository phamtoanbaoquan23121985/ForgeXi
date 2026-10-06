"""Short-lived Nebius AI Cloud IAM credential provider.

Token acquisition is injected so private-key/JWT handling can live in a
dedicated SDK, CLI, workload-identity, or secret-managed boundary rather than
inside ForgeXi agent/evidence code.
"""

from __future__ import annotations

import time
from typing import Callable, Mapping

from .credentials import BearerCredential, ExpiringCredentialProvider


class IAMCredentialProvider:
    def __init__(
        self,
        exchange: Callable[[], Mapping[str, object]],
        *,
        refresh_skew_seconds: float = 300.0,
        clock: Callable[[], float] = time.time,
    ):
        self._clock = clock

        def mint() -> BearerCredential:
            payload = exchange()
            token = str(payload.get("accessToken") or "")
            try:
                lifetime = float(payload["expiresIn"])
            except (KeyError, TypeError, ValueError) as exc:
                raise RuntimeError("IAM token exchange did not return a valid expiresIn") from exc
            if not token or lifetime <= 0:
                raise RuntimeError("IAM token exchange returned an invalid credential")
            return BearerCredential(token, expires_at=self._clock() + lifetime)

        self._provider = ExpiringCredentialProvider(
            mint,
            refresh_skew_seconds=refresh_skew_seconds,
            clock=clock,
        )

    def get(self) -> BearerCredential:
        return self._provider.get()

    def __repr__(self) -> str:
        return "IAMCredentialProvider(<redacted>)"
