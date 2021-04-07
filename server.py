import socket
import threading
from datetime import datetime


HOST = "2001:818:e2c1:bf00:7929:aba0:9b56:7a62" # Server IP address
PORT = 1234
ADDRESS = (HOST, PORT)

MESSAGE_SIZE = 1024
ENCODING = 'utf-8'
PING_MESSAGE = "ping"

CLIENTS = []
client_count = 0

s_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s_socket.bind(ADDRESS)


def server_start():
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"[{current_time}] Server {ADDRESS} online.")
    s_socket.listen()

    thread_broadcast = threading.Thread(target=server_broadcast, args=())
    thread_broadcast.start()

    while True:
        connection, address = s_socket.accept()
        thread_connection = threading.Thread(target=client_connect, args=(connection, address))
        thread_connection.start()


def client_connect(connection, address):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"[{current_time}] Client {address} connected to server.")
    CLIENTS.append(connection)
    global client_count
    client_count += 1
    print(f"Active Connections: {client_count}")
    while True:
        try:
            message = connection.recv(MESSAGE_SIZE).decode(ENCODING)
            if (message):
                # if (message == DISCONNECT_MESSAGE):
                #     print(f"Client {address} disconnected from server.")
                #     connection.close()
                #     CLIENT.remove(connection)
                #     client_count -= 1
                #     break
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] Client {address}: {message}")
                if (message == PING_MESSAGE):
                    response = '{"message": "pong", "priority": 1}'
                    connection.send(response.encode(ENCODING))
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] Server: pong")
        except ConnectionResetError:
            print(f"Client {address} disconnected from server.")
            connection.close()
            CLIENTS.remove(connection)
            client_count -= 1
            break



def server_broadcast():
    while True:
        message = input()
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] Server: {message}")
        for connection in CLIENTS:
            connection.send(message.encode(ENCODING))


if __name__ == '__main__':
    print("Server is starting...")
    server_start()
