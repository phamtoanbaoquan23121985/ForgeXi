from services.runtime.credentials import BearerCredential
from services.runtime.nebius_client import NebiusClient
from services.runtime.protocol import DecisionRequest


class Provider:
    def get(self):
        return BearerCredential("short-lived")


class Response:
    status = 200
    def read(self):
        return b'{"model":"m","choices":[{"message":{"content":"OK"}}]}'


class Transport:
    def __init__(self):
        self.headers = None
    def post_json(self, url, headers, payload, timeout):
        self.headers = headers
        return Response()


def test_client_accepts_credential_provider_instead_of_owning_secret():
    transport = Transport()
    client = NebiusClient(credential_provider=Provider(), transport=transport)
    response = client.decide(DecisionRequest(model="m", messages=({"role":"user","content":"x"},)))
    assert response.text == "OK"
    assert transport.headers["Authorization"] == "Bearer short-lived"
    assert "short-lived" not in repr(client)
