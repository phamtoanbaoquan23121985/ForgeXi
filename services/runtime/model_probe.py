"""Authenticated read-only /models capability probe."""

from __future__ import annotations

import time

from .auth_negotiation import AuthMode
from .capability_probe import ProbeResult


class ModelProbe:
    def __init__(self, transport, credential_provider, base_url: str, auth_mode: AuthMode, *, timeout_seconds=20.0, clock_ns=time.monotonic_ns):
        self._transport = transport
        self._credentials = credential_provider
        self._base_url = base_url.rstrip("/")
        self._auth_mode = auth_mode
        self._timeout = timeout_seconds
        self._clock_ns = clock_ns

    def probe(self, model: str) -> ProbeResult:
        start = self._clock_ns()
        credential = self._credentials.get()
        response = self._transport.get_json(
            f"{self._base_url}/models",
            {"Authorization": f"Bearer {credential.value}"},
            self._timeout,
        )
        models = []
        if 200 <= response.status < 300:
            models = [str(item.get("id")) for item in (response.payload.get("data") or []) if isinstance(item, dict) and item.get("id")]
        status = "ok" if model in models else ("model_unavailable" if 200 <= response.status < 300 else f"http_{response.status}")
        latency_ms = (self._clock_ns() - start) // 1_000_000
        return ProbeResult(self._auth_mode, model, "models", status, int(latency_ms))
