import json

from tools.repo_executor import CommandPolicy, RepoExecutor


def test_malformed_json_is_detected_not_silently_accepted():
    malformed='{"tool":"run_test"'
    try:
        json.loads(malformed)
        accepted=True
    except json.JSONDecodeError:
        accepted=False
    assert accepted is False


def test_truncated_model_output_is_detected_not_silently_accepted():
    truncated='{"action":"repair","args":{"path":"x.py"}'
    try:
        json.loads(truncated)
        accepted=True
    except json.JSONDecodeError:
        accepted=False
    assert accepted is False


def test_real_subprocess_timeout_is_observed(tmp_path):
    executor=RepoExecutor(tmp_path,CommandPolicy(allowed_programs={"python3"},timeout_seconds=0.05))
    result=executor.run(["python3","-c","import time; time.sleep(1)"])
    assert result.timed_out is True
    assert result.exit_code is None


def test_real_subprocess_crash_is_observed(tmp_path):
    executor=RepoExecutor(tmp_path,CommandPolicy(allowed_programs={"python3"}))
    result=executor.run(["python3","-c","raise SystemExit(17)"])
    assert result.timed_out is False
    assert result.exit_code == 17
