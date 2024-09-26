import threading
import socket
from datetime import datetime

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()

def broadcast(message, sender=None):
    with clients_lock:
        for client in clients:
            if client != sender:
                try:
                    client.send(message.encode(FORMAT))
                except Exception as e:
                    print(e)
def handle_client(conn, addr):
    print(f"\n[NEW CONNECTION] {addr} Connected")
    try:
        connected = True
        while connected:
            try:
                msg = conn.recv(1024).decode(FORMAT)
                if not msg:
                    break

                if msg == DISCONNECT_MESSAGE:
                    connected = False

                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"\n[{time}],client-[{addr}]:{msg}")

                broadcast(f"\nBroadcast [{time}],client-[{addr}]:{msg}", conn)

                with clients_lock:
                    for c in clients:
                        c.sendall(f"\n[{addr}] {msg}".encode(FORMAT))
            except ConnectionResetError as e:
                print(e)
                break
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()
def serverToClient():
    """Allows the server to send messages to all connected clients."""
    while True:
        msg = input("[SERVER MESSAGE] : ")
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = f"\n[{time}] SERVER: {msg}"
        print(msg)
        broadcast(msg)

def start():
    print('[SERVER STARTED]!')
    server.listen()

    server_thread = threading.Thread(target=serverToClient)
    server_thread.start()
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\nActive: {threading.active_count() - 1}")
        
start()
