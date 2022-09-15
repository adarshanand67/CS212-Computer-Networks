'''
Member 1: Aniket Akshay Chaudhri (2003104)
Member 2: Adarsh Anand (2003101)
'''

import socket   # import socket module
import threading    # import threading module

IP = socket.gethostbyname(socket.gethostname())  # get IP address
PORT = 5001  # set port and size
ADDR = (IP, PORT)   # set address and size
SIZE = 1024   # set size of message
FORMAT = 'utf-8'    # set format of message
DISCONNECT_MESSAGE = "q"  # set disconnect message


def main():
    ''' main function '''
    # create client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)    # connect to server

    print(f"[CONNECTED] Connected to {IP}:{PORT}")  # print connected message

    name = input("Enter your name: ")   # get name from user
    client.send(name.encode(FORMAT))    # send name to server

    connected = True
    while connected:
        msg = input("> ")   # get message from user
        client.send(msg.encode(FORMAT))  # send message to server
        if msg == DISCONNECT_MESSAGE:
            connected = False
        msg = client.recv(SIZE).decode(FORMAT)  # get message from server
        print(f"[SERVER] {msg}")    # print message from server


if __name__ == "__main__":
    main()
