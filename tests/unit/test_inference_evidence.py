from services.runtime.protocol import DecisionResponse, TokenUsage
from services.validator.inference_receipt import inference_evidence


def test_inference_evidence_contains_metrics_and_digest_not_text():
    response = DecisionResponse("sensitive model output", "nvidia/model", 31, TokenUsage(10, 4))
    evidence = inference_evidence(response)
    assert evidence["input_tokens"] == 10
    assert evidence["output_tokens"] == 4
    assert evidence["total_tokens"] == 14
    assert evidence["latency_ms"] == 31
    assert len(evidence["response_digest"]) == 64
    assert "sensitive model output" not in repr(evidence)
