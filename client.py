import os
import zmq


def connect_server():
    context = zmq.Context()
    print("Connecting to server…")
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.connect(os.environ['server_url'])

    while True:
        message = socket.recv()
        print("Received reply:", message.decode("utf-8"))


if __name__ == '__main__':
    connect_server()
