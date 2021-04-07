import socket
import threading
import time


SERVER_HOST = "192.168.1.69" # Change to server IP address
PORT = 1234
ADDRESS = (SERVER_HOST, PORT)

MESSAGE_SIZE = 1024
ENCODING = 'utf-8'
DISCONNECT_MESSAGE = "!!!!!" # Not used yet

c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_socket.connect(ADDRESS)


def ping():
    while True:
        c_socket.send("Connected?".encode(ENCODING))
        response = c_socket.recv(MESSAGE_SIZE).decode(ENCODING)
        print(response)
        time.sleep(10)


def listen():
    while True:
        print(c_socket.recv(MESSAGE_SIZE).decode(ENCODING))


if __name__ == '__main__':
    thread_ping = threading.Thread(target=ping, args=())
    thread_ping.start()
    thread_listen = threading.Thread(target=listen, args=())
    thread_listen.start()
