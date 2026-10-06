"""Nebius Token Factory adapter with bounded retry and normalized evidence."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Callable

from .credentials import CredentialProvider, EnvironmentCredentialProvider
from .protocol import DecisionRequest, DecisionResponse, TokenUsage


DEFAULT_BASE_URL = "https://api.tokenfactory.nebius.com/v1"


class ProviderError(RuntimeError):
    pass


@dataclass
class UrllibTransport:
    def post_json(self, url, headers, payload, timeout):
        body = json.dumps(payload, separators=(",", ":")).encode()
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return _HttpResponse(response.status, json.loads(response.read()))
        except urllib.error.HTTPError as exc:
            try:
                payload = json.loads(exc.read())
            except Exception:
                payload = {}
            return _HttpResponse(exc.code, payload)


@dataclass
class _HttpResponse:
    status: int
    payload: dict

    def read(self):
        return json.dumps(self.payload).encode()


class NebiusClient:
    def __init__(
        self,
        api_key: str | None = None,
        *,
        credential_provider: CredentialProvider | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout_seconds: float = 60.0,
        max_retries: int = 2,
        transport=None,
        clock_ns: Callable[[], int] = time.monotonic_ns,
    ):
        if api_key and credential_provider is not None:
            raise ValueError("provide api_key or credential_provider, not both")
        if credential_provider is None:
            if api_key:
                class _StaticProvider:
                    def get(self_nonlocal):
                        from .credentials import BearerCredential
                        return BearerCredential(api_key)
                credential_provider = _StaticProvider()
            else:
                credential_provider = EnvironmentCredentialProvider("NEBIUS_API_KEY")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if max_retries < 0:
            raise ValueError("max_retries must be nonnegative")
        self._credential_provider = credential_provider
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout_seconds
        self._max_retries = max_retries
        self._transport = transport or UrllibTransport()
        self._clock_ns = clock_ns

    def decide(self, request: DecisionRequest) -> DecisionResponse:
        payload = {
            "model": request.model,
            "messages": list(request.messages),
            "temperature": request.temperature,
        }
        credential = self._credential_provider.get()
        headers = {
            "Authorization": f"Bearer {credential.value}",
            "Content-Type": "application/json",
        }
        start = self._clock_ns()
        last_status = None
        for attempt in range(self._max_retries + 1):
            response = self._transport.post_json(
                f"{self._base_url}/chat/completions",
                headers,
                payload,
                self._timeout,
            )
            last_status = response.status
            if 200 <= response.status < 300:
                data = json.loads(response.read())
                try:
                    text = data["choices"][0]["message"]["content"]
                except (KeyError, IndexError, TypeError) as exc:
                    raise ProviderError("invalid provider response") from exc
                usage = data.get("usage") or {}
                latency_ms = (self._clock_ns() - start) // 1_000_000
                return DecisionResponse(
                    text=text,
                    model=str(data.get("model") or request.model),
                    latency_ms=int(latency_ms),
                    usage=TokenUsage(
                        input_tokens=int(usage.get("prompt_tokens") or 0),
                        output_tokens=int(usage.get("completion_tokens") or 0),
                    ),
                )
            if response.status not in {408, 429, 500, 502, 503, 504}:
                break
            if attempt == self._max_retries:
                break
        raise ProviderError(f"Nebius provider request failed with HTTP {last_status}")
