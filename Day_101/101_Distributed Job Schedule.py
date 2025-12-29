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
   for job_name, job_data in jobs.items():
        job = json.loads(job_data)
        if now - job["last_run"] >= job["interval"]:
            job["last_run"] = now
            r.hset("scheduled_jobs", job_name, json.dumps(job))
            r.lpush("job_queue", json.dumps(job))
            print(f"Queued job: {job_name}")

    time.sleep(1)




worker.py

import redis
import json
import time

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def process(job):
    print(f"Executing job: {job['name']} | payload: {job['payload']}")
    time.sleep(2)
    print("Done.")

while True:
    _, job_data = r.brpop("job_queue")
    job = json.loads(job_data)
    process(job)
