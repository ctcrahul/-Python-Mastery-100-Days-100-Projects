"""
Project 90 — Job Scheduler with Priority Queue

Run:
    python job_scheduler.py

Concepts:
- Priority Queue
- Scheduling
- Delayed execution
- Worker loop
"""

import time
import threading
import heapq
import itertools


class Job:
    _ids = itertools.count()

    def __init__(self, name, priority, delay, duration):
        self.name = name
        self.priority = priority
        self.run_at = time.time() + delay
        self.duration = duration
        self.id = next(Job._ids)

    def __lt__(self, other):
        # heap order: run_at, priority (higher first), id
        return (self.run_at, -self.priority, self.id) < (
            other.run_at, -other.priority, other.id
        )

class JobScheduler:
    def __init__(self):
        self.jobs = []
        self.lock = threading.Lock()
        self.running = True

    def add_job(self, name, priority=1, delay=0, duration=1):
        job = Job(name, priority, delay, duration)
        with self.lock:
            heapq.heappush(self.jobs, job)
        print(f"[ADDED] {name} (priority={priority}, delay={delay}s)")

    def run(self):
        print("Scheduler started\n")
        while self.running:
            with self.lock:
                if not self.jobs:
                    time.sleep(0.1)
                    continue
