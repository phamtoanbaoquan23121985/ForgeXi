"""Map browser tools to bounded ForgeXi domain operations."""

from __future__ import annotations

from .contract import sanitize_tool_result, validate_run_task


class WebMCPDispatcher:
    def __init__(self, domain):
        self._domain = domain

    def invoke(self, name: str, payload: dict):
        if name == "probe_models":
            if payload:
                raise ValueError("probe_models accepts no input")
            result = self._domain.probe_models()
        elif name == "run_nemotron_decision":
            if set(payload) != {"prompt"} or not isinstance(payload["prompt"], str) or not payload["prompt"].strip():
                raise ValueError("invalid decision input")
            result = self._domain.run_nemotron_decision(payload["prompt"].strip())
        elif name == "run_forgexi_task":
            args = validate_run_task(payload)
            result = self._domain.run_forgexi_task(**args)
        elif name in {"get_run_status", "get_evidence_receipt"}:
            if set(payload) != {"run_id"} or not isinstance(payload["run_id"], str) or not payload["run_id"].strip():
                raise ValueError("invalid run_id")
            method = getattr(self._domain, name)
            result = method(payload["run_id"].strip())
        else:
            raise ValueError(f"unknown WebMCP tool: {name}")
        return sanitize_tool_result(result)
