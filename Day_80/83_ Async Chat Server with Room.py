"""
Project 83 — Async Chat Server with Rooms (TCP)
Run server:
    python async_chat_server.py

Then connect using multiple terminals:
    nc localhost 8888
    telnet localhost 8888
    (or a simple Python client)

Commands available:
    /nick <name>
    /join <room>
    /rooms
    /users
    /msg <message>
    /quit
"""

import asyncio
from collections import defaultdict


class ChatServer:
    def __init__(self):
        self.rooms = defaultdict(set)      # room -> set of writers
        self.usernames = {}                # writer -> name
     
