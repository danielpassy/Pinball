import datetime
import os


def generate_save_file(P1, P2, bolaXY, bola_speed):
    tempo_atual = datetime.datetime.now()
    tempo_atual = str(tempo_atual)
    print('saved')
    tempo_atual = tempo_atual.replace(":", "-")
    tempo_atual = tempo_atual + '.txt'
    path = os.getcwd()
    if not (os.path.isdir(os.path.join(path, "save"))):
        try:
            os.mkdir(os.path.join(path, "save"))
        except OSError:
            print("Creation of the directory %s failed" % os.path.join(path, "save"))
    currentstate = "P1 {}\nP2 {}\nball_position {} {}\nball_velocity {} {}".format(P1, P2, bolaXY[0], bolaXY[1],
                                                                                   bola_speed[0], bola_speed[1])
    print("Successfully created the directory %s " % os.path.join(path, "save"))
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


# save_game(6, 794, [288, 268], [-0.7147161699707916, -0.22960815220284236])
# path = os.getcwd()
# print(os.path.isdir(os.path.join(path, "save")))

# exempo de saved states
# 6 794 [288, 268] [-0.7147161699707916, -0.22960815220284236]
# 6 794 [192, 66] [-0.8538626488086973, -0.9896400013971334]
# 6 794 [128, -6] [-0.8538626488086973, -0.9896400013971334]
# 6 794 [56, 69] [-0.8538626488086973, 0.9896400013971334]
