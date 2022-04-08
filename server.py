import pickle
import socket
import threading
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
server = "fe80::b042:9587:8d2d:7d69%20"
port = 55550

# criação de socket para ipv6 e UDP
s6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
try:
    s6.bind((server,port))
except socket.error as e:
    print(e)
print("Waiting for connection, Server Started for AER Trivia Game")

# store ids de games
games = {}
# keep track dos jogos
idCount = 0

# player vai ser o nr de jogador 1 ou 0 - current player
def threaded_client(s, p, gameId,addr,data6):
    # este idCount server para verificar casos como um jogador abandonar um jogo a meio
    global idCount
    data = data6.decode('utf-8')

#while True:  # vamos ter 3 opções: um get do jogo do server, um resetForward uma answer à questão
    #try:
        #data = s.recvfrom(4096*4,addr).decode()

    if gameId in games:  # verificar se o jogo ainda existe e se algum cliente não desconectou mais cedo
        game = games[gameId]

        if not data:
            print("Data Invalid")

        else:
            if data == "leave":
                # do something
                print("Recebi leave")
                game.stopForward = True
                print("Lost Connection")
                try:
                   del games[gameId]
                   print("Closing Game ", gameId)

                   for address in activeP_game[gameId]:
                        players_num.pop(address)
                        players_threads.pop(address)
                        players_game.pop(address)
                   activeP_game.pop(gameId)
                except:
                    pass
                idCount -= 2

            elif data == "client":
                s.sendto(str.encode(str(p)), addr)  # vamos enviar que jogador somos [0,1]

            elif data == "reset":
                print("--------------------------------------------------")
                print("-Got a reset from", p)
                game.resetWent()


                try:
                    del games[gameId]
                    print("Closing Game ", gameId)
                    for address in activeP_game[gameId]:
                        players_num.pop(address)
                        players_threads.pop(address)
                        players_game.pop(address)
                    activeP_game.pop(gameId)
                except:
                    pass
                idCount -= 1

            elif data == "resetForward":
                print("-Got a resetForward from", p)
                game.resetForward(p)
                print("Jogador ", p, "está na questão: ", game.currentQuestion(p))
                print("--------------------------------------------------")
            elif data != "get":
                print("----------------------RESPOSTA from", p,"-----------")
                print("-Got an answer from ", p)
                game.play(p, data)




            s.sendto(pickle.dumps(game),addr)
    else:
        print("No game")
            #break
    #except:
        #break
#print("Lost Connection")
#try:
    #   del games[gameId]
    #  print("Closing Game ", gameId)

#except:
    #   pass
    #idCount -= 1
    #s.close()

# Thread por pedido de um player
players_threads = {}

# Número de jogador de um player em qualquer jogo
players_num = {}

# Id de jogo de cada player
players_game = {}

activeP_game = {}


while True:
    #Começo de comunicação com clientes/players
    try:
        data6, addr6 = s6.recvfrom(4096)

        # De modo a não criar sempre jogos
        if addr6 in players_threads:
            thr = threading.Thread(target=threaded_client, args=(s6, players_num[addr6], players_game[addr6], addr6,data6))
            players_threads[addr6] = thr
            players_threads[addr6].start()

        else:
            idCount += 1
            print("--------------------------------------------------")
            print("Conectado a : ", addr6, ", IDCOUNT de :", idCount)
            print("--------------------------------------------------")
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

            # Player Number
            players_num[addr6] = p

            # Id de jogo do player
            players_game[addr6] = gameId

            #Controlo de dos dois clientes por jogo
            if gameId not in activeP_game:
                activeP_game[gameId] = [addr6]

            else:
                activeP_game[gameId].append(addr6)

            thr = threading.Thread(target=threaded_client, args=(s6, p, gameId, addr6, data6))
            players_threads[addr6] = thr
            players_threads[addr6].start()

    except:
        pass