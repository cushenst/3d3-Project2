import socket
import threading


HOST = "2001:818:e2c1:bf00:b5ba:858a:3dbc:9150" # Server IP address
PORT = 1234
ADDRESS = (HOST, PORT)

MESSAGE_SIZE = 1024
ENCODING = 'utf-8'
DISCONNECT_MESSAGE = "!!!!!" # Not used yet

CLIENTS = []
client_count = 0

s_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s_socket.bind(ADDRESS)


def server_start():
    print(f"Server {ADDRESS}")
    s_socket.listen()

    thread_broadcast = threading.Thread(target=server_broadcast, args=())
    thread_broadcast.start()

    while True:
        connection, address = s_socket.accept()
        thread_connection = threading.Thread(target=client_connect, args=(connection, address))
        thread_connection.start()


def client_connect(connection, address):
    print(f"Client {address} connected to server.")
    CLIENTS.append(connection)
    global client_count
    client_count += 1
    print(f"Active Connections: {client_count}")
    while True:
        message = connection.recv(MESSAGE_SIZE).decode(ENCODING)
        if (message):
            if (message == DISCONNECT_MESSAGE):
                print(f"Client {address} disconnected from server.")
                connection.close()
                CLIENT.remove(connection)
                client_count -= 1
                break
            print(f"{address}: {message}")
            connection.send("Yes!".encode(ENCODING))


def server_broadcast():
    while True:
        dummy_message = input()
        for connection in CLIENTS:
            connection.send(dummy_message.encode(ENCODING))


if __name__ == '__main__':
    print("Server is starting...")
    server_start()
