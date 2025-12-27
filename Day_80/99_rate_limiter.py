import time
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

RATE_LIMIT = 5        # requests
WINDOW = 10           # seconds

def is_allowed(user_id):
    key = f"rate:{user_id}"
    now = int(time.time())

    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, now - WINDOW)
    pipe.zcard(key)
    pipe.zadd(key, {now: now})
    pipe.expire(key, WINDOW)
    _, count, _, _ = pipe.execute()

    return count < RATE_LIMIT



# --------- Test Simulation ----------
if __name__ == "__main__":
    user = "user_123"

    for i in range(10):
        allowed = is_allowed(user)
        print(f"Request {i+1} ->", "ALLOWED" if allowed else "BLOCKED")
        time.sleep(1)
