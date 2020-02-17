from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from termcolor import colored
import json


SERVER = '10.0.10.72'
PORT = 3000
ADDR = (SERVER, PORT)
BUFSIZ = 1024

def receive():
    while True:
        msg = client_socket.recv(BUFSIZ).decode('utf-8')

        if msg:
            msg = json.loads(msg)

            if msg['sender'] == 'server':
                print(colored(msg['message'], 'red'))
            else:
                print(colored(f"{msg['sender']}: {msg['message']}", 'blue'))

def send():
    while True:
        msg = input()
        if msg == '':
            continue
        client_socket.send(bytes(msg, 'utf-8'))

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

name = input("What is your name? ")
client_socket.send(bytes(name, 'utf-8'))

RECV_THREAD = Thread(target=receive)
RECV_THREAD.start()
send()