import pytest

from services.runtime.auth_negotiation import (
    AuthCapability,
    AuthMode,
    AuthNegotiator,
)


def test_ai_cloud_prefers_short_lived_iam():
    n = AuthNegotiator()
    assert n.select({AuthCapability.IAM_ACCESS_TOKEN, AuthCapability.STATIC_BEARER}) is AuthMode.IAM


def test_token_factory_uses_only_declared_supported_mode():
    n = AuthNegotiator()
    assert n.select({AuthCapability.TOKEN_FACTORY_API_KEY}) is AuthMode.TOKEN_FACTORY


def test_no_supported_auth_fails_closed():
    with pytest.raises(RuntimeError, match="no supported authentication"):
        AuthNegotiator().select(set())
