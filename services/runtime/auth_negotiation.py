"""Fail-closed authentication capability negotiation."""

from __future__ import annotations

from enum import Enum


class AuthCapability(str, Enum):
    IAM_ACCESS_TOKEN = "iam_access_token"
    TOKEN_FACTORY_API_KEY = "token_factory_api_key"
    STATIC_BEARER = "static_bearer"


class AuthMode(str, Enum):
    IAM = "iam"
    TOKEN_FACTORY = "token_factory"
    STATIC = "static"


class AuthNegotiator:
    _preference = (
        (AuthCapability.IAM_ACCESS_TOKEN, AuthMode.IAM),
        (AuthCapability.TOKEN_FACTORY_API_KEY, AuthMode.TOKEN_FACTORY),
        (AuthCapability.STATIC_BEARER, AuthMode.STATIC),
    )

    def select(self, capabilities: set[AuthCapability]) -> AuthMode:
        for capability, mode in self._preference:
            if capability in capabilities:
                return mode
        raise RuntimeError("no supported authentication capability")
