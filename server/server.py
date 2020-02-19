from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from sock_client import Sock_Client
import json
import time

HOST = ''
PORT = 3000
ADDR = (HOST, PORT)
MAX_CONNS = 10
BUFSIZ = 1024

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERVER.bind(ADDR)

SOCK_CLIENTS = []
MESSAGES = []

def check_user_quit(sock_client, data):
    if data == "{quit}" or data == "":
        return True  
    else:
        return False

def send(sock_client, msg, **kwargs):
    payload = {
        "sender": "server",
        "message": msg,
        "history": kwargs.get('history')
    }
    sock_client.conn.send(json.dumps(payload).encode('utf-8'))

def broadcast(sender, msg):
    try:
        payload = {}

        for sock_client in SOCK_CLIENTS:
            if sock_client.just_joined == True and len(MESSAGES) != 0:
                payload = {
                    "sender": sender,
                    "message": msg,
                    "history": MESSAGES
                }
                sock_client.conn.send(json.dumps(payload).encode('utf-8'))
            else:
                payload = {
                    "sender": sender,
                    "message": msg
                }
                if sock_client.name != sender:
                    sock_client.conn.send(json.dumps(payload).encode('utf-8'))
            
    except Exception as e:
        print(f"[EXCEPTION][BROADCAST]: {e}")


def sock_client_communication(sock_client):
    try:       
        while True:

            # TASK move_sock_client_setup_in_loop checkout
            if sock_client.just_joined == True:

                data = sock_client.conn.recv(BUFSIZ).decode('utf-8')
                
                if check_user_quit(sock_client, data) == True:

                    sock_client.conn.close()
                    SOCK_CLIENTS.remove(sock_client)
                    msg = f"{sock_client.addr} has left the chat..."
                    broadcast('server', msg)
                    print(f"Connection to {addr} closed")    
                    print(f"{len(SOCK_CLIENTS)} Current Connections")

                else:
                    sock_client.set_name(data)

                    name = sock_client.name
                    addr = sock_client.addr
                    conn = sock_client.conn

                    msg = f"{name} has joined the chat..."
                    broadcast('server', msg)
                    print(f"{msg}")  

                    sock_client.just_joined = False
            # TASK move_sock_client_setup_in_loop checkout
            else:
                msg = conn.recv(BUFSIZ).decode('utf-8')

                if check_user_quit(sock_client, msg):
                    conn.close()
                    SOCK_CLIENTS.remove(sock_client)
                    msg = f"{name} has left the chat..."
                    broadcast('server', msg)
                    print(f"Connection to {name}:{addr} closed")
                    print(f"{len(SOCK_CLIENTS)} Current Connections")
                    break                
                else:
                    broadcast(sock_client.name, msg)
                    MESSAGES.append({
                        'sender': sock_client.name,
                        'message': msg,
                        'time': time.time()
                        })
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
            print(f"{len(SOCK_CLIENTS)} Current Connections")
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