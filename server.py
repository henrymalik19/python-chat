from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from connection import Connection
import json

HOST = ''
PORT = 3000
ADDR = (HOST, PORT)
MAX_CONNS = 10
BUFSIZ = 1024

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

CONNECTIONS = []

def broadcast(msg, sender):
    try:
        payload = {
            "sender": sender,
            "message": msg
            }
        for connection in CONNECTIONS:
            if connection.name != sender:
                connection.client.send(json.dumps(payload).encode('utf-8'))
            
    except Exception as e:
        print(f"[EXCEPTION][BROADCAST]: {e}")

def client_communication(connection):

    connection.set_name(connection.client.recv(BUFSIZ).decode('utf-8'))

    name = connection.name
    addr = connection.addr
    client = connection.client

    msg = f"{name} has joined the chat..."
    broadcast(msg, 'server')
    print(msg)
    
    while True:
        try:
            msg = client.recv(BUFSIZ).decode('utf-8')

            if msg == "{quit}":
                client.close()
                CONNECTIONS.remove(connection)
                print(f"Connection to {name} closed")
                break                
            else:
                broadcast(msg, name)
                print(f"{name}: {msg}")

        except Exception as e:
            print(f"[EXCEPTION][CLIENT_COMMUNICATION]: {e}")


def handle_connections():
    while True:
        try:
            client, addr = SERVER.accept()
            connection = Connection(client=client, addr=addr)
            CONNECTIONS.append(connection)

            print(f"New Conection: {connection.addr}")
            Thread(target=client_communication, args=(connection,)).start()

        except Exception as e:
            print(f"[EXCEPTION][HANDLE_CONNECTIONS]: {e}")

    print("[SERVER DISCONNECTED]")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNS)
    print(f"Server Listening on Port: {str(PORT)}")
    print("Waiting for Connecions...")
    ACCEPT_THREAD = Thread(target=handle_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()