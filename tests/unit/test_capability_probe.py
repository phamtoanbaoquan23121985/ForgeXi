from services.runtime.auth_negotiation import AuthMode
from services.runtime.capability_probe import ProbeResult, evidence_fields


def test_probe_evidence_is_strictly_whitelisted():
    result = ProbeResult(
        auth_mode=AuthMode.IAM,
        model="nvidia/model",
        endpoint_capability="models",
        status="ok",
        latency_ms=12,
    )
    assert evidence_fields(result) == {
        "auth_mode": "iam",
        "model": "nvidia/model",
        "endpoint_capability": "models",
        "status": "ok",
        "latency_ms": 12,
    }


def test_probe_result_cannot_carry_credentials():
    assert "credential" not in ProbeResult.__dataclass_fields__
    assert "headers" not in ProbeResult.__dataclass_fields__
