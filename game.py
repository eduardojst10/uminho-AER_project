class Game:
    def __init__(self,id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        #tempo que cada jogador demorou a fazer cada pergunta
        self.times = [None, None]
        self.wins = [0, 0]
        self.ties = 0



    def get_player_move(self, p):
        """
            :param p: [0,1]
            :return: Move
        """
        return self.moves[p]

    # Executa um move, uma jogada
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    # se estamos prontos para começar o jogo, ou seja, se os dois jogadores estão prontos
    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False




