"""
Project 80 — In-Memory Message Broker (Event-Driven Architecture Simulator)

Features:
- Create topics
- Publish messages
- Subscribe consumers to topics
- Each consumer tracks its own offset
- Consumer groups (shared offset)
- Retention policy (max messages per topic)
- Simple CLI-driven simulation
"""

from collections import defaultdict, deque
import shlex


class MessageBroker:
    def __init__(self, retention=100):
        self.topics = defaultdict(lambda: deque(maxlen=retention))
        self.consumers = {}              # consumer_name -> { "topic": topic, "offset": index }
        self.consumer_groups = {}        # group_name -> { "topic": topic, "offset": index }

    # --------------------------
    # Topics
    # --------------------------
    def create_topic(self, name):
        if name in self.topics:
            return "Topic already exists"
        self.topics[name] = deque(maxlen=100)
        return f"Topic '{name}' created"
