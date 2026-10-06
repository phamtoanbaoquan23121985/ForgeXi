import hashlib
from tools.evb import build_manifest, verify_materialized_tree, evb_decision


def test_manifest_is_canonical_and_has_digest():
    m=build_manifest("abc",{"a.py":"00","b.py":"11"})
    assert m["source_sha"]=="abc"
    assert len(m["manifest_sha256"])==64


def test_tampered_materialized_file_is_unverified(tmp_path):
    p=tmp_path/"a.py";p.write_text("real")
    expected=hashlib.sha256(b"different").hexdigest()
    result=verify_materialized_tree(tmp_path,{"a.py":expected})
    assert result["verified"] is False
    assert result["mismatches"]==["a.py"]


def test_missing_file_is_unverified(tmp_path):
    result=verify_materialized_tree(tmp_path,{"missing.py":"0"*64})
    assert result["verified"] is False
    assert result["missing"]==["missing.py"]


def test_evb_never_hardens_unverified_source():
    assert evb_decision(source_verified=False,hardening_decision="HARDENED")=="UNVERIFIED"
    assert evb_decision(source_verified=True,hardening_decision="NOT_HARDENED")=="NOT_HARDENED"
    assert evb_decision(source_verified=True,hardening_decision="HARDENED")=="HARDENED"
