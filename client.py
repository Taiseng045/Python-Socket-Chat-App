import socket
import time
import threading

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
        print("conented")
    except ConnectionRefusedError as e:
        print(e)
        return None
    return client

def receive_messages(client):
    """Continuously receives messages from the server and prints them."""
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if not msg:
                break
            print(msg)
        except ConnectionResetError as e:
            print(e)
            break

def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)


def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()
    if connection is None:
        return

    # Start a thread to listen for incoming messages
    receive_thread = threading.Thread(target=receive_messages, args=(connection,))
    receive_thread.start()
    while True:
        msg = input("Message (q for quit): ")

        if msg == 'q':
            break

        send(connection, msg)

    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1)
    print('Disconnected')


start()
