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
