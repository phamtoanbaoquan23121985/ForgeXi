"""ForgeXi Ephemeral Verification Bridge (EVB) provenance primitives."""
from __future__ import annotations
import hashlib,json
from pathlib import Path


def _digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def build_manifest(source_sha,files):
    body={"schema":"forgexi.evb.v1","source_sha":source_sha,"files":dict(sorted(files.items()))}
    body["manifest_sha256"]=_digest(body)
    return body


def verify_materialized_tree(root,files):
    root=Path(root);missing=[];mismatches=[]
    for rel,expected in sorted(files.items()):
        p=root/rel
        if not p.is_file(): missing.append(rel);continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=expected: mismatches.append(rel)
    return {"verified":not missing and not mismatches,"missing":missing,"mismatches":mismatches}


def evb_decision(*,source_verified,hardening_decision):
    if not source_verified:return "UNVERIFIED"
    return "HARDENED" if hardening_decision=="HARDENED" else "NOT_HARDENED"
