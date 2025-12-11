"""
Project 84 — Distributed Key-Value Store with Gossip Replication

Run nodes:
    python distributed_kv.py --port 5001 --peers 5002 5003
    python distributed_kv.py --port 5002 --peers 5001 5003
    python distributed_kv.py --port 5003 --peers 5001 5002

Set:
    curl -X POST localhost:5001/put -d "key=a&value=10"

Get:
    curl "localhost:5003/get?key=a"

Nodes will gossip and converge eventually.
"""

import argparse
import threading
import time
import requests
from fastapi import FastAPI, Request
from uvicorn import run

app = FastAPI()

store = {}          # key -> { "value": ..., "vclock": {node: counter} }
peers = []          # peer ports
node_id = None


def merge_vclocks(vc1, vc2):
    merged = {}
    for k in set(vc1) | set(vc2):
        merged[k] = max(vc1.get(k, 0), vc2.get(k, 0))
    return merged


def vclock_compare(vc1, vc2):
    """Return:
       -1 if vc1 < vc2
        0 if concurrent
        1 if vc1 > vc2
    """
    gt = False
    lt = False
    all_keys = set(vc1) | set(vc2)

    for k in all_keys:
        a = vc1.get(k, 0)
        b = vc2.get(k, 0)
        if a > b:
            gt = True
        if a < b:
            lt = True

    if gt and not lt:
        return 1
    if lt and not gt:
        return -1
    return 0

@app.post("/put")
async def put(request: Request):
    global store
    form = await request.form()
    key = form["key"]
    value = form["value"]

    existing = store.get(key)
    new_vc = {node_id: (existing["vclock"].get(node_id, 0) + 1) if existing else 1}

    if existing:
        merged_vc = merge_vclocks(existing["vclock"], new_vc)
    else:
        merged_vc = new_vc

    store[key] = {
        "value": value,
        "vclock": merged_vc
    }
    return {"status": "OK", "node": node_id}


@app.get("/get")
async def get(key: str):
    item = store.get(key)
    if not item:
        return {"value": None, "vclock": {}}
    return item

@app.post("/gossip")
async def gossip(incoming: dict):
    global store
    for key, item in incoming.items():
        if key not in store:
            store[key] = item
            continue

        local = store[key]
        cmp = vclock_compare(local["vclock"], item["vclock"])

        if cmp == -1:
            store[key] = item
        elif cmp == 0:
            # concurrent -> keep both? For now we merge vector clocks, pick incoming value
            merged_vc = merge_vclocks(local["vclock"], item["vclock"])
            store[key] = {"value": item["value"], "vclock": merged_vc}

    return {"status": "merged"}


def gossip_loop():
    while True:
        time.sleep(2)
        for p in peers:
            try:
                requests.post(f"http://localhost:{p}/gossip", json=store, timeout=1)
            except:
                pass
