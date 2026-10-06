# ForgeXi Resilience Layer

ForgeXi recovers from operational faults; it does not bypass trust or verification boundaries.

## Error classes

- transient/network/5xx: bounded exponential retry
- throttling: bounded retry; provider retry hints should take precedence when available
- dependency failure: circuit breaker + bulkhead/fallback path
- malformed model output: schema repair/re-prompt within a fixed budget
- execution failure: diagnose/repair/rollback
- verification failure: repair/retest within the task budget
- auth (401/403): fail closed
- policy/sandbox violation: fail closed
- fatal/invalid request: fail closed

Every retry consumes a retry budget. Repeated dependency failures open a circuit rather than creating a retry storm. Recovery never changes a failed verification into success; only a new observed verification event may do that.

Planned fault-injection matrix includes timeout, DNS failure, 429, 5xx, malformed JSON, truncated model output, subprocess timeout, non-zero exit, test failure, evidence tamper, missing credential, expired credential, and deployment dependency outage.
