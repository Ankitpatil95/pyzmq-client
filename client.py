"""
This module will connect to the server and display the broadcast message.
"""
import os
import zmq


def connect_server():
    """
    This function will connect to the server
    :return:
    """
    context = zmq.Context()
    print("Connecting to server...")
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.connect(os.environ['server_url'])
    print("Connected to server")
    print("Listening to server...")

    while True:
        message = socket.recv()
        print("Received reply:", message.decode("utf-8"))


if __name__ == '__main__':
    connect_server()
