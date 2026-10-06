"""Capability-driven runtime construction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

from .auth_negotiation import AuthCapability, AuthMode, AuthNegotiator


@dataclass(frozen=True)
class EndpointProfile:
    name: str
    base_url: str
    capabilities: FrozenSet[AuthCapability]

    def __post_init__(self):
        if not self.name.strip() or not self.base_url.strip():
            raise ValueError("endpoint name and base_url must be non-empty")


@dataclass(frozen=True)
class RuntimeBinding:
    profile: EndpointProfile
    auth_mode: AuthMode
    credential_provider: object


class RuntimeFactory:
    def __init__(self, *, iam_provider=None, token_factory_provider=None, static_provider=None):
        self._providers = {
            AuthMode.IAM: iam_provider,
            AuthMode.TOKEN_FACTORY: token_factory_provider,
            AuthMode.STATIC: static_provider,
        }

    def build(self, profile: EndpointProfile) -> RuntimeBinding:
        mode = AuthNegotiator().select(set(profile.capabilities))
        provider = self._providers[mode]
        if provider is None:
            raise RuntimeError(f"credential provider unavailable for selected auth mode: {mode.value}")
        return RuntimeBinding(profile, mode, provider)
