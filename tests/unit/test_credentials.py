import pytest

from services.runtime.credentials import (
    BearerCredential,
    EnvironmentCredentialProvider,
    ExpiringCredentialProvider,
)


class Clock:
    def __init__(self, now=1000):
        self.now = now
    def __call__(self):
        return self.now


def test_environment_provider_reads_at_resolution_time(monkeypatch):
    monkeypatch.setenv("NEBIUS_API_KEY", "secret-a")
    provider = EnvironmentCredentialProvider("NEBIUS_API_KEY")
    assert provider.get().value == "secret-a"
    monkeypatch.setenv("NEBIUS_API_KEY", "secret-b")
    assert provider.get().value == "secret-b"


def test_expiring_provider_refreshes_before_expiry():
    clock = Clock()
    calls = []
    def mint():
        calls.append(1)
        return BearerCredential("ephemeral", expires_at=clock.now + 60)
    provider = ExpiringCredentialProvider(mint, refresh_skew_seconds=10, clock=clock)
    assert provider.get().value == "ephemeral"
    assert len(calls) == 1
    clock.now = 1051
    provider.get()
    assert len(calls) == 2


def test_credential_repr_never_contains_value():
    credential = BearerCredential("do-not-print", expires_at=1234)
    assert "do-not-print" not in repr(credential)


def test_empty_credential_is_rejected():
    with pytest.raises(ValueError):
        BearerCredential("")
