from services.resilience.engine import RecoveryEngine
from services.resilience.policy import ErrorClass, RecoveryPolicy
from services.resilience.retry_budget import RetryBudget


def test_transient_recovers_then_returns_value():
    calls=[RuntimeError("temporary"), "ok"]
    engine=RecoveryEngine(RecoveryPolicy(max_retries=2), RetryBudget(capacity=4), sleeper=lambda _:None)
    assert engine.run(lambda: calls.pop(0), classify=lambda e: ErrorClass.TRANSIENT) == "ok"


def test_auth_error_is_never_retried():
    count=[0]
    def operation():
        count[0]+=1
        raise PermissionError("auth")
    engine=RecoveryEngine(RecoveryPolicy(max_retries=5), RetryBudget(capacity=10), sleeper=lambda _:None)
    try: engine.run(operation, classify=lambda e: ErrorClass.AUTH)
    except PermissionError: pass
    assert count[0] == 1


def test_retry_budget_exhaustion_stops_operation():
    count=[0]
    def operation():
        count[0]+=1
        raise RuntimeError("down")
    engine=RecoveryEngine(RecoveryPolicy(max_retries=5), RetryBudget(capacity=1), sleeper=lambda _:None)
    try: engine.run(operation, classify=lambda e: ErrorClass.TRANSIENT)
    except RuntimeError: pass
    assert count[0] == 2
