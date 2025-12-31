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


# -----------------------------
# CONSUMER
# -----------------------------
class Consumer:
    def __init__(self, name):
        self.name = name

    def consume(self, event):
        print(f"[{self.name}] received -> {event['data']}")

# -----------------------------
# PRODUCER
# -----------------------------
class Producer:
    def __init__(self, broker):
        self.broker = broker

    def send(self, topic, message):
        self.broker.publish(topic, message)


# -----------------------------
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
        producer.send("orders", {"order_id": i, "amount": 100 + i})
        time.sleep(1)
