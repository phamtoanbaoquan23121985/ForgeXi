"""Canonical tamper-evident evidence chain."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Mapping


_FORBIDDEN_KEY_PARTS = ("api_key", "authorization", "password", "secret", "token")
_GENESIS = "0" * 64


def _canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _reject_secrets(value, path="root") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            lowered = str(key).lower()
            if any(part in lowered for part in _FORBIDDEN_KEY_PARTS):
                raise ValueError(f"secret-like evidence field rejected at {path}.{key}")
            _reject_secrets(child, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_secrets(child, f"{path}[{index}]")


class EvidenceChain:
    def __init__(self, run_id: str):
        if not run_id.strip():
            raise ValueError("run_id must be non-empty")
        self.run_id = run_id
        self._events: list[dict] = []

    def append(self, kind: str, observed: Mapping[str, object]) -> dict:
        if not kind.strip():
            raise ValueError("kind must be non-empty")
        _reject_secrets(observed)
        previous = self._events[-1]["hash"] if self._events else _GENESIS
        body = {
            "sequence": len(self._events),
            "kind": kind,
            "previous_hash": previous,
            "observed": deepcopy(dict(observed)),
        }
        event_hash = hashlib.sha256(_canonical(body)).hexdigest()
        event = {**body, "hash": event_hash}
        self._events.append(event)
        return deepcopy(event)

    def document(self) -> dict:
        return {
            "schema_version": "1.0",
            "run_id": self.run_id,
            "hash_algorithm": "sha256",
            "events": deepcopy(self._events),
        }

    @staticmethod
    def verify(document: Mapping[str, object]) -> bool:
        try:
            previous = _GENESIS
            for expected_sequence, event in enumerate(document["events"]):
                if event["sequence"] != expected_sequence or event["previous_hash"] != previous:
                    return False
                body = {
                    "sequence": event["sequence"],
                    "kind": event["kind"],
                    "previous_hash": event["previous_hash"],
                    "observed": event["observed"],
                }
                digest = hashlib.sha256(_canonical(body)).hexdigest()
                if digest != event["hash"]:
                    return False
                previous = digest
            return True
        except (KeyError, TypeError):
            return False
