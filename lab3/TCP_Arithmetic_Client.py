# socket program to send mathematical expression to server and receive the result repeatedly

import socket
import re

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
