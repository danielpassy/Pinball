import datetime
import os



def save_game(p1, p2, bolaXY, bola_speed):
    tempo_atual = datetime.datetime.now()
    currentstate = "p1 {}\np2 {}\nball_position {} {}\nball_velocity {} {}".format(p1, p2, bolaXY[0], bolaXY[1],
                                                                                   bola_speed[0], bola_speed[1])
    tempo_atual = str(tempo_atual)
    print(tempo_atual)
    tempo_atual = tempo_atual.replace(":", "-")
    print(tempo_atual)
    tempo_atual = tempo_atual + '.txt'
    path = os.getcwd()
    path = os.path.join(path, "save", tempo_atual)
    file = open(path, 'x')
    file.write(currentstate)
    # f = open()


def load_save_game(game):
    try:
        file = open('game')
    except FileNotFoundError:
        print("the game was not found")
        return 404

    # reading
    p1 = file.readline()
    p1 = p1.split(" ")
    p2 = file.readline()
    p2 = p2.split(" ")
    ball_position = file.readline()
    ball_position = ball_position.split(" ")
    ball_velocity = file.readline()
    ball_velocity = ball_velocity.split(" ")

    if p1[0] != 'p1' or p2[0] != "p2" or ball_position != "ball_position" or ball_velocity != ball_velocity:
        return 'corrupted file'
    return p1, p2, ball_position, ball_velocity
