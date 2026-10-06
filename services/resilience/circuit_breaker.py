"""Small deterministic circuit breaker for dependency isolation."""


class CircuitBreaker:
    def __init__(self, *, failure_threshold=3, recovery_seconds=30.0, clock):
        if failure_threshold < 1 or recovery_seconds <= 0: raise ValueError("invalid breaker configuration")
        self.threshold=failure_threshold; self.recovery_seconds=recovery_seconds; self.clock=clock
        self.failures=0; self.opened_at=None

    def allow(self):
        if self.opened_at is None: return True
        return self.clock()-self.opened_at >= self.recovery_seconds

    def failure(self):
        self.failures += 1
        if self.failures >= self.threshold and self.opened_at is None:
            self.opened_at=self.clock()

    def success(self):
        self.failures=0; self.opened_at=None
