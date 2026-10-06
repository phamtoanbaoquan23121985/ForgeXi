from services.runtime.model_probe import ModelProbe
from services.runtime.auth_negotiation import AuthMode


class Credential:
    value = "secret-value"
class Credentials:
    def get(self): return Credential()
class Transport:
    def get_json(self, url, headers, timeout):
        assert headers["Authorization"] == "Bearer secret-value"
        return type("R", (), {"status":200, "payload":{"data":[{"id":"nvidia/nemotron"}]}})()


def test_probe_binds_requested_model_without_exposing_credential():
    result = ModelProbe(Transport(), Credentials(), "https://example/v1", AuthMode.TOKEN_FACTORY, clock_ns=iter([0, 7_000_000]).__next__).probe("nvidia/nemotron")
    assert result.status == "ok"
    assert result.model == "nvidia/nemotron"
    assert result.latency_ms == 7
    assert "secret-value" not in repr(result)


def test_probe_reports_model_missing():
    class Empty(Transport):
        def get_json(self, url, headers, timeout):
            return type("R", (), {"status":200, "payload":{"data":[]}})()
    result = ModelProbe(Empty(), Credentials(), "https://example/v1", AuthMode.TOKEN_FACTORY).probe("nvidia/nemotron")
    assert result.status == "model_unavailable"
