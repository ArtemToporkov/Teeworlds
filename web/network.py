import pickle
import socket


class Network:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, port)

    def connect(self):
        try:
            self.client.connect(self.addr)
            data_from_server = pickle.loads(self.client.recv(2**16))
            return data_from_server
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
