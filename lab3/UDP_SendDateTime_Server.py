'''
Member 1: Aniket Akshay Chaudhri (2003104)
Member 2: Adarsh Anand (2003101)
'''
# socket program to send the current date and time to the client

import socket
import sys
import random
import time

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = 'localhost'

# bind the socket to a port
port = 43387

s.bind((host, port))

while True:
    # receive data from the client
    data, addr = s.recvfrom(1024)  # buffer size is 1024 bytes
    print("Server received MESSAGE=", data.decode(), " from ADDR=", addr)

    if data.decode() == "SEND_DATE":
        # send some bytes (encode the string into Bytes first)
        message = time.strftime("%d/%m/%Y")
        s.sendto(message.encode('utf-8'), (addr[0], addr[1]))
    elif data.decode() == "SEND_TIME":
        # send some bytes (encode the string into Bytes first)
        message = time.strftime("%H:%M:%S")
        s.sendto(message.encode('utf-8'), (addr[0], addr[1]))
    elif data.decode() == "quit":
        break

# close the socket
s.close()
