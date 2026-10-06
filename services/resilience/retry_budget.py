"""Aggregate retry budget prevents retry amplification."""


class RetryBudget:
    def __init__(self, *, capacity: int):
        if capacity < 0: raise ValueError("capacity must be nonnegative")
        self.capacity=capacity
        self.used=0

    def take(self) -> bool:
        if self.used >= self.capacity: return False
        self.used += 1
        return True
