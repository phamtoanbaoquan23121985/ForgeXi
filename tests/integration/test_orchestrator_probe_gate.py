import pytest

from services.orchestrator.runtime_gate import RuntimeGate
from services.runtime.auth_negotiation import AuthMode
from services.runtime.capability_probe import ProbeResult
from services.validator.evidence_chain import EvidenceChain


def test_failed_probe_blocks_runtime_action_and_is_recorded():
    called = []
    gate = RuntimeGate(EvidenceChain("run-1"))
    probe = ProbeResult(AuthMode.IAM, "nvidia/model", "models", "failed", 5)

    with pytest.raises(RuntimeError, match="capability probe failed"):
        gate.require(probe, lambda: called.append(True))

    assert called == []
    doc = gate.evidence.document()
    assert doc["events"][0]["kind"] == "capability_probe"
    assert doc["events"][0]["observed"]["status"] == "failed"


def test_successful_probe_allows_runtime_action():
    called = []
    gate = RuntimeGate(EvidenceChain("run-2"))
    probe = ProbeResult(AuthMode.IAM, "nvidia/model", "models", "ok", 5)
    assert gate.require(probe, lambda: called.append(True) or "done") == "done"
    assert called == [True]
