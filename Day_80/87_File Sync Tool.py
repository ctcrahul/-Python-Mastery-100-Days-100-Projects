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
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def sync(src, dst, delete_extra=False):
    src_files = collect_files(src)
    dst_files = collect_files(dst) if os.path.exists(dst) else {}

    copied = updated = deleted = 0

    # Copy & update
    for rel, src_path in src_files.items():
        dst_path = os.path.join(dst, rel)
        ensure_dir(os.path.dirname(dst_path))

        if rel not in dst_files:
            shutil.copy2(src_path, dst_path)
            print(f"[COPY] {rel}")
            copied += 1
        else:
            if file_hash(src_path) != file_hash(dst_files[rel]):
                shutil.copy2(src_path, dst_path)
                print(f"[UPDATE] {rel}")
                updated += 1

    # Delete extra files
