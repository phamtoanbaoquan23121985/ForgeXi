"""Tamper-evident EVB evidence envelope."""
from __future__ import annotations
import hashlib,json
from tools.evb import evb_decision


def build_evb_receipt(*,source_sha,manifest_sha256,source_verified,hardening,verifier):
    body={
      "schema":"forgexi.evb.receipt.v1",
      "source_sha":source_sha,
      "manifest_sha256":manifest_sha256,
      "source_verified":bool(source_verified),
      "hardening_receipt_sha256":hardening.get("receipt_sha256"),
      "verifier":verifier,
      "decision":evb_decision(source_verified=source_verified,hardening_decision=hardening.get("decision")),
    }
    body["receipt_sha256"]=hashlib.sha256(json.dumps(body,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return body
