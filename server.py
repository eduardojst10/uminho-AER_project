import pickle
import socket
from _thread import *
from game import Game

# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.
#
# Usage:
#   mcast -s (sender, IPv4)
#   mcast -s -6 (sender, IPv6)
#   mcast    (receivers, IPv4)
#   mcast  -6  (receivers, IPv6)


# fazer com ip do server no core
server = "fe80::b042:9587:8d2d:7d69%19"
port = 55550

# criação de socket para ipv4 e TCP
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#try:
#    s6.bind((server, port))
#except socket.error as e:
#    print(e)


# criação de socket para ipv6 e UDP
s6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
s6.bind(("fe80::b042:9587:8d2d:7d69%19",55550))



# vai começar a ouvir
#s.listen(2)
#s6.listen(2)
print("Waiting for connection, Server Started for AER Trivia Game")

# store ids de games
games = {}
# keep track dos jogos
idCount = 0


# player vai ser o nr de jogador 1 ou 0 - current player
def threaded_client(s, p, gameId,addr):
    # este idCount server para verificar casos como um jogador abandonar um jogo a meio
    global idCount

    s.sendto(str.encode(str(p)),addr)  # vamos enviar que jogador somos [0,1]

    reply = ""
    while True:  # vamos ter 3 opções: um get do jogo do server, um resetForward uma answer à questão
        try:
            data = s.recvfrom(4096*4,addr).decode()
            if gameId in games:  # verificar se o jogo ainda existe e se algum cliente não desconectou mais cedo
                game = games[gameId]

                if not data:
                    break

                else:
                    if data == "reset":
                        game.resetWent()

                    elif data == "resetForward":
                        print("got a resetForward from", p)
                        game.resetForward(p)
                        print("Jogador ", p, "está na questão: ", game.currentQuestion(p))
                        print("--------------------------------------------------")
                    elif data != "get":
                        print("got an answer from ",p)
                        game.play(p, data)

                    s.sendto(pickle.dumps(game),addr)
            else:
                break
        except:
            break
    print("Lost Connection")
    try:
        del games[gameId]
        print("Closing Game ", gameId)

    except:
        pass
    idCount -= 1
    s.close()


while True:
    print("vou receber")
    data6,addr6 = s6.recvfrom(4096)
    #conn, addr = s.accept()
    print("Conectado a : ", addr6)
    idCount += 1
    p = 0
    # o que gameId vai fazer é dizer-nos quando é necessário criar mais um jogo
    # por exemplo se tivermos 6 pessoas apenas precisamos de 3 jogos, com 7 temos de ter +1 e esperar pelo 8º jogador
    # the floor division // rounds the result down to the nearest whole number
    # Se tivermos 4 pessoas, são dois jogos temos então a conta (4-1) // 2 = 3 // 2 = 1, logo vamos no jogo com indice 1 (dois jogos com ids, 0 e 1 )
    gameId = (idCount - 1) // 2

    # se precisamos de criar mais um jogo ou não consoante o número de pessoas
    if idCount % 2 == 1:
        # cria um novo jogo e adiciona ao dic
        games[gameId] = Game(gameId)
        print("Creating a new game: ", gameId)
    else:
        # sendo assim já temos o numero de pessoas certas para começar um jogo, o estado do jogo é de ready
        games[gameId].ready = True
        # current player
        p = 1

    start_new_thread(threaded_client, (s6, p, gameId,addr6))
