"""Normalized secret-free inference evidence."""

from __future__ import annotations

import hashlib

from services.runtime.protocol import DecisionResponse


def inference_evidence(response: DecisionResponse) -> dict[str, object]:
    return {
        "model": response.model,
        "latency_ms": response.latency_ms,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "total_tokens": response.usage.total_tokens,
        "response_digest": hashlib.sha256(response.text.encode("utf-8")).hexdigest(),
    }
