from tools.evb_receipt import build_evb_receipt


def test_receipt_binds_manifest_and_hardening_receipt():
    r=build_evb_receipt(source_sha="abc",manifest_sha256="1"*64,source_verified=True,
        hardening={"decision":"HARDENED","receipt_sha256":"2"*64},verifier="chatgpt-ephemeral")
    assert r["decision"]=="HARDENED"
    assert len(r["receipt_sha256"])==64


def test_unverified_source_overrides_hardening_claim():
    r=build_evb_receipt(source_sha="abc",manifest_sha256="1"*64,source_verified=False,
        hardening={"decision":"HARDENED","receipt_sha256":"2"*64},verifier="chatgpt-ephemeral")
    assert r["decision"]=="UNVERIFIED"
