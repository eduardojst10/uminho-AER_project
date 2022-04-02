class Game:
    def __init__(self, id):
        # estados de jogo para cada jogador e para o jogo em si
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id

        # estados de perguntas para cada jogador: flags de avanço
        self.p1forward = False
        self.p2forward = False

        # Variáveis que vou precisar para trivia quiz
        # tempo total que cada jogador demorou a fazer o questionário

        self.moves = [None, None] # respostas atuais de cada jogador
        self.current = [0,0] # acho que vou ter de ter o current para dois jogadores
        self.total = 0 # total de questões
        self.answers = {} # número da questão e número da resposta certa
        self.times = [None, None] # tempo que cada jogador demorou a realizar o jogo
        self.points = [0, 0]  # Pontos de cada jogador
        self.questions_options = {}
        self.total = 0

        f = open("trivia_gameSHORT_TEST.txt", "r")
        trivia_data = f.readlines()
        f.close()

        quest_bool = 0
        i = 0
        options = []
        for text_line in trivia_data:
            i += 1
            if quest_bool == 0:
                options = []
                self.answers.update({text_line.rstrip(): int(trivia_data[i + 4])})
                self.total += 1
                quest_bool = 6

            else:
                options.append(text_line.rstrip())
                self.questions_options.update({self.total - 1: options})
            quest_bool -= 1

        self.questOrd = list(self.answers)

    # Player responde a uma questão
    def play(self, player, choice):
            self.moves[player] = choice

            answer = int(choice)
            print("SOU O JOGADOR ", player)
            if answer == self.answers[self.questOrd[self.current[player]]]:
             if player == 0:
                    self.points[0] += 10
             else:
                    self.points[1] += 10

            self.forwardPlayer(player)

    # Método que passa para a próxima pergunta no current player
    def nextQuestion(self,player):
        self.current[player] += 1

    # Método que obtém a pergunta atual para o player que avançou
    def currentQuestion(self,player):
        return self.questOrd[self.current[player]]

    # Método Tag que indica ao jogo para avançar pergunta num determinado jogador
    def forwardPlayer(self, player):
        if self.current[player] == self.total-1:
            print("Jogador ",player, "já acabou quizz")
            if player == 0:
                self.p1Went = True
                print("O Jogador obteve os seguintes pontos:", self.points[0])
            else:
                self.p2Went = True
                print("O Jogador obteve os seguintes pontos:", self.points[1])

        else:
            if player == 0:
                print("vou para próxima pergunta no Jogador 0")
                self.p1forward = True
            else:
                print("vou para próxima pergunta no Jogador 1")
                self.p2forward = True

    # Método que permite ao Jogador player avança para a próxima pergunta e dar reset às flags de avanço de pergunta
    def resetForward(self, player):
        self.nextQuestion(player)
        if player == 0:
            self.p1forward = False
        else:
            self.p2forward = False

    # Método que verifica se estamos prontos para começar o jogo, ou seja, se os dois jogadores estão prontos
    def connected(self):
            return self.ready

    # Método que verifica se ambos os jogadores acabaram a ronda do quiz
    def bothWent(self):
            return self.p1Went and self.p2Went

    # Método que quando acaba o quizz para os dois jogadores dá rest ao jogo para o menu deste
    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

    # método que define o winner do jogo
    # 1 métrica: pontos
    # 2 métrica: tempo
    def winner(self):
        if self.bothWent():
            points1 = self.points[0]
            points2 = self.points[1]

            time1 = self.times[0]
            time2 = self.times[1]

            if points1 > points2:
                winner = 0
            elif points2 > points1:
                winner = 1
            else:
                if time1 > time2:
                    winner = 0
                elif time2 > time1:
                    winner = 1

                else:
                    winner = -1
        else:
            winner = 2

        return winner





