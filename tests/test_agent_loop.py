from forgexi.core import AgentLoop, AgentState, StepResult
from forgexi.evidence import EvidenceLedger


def test_agent_starts_in_plan_and_reaches_verified_after_successful_test():
    ledger = EvidenceLedger(run_id="run-001")
    agent = AgentLoop(ledger=ledger)

    assert agent.state is AgentState.PLAN

    agent.advance(StepResult.ok("plan", {"tasks": ["inspect"]}))
    assert agent.state is AgentState.INSPECT

    agent.advance(StepResult.ok("inspect", {"files": ["src/app.py"]}))
    assert agent.state is AgentState.ACT

    agent.advance(StepResult.ok("act", {"patch": "example"}))
    assert agent.state is AgentState.TEST

    agent.advance(StepResult.ok("test", {"exit_code": 0}))
    assert agent.state is AgentState.VERIFY

    agent.advance(StepResult.ok("verify", {"tests_passed": 1}))
    assert agent.state is AgentState.DONE
    assert ledger.events[-1].phase == "verify"


def test_failed_test_routes_to_diagnose_then_repair_then_retest():
    ledger = EvidenceLedger(run_id="run-002")
    agent = AgentLoop(ledger=ledger)
    for phase in ("plan", "inspect", "act"):
        agent.advance(StepResult.ok(phase, {}))

    agent.advance(StepResult.fail("test", {"exit_code": 1}))
    assert agent.state is AgentState.DIAGNOSE

    agent.advance(StepResult.ok("diagnose", {"cause": "regression"}))
    assert agent.state is AgentState.REPAIR

    agent.advance(StepResult.ok("repair", {"patch": "fix"}))
    assert agent.state is AgentState.TEST


def test_evidence_ledger_is_deterministic_and_refuses_unmeasured_metrics():
    ledger = EvidenceLedger(run_id="run-003")
    ledger.record("test", True, {"exit_code": 0})
    scorecard = ledger.scorecard()

    assert scorecard["run_id"] == "run-003"
    assert scorecard["events"][0]["phase"] == "test"
    assert "quality_score" not in scorecard
