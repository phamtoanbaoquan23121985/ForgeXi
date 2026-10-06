from services.resilience.fault_campaign import FaultCase, FaultCampaign, aggregate_metrics


def test_campaign_measures_recovery_and_unrecoverable_outcomes():
    clock=[0]
    def now():
        clock[0]+=1_000_000
        return clock[0]

    cases=[
        FaultCase("dns_failure", True, failures=1),
        FaultCase("connection_reset", True, failures=1),
        FaultCase("timeout", True, failures=1),
        FaultCase("http_429", True, failures=2),
        FaultCase("http_503", True, failures=1),
        FaultCase("malformed_json", True, failures=1),
        FaultCase("truncated_output", True, failures=1),
        FaultCase("subprocess_hang", True, failures=1),
        FaultCase("subprocess_crash", True, failures=1),
        FaultCase("test_failure", True, failures=1),
        FaultCase("corrupted_evidence", False, failures=1),
        FaultCase("expired_credential", True, failures=1),
    ]
    results=FaultCampaign(clock_ns=now).run(cases)
    metrics=aggregate_metrics(results)
    assert metrics["cases"] == 12
    assert metrics["recoverable_cases"] == 11
    assert metrics["recovered_cases"] == 11
    assert metrics["unrecoverable_cases"] == 1
    assert metrics["recovery_rate"] == 1.0
    assert metrics["unrecoverable_rate"] == 1/12
    assert metrics["retries"] == sum(c.failures for c in cases if c.recoverable)


def test_campaign_does_not_convert_tamper_detection_into_success():
    result=FaultCampaign().run([FaultCase("corrupted_evidence", False, failures=1)])[0]
    assert result.recovered is False
    assert result.status == "fail_closed"
    assert result.retries == 0
