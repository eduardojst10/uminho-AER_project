import socket
# serialize and deserialize objects
import pickle


class Network:

    def __init__(self):

        # SOCK_STREAM - TCP || SOCK_DGRAM - UDP
        #self.client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.client = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

        self.server = "fe80::b042:9587:8d2d:7d69%19"
        self.port = 55550
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            #IPv4 TCP
            #self.client.connect(self.addr)
            # return self.client.recv(2048)
            # O que vamos dar ao server é o número de player
            msg = "client"
            self.client.sendto(msg.encode('utf-8'),self.addr)

            data,addr = self.client.recvfrom(2048)
            return int(data)
        except:
            print("No connection")

    def send(self, data):
        try:
            # vamos enviar string de dados e vamos receber objectos, neste caso o jogo
            self.client.sendto(str.encode(data),self.addr)
            datagame,address = self.client.recvfrom(2048 * 8)
            return pickle.loads(datagame)

        except socket.error as e:
            print(e)
