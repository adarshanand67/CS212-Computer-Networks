'''
Member 1: Aniket Akshay Chaudhri (2003104)
Member 2: Adarsh Anand (2003101)
'''

##################################
# server

import socket   # import socket module
import threading    # import threading module

IP = socket.gethostbyname(socket.gethostname())  # get IP address
PORT = 5001  # set port and size
ADDR = (IP, PORT)   # set address and size
SIZE = 1024   # set size of message
FORMAT = 'utf-8'    # set format of message
DISCONNECT_MESSAGE = "q"  # set disconnect message

clients = []    # list of clients and their names
clientname = {}  # run main function if this file is run


def handle_client(conn, addr):
    ''' function that handles each client '''
    print(f"[NEW CONNECTION] {clientname[addr]} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)    # get message from client
        if msg == DISCONNECT_MESSAGE:
            connected = False

        print(f"[{clientname[addr]}] {msg}")
        msg = f"{clientname[addr]} : {msg}\n"  # add name to message
        # conn.send(msg.encode(FORMAT))
        for client in clients:
            client[0].send(msg.encode(FORMAT))  # send message to all clients

    conn.close()    # close connection


def main():
    ''' main function '''
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
    server.bind(ADDR)   # bind socket to address

    server.listen()    # start listening for connections
    # print listening message
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()  # accept new connection
        clients.append((conn, addr))  # add new connection to clients list

        name = conn.recv(SIZE).decode(FORMAT)   # get name of client
        clientname[addr] = name  # add name to clientname dictionary

        thread = threading.Thread(target=handle_client, args=(
            conn, addr))  # create new thread for each client
        thread.start()  # start thread

        # print number of active connections
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()


#####################################
# Client

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
