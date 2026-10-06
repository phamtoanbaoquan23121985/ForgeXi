import copy

from services.validator.evidence_chain import EvidenceChain


def test_chain_is_deterministic_and_verifiable():
    chain = EvidenceChain(run_id="run-1")
    chain.append("tool", {"argv": ["pytest"], "exit_code": 0})
    chain.append("verify", {"passed": True})
    document = chain.document()
    assert EvidenceChain.verify(document) is True
    assert document["events"][1]["previous_hash"] == document["events"][0]["hash"]


def test_tampering_breaks_verification():
    chain = EvidenceChain(run_id="run-1")
    chain.append("tool", {"exit_code": 0})
    document = copy.deepcopy(chain.document())
    document["events"][0]["observed"]["exit_code"] = 1
    assert EvidenceChain.verify(document) is False


def test_secret_like_fields_are_rejected():
    chain = EvidenceChain(run_id="run-1")
    try:
        chain.append("provider", {"api_key": "secret"})
    except ValueError as exc:
        assert "secret" in str(exc).lower()
    else:
        raise AssertionError("secret-like evidence key was accepted")
