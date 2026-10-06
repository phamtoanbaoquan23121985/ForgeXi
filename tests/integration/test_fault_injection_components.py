import socket
import urllib.error

import pytest

from services.resilience.engine import RecoveryEngine
from services.resilience.policy import ErrorClass, RecoveryPolicy
from services.resilience.retry_budget import RetryBudget
from services.validator.evidence_chain import EvidenceChain


@pytest.mark.parametrize("fault", [socket.gaierror("dns"), ConnectionResetError("reset"), TimeoutError("timeout"), urllib.error.URLError("network")])
def test_network_faults_recover_within_budget(fault):
    calls=[0]
    def op():
        calls[0]+=1
        if calls[0] == 1: raise fault
        return "ok"
    engine=RecoveryEngine(RecoveryPolicy(max_retries=2),RetryBudget(capacity=2),sleeper=lambda _:None)
    assert engine.run(op,classify=lambda e: ErrorClass.TRANSIENT) == "ok"
    assert calls[0] == 2


def test_corrupted_evidence_is_detected_and_never_recovered_as_valid():
    chain=EvidenceChain("fault")
    chain.append("test",{"status":"ok"})
    document=chain.document()
    document["events"][0]["observed"]["status"]="forged"
    assert EvidenceChain.verify(document) is False


def test_auth_fault_fails_closed_without_retry():
    calls=[0]
    def op():
        calls[0]+=1
        raise PermissionError("expired credential")
    engine=RecoveryEngine(RecoveryPolicy(max_retries=4),RetryBudget(capacity=4),sleeper=lambda _:None)
    with pytest.raises(PermissionError):
        engine.run(op,classify=lambda e: ErrorClass.AUTH)
    assert calls[0] == 1
