import pytest

from benchmarks.metrics import RunResult, paired_results


def run(arm: str, *, seed: int = 7) -> RunResult:
    return RunResult(
        arm=arm,
        task_id="fixture-001",
        base_sha="abc123",
        seed=seed,
        wall_time_seconds=60,
        verified=arm == "forgexi",
    )


def test_accepts_exactly_matched_pair():
    pairs = paired_results([run("forgexi"), run("baseline")])
    assert len(pairs) == 1
    assert pairs[0][0].arm == "baseline"
    assert pairs[0][1].arm == "forgexi"


def test_rejects_missing_arm():
    with pytest.raises(ValueError, match="incomplete benchmark pair"):
        paired_results([run("forgexi")])


def test_rejects_mismatched_seed_instead_of_comparing_unfairly():
    with pytest.raises(ValueError, match="incomplete benchmark pair"):
        paired_results([run("baseline", seed=7), run("forgexi", seed=8)])


def test_rejects_duplicate_arm():
    with pytest.raises(ValueError, match="duplicate arm"):
        paired_results([run("baseline"), run("baseline"), run("forgexi")])
