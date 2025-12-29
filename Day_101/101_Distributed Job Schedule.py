Scheduler → Redis Queue → Worker(s) → Job Execution
                         ↓
                    Execution Logs


scheduler.py

import redis
import time
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def schedule_job(name, interval_seconds, payload):
    job = {
        "name": name,
        "interval": interval_seconds,
        "payload": payload,
        "last_run": 0
    }
    r.hset("scheduled_jobs", name, json.dumps(job))
    print(f"Scheduled job: {name}")

if __name__ == "__main__":
    schedule_job("email_report", 10, {"type": "email"})
    schedule_job("cleanup_temp", 15, {"type": "cleanup"})


scheduler_runner.py

import redis
import json
import time

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

while True:
    jobs = r.hgetall("scheduled_jobs")
    now = int(time.time())
