import pygame
from networkProtocol import Network

# add a font

pygame.font.init()
bg = pygame.image.load("menu_img.jpg")
width = 750
height = 750
bts = []
win = pygame.display.set_mode((width, height))

pygame.display.set_caption("clientNode")


class Button:
    def __init__(self, text, x, y, color, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, win, font):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0, 3, 3, 3, 3)
        font = pygame.font.SysFont("Cambria", font)
        text = font.render(self.text, True, (255, 255, 255))
        # centrar no meio do button
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    # pos : tuplo de x,y da posicao do rato
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    global btns
    win.blit(bg, (0, 0))

    if not (game.connected()):
        font = pygame.font.SysFont("Cambria", 50)
        text = font.render("Wainting for Player...", True, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

    else:

        # CAIXA TEXTO - Titulo jogo
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("AER TRIVIA", True, (255, 0, 0))
        text_rect = text.get_rect(center=(width / 2, (height / 2) - 300))
        win.blit(text, text_rect)

        if game.bothWent() :  # se somos o jogador 0 e já jogamos apresenta a nossa jogada
            font = pygame.font.SysFont("Cambria", 90)
            # verifica que jogador sou e se sou o winner
            if (game.winner() == 1 and p == 1) or (game.winner() == 0 and p == 0):
                text = font.render("You won!", True, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", True, (255, 0, 0))

            else:
                text = font.render("You Lost...", True, (255, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)  # tempo que fica

        elif game.p2Went and p == 1:  # se somos o jogador 1 e já jogamos apresenta a nossa jogada
            text2 = font.render("Wainting for oppenent to finish", True, (0, 0, 0))
            text_rect2 = text.get_rect(center=(width / 2, (height / 2) - 200))
            win.blit(text2, text_rect2)

        elif game.p1Went and p == 0 :
            text1 = font.render("Wainting for oppenent to finish", True, (0, 0, 0))
            text_rect1 = text.get_rect(center=(width / 2, (height / 2) - 200))
            win.blit(text1, text_rect1)

        else:  # caso contrário ficamos à espera de qualquer move

            # CAIXA TEXTO para questão
            font = pygame.font.SysFont("Cambria", 30)
            # Current question do jogador p
            text = font.render(game.currentQuestion(p).encode('utf-8').rstrip(), True, (0, 0, 0))
            text_rect = text.get_rect(center=(width / 2, (height / 2) - 200))
            win.blit(text, text_rect)

            options = game.questions_options[game.current[p]]

            # Update de botões
            btns = [Button("1. " + options[0], 210, 250, (191, 20, 20), 400, 50),
                    Button("2. " + options[1], 210, 350, (191, 20, 20), 400, 50),
                    Button("3. " + options[2], 210, 450, (191, 20, 20), 400, 50),
                    Button("4. " + options[3], 210, 550, (191, 20, 20), 400, 50)]

            for btn in btns:
                btn.draw(win, 35)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    print("Já iniciei a comunicacao")


    # sabemos qual o jogador
    player = n.getP()
    print("És o jogador: ", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get Game")
            break

        # Dois jogadores acabaram
        if game.bothWent():
            redrawWindow(win, game, player)
            try:
                game = n.send("reset")  # dar reset para novo jogo
                run = False
                #pygame.quit()
            except:
                run = False
                print("Couldn't get game")
                break

        if (player == 0 and game.p1forward) or (player == 1 and game.p2forward):
            # pygame.time.delay(500)
            try:
                game = n.send("resetForward")  # dar reset para avançarmos para a próxima pergunta
                redrawWindow(win, game, player)
            except:
                run = False
                print("Couldn't get game")
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # se clicaram no botão essq, meio ou dir
                pos = pygame.mouse.get_pos()  # se sim, vamos buscar a posicao onde clicaram
                for btn in btns:
                    # game.connectd() - para não fazer um move caso o outro jogador não esteja conectado
                    if btn.click(pos) and game.connected():
                       print(btn.text)
                       n.send(btn.text[0])
                       print("CLIQUEI NO BOTAO", btn.text[0])

        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    # text_rect = text.get_rect(center=(width / 2, (height / 2) - 200))
    bplay = Button("Play Game", 315, 250, (255, 0, 0),150,100)
    bquit = Button("Quit", 315, 400, (255, 0, 0),150,100)

    while run:
        clock.tick(60)
        # win.fill((128, 128, 128))
        win.blit(bg, (0, 0))


        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Welcome to AER TRIVIA!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(width / 2, (height / 2)-200))
        win.blit(text, text_rect)

        # botões de Menu
        bplay.draw(win, 30)
        bquit.draw(win, 30)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if bplay.click(pos):
                    run = False
                elif bquit.click(pos):
                    pygame.quit()
                    run = False
                else:
                    pass

    main()


while True:  # Caso o alguém se desconecte vamos manter a main a correr
    menu_screen()


# PARA TESTAR MAIS RAPIDAMENTE
#while True:
 #   main()
