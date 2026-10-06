"""Server-side validation and result sanitization for browser WebMCP tools."""

from __future__ import annotations

from collections.abc import Mapping

TOOL_NAMES = (
    "probe_models",
    "run_nemotron_decision",
    "run_forgexi_task",
    "get_run_status",
    "get_evidence_receipt",
)

_FORBIDDEN_KEYS = {
    "authorization", "api_key", "apikey", "access_token", "refresh_token",
    "private_key", "headers", "cookie", "set_cookie", "password", "secret",
}


def _unsafe_key(key: object) -> bool:
    normalized = str(key).lower().replace("-", "_")
    return normalized in _FORBIDDEN_KEYS or normalized.endswith("_secret")


def sanitize_tool_result(value):
    if isinstance(value, Mapping):
        for key, item in value.items():
            if _unsafe_key(key):
                raise ValueError(f"unsafe result field: {key}")
            sanitize_tool_result(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            sanitize_tool_result(item)
    return value


def validate_run_task(payload: Mapping[str, object]) -> dict[str, object]:
    allowed = {"task", "max_repairs"}
    if set(payload) - allowed:
        raise ValueError("unsupported run task input")
    task = payload.get("task")
    if not isinstance(task, str) or not task.strip() or len(task) > 4000:
        raise ValueError("task must be a non-empty string up to 4000 characters")
    repairs = payload.get("max_repairs", 2)
    if not isinstance(repairs, int) or isinstance(repairs, bool) or not 0 <= repairs <= 5:
        raise ValueError("max_repairs must be an integer from 0 to 5")
    return {"task": task.strip(), "max_repairs": repairs}
