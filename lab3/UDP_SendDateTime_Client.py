'''
Member 1: Aniket Akshay Chaudhri (2003104)
Member 2: Adarsh Anand (2003101)
'''
# socket program to request the current date and time from the server repeatedly until the user enters "quit"

import socket
import sys
import random
import time

# create a socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host='localhost'
port=43387  # this is the server's port number, which the client needs to know

messages = ["SEND_DATE", "SEND_TIME"]

while True:
    # send some bytes (encode the string into Bytes first)
    time.sleep(random.uniform(1,2))
    message = random.choice(messages)
    s.sendto( message.encode('utf-8'), (host,port))

    # see if the other side responds
    data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
    print("Client received MESSAGE=",data.decode()," from ADDR=",addr)

    if message == "quit":
        break

# close the connection
s.close()
