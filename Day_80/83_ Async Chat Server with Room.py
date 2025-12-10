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
        await self.register(writer)

        asyncio.create_task(self.broadcaster(writer))

        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                text = data.decode().strip()
                if text.startswith("/"):
                    await self.handle_command(writer, text)
                else:
                    await self.send(writer, "Unknown command. Use /msg to chat.")
        except Exception:
            pass

        await self.unregister(writer)

    async def handle_command(self, writer, text):
        parts = text.split(" ", 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "/nick":
            self.usernames[writer] = arg or self.usernames[writer]
            await self.send(writer, f"Name set to {self.usernames[writer]}")

        elif cmd == "/join":
            new_room = arg.strip()
            old_room = self.user_rooms.get(writer)

            if old_room and writer in self.rooms[old_room]:
                self.rooms[old_room].remove(writer)

            self.rooms[new_room].add(writer)
            self.user_rooms[writer] = new_room
            await self.send(writer, f"You joined room '{new_room}'")

        elif cmd == "/rooms":
            await self.send(writer, "Rooms: " + ", ".join(self.rooms.keys()))

        elif cmd == "/users":
            names = [self.usernames[w] for w in self.usernames]
            await self.send(writer, "Users: " + ", ".join(names))

        elif cmd == "/msg":
            room = self.user_rooms.get(writer)
            if not room:
                await self.send(writer, "Join a room first with /join <room>")
                return
            sender = self.usernames.get(writer, "unknown")
            message = f"[{room}] {sender}: {arg}"
            for w in list(self.rooms[room]):
                await self.send(w, message)

        elif cmd == "/quit":
            await self.send(writer, "Goodbye.")
            await self.unregister(writer)

        else:
            await self.send(writer, "Unknown command")

    async def run(self, host="127.0.0.1", port=8888):
        server = await asyncio.start_server(self.handle, host, port)
        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        print(f"Server running on {addrs}")
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(ChatServer().run())
