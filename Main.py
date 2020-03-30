import random
import sys
from cgitb import text
from tkinter import font

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)
RED = (255, 255, 0)
VIOLET = (0, 0, 255)

import pygame

global win


def setup():
    pygame.init()
    global win
    global X
    global Y
    X = 800
    Y = 600
    win = pygame.display.set_mode((X, Y))
    # score utility
    score_render_wrapper = [0, 0, 0]
    score_render_wrapper[2] = pygame.font.Font('freesansbold.ttf', 32)
    score_render_wrapper[0] = score_render_wrapper[2].render("P1: 0    P2: 0",
                                                             True, GREEN, BLACK)
    score_render_wrapper[1] = score_render_wrapper[0].get_rect()
    score_render_wrapper[1].center = (X // 2, 16)
    return win, score_render_wrapper


# Cria tela


class Player:
    global win
    YSize_player = 100
    t = 5  # thickness
    XY_player = [0, 0]
    V_player = 7

    def __init__(self, Player_Number):
        self.score = 0

        if (Player_Number == 1):
            self.PlayerNumber = 1
            pygame.draw.line(win, VIOLET, (self.t + 1, 250), (self.t + 1, 250 + self.YSize_player),
                             self.t)
            self.XY_player = [self.t + 1, 250]
        else:
            self.PlayerNumber = 0
            pygame.draw.line(win, BLUE, (X - (self.t + 1), 250),
                             (X - (self.t + 1), 250 + self.YSize_player), self.t)
            self.XY_player = [X - (self.t + 1), 250]

    # Write here the position, the rendering, the score

    def mov_down(self):
        if self.XY_player[1] > Y - self.YSize_player:
            return
        self.XY_player = [self.XY_player[0], self.XY_player[1] + self.V_player]

    def mov_up(self):
        if self.XY_player[1] < 0:
            return
        self.XY_player = [self.XY_player[0], self.XY_player[1] - self.V_player]

    def getPosition(self):
        return self.XY_player

    def getScore(self):
        return self.score

    def addScore(self):
        self.score += 1

        pass
        # pontuacao += 1
        # TODO: fazer o esquema da pontuacao

    def update(self):
        if (self.PlayerNumber == 1):
            pygame.draw.line(win, (0, 0, 255), (self.XY_player[0], self.XY_player[1]),
                             (self.XY_player[0], self.XY_player[1] + self.YSize_player), self.t)
        elif (self.PlayerNumber == 0):
            pygame.draw.line(win, (200, 0, 255), (self.XY_player[0], self.XY_player[1]),
                             (self.XY_player[0], self.XY_player[1] + self.YSize_player), self.t)
        self.getScore()


class Ball:
    currentPosition = []
    velocidadexy = []
    i = 0
    radii = 10
    securecontrol = 3
    debugTheBallInt = 10  # evita que a bola comece com velocdiade 0, ball object não aceita float, para o int metodo não arredondar para 0

    def __init__(self):
        pygame.draw.circle(win, (255, 0, 0), (400, 300), self.radii, 0)
        self.currentPosition = [400, 300]
        while True:
            self.velocidadexy = [random.uniform(-1, 1), random.uniform(-1, 1)]
            if abs(self.velocidadexy[1]) and abs(self.velocidadexy[0]) > 1 / self.debugTheBallInt: break

    def checkIfbounces(self, p1, p2, size):
        # top bounce
        if (self.currentPosition[1] + self.radii < 0):
            self.currentPosition = [self.currentPosition[0], self.currentPosition[1] + self.radii + 2]
            self.velocidadexy[1] = -self.velocidadexy[1]

        # bottom
        if (self.currentPosition[1] + self.radii > 600):
            self.currentPosition = [self.currentPosition[0], 600 - self.radii]
            self.velocidadexy[1] = - self.velocidadexy[1]
        # p1
        if self.securecontrol != 1:
            if (p1[1] < self.currentPosition[1] < p1[1] + size) and (
                    p1[0] - 2 < self.currentPosition[0] - self.radii < (
                    p1[0] - self.velocidadexy[0] * self.debugTheBallInt)):
                print(("a fodelança é {}".format(self.velocidadexy[0] * self.debugTheBallInt)))
                self.velocidadexy[0] = -self.velocidadexy[0]
                print("CARALHOU")
                print(self.velocidadexy[0])
                self.securecontrol = 1

        # TODO: receive position array and check if is the same as the ball
        # p2
        if self.securecontrol != 2:
            if (p2[1] - 2 < self.currentPosition[1] < p2[1] + size) and (
                    p2[0] < self.currentPosition[0] + self.radii < p2[0] + self.velocidadexy[0] * self.debugTheBallInt):
                print(("a fodelança é {}".format(self.velocidadexy[0] * self.debugTheBallInt)))
                self.velocidadexy[0] = -self.velocidadexy[0]
                print("CARALHOU2")
                self.securecontrol = 2

    def checkifOver(self):
        if self.currentPosition[0] < - self.radii:
            return "player1"

        if self.currentPosition[0] > 800 + self.radii:
            return "player2"
        return False

    def update(self):
        # if (self.i > self.paraNaoFoderTudo):
        pygame.draw.circle(win, (255, 0, 0),
                           (self.currentPosition[0] + int(self.debugTheBallInt * self.velocidadexy[0]),
                            self.currentPosition[1] + int(self.debugTheBallInt * self.velocidadexy[1])), 10, 0)
        self.currentPosition = [self.currentPosition[0] + int(self.debugTheBallInt * self.velocidadexy[0]),
                                self.currentPosition[1] + int(self.debugTheBallInt * self.velocidadexy[1])]
    #     self.i = 0
    # else:
    #     self.i += 1
    #     pygame.draw.circle(win, (255, 0, 0),
    #                        (self.currentposition[0], self.currentposition[1]), 10, 0)
    # pass


class controle():
    def atualizar(self, player1, player2, bola, clock, score_render_wrapper):
        win.fill((0, 0, 0))

        score_render_wrapper[0] = score_render_wrapper[2].render(
            "P1: {}    P2: {}".format(player1.getScore(), player2.getScore()),
            True, GREEN, BLACK)
        win.blit(score_render_wrapper[0], score_render_wrapper[1])
        player1.update()
        player2.update()
        bola.update()
        clock.tick(60)

        # TODO: add more funcionalities


### MAIN, obviously, criação de objetos.
def main():
    win, score_render_wrapper = setup()

    Clocker = pygame.time.Clock()
    player1 = Player(1)
    player2 = Player(2)
    bola = Ball()
    mastercontrol = controle()
    ### Main game loop

    # check posição da bola
    while (1):
        bola.checkIfbounces(player1.XY_player, player2.XY_player, Player.YSize_player)
        status = bola.checkifOver()
        if (status != False):
            if (status == "player1"):
                player1.addScore()
                del bola
                bola = Ball()
            elif (status == "player2"):
                player2.addScore()
                del bola
                bola = Ball()

        # Check comando pressionado
        state = pygame.key.get_pressed()
        if state[pygame.K_DOWN]:
            player2.mov_down()
        if state[pygame.K_UP]:
            player2.mov_up()
        if state[pygame.K_s]:
            player1.mov_down()
        if state[pygame.K_w]:
            player1.mov_up()
        ### EXIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("tshau")
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        ### update screen
        mastercontrol.atualizar(player1, player2, bola, Clocker, score_render_wrapper)
        pygame.display.update()


main()
