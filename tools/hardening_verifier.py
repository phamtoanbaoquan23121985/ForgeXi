"""Evidence-grade hardening scorecard builder."""

from __future__ import annotations
import hashlib
import json


def _gate(metrics):
    return (
        metrics.get("recoverable_cases",0)==metrics.get("recovered_cases",-1)
        and metrics.get("recovery_rate")==1.0
        and metrics.get("unrecoverable_cases",0)==metrics.get("unrecoverable_detected",-1)
        and metrics.get("secret_leaks")==0
    )


def build_scorecard(*,source_sha,verifier,pytest_exit_code,tests,fault_metrics):
    body={
        "schema":"forgexi.hardening.v1",
        "source_sha":source_sha,
        "verifier":verifier,
        "pytest_exit_code":pytest_exit_code,
        "tests":tests,
        "fault_metrics":fault_metrics,
    }
    body["decision"]="HARDENED" if pytest_exit_code==0 and tests.get("failed",0)==0 and _gate(fault_metrics) else "NOT_HARDENED"
    canonical=json.dumps(body,sort_keys=True,separators=(",",":")).encode()
    body["receipt_sha256"]=hashlib.sha256(canonical).hexdigest()
    return body


def exit_code(scorecard):
    return 0 if scorecard["decision"]=="HARDENED" else 1
