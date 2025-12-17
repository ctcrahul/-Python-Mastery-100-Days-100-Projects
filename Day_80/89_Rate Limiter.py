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

class SlidingWindow:
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window = window_seconds
        self.events = deque()
        self.lock = threading.Lock()

    def allow(self):
        with self.lock:
            now = time.time()
            while self.events and self.events[0] <= now - self.window:
                self.events.popleft()

            if len(self.events) < self.limit:
                self.events.append(now)
                return True
            return False


class RateLimiter:
    def __init__(self, rate, capacity, window_limit, window_seconds):
        self.buckets = defaultdict(lambda: TokenBucket(rate, capacity))
        self.windows = defaultdict(lambda: SlidingWindow(window_limit, window_seconds))

    def allow(self, user_id):
        # both must allow
        return self.buckets[user_id].allow() and self.windows[user_id].allow()

