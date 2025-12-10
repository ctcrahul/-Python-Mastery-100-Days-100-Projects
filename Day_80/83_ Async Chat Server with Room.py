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
             self.user_rooms = {}               # writer -> room
        self.message_queues = {}           # writer -> asyncio.Queue

    async def register(self, writer):
        self.usernames[writer] = f"user{len(self.usernames)+1}"
        self.user_rooms[writer] = None
        self.message_queues[writer] = asyncio.Queue()
        await self.send(writer, f"Welcome. Set name with: /nick <name>")

    async def unregister(self, writer):
        room = self.user_rooms.get(writer)
        if room and writer in self.rooms[room]:
            self.rooms[room].remove(writer)

        self.usernames.pop(writer, None)
        self.user_rooms.pop(writer, None)
        self.message_queues.pop(writer, None)

        writer.close()
        await writer.wait_closed()

    async def send(self, writer, message):
        # push message into user's queue
        await self.message_queues[writer].put(message + "\n")

    async def broadcaster(self, writer):
        queue = self.message_queues[writer]
        while True:
            msg = await queue.get()
            try:
                writer.write(msg.encode())
                await writer.drain()
            except Exception:
                break

    async def handle(self, reader, writer):
