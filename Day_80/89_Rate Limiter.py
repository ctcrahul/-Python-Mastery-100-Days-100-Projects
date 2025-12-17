"""
Project 89 — Rate Limiter (Token Bucket + Sliding Window)

Features:
- Token Bucket for steady traffic
- Sliding Window for burst control
- Thread-safe
"""

import time
import threading
from collections import deque, defaultdict


class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate              # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def allow(self, tokens=1):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            refill = elapsed * self.rate
            self.tokens = min(self.capacity, self.tokens + refill)
            self.last_refill = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
