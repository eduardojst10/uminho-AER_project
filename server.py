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
server = "127.0.0.1"
port = 55550


# criação de socket para ipv4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

# vai começar a ouvir
s.listen(2)
print("Waiting for connection, Server Started for Game")

connected = set()
# store ids de games
games = {}
# keep track dos jogos
idCount = 0


# player vai ser o nr de jogador 1 ou 0 - current player
def threaded_client(conn, p, gameId):
    # este idCount server para verificar casos como um jogador abandonar um jogo a meio
    global idCount

    conn.send(str.encode(str(p)))  # vamos enviar que jogador somos [0,1]

    reply = ""
    while True:  # vamos ter 3 opções: um get do jogo do server, um reset ou então um move (pedra ,papel, tesoura) e verificar se o jogo ainda existe
        try:
            data = conn.recv(4096).decode()
            if gameId in games:  # verificar se o jogo ainda existe e se algum cliente não desconectou mais cedo
                game = games[gameId]

                if not data:
                    break

                else:
                    if data == "reset":
                        game.resetWent()

                    elif data != "get":
                        game.play(p, data)

                    # de qualquer forma ele vai sempre dar dump ao jogo para o cliente
                    conn.sendall(pickle.dumps(game))
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
    conn.close()


while True:
    conn, addr = s.accept()
    print("Conectado a : ", addr)
    idCount += 1
    p = 0

    # por exemplo se tivermos 6 pessoas apenas precisamos de 3 jogos, com 7 temos de ter +1 e esperar pelo 8.º jogador
    # the floor division // rounds the result DOWN to the nearest whole number
    # Se tivermos 4 pessoas, são dois jogos temos então a conta (4-1) // 2 = 3 // 2 = 1
    # logo vamos no jogo com indice 1 (dois jogos com ids, 0 e 1 )

    # o que gameId vai fazer é dizer-nos quando é necessário criar mais um jogo,
    gameId = (idCount - 1) // 2

    # se precisamos de criar mais um jogo ou não consoante o número de pessoas
    if idCount % 2 == 1:
        # cria um novo jogo e adiciona ao dic
        games[gameId] = Game(gameId)
        print("Creating a new game: ", gameId)
    else:
        # sendo assim já temos o número de pessoas certas para começar um jogo, o estado do jogo é de ready
        games[gameId].ready = True
        # current player
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
