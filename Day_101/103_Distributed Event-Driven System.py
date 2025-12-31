import threading
import time
import uuid
from collections import defaultdict, deque

# -----------------------------
# BROKER CORE
# -----------------------------
class EventBroker:
      def __init__(self):
        self.topics = defaultdict(deque)
        self.subscribers = defaultdict(list)
        self.lock = threading.Lock()

    def publish(self, topic, message):
        with self.lock:
            event = {
                "id": str(uuid.uuid4()),
                "timestamp": time.time(),
                "data": message
            }
            self.topics[topic].append(event)
            print(f"[BROKER] Event published to '{topic}'")
