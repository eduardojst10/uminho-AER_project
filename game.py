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


    def winner(self):
        # verificar por letras os moves e ver
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1  # tie

        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False




