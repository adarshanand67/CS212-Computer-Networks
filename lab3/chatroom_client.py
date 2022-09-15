# socket program to implement chatroom client

import socket
import select
import sys
import queue

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setblocking(False)

# name of client
name = input("Enter your name: ")

# connect to the server
host = 'localhost'
port = 10000  # this is the server's port number, which the client needs to know
client.connect((host, port))

# send some bytes
client.send(name.encode('utf-8'))

# read a response
response = client.recv(1024)
print("CLIENT RECEIVED: ", response.decode())


