import socket
import threading
import time
import json


HOST = "2001:818:e2c1:bf00:4414:e8a3:97fb:fd77" # Server IP address
PORT = 1234
ADDRESS = (HOST, PORT)

MESSAGE_SIZE = 1024
ENCODING = 'utf-8'
PING_MESSAGE = "ping"

CLIENTS = []
client_count = 0

s_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_socket.bind(ADDRESS)


def server_start():
    current_time = time.strftime("%x %X")
    print(f"[{current_time}] Server {ADDRESS} online.")
    s_socket.listen()

    thread_commands = threading.Thread(target=server_commands, args=())
    thread_commands.setDaemon(True)
    thread_commands.start()

    while True:
        connection, address = s_socket.accept()
        thread_connection = threading.Thread(target=client_connect, args=(connection, address))
        thread_connection.setDaemon(True)
        thread_connection.start()


def server_commands():
    while True:
        command = input()
        if (command == "broadcast"):
            server_broadcast()
        elif (command == "connections"):
            server_connections()
        elif (command == "help"):
            server_help()
        else:
            print("Command not found. Try in \"help\".")


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
    print("Enter message: ")
    message = input()
    print("Enter priority: ")
    priority = int(input())
    json_message = {"message": message, "priority": priority}
    json_message = json.dumps(json_message)

    for connection in CLIENTS:
        connection.send(json_message.encode(ENCODING))

    current_time = time.strftime("%x %X")
    print(f"[{current_time}] Server: {json_message}")


def server_connections():
    current_time = time.strftime("%x %X")
    print(f"[{current_time}] Server: {client_count} active connections.")
    for connection in CLIENTS:
        print(connection)


def server_help():
    print("\"broadcast\" - broadcasts message and priority to all active connections.")
    print("\"connections\" - shows the number of active connections and lists them.")
    print("\"help\" - lists all acceptable commands.")


if __name__ == '__main__':
    print("Server is starting...")
    server_start()
