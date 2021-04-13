import socket
import threading
import time
import json
from routes import json_var

HOST = "127.0.0.1" # Server IP address
PORT = 1234
ADDRESS = (HOST, PORT)

MESSAGE_SIZE = 1024
ENCODING = 'utf-8'
PING_MESSAGE = "ping"

CLIENTS = []
client_count = 0

s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_socket.bind(ADDRESS)


def server_start():
    current_time = time.strftime("%x %X")
    print(f"[{current_time}] Server {ADDRESS} online.")
    s_socket.listen()

    thread_broadcast = threading.Thread(target=server_broadcast, args=())
    thread_broadcast.start()

    while True:
        connection, address = s_socket.accept()
        thread_connection = threading.Thread(target=client_connect, args=(connection, address))
        thread_connection.start()


def client_connect(connection, address):
    current_time = time.strftime("%x %X")
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
                current_time = time.strftime("%x %X")
                print(f"[{current_time}] Client {address}: {message}")
                if (message == PING_MESSAGE):
                    json_response = {"message": "pong", "priority": 1}
                    json_response = json.dumps(json_response)
                    connection.send(json_response.encode(ENCODING))
                    current_time = time.strftime("%x %X")
                    print(f"[{current_time}] Server: {json_response}")
        except ConnectionResetError:
            current_time = time.strftime("%x %X")
            print(f"[{current_time}] Client {address} disconnected from server.")
            connection.close()
            CLIENTS.remove(connection)
            client_count -= 1
            break



def server_broadcast():
    while True:
        message = json_var["message"]
        priority = json_var["priority"]
        json_message = {"message": message, "priority": priority}
        json_message = json.dumps(json_message)

        for connection in CLIENTS:
            connection.send(json_message.encode(ENCODING))

        current_time = time.strftime("%x %X")
        print(f"[{current_time}] Server: {json_message}")


if __name__ == '__main__':
    print("Server is starting...")
    server_start()
