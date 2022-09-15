import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5001
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Connected to {IP}:{PORT}")
    name = input("Enter your name: ")
    client.send(name.encode(FORMAT))
    connected = True
    while connected:
        msg = input("> ")
        client.send(msg.encode(FORMAT))
        if msg == DISCONNECT_MESSAGE:
            connected = False
        # else:
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

if __name__ == "__main__":
    main()