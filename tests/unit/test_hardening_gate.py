from services.resilience.fault_campaign import hardening_gate


def test_hardening_requires_full_recovery_and_fail_closed_detection():
    metrics={"recoverable_cases":11,"recovered_cases":11,"recovery_rate":1.0,"unrecoverable_cases":1,"unrecoverable_detected":1,"secret_leaks":0}
    assert hardening_gate(metrics)["hardened"] is True


def test_hardening_rejects_secret_leak_or_missed_recovery():
    assert hardening_gate({"recoverable_cases":1,"recovered_cases":0,"recovery_rate":0.0,"unrecoverable_cases":1,"unrecoverable_detected":1,"secret_leaks":0})["hardened"] is False
    assert hardening_gate({"recoverable_cases":1,"recovered_cases":1,"recovery_rate":1.0,"unrecoverable_cases":1,"unrecoverable_detected":1,"secret_leaks":1})["hardened"] is False
