from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import json

SERVER = '10.0.10.72'
PORT = 3000
ADDR = (SERVER, PORT)
BUFSIZ = 1024

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

name = input("What's your name? ")
client_socket.send(bytes(name, 'utf-8'))

def receive():
    while True:
        msg = client_socket.recv(BUFSIZ).decode('utf-8')

        if msg:
            msg = json.loads(msg)

            if msg['sender'] == 'server':
                print(msg['message'])
            else:
                print(f"> {msg['sender']}: {msg['message']}")


RECV_THREAD = Thread(target=receive)
RECV_THREAD.start()

while True:
    msg = input('\n')
    client_socket.send(bytes(msg, 'utf-8'))