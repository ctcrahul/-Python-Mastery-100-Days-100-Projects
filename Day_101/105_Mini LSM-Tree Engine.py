import os
import json
import time

DATA_DIR = "db_data"
WAL_FILE = f"{DATA_DIR}/wal.log"
SSTABLE = f"{DATA_DIR}/sstable.json"

os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------
# STORAGE ENGINE
# -------------------------
class MiniDB:
    def __init__(self):
        self.memtable = {}
        self.load_sstable()
        self.replay_wal()

    def load_sstable(self):
        if os.path.exists(SSTABLE):
            with open(SSTABLE, "r") as f:
                self.disk = json.load(f)
        else:
            self.disk = {}

    def replay_wal(self):
        if not os.path.exists(WAL_FILE):
            return
        with open(WAL_FILE, "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                self.memtable[key] = value
    def write_wal(self, key, value):
        with open(WAL_FILE, "a") as f:
            f.write(f"{key}={value}\n")

    def put(self, key, value):
        self.memtable[key] = value
        self.write_wal(key, value)
        if len(self.memtable) >= 5:
            self.flush()

    def get(self, key):
        if key in self.memtable:
            return self.memtable[key]
        return self.disk.get(key, None)
