import pytest

from services.validator.evidence_chain import EvidenceChain


def test_usage_token_metrics_are_allowed():
    chain = EvidenceChain("r1")
    event = chain.append("inference", {"input_tokens": 10, "output_tokens": 4, "total_tokens": 14})
    assert event["observed"]["total_tokens"] == 14


@pytest.mark.parametrize("key", ["token", "access_token", "refresh_token", "api_key", "authorization", "private_key", "password", "client_secret"])
def test_actual_secret_fields_are_rejected(key):
    with pytest.raises(ValueError, match="secret-like"):
        EvidenceChain("r1").append("bad", {key: "secret"})
