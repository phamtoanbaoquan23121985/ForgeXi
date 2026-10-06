from services.resilience.retry_budget import RetryBudget


def test_retry_budget_prevents_retry_storm():
    budget=RetryBudget(capacity=2)
    assert budget.take()
    assert budget.take()
    assert not budget.take()
