from tools.repo_executor import CommandPolicy, RepoExecutor


def test_child_environment_does_not_inherit_nebius_secret(tmp_path, monkeypatch):
    monkeypatch.setenv("NEBIUS_API_KEY", "must-not-leak")
    executor = RepoExecutor(tmp_path, CommandPolicy(allowed_programs={"python3"}))
    result = executor.run(["python3", "-c", "import os; print(os.getenv('NEBIUS_API_KEY','missing'))"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "missing"


def test_child_gets_only_explicit_safe_environment(tmp_path):
    executor = RepoExecutor(tmp_path, CommandPolicy(allowed_programs={"python3"}, safe_environment={"FORGEXI_TEST":"yes"}))
    result = executor.run(["python3", "-c", "import os; print(os.getenv('FORGEXI_TEST','no'))"])
    assert result.stdout.strip() == "yes"
