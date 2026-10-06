from forgexi.evidence import EvidenceLedger


def test_scorecard_contains_only_observed_event_payloads():
    ledger = EvidenceLedger(run_id="run-evidence")
    ledger.record("verify", True, {"tests_passed": 7, "latency_ms": 12.5})
    card = ledger.scorecard()
    assert card == {
        "schema_version": "1.0",
        "run_id": "run-evidence",
        "events": [{
            "sequence": 0,
            "phase": "verify",
            "success": True,
            "observed": {"latency_ms": 12.5, "tests_passed": 7},
        }],
    }
