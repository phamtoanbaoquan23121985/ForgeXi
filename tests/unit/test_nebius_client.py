import json

import pytest

from services.runtime.nebius_client import NebiusClient, ProviderError
from services.runtime.protocol import DecisionRequest


class FakeResponse:
    def __init__(self, status, payload):
        self.status = status
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode()


class FakeTransport:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def post_json(self, url, headers, payload, timeout):
        self.calls.append((url, headers, payload, timeout))
        item = next(self.responses)
        if isinstance(item, Exception):
            raise item
        return item


def request():
    return DecisionRequest(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=({"role": "user", "content": "Return OK"},),
    )


def test_adapter_normalizes_text_usage_latency_and_never_exposes_key():
    transport = FakeTransport([FakeResponse(200, {
        "model": "nvidia/nemotron-3-super-120b-a12b",
        "choices": [{"message": {"content": "OK"}}],
        "usage": {"prompt_tokens": 5, "completion_tokens": 2},
    })])
    client = NebiusClient(api_key="top-secret", transport=transport, clock_ns=iter([0, 2_000_000]).__next__)

    response = client.decide(request())

    assert response.text == "OK"
    assert response.usage.total_tokens == 7
    assert response.latency_ms == 2
    assert "top-secret" not in repr(response)
    assert transport.calls[0][1]["Authorization"] == "Bearer top-secret"


def test_adapter_retries_transient_error_but_is_bounded():
    transport = FakeTransport([
        FakeResponse(503, {"error": "busy"}),
        FakeResponse(200, {"model": "m", "choices": [{"message": {"content": "OK"}}]}),
    ])
    client = NebiusClient(api_key="secret", transport=transport, max_retries=1)
    assert client.decide(request()).text == "OK"
    assert len(transport.calls) == 2


def test_adapter_does_not_retry_auth_failure():
    transport = FakeTransport([FakeResponse(401, {"error": "bad key"})])
    client = NebiusClient(api_key="secret", transport=transport, max_retries=3)
    with pytest.raises(ProviderError, match="401"):
        client.decide(request())
    assert len(transport.calls) == 1
