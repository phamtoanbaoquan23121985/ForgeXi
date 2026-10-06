from services.orchestrator.closed_loop import ClosedLoop, Verification


class Decisions:
    def __init__(self): self.calls = []
    def decide(self, phase, task, failure=None):
        self.calls.append(phase)
        return {"summary": phase}


class Work:
    def __init__(self, test_results): self.test_results = iter(test_results); self.repairs = 0
    def act(self, decision): return {"changed": True}
    def test(self): return next(self.test_results)
    def repair(self, decision): self.repairs += 1; return {"changed": True}
    def verify(self): return Verification(True, "verified")


def test_success_path_finishes_without_repair():
    loop = ClosedLoop(Decisions(), Work([Verification(True, "tests pass")]), max_repairs=2)
    result = loop.run("fix bug")
    assert result.status == "verified"
    assert result.repairs == 0


def test_failure_diagnoses_repairs_retests_and_verifies():
    decisions = Decisions(); work = Work([Verification(False, "failed"), Verification(True, "passed")])
    result = ClosedLoop(decisions, work, max_repairs=2).run("fix bug")
    assert result.status == "verified"
    assert result.repairs == 1
    assert decisions.calls == ["plan", "diagnose", "repair"]


def test_repair_budget_exhaustion_never_reports_verified():
    result = ClosedLoop(Decisions(), Work([Verification(False, "x"), Verification(False, "x")]), max_repairs=1).run("fix")
    assert result.status == "failed"
