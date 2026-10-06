from services.runtime.auth_negotiation import AuthMode
from services.runtime.capability_probe import ProbeResult, record_probe
from services.validator.evidence_chain import EvidenceChain


def test_probe_records_tamper_evident_secret_free_receipt():
    chain = EvidenceChain("probe-1")
    record_probe(chain, ProbeResult(AuthMode.IAM, "nvidia/model", "models", "ok", 9))
    doc = chain.document()
    assert EvidenceChain.verify(doc)
    observed = doc["events"][0]["observed"]
    assert set(observed) == {"auth_mode", "model", "endpoint_capability", "status", "latency_ms"}
