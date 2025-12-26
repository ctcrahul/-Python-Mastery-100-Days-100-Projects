# Project 98 - Task Producer

import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def send_task(task_name, payload):
    task = {
        "task": task_name,
        "data": payload
    }
    r.lpush("task_queue", json.dumps(task))
    print("Task sent:", task)

if __name__ == "__main__":
    while True:
        data = input("Enter task data (or 'exit'): ")
        if data == "exit":
            break
        send_task("process_data", data)
