'''
Member 1: Aniket Akshay Chaudhri (2003104)
Member 2: Adarsh Anand (2003101)
'''
# socket program to receive mathematical expression from client and send the result repeatedly

#############################################
# This is the Server program

import re
import socket

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a host and a port
host = 'localhost'
port = 3000  # arbitrarily chosen non-privileged port number
s.bind((host, port))
print("Server started...waiting for a connection from the client")

# start listening for TCP connections made to this socket
# the argument "1" is the max number of queued up clients allowed
s.listen(1)

# accept a connection
connection_socket, addr = s.accept()
print("Connection initiated from ", addr)

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

###################################
# This is the Client program

# socket program to send mathematical expression to server and receive the result repeatedly


# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def isNumber(expression):
    if expression == "q":
        return True
    try:
        float(expression)
        return True
    except:
        return False


def isValidExpression(expression):
    if expression == "q":
        return True
    values = expression.split(" ")

    # Check division by zero
    if (len(values) == 3):
        if (values[1] == "/" and values[2] == "0"):
            return False

    if (len(values) == 3):
        if (isNumber(values[0]) and isNumber(values[2])):
            if (values[1] == "+" or values[1] == "-" or values[1] == "*" or values[1] == "/"):
                return True
    return False


# name of client
name = input("Enter your name: ")

# connect to the server
host = 'localhost'
port = 3000  # this is the server's port number, which the client needs to know
s.connect((host, port))

# send some bytes
s.send(name.encode('utf-8'))

# read a response
response = s.recv(1024)
print("CLIENT RECEIVED: ", response.decode())

while True:
    # send some bytes
    expression = input("Enter an expression: ")
    if (isValidExpression(expression)):
        s.send(expression.encode('utf-8'))
    else:
        print("Invalid expression")
        continue

    # read a response
    response = s.recv(1024)
    print("CLIENT RECEIVED: ", response.decode())

    if response.decode() == "Bye":
        break

# close the connection
s.close()


