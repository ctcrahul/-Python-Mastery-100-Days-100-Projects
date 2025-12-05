"""
Project 78 — Local Key-Value Store with Write-Ahead Logging

Features:
- SET key value
- GET key
- DEL key
- EXISTS key
- KEYS pattern
- Persistence using a Write-Ahead Log (wal.log)
- Recovery: rebuild state from WAL on startup
- Simple CLI REPL

Run:
    python kv_store.py

Example commands:
    SET name raj
    GET name
    DEL name
    EXISTS name
    KEYS *
"""

import os
import shlex

WAL_FILE = "wal.log"


class KeyValueStore:
    def __init__(self):
        self.data = {}
        self.load_from_wal()

    def load_from_wal(self):
        if not os.path.exists(WAL_FILE):
            return

        with open(WAL_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = shlex.split(line.strip())
                if not parts:
                    continue
                cmd = parts[0].upper()

                if cmd == "SET" and len(parts) >= 3:
                    key = parts[1]
                    value = " ".join(parts[2:])
                    self.data[key] = value

                elif cmd == "DEL" and len(parts) == 2:
                    key = parts[1]
                    self.data.pop(key, None)

    def append_wal(self, line):
        with open(WAL_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def set(self, key, value):
        self.data[key] = value
        self.append_wal(f"SET {key} {value}")
        return "OK"

    def get(self, key):
        return self.data.get(key, "(nil)")

    def delete(self, key):
        existed = key in self.data
        self.data.pop(key, None)
        self.append_wal(f"DEL {key}")
        return "1" if existed else "0"
    def exists(self, key):
        return "1" if key in self.data else "0"

    def keys(self, pattern="*"):
        if pattern == "*":
            return " ".join(self.data.keys())
        # very naive pattern match
        if "*" in pattern:
            prefix = pattern.split("*")[0]
            return " ".join(k for k in self.data if k.startswith(prefix))
        return pattern if pattern in self.data else ""


def repl():
    store = KeyValueStore()
    print("KV Store (type EXIT to quit)")

    while True:
        try:
            raw = input("> ").strip()
        except EOFError:
            break

        if not raw:
            continue

        parts = shlex.split(raw)
        cmd = parts[0].upper()

        if cmd == "EXIT":
            print("Bye.")
            break

def repl():
    store = KeyValueStore()
    print("KV Store (type EXIT to quit)")

    while True:
        try:
            raw = input("> ").strip()
        except EOFError:
            break

        if not raw:
            continue

        parts = shlex.split(raw)
        cmd = parts[0].upper()

        if cmd == "EXIT":
            print("Bye.")
            break

        if cmd == "SET" and len(parts) >= 3:
            key = parts[1]
            value = " ".join(parts[2:])
            print(store.set(key, value))

        elif cmd == "GET" and len(parts) == 2:
            print(store.get(parts[1]))

        elif cmd == "DEL" and len(parts) == 2:
            print(store.delete(parts[1]))

        elif cmd == "EXISTS" and len(parts) == 2:
            print(store.exists(parts[1]))

        elif cmd == "KEYS":
            pattern = parts[1] if len(parts) == 2 else "*"
            print(store.keys(pattern))

        else:
            print("ERR unknown command")
    

if __name__ == "__main__":
    repl()
