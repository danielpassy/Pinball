############### Dependências locais
import random
import sys
import src.postgreSQL as postgreSQL

########## definições ##########
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)
RED = (255, 255, 0)
VIOLET = (0, 0, 255)

########## Dependências Externas ##########
import pygame

########## Global variables ##########
global win, X, Y


class Player:
    global win
    y_player_size = 100
    t = 5  # thickness
    XY_player = [0, 0]
    V_player = 7

    def __init__(self, Player_Number):
        self.score = 0

        if Player_Number == 1:
            self.PlayerNumber = 1
            pygame.draw.line(win, VIOLET, (self.t + 1, 250), (self.t + 1, 250 + self.y_player_size),
                             self.t)
            self.XY_player = [self.t + 1, 250]
        else:
            self.PlayerNumber = 0
            pygame.draw.line(win, BLUE, (X - (self.t + 1), 250),
                             (X - (self.t + 1), 250 + self.y_player_size), self.t)
            self.XY_player = [X - (self.t + 1), 250]

    # Write here the position, the rendering, the score

    def mov_down(self):
        if self.XY_player[1] > Y - self.y_player_size:
            return
        self.XY_player = [self.XY_player[0], self.XY_player[1] + self.V_player]

    def mov_up(self):
        if self.XY_player[1] < 0:
            return
        self.XY_player = [self.XY_player[0], self.XY_player[1] - self.V_player]

    @property
    def getPosition(self):
        return self.XY_player

    def getScore(self):
        return self.score

    def addScore(self):
        self.score += 1

    def update(self):
        if self.PlayerNumber == 1:
            pygame.draw.line(win, (0, 0, 255), (self.XY_player[0], self.XY_player[1]),
                             (self.XY_player[0], self.XY_player[1] + self.y_player_size), self.t)
        elif self.PlayerNumber == 0:
            pygame.draw.line(win, (200, 0, 255), (self.XY_player[0], self.XY_player[1]),
                             (self.XY_player[0], self.XY_player[1] + self.y_player_size), self.t)
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
        if self.currentPosition[1] + self.radii < 0:
            self.currentPosition = [self.currentPosition[0], self.currentPosition[1] + self.radii + 2]
            self.velocidadexy[1] = -self.velocidadexy[1]

        # bottom
        if self.currentPosition[1] + self.radii > 600:
            self.currentPosition = [self.currentPosition[0], 600 - self.radii]
            self.velocidadexy[1] = - self.velocidadexy[1]
        # p1
        if self.securecontrol != 1:
            if (p1[1] < self.currentPosition[1] < p1[1] + size) and (
                    p1[0] - 2 < self.currentPosition[0] - self.radii < (
                    p1[0] - self.velocidadexy[0] * self.debugTheBallInt)):
                self.velocidadexy[0] = -self.velocidadexy[0]
                self.securecontrol = 1

        # p2
        if self.securecontrol != 2:
            if (p2[1] - 2 < self.currentPosition[1] < p2[1] + size) and (
                    p2[0] < self.currentPosition[0] + self.radii < p2[0] + self.velocidadexy[0] * self.debugTheBallInt):
                self.velocidadexy[0] = -self.velocidadexy[0]
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


### renova a tela frame a frame
def update(player1, player2, bola, clock, score_render_wrapper):
    win.fill((0, 0, 0))

    score_render_wrapper[0] = score_render_wrapper[2].render(
        "P1: {}    P2: {}".format(player1.getScore(), player2.getScore()),
        True, GREEN, BLACK)
    win.blit(score_render_wrapper[0], score_render_wrapper[1])
    player1.update()
    player2.update()
    bola.update()
    clock.tick(60)


### MAIN, obviously, criação de objetos.
def game():
    global win
    global X
    global Y

    # setup da tela
    pygame.init()
    X = 800
    Y = 600
    win = pygame.display.set_mode((X, Y))

    # initializa o placar
    score_render_wrapper = [0, 0, 0]
    score_render_wrapper[2] = pygame.font.Font('freesansbold.ttf', 32)
    score_render_wrapper[0] = score_render_wrapper[2].render("P1: 0    P2: 0",
                                                             True, GREEN, BLACK)
    score_render_wrapper[1] = score_render_wrapper[0].get_rect()
    score_render_wrapper[1].center = (X // 2, 16)

    # Intialize objects
    Clocker = pygame.time.Clock()
    player1 = Player(1)
    player2 = Player(2)
    bola = Ball()

    ### Main game loop
    while 1:

        #### CONTROLA A BOLA
        bola.checkIfbounces(player1.XY_player, player2.XY_player, Player.y_player_size)
        status = bola.checkifOver()
        if status:
            if status == "player1":
                player1.addScore()
                del bola
                bola = Ball()
            elif status == "player2":
                player2.addScore()
                del bola
                bola = Ball()

        #### recebe comando dos palyers
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
            if event.type == pygame.KEYUP:
                ############## K SALVA O JOGO, AINDA NÃO SAQUEI COMO SALVA COM DUAS TECLAS AO MSM TEMPO KKKKKK ########
                if (event.key == pygame.K_k):
                    save = postgreSQL.generate_save_file(player1.XY_player[0], player2.XY_player[0],
                                                         bola.currentPosition, bola.velocidadexy)
                    postgreSQL.save_file(save)

                if (event.key == pygame.K_l):
                    player1.XY_player[1], player2.XY_player[1], bola.currentPosition[0], bola.currentPosition[1], \
                    bola.velocidadexy[0], bola.velocidadexy[1] = postgreSQL.get_save_file()
        ### update screen
        update(player1, player2, bola, Clocker, score_render_wrapper)
        pygame.display.update()


if __name__ == "__main__":
    game()
