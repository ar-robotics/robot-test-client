from threading import Thread

import socket
import json

from .utils import get_config

# import brotli


class Client:
    def __init__(self):
        config = get_config()
        address = config["address"]
        port = config["port"]
        self.packet_size = config["packet_size"]

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (address, port)
        self.client_socket.connect(server_address)

        self.thread = Thread(target=self.receive_messages, daemon=True)
        self.thread.start()

        self.ask_for_inputs()

    def receive(self) -> None:
        data = self.client_socket.recv(self.packet_size)

        # check if "bro" is first byte, then decompress with brotli

        print(f"<- RECV {data[:50]}")

    def receive_messages(self) -> None:
        while True:
            self.receive()

    def send_data(self, data: dict) -> None:
        message = json.dumps(data)
        print(f"-> SEND {message}")
        self.client_socket.sendall(message.encode())

    def send_command(self, command: str) -> None:
        try:
            data = json.loads(command)
        except json.JSONDecodeError:
            print(f"Invalid JSON command {command}")
            return

        self.send_data(data)

    def ask_for_inputs(self) -> None:
        while True:
            command = input("Enter a JSON command: ")
            self.send_command(command)
