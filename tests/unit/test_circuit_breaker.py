from services.resilience.circuit_breaker import CircuitBreaker


def test_breaker_opens_after_threshold_and_recovers_after_cooldown():
    now=[0.0]
    breaker=CircuitBreaker(failure_threshold=2,recovery_seconds=10,clock=lambda:now[0])
    assert breaker.allow()
    breaker.failure(); breaker.failure()
    assert not breaker.allow()
    now[0]=11.0
    assert breaker.allow()
    breaker.success()
    assert breaker.allow()
