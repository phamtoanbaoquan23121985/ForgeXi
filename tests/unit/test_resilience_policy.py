import pytest

from services.resilience.policy import ErrorClass, classify_error, RecoveryPolicy


@pytest.mark.parametrize(("status","expected"), [(408,ErrorClass.TRANSIENT),(429,ErrorClass.THROTTLED),(500,ErrorClass.TRANSIENT),(503,ErrorClass.TRANSIENT),(401,ErrorClass.AUTH),(403,ErrorClass.AUTH),(400,ErrorClass.FATAL)])
def test_http_errors_are_classified(status, expected):
    assert classify_error(http_status=status) is expected


def test_auth_and_policy_fail_closed_without_retry():
    policy = RecoveryPolicy()
    assert policy.action_for(ErrorClass.AUTH).kind == "fail_closed"
    assert policy.action_for(ErrorClass.POLICY).kind == "fail_closed"


def test_transient_fault_uses_bounded_retry_not_infinite_retry():
    action = RecoveryPolicy(max_retries=3).action_for(ErrorClass.TRANSIENT)
    assert action.kind == "retry"
    assert action.max_attempts == 3


def test_verification_failure_routes_to_repair():
    assert RecoveryPolicy().action_for(ErrorClass.VERIFICATION).kind == "repair"
