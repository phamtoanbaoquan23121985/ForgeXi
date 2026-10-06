"""Typed recovery policy: recover faults without bypassing trust boundaries."""

from dataclasses import dataclass
from enum import Enum


class ErrorClass(str, Enum):
    TRANSIENT="transient"
    THROTTLED="throttled"
    AUTH="auth"
    POLICY="policy"
    MODEL_OUTPUT="model_output"
    EXECUTION="execution"
    VERIFICATION="verification"
    DEPENDENCY="dependency"
    FATAL="fatal"


@dataclass(frozen=True)
class RecoveryAction:
    kind: str
    max_attempts: int = 0


def classify_error(*, http_status: int | None = None, kind: str | None = None) -> ErrorClass:
    if kind:
        try:
            return ErrorClass(kind)
        except ValueError:
            return ErrorClass.FATAL
    if http_status in {401,403}: return ErrorClass.AUTH
    if http_status == 429: return ErrorClass.THROTTLED
    if http_status in {408,500,502,503,504}: return ErrorClass.TRANSIENT
    return ErrorClass.FATAL


class RecoveryPolicy:
    def __init__(self, *, max_retries: int=2):
        if not 0 <= max_retries <= 5:
            raise ValueError("max_retries must be between 0 and 5")
        self.max_retries=max_retries

    def action_for(self, error: ErrorClass) -> RecoveryAction:
        if error in {ErrorClass.AUTH,ErrorClass.POLICY,ErrorClass.FATAL}:
            return RecoveryAction("fail_closed")
        if error in {ErrorClass.TRANSIENT,ErrorClass.THROTTLED,ErrorClass.DEPENDENCY}:
            return RecoveryAction("retry",self.max_retries)
        if error in {ErrorClass.MODEL_OUTPUT,ErrorClass.EXECUTION,ErrorClass.VERIFICATION}:
            return RecoveryAction("repair",2)
        return RecoveryAction("fail_closed")
