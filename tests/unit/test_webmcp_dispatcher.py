import pytest

from services.webmcp.dispatcher import WebMCPDispatcher


class Domain:
    def probe_models(self): return {"status":"ok","models":["nvidia/model"]}
    def run_nemotron_decision(self, prompt): return {"model":"nvidia/model","text":"ok"}
    def run_forgexi_task(self, task, max_repairs): return {"run_id":"r1","status":"running"}
    def get_run_status(self, run_id): return {"run_id":run_id,"status":"verified"}
    def get_evidence_receipt(self, run_id): return {"run_id":run_id,"final_hash":"abc"}


def test_dispatcher_exposes_only_named_domain_operations():
    d = WebMCPDispatcher(Domain())
    assert d.invoke("probe_models", {})["status"] == "ok"
    assert d.invoke("run_forgexi_task", {"task":"fix test","max_repairs":1})["run_id"] == "r1"
    with pytest.raises(ValueError, match="unknown WebMCP tool"):
        d.invoke("shell", {"command":"id"})


def test_dispatcher_rejects_secret_result():
    class Bad(Domain):
        def probe_models(self): return {"authorization":"Bearer nope"}
    with pytest.raises(ValueError, match="unsafe"):
        WebMCPDispatcher(Bad()).invoke("probe_models", {})
