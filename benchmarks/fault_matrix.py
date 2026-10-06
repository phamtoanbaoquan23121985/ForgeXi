"""Canonical ForgeXi hardening fault matrix.

Expected outcome is explicit: recover means retry/refresh/repair followed by a
new observed success; fail_closed means the unsafe state must never be promoted
to success.
"""

FAULT_MATRIX = (
    ("dns_failure", "recover"),
    ("connection_reset", "recover"),
    ("timeout", "recover"),
    ("http_429", "recover"),
    ("http_5xx", "recover"),
    ("malformed_json", "repair"),
    ("truncated_nemotron_output", "repair"),
    ("subprocess_hang", "recover"),
    ("subprocess_crash", "repair"),
    ("test_failure", "repair"),
    ("corrupted_evidence", "fail_closed"),
    ("expired_credential", "refresh_or_fail_closed"),
)
