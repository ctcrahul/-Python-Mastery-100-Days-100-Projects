"""
Project 87 — File Sync Tool (Source -> Target)

Usage:
    python file_sync.py SRC DST
    python file_sync.py SRC DST --delete

Features:
- Copies new files
- Updates modified files using SHA256 hash
- Optionally deletes extra files in target
"""

import os
import shutil
import hashlib
import argparse


def file_hash(path, chunk_size=8192):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def collect_files(root):
    files = {}
    for base, _, filenames in os.walk(root):
        for name in filenames:
            full = os.path.join(base, name)
            rel = os.path.relpath(full, root)
            files[rel] = full
    return files
