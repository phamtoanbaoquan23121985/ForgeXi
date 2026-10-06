"""Bounded, workspace-confined subprocess execution."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Sequence


@dataclass(frozen=True)
class CommandPolicy:
    allowed_programs: set[str]
    timeout_seconds: float = 30.0
    max_output_bytes: int = 64 * 1024
    safe_environment: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.max_output_bytes <= 0:
            raise ValueError("max_output_bytes must be positive")


@dataclass(frozen=True)
class ExecutionResult:
    argv: tuple[str, ...]
    exit_code: int | None
    stdout: str
    stderr: str
    timed_out: bool
    stdout_truncated: bool
    stderr_truncated: bool


class RepoExecutor:
    def __init__(self, workspace: str | os.PathLike[str], policy: CommandPolicy):
        self.workspace = Path(workspace).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.policy = policy

    def _cwd(self, cwd) -> Path:
        target = self.workspace if cwd is None else Path(cwd).resolve()
        try:
            target.relative_to(self.workspace)
        except ValueError as exc:
            raise PermissionError("working directory escapes workspace") from exc
        return target

    def _environment(self) -> dict[str, str]:
        env = {}
        for key in ("PATH", "HOME", "TMPDIR", "LANG", "LC_ALL", "SYSTEMROOT"):
            value = os.environ.get(key)
            if value is not None:
                env[key] = value
        env.update({str(k): str(v) for k, v in self.policy.safe_environment.items()})
        return env

    def run(self, argv: Sequence[str], *, cwd=None) -> ExecutionResult:
        if not argv:
            raise ValueError("argv must be non-empty")
        program = str(argv[0])
        if program not in self.policy.allowed_programs:
            raise PermissionError(f"program not allowed: {program}")
        target = self._cwd(cwd)
        try:
            proc = subprocess.run(list(argv), cwd=target, env=self._environment(), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=self.policy.timeout_seconds, check=False, shell=False)
            out, out_cut = _bounded(proc.stdout, self.policy.max_output_bytes)
            err, err_cut = _bounded(proc.stderr, self.policy.max_output_bytes)
            return ExecutionResult(tuple(argv), proc.returncode, out, err, False, out_cut, err_cut)
        except subprocess.TimeoutExpired as exc:
            out, out_cut = _bounded(exc.stdout or b"", self.policy.max_output_bytes)
            err, err_cut = _bounded(exc.stderr or b"", self.policy.max_output_bytes)
            return ExecutionResult(tuple(argv), None, out, err, True, out_cut, err_cut)


def _bounded(value: bytes | str, limit: int) -> tuple[str, bool]:
    raw = value if isinstance(value, bytes) else value.encode()
    cut = len(raw) > limit
    return raw[:limit].decode("utf-8", errors="replace"), cut
