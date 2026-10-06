import pytest

from services.webmcp.contract import (
    TOOL_NAMES,
    sanitize_tool_result,
    validate_run_task,
)


def test_expected_tool_surface_is_exact():
    assert TOOL_NAMES == (
        "probe_models",
        "run_nemotron_decision",
        "run_forgexi_task",
        "get_run_status",
        "get_evidence_receipt",
    )


@pytest.mark.parametrize("payload", [
    {"authorization": "Bearer secret"},
    {"api_key": "secret"},
    {"headers": {"x": "y"}},
    {"access_token": "secret"},
])
def test_results_reject_secret_bearing_fields(payload):
    with pytest.raises(ValueError, match="unsafe"):
        sanitize_tool_result(payload)


def test_run_task_rejects_arbitrary_shell_or_url():
    with pytest.raises(ValueError):
        validate_run_task({"task": "fix bug", "shell": "rm -rf /"})
    with pytest.raises(ValueError):
        validate_run_task({"task": "fix bug", "url": "https://evil.invalid"})


def test_run_task_accepts_bounded_task():
    assert validate_run_task({"task": "fix failing unit test", "max_repairs": 2})["max_repairs"] == 2
