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
    def subscribe(self, topic, consumer):
        self.subscribers[topic].append(consumer)

    def start_dispatcher(self):
        def dispatch():
            while True:
                for topic, queue in self.topics.items():
                    while queue:
                        event = queue.popleft()
                        for consumer in self.subscribers[topic]:
                            consumer.consume(event)
                time.sleep(0.1)

        threading.Thread(target=dispatch, daemon=True).start()

# SYSTEM START
# -----------------------------
if __name__ == "__main__":
    broker = EventBroker()

    consumer_a = Consumer("AnalyticsService")
    consumer_b = Consumer("NotificationService")

    broker.subscribe("orders", consumer_a)
    broker.subscribe("orders", consumer_b)

    broker.start_dispatcher()

    producer = Producer(broker)

    for i in range(5):
        producer.send("orders", {"order_i
