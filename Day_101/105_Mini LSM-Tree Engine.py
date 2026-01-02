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
