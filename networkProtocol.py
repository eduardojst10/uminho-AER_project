import socket
import pickle

# Necessário ver como fazer comunicação com IPv6


class NetworkPro:
    def __init__(self):
        #inicialmente está conexão ipv4
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.3.7" # meu local server podia ter usado o clássico 127.0.0.1
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)