import time
import threading
import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn

# ---------------- GLOBAL STATE ----------------
TASK_QUEUE = []
TASK_LOG = []
RATE_LIMIT = {}
MAX_REQ = 5
WINDOW = 10  # seconds

# ---------------- UTILS ----------------
def now():
    return int(time.time())

def rate_limit(ip):
    timestamps = RATE_LIMIT.get(ip, [])
    timestamps = [t for t in timestamps if now() - t < WINDOW]

    if len(timestamps) >= MAX_REQ:
        return False

    timestamps.append(now())
    RATE_LIMIT[ip] = timestamps
    return True

# ---------------- TASK EXECUTOR ----------------
def worker():
    while True:
        if TASK_QUEUE:
            task = TASK_QUEUE.pop(0)
            log = {
                "id": task["id"],
                "status": "running",
                "timestamp": now()
            }
            TASK_LOG.append(log)
            time.sleep(2)  # simulate work
            log["status"] = "completed"
        time.sleep(1)

# ---------------- API ----------------
app = FastAPI()

@app.middleware("http")
async def limiter(request: Request, call_next):
    ip = request.client.host
    if not rate_limit(ip):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    return await call_next(request)

@app.post("/submit")
def submit_task(data: dict):
    task = {
        "id": str(uuid.uuid4()),
        "payload": data,
        "created": now()
    }
    TASK_QUEUE.append(task)
    return {"message": "Task queued", "task_id": task["id"]}

@app.get("/tasks")
def all_tasks():
    return TASK_LOG

@app.get("/")
def health():
    return {"status": "system running"}

# ---------------- START WORKER ----------------
threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run("project_102:app", host="0.0.0.0", port=8000)
