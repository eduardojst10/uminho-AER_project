from typing import NewType
import pygame
from network import Network

# add a font
pygame.font.init()

withd = 800
height = 800

win = pygame.display.set_mode((withd, height))

pygame.display.set_caption("clientNode")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 35)
        text = font.render(self.text, True, (255, 255, 255))
        # centrar
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
    win.fill((128, 128, 128))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Wainting for Player...", True, (255, 0, 0), True)
        win.blit(text, (withd / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your move", True, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Player 2", True, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, True, (0, 0, 0))
            text2 = font.render(move2, True, (0, 0, 0))

        else:
            if game.p1Went and p == 0:  # se somos o jogador 0 e já jogamos apresenta a nossa jogada
                text1 = font.render(move1, True, (0, 0, 0))
            elif game.p1Went:  # se somos o jogador 1 e o jog 0 já foi então o move do outro jogador é apresentado como Locked In
                text1 = font.render("Locked In", True, (0, 0, 0))

            else:  # caso contrário ficamos à espera de qualquer move
                text1 = font.render("Wainting...", True, (0, 0, 0))

            if game.p2Went and p == 1:  # se somos o jogador 1 e já jogamos apresenta a nossa jogada
                text2 = font.render(move2, True, (0, 0, 0))
            elif game.p2Went:  # se somos o jogador 0 e o jog 1 já foi então o move do outro jogador é apresentado como Locked In
                text2 = font.render("Locked In", True, (0, 0, 0))

            else:  # caso contrário ficamos à espera de qualquer move
                text2 = font.render("Wainting...", True, (0, 0, 0))

        # o modo como é apresentado o texto varia de jogador em jogador
        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))

        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)
    pygame.display.update()


# butões do menu
btns = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (255, 0, 0)),
        Button("Paper", 450, 500, (0, 255, 0))]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    # sabemos qual o jogador
    player = int(n.getP())
    print("You are player: ", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")  # dar reset para jogarmos as próximas rondas
            except:
                run = False
                print("Couldnt get game")
                break

            # Apresentação de resultado
            font = pygame.font.SysFont("comicsans", 90)

            # verifica que jogador sou e se sou o winner
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won!", True, (255, 0, 0))

            elif game.winner() == -1:
                text = font.render("Tie Game!", True, (255, 0, 0))

            else:
                text = font.render("You Lost...", True, (255, 0, 0))

            win.blit(text, (withd/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)  # tempo que fica

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # se clicaram no botão essq, meio ou dir
                pos = pygame.mouse.get_pos()  # se sim, vamos buscar a posicao onde clicaram
                for btn in btns:
                    # game.connectd() - para não fazer um move caso o outro jogador não esteja conectado
                    if btn.click(pos) and game.connected():
                        # check what our current player is
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)

                        else:
                            if not game.p2Went:
                                n.send(btn.text)
        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    bplay = Button("Play Game", 50, 100, (255, 0, 0))
    bquit = Button("Quit Game", 50, 200, (255, 0, 0))

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))

        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Welcome to AER Trivia! Click to Play!", True, (255, 0, 0))
        win.blit(text, (100, 350))

        # botões de Menu
        bplay.draw(win)
        bquit.draw(win)

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
