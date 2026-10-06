import json

from tools.hardening_verifier import build_scorecard, exit_code


def test_scorecard_is_hardened_only_when_tests_and_fault_gate_pass():
    card=build_scorecard(source_sha="abc", verifier="test", pytest_exit_code=0,
        tests={"passed":42,"failed":0,"skipped":0},
        fault_metrics={"recoverable_cases":11,"recovered_cases":11,"recovery_rate":1.0,
        "unrecoverable_cases":1,"unrecoverable_detected":1,"unrecoverable_rate":1/12,
        "retries":12,"recovery_latency_ms":1.0,"secret_leaks":0})
    assert card["decision"]=="HARDENED"
    assert exit_code(card)==0
    assert card["receipt_sha256"]


def test_failed_test_forces_not_hardened():
    card=build_scorecard(source_sha="abc",verifier="test",pytest_exit_code=1,
        tests={"passed":41,"failed":1,"skipped":0},
        fault_metrics={"recoverable_cases":11,"recovered_cases":11,"recovery_rate":1.0,
        "unrecoverable_cases":1,"unrecoverable_detected":1,"secret_leaks":0})
    assert card["decision"]=="NOT_HARDENED"
    assert exit_code(card)==1


def test_receipt_is_deterministic_for_same_observations():
    kwargs=dict(source_sha="abc",verifier="test",pytest_exit_code=0,
        tests={"passed":1,"failed":0,"skipped":0},
        fault_metrics={"recoverable_cases":1,"recovered_cases":1,"recovery_rate":1.0,
        "unrecoverable_cases":1,"unrecoverable_detected":1,"secret_leaks":0})
    assert build_scorecard(**kwargs)["receipt_sha256"]==build_scorecard(**kwargs)["receipt_sha256"]
