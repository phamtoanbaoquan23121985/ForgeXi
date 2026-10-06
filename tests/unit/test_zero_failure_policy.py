from tools.hardening_verifier import build_scorecard, exit_code


BASE=dict(source_sha="abc",verifier="test",pytest_exit_code=0,
 tests={"passed":10,"failed":0,"skipped":0},
 fault_metrics={"recoverable_cases":1,"recovered_cases":1,"recovery_rate":1.0,
 "unrecoverable_cases":1,"unrecoverable_detected":1,"secret_leaks":0})


def test_zero_failure_policy_accepts_clean_run():
    assert build_scorecard(**BASE)["decision"]=="HARDENED"


def test_skip_is_not_clean():
    x={**BASE,"tests":{**BASE["tests"],"skipped":1}}
    assert build_scorecard(**x)["decision"]=="NOT_HARDENED"


def test_xfail_is_not_clean():
    x={**BASE,"tests":{**BASE["tests"],"xfailed":1}}
    assert build_scorecard(**x)["decision"]=="NOT_HARDENED"


def test_zero_collected_tests_is_not_clean():
    x={**BASE,"tests":{"passed":0,"failed":0,"skipped":0}}
    assert build_scorecard(**x)["decision"]=="NOT_HARDENED"
