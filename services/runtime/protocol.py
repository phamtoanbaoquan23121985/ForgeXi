"""Provider-neutral inference contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol, Sequence


@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0

    def __post_init__(self) -> None:
        if self.input_tokens < 0 or self.output_tokens < 0:
            raise ValueError("token counts must be nonnegative")

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass(frozen=True)
class DecisionRequest:
    model: str
    messages: Sequence[Mapping[str, object]]
    temperature: float = 0.0

    def __post_init__(self) -> None:
        if not self.model.strip():
            raise ValueError("model must be non-empty")
        if not self.messages:
            raise ValueError("messages must be non-empty")


@dataclass(frozen=True)
class DecisionResponse:
    text: str
    model: str
    latency_ms: int
    usage: TokenUsage

    def __post_init__(self) -> None:
        if self.latency_ms < 0:
            raise ValueError("latency_ms must be nonnegative")


class DecisionProvider(Protocol):
    def decide(self, request: DecisionRequest) -> DecisionResponse: ...
