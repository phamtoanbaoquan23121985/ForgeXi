import pytest

from services.runtime.protocol import DecisionRequest, DecisionResponse, TokenUsage


def test_request_rejects_empty_model_and_messages():
    with pytest.raises(ValueError):
        DecisionRequest(model="", messages=({"role": "user", "content": "x"},))
    with pytest.raises(ValueError):
        DecisionRequest(model="nvidia/model", messages=())


def test_response_requires_nonnegative_metrics():
    with pytest.raises(ValueError):
        DecisionResponse(text="x", model="m", latency_ms=-1, usage=TokenUsage(1, 1))


def test_usage_total_is_derived_not_claimed():
    usage = TokenUsage(input_tokens=7, output_tokens=3)
    assert usage.total_tokens == 10
