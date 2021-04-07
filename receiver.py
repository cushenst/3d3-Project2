import json
import socket
import threading
import time

import transmit

PORT = 1234
SERVER = "localhost"
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)


def connect():
    global sock
    retry_time = 2
    a = -1
    while True:
        if a == 61:
            print("Connecting...")
        a = sock.connect_ex((SERVER, PORT))
        print(a)
        if a == 0:
            print("Connection established")
            break
        if a != 61:
            sock.close()
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            print(f"Connecting Failed waiting {retry_time} seconds")
            time.sleep(retry_time)
            retry_time *= 2
    return 1


def send_ping():
    global sent_ping
    global ping_received
    ping_interval = 60
    while True:
        if time.time() % ping_interval >= 5 and sent_ping and not ping_received:
            print("pong timeout")
            sent_ping = False
            sock.close()
            connect()
        elif ping_received:
            print("pong received")
            sent_ping = False
            ping_received = False
        elif time.time() % ping_interval <= 1 and not sent_ping:
            try:
                sock.send("ping".encode("utf-8"))
                sent_ping = True
                print("ping sent")
            except Exception as e:
                print("Error:", e)
                sock.close()
                connect()


def receive_data():
    global sent_ping
    global ping_received
    while True:
        try:
            data = sock.recv(64)
            if data:
                data = data.decode("utf-8")
                decoded_data = json.loads(data)
                message = decoded_data["message"]
                priorty = decoded_data["priority"]

                print(message)

                if message == "pong" and sent_ping and not ping_received:
                    print(message)
                    ping_received = True

                if priorty == 5:
                    transmit.send_over_sound(message)
        except OSError:
            pass
        except Exception as e:
            print("Error receiver:", e)
            sock.close()
            connect()


if __name__ == "__main__":
    connected = False
    connect()
    print("Sample message: {}".format(json.dumps({"message": "Hello World", "priority": 1})))
    sent_ping = False
    ping_received = False
    t1 = threading.Thread(target=receive_data, args=())
    t1.setDaemon(True)
    t1.start()
    t2 = threading.Thread(target=send_ping, args=())
    t2.setDaemon(True)
    t2.start()
    t2.join()
