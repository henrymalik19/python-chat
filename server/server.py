from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from sock_client import Sock_Client
import json

HOST = ''
PORT = 3000
ADDR = (HOST, PORT)
MAX_CONNS = 10
BUFSIZ = 1024

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERVER.bind(ADDR)

SOCK_CLIENTS = []

def broadcast(msg, sender):
    try:
        if isinstance(sender, str):
            payload = {
                "sender": 'server',
                "message": msg
            }
        else:
            payload = {
                "sender": sender.name,
                "message": msg
                }
        for sock_client in SOCK_CLIENTS:
            if sock_client != sender:
                sock_client.conn.send(json.dumps(payload).encode('utf-8'))
            
    except Exception as e:
        print(f"[EXCEPTION][BROADCAST]: {e}")


def sock_client_communication(sock_client):
    try:
        sock_client.set_name(sock_client.conn.recv(BUFSIZ).decode('utf-8'))

        name = sock_client.name
        addr = sock_client.addr
        conn = sock_client.conn

        if name == "{quit}" or name == "":
            conn.close()
            SOCK_CLIENTS.remove(sock_client)
            msg = f"{addr} has left the chat..."
            broadcast(msg, 'server')
            print(f"Connection to {addr} closed")    
            return           
        else:
            msg = f"{name} has joined the chat..."
            broadcast(msg, 'server')
            print(f"client sent: {msg}")   
        
        while True:
        
            msg = conn.recv(BUFSIZ).decode('utf-8')

            if msg == "{quit}" or msg == "":
                conn.close()
                SOCK_CLIENTS.remove(sock_client)
                msg = f"{name} has left the chat..."
                broadcast(msg, 'server')
                print(f"Connection to {name}:{addr} closed")
                break                
            else:
                broadcast(msg, sock_client)
                print(f"{name}: {msg}")
    except Exception as e:
        print(f"[EXCEPTION][SOCK_CLIENT_COMMUNICATION]: {e}")
        


def handle_connections():
    while True:
        try:
            conn, addr = SERVER.accept()
            sock_client = Sock_Client(conn=conn, addr=addr)
            SOCK_CLIENTS.append(sock_client)

            print(f"New Conection: {sock_client.addr}")
            Thread(target=sock_client_communication, args=(sock_client,)).start()

        except Exception as e:
            print(f"[EXCEPTION][HANDLE_CONNECTIONS]: {e}")
            break

    print("[SERVER DISCONNECTED]")
    SERVER.close()


if __name__ == "__main__":
    SERVER.listen(MAX_CONNS)
    print(f"Server Listening on Port: {str(PORT)}")
    print("Waiting for Connecions...")
    ACCEPT_THREAD = Thread(target=handle_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()