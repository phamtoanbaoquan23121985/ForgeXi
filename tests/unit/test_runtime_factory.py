import pytest

from services.runtime.auth_negotiation import AuthCapability, AuthMode
from services.runtime.runtime_factory import EndpointProfile, RuntimeFactory


class Provider:
    def __init__(self, value):
        self.value = value
    def get(self):
        return self.value


def test_factory_prefers_iam_when_endpoint_declares_it():
    profile = EndpointProfile(
        name="cloud-api",
        base_url="https://example.invalid/v1",
        capabilities=frozenset({AuthCapability.IAM_ACCESS_TOKEN, AuthCapability.STATIC_BEARER}),
    )
    runtime = RuntimeFactory(iam_provider=Provider("iam"), static_provider=Provider("static")).build(profile)
    assert runtime.auth_mode is AuthMode.IAM


def test_factory_refuses_missing_provider_for_selected_capability():
    profile = EndpointProfile(
        name="cloud-api",
        base_url="https://example.invalid/v1",
        capabilities=frozenset({AuthCapability.IAM_ACCESS_TOKEN}),
    )
    with pytest.raises(RuntimeError, match="credential provider"):
        RuntimeFactory().build(profile)
