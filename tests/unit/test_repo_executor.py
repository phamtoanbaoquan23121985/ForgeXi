import sys

import pytest

from tools.repo_executor import CommandPolicy, RepoExecutor


def test_rejects_command_not_on_allowlist(tmp_path):
    executor = RepoExecutor(tmp_path, CommandPolicy(allowed_programs={"git"}))
    with pytest.raises(PermissionError):
        executor.run([sys.executable, "-c", "print('x')"])


def test_rejects_working_directory_escape(tmp_path):
    executor = RepoExecutor(tmp_path, CommandPolicy(allowed_programs={sys.executable}))
    with pytest.raises(PermissionError):
        executor.run([sys.executable, "-c", "print('x')"], cwd=tmp_path.parent)


def test_captures_exit_output_and_truncates(tmp_path):
    executor = RepoExecutor(
        tmp_path,
        CommandPolicy(allowed_programs={sys.executable}, max_output_bytes=4),
    )
    result = executor.run([sys.executable, "-c", "print('abcdef', end='')"])
    assert result.exit_code == 0
    assert result.stdout == "abcd"
    assert result.stdout_truncated is True


def test_timeout_is_observed_not_hidden(tmp_path):
    executor = RepoExecutor(
        tmp_path,
        CommandPolicy(allowed_programs={sys.executable}, timeout_seconds=0.05),
    )
    result = executor.run([sys.executable, "-c", "import time; time.sleep(1)"])
    assert result.timed_out is True
    assert result.exit_code is None
