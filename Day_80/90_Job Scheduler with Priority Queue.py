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

                job = self.jobs[0]
                now = time.time()

                if job.run_at > now:
                    time.sleep(job.run_at - now)
                    continue

                heapq.heappop(self.jobs)

            self.execute(job)

    def execute(self, job):
        print(f"[RUNNING] {job.name}")
        time.sleep(job.duration)
        print(f"[DONE] {job.name}")

    def stop(self):
        self.running = False


# ---------------- Demo ----------------
if __name__ == "__main__":
    scheduler = JobScheduler()

    t = threading.Thread(target=scheduler.run, daemon=True)
    t.start()

    scheduler.add_job("low_priority", priority=1, delay=0, duration=2)
    scheduler.add_job("high_priority", priority=5, delay=0, duration=1)
    scheduler.add_job("delayed_job", priority=3, delay=3, duration=1)
    scheduler.add_job("medium_priority", priority=3, delay=0, duration=1)

    time.sleep(8)
    scheduler.stop()
