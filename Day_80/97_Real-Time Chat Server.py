# Project 97: Real-Time Chat Server
# Author: You

import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat.".encode("utf-8"))
            client.close()
            break
def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server started...")

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
