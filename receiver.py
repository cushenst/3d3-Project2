import json
import socket
import threading
import time
import sys
import subprocess


# import transmit

PORT = 1234
SERVER = "2a04:b480:20:15:3d3::1"
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)


def connect():
    global sock
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    retry_time = 2
    a = -1
    while True:
        if a == 61:
            print("Connecting...")
        a = sock.connect_ex((SERVER, PORT))
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
        if retry_time >= 32:
            subprocess.Popen(["python3", "audio-receiver.py"])
            sys.exit()

    return 1


def send_ping():
    global sent_ping
    global ping_received
    global last_ping_time
    ping_interval = 60
    while True:
        time.sleep(0.5)
        if time.time() % ping_interval >= 5 and sent_ping and not ping_received:
            print("pong timeout")
            sent_ping = False
            sock.close()
            connect()
        elif ping_received:
            print("pong received")
            sent_ping = False
            ping_received = False
        elif time.time() % ping_interval <= 1 and not sent_ping and last_ping_time < int(time.time())-15:
            try:
                sock.send("ping".encode("utf-8"))
                last_ping_time = int(time.time())
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

                if message == "pong" and sent_ping and not ping_received:
                    ping_received = True
                else:
                    current_time = time.strftime("%x %X")
                    message_formatted = f"{current_time}: {message}"
                    print(message_formatted)

                if priorty == 5:
                    # transmit.send_over_sound(message)
                    print("Sound playing...")
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
    last_ping_time = 0
    ping_received = False
    t1 = threading.Thread(target=receive_data, args=())
    t1.setDaemon(True)
    t1.start()
    t2 = threading.Thread(target=send_ping, args=())
    t2.setDaemon(True)
    t2.start()
    t2.join()
