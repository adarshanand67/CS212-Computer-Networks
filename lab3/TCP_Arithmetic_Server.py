# socket program to receive mathematical expression from client and send the result repeatedly

import socket

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a host and a port
host = 'localhost'
port = 3000  # arbitrarily chosen non-privileged port number
s.bind((host,port))
print("Server started...waiting for a connection from the client")

# start listening for TCP connections made to this socket
# the argument "1" is the max number of queued up clients allowed
s.listen(1)

# accept a connection
connection_socket, addr = s.accept()
print("Connection initiated from ",addr)

client_name = connection_socket.recv(1024).decode()
connection_socket.send("Hello {}".format(client_name).encode('utf-8'))

while True:
    # receive some bytes and print them
    # the argument 1024 is the maximum number of characters to be read at a time
    data = connection_socket.recv(1024)
    print("SERVER RECEIVED: ", data.decode())

    if data.decode() == "q":
        connection_socket.send("Bye".encode('utf-8'))
        print("Session ended")
        break

    # send some bytes...
    connection_socket.send(str(eval(data.decode())).encode('utf-8'))

# close the connection
connection_socket.close()

