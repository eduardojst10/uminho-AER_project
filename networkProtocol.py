import socket
# serialize and deserialize objects
import pickle


class Network:

    def __init__(self):

        # SOCK_STREAM - TCP || SOCK_DGRAM - UDP
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 55550
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            # O que vamos dar ao server é o número de player
            return self.client.recv(2048).decode()
        except:
            print("No connection")

    def send(self, data):
        try:
            # vamos enviar string de dados e vamos receber objectos, neste caso o jogo
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*6))

        except socket.error as e:
            print(e)
