import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5001
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = []
clientname = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False

        print(f"[{clientname[addr]}] {msg}")
        msg = f"{clientname[addr]} : {msg}"
        # conn.send(msg.encode(FORMAT))
        for client in clients:
            client[0].send(msg.encode(FORMAT))

    conn.close()


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append((conn,addr))
        name = conn.recv(SIZE).decode(FORMAT)
        clientname[addr] = name
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # -1 because of the main thread
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()
