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
   # --------------------------
    # Producer
    # --------------------------
    def publish(self, topic, message):
        if topic not in self.topics:
            return "Topic not found"
        self.topics[topic].append(message)
        return f"Published to {topic}: {message}"

    # --------------------------
    # Consumer
    # --------------------------
    def subscribe(self, consumer, topic):
        if topic not in self.topics:
            return "Topic not found"

        self.consumers[consumer] = {
            "topic": topic,
            "offset": 0
        }
        return f"Consumer '{consumer}' subscribed to '{topic}'"

    def poll(self, consumer):
        if consumer not in self.consumers:
            return "Unknown consumer"

        info = self.consumers[consumer]
        topic = info["topic"]
        offset = info["offset"]
        messages = self.topics[topic]

        if offset >= len(messages):
            return "(no new messages)"

        msg = messages[offset]
        info["offset"] += 1
        return msg
    # --------------------------
    # Consumer Groups
    # --------------------------
    def create_group(self, group, topic):
        if topic not in self.topics:
            return "Topic not found"

        self.consumer_groups[group] = {
            "topic": topic,
            "offset": 0
        }
        return f"Group '{group}' created"

    def poll_group(self, group):
        if group not in self.consumer_groups:
            return "Unknown group"

        info = self.consumer_groups[group]
        topic = info["topic"]
        offset = info["offset"]
        messages = self.topics[topic]

        if offset >= len(messages):
            return "(no new messages)"

        msg = messages[offset]
        info["offset"] += 1
        return msg

