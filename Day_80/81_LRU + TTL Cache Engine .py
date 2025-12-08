"""
Project 81 — LRU + TTL Cache Engine (Thread-Safe)
A real in-memory cache with:
- GET / SET
- TTL expiration
- LRU eviction policy
- Hit/Miss counters
- Background cleaner thread
"""

import time
import threading


class Node:
    def __init__(self, key, value, expire_at):
        self.key = key
        self.value = value
        self.expire_at = expire_at
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity=5, cleanup_interval=2):
        self.capacity = capacity
        self.map = {}
        self.lock = threading.Lock()
        self.head = Node(None, None, None)
        self.tail = Node(None, None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.hits = 0
        self.misses = 0

        # Background cleanup
        self.cleanup_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True
        )
        self.cleanup_thread.start()
        self.cleanup_interval = cleanup_interval

    # -------------------------
    # Internal List Operations
    # -------------------------
    def _add_to_front(self, node):
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node
    def _remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def _move_to_front(self, node):
        self._remove(node)
        self._add_to_front(node)

    # -------------------------
    # Core Cache
    # -------------------------
    def set(self, key, value, ttl=None):
        with self.lock:
            expire_at = time.time() + ttl if ttl else None

            if key in self.map:
                node = self.map[key]
                node.value = value
                node.expire_at = expire_at
                self._move_to_front(node)
                return "OK"

            if len(self.map) >= self.capacity:
                # evict LRU
                lru = self.tail.prev
                self._remove(lru)
                del self.map[lru.key]

            node = Node(key, value, expire_at)
            self.map[key] = node
            self._add_to_front(node)

            return "OK"
   def get(self, key):
        with self.lock:
            if key not in self.map:
                self.misses += 1
                return None

            node = self.map[key]

            # TTL check
            if node.expire_at and node.expire_at < time.time():
                self._remove(node)
                del self.map[key]
                self.misses += 1
                return None

            # LRU update
            self._move_to_front(node)
            self.hits += 1
            return node.value

    # -------------------------
    # Background cleaner
    # -------------------------
    def _cleanup_loop(self):
        while True:
            time.sleep(self.cleanup_interval)
            now = time.time()

            with self.lock:
                expired = []
                for key, node in list(self.map.items()):
                    if node.expire_at and node.expire_at < now:
                        expired.append(key)
             for key in expired:
                    node = self.map[key]
                    self._remove(node)
                    del self.map[key]

    # -------------------------
    # Stats
    # -------------------------
    def stats(self):
        return {
            "count": len(self.map),
            "hits": self.hits,
            "misses": self.misses,
            "keys": list(self.map.keys()),
        }


# -------------------------
# Demo
# -------------------------
if __name__ == "__main__":
    cache = LRUCache(capacity=3)

    cache.set("a", 1, ttl=3)
    cache.set("b", 2)
    cache.set("c", 3)
    print(cache.get("a"))
    cache.set("d", 4)  # should evict LRU of b/c
    print(cache.stats())
