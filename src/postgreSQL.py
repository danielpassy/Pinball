import psycopg2
import datetime
import os


def generate_save_file(P1, P2, bolaXY, bola_speed):
    tempo_atual = str(datetime.datetime.now())
    tempo_atual = tempo_atual.replace(":", "-")
    save = """INSERT INTO saved VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(tempo_atual, P1, P2,
                                                                                           bolaXY[0], bolaXY[1],
                                                                                           bola_speed[0],
                                                                                           bola_speed[1])
    print(save)
    return save


# connect to the db, hopefully
def save_file(save):
    try:
        f = open('password.txt', 'r')
        password = f.read()
        connection = psycopg2.connect(
            host='localhost',
            database='pythonic',
            user='postgres',
            password=password)
        # TODO: testar para ver se esta conexão funciona, verificando se gera o password corretamente

        cursor = connection.cursor()
        cursor.execute(save)
        connection.commit()
        print('salvo de maneira bem sucedida')


    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to insert record into saved table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def get_save_file():
    try:
        f = open('password.txt', 'r')
        password = f.read()
        connection = psycopg2.connect(
            host='localhost',
            database='pythonic',
            user='postgres',
            password=password)

        # get the name list form the DB
        cursor = connection.cursor()
        cursor.execute("""SELECT game_name FROM saved""")
        game_names = cursor.fetchall()
        count = cursor.rowcount
        # game_names = list(sum(game_names, ()))
        # print(game_names)

        # Input. which game user wants and try to match
        for i in game_names:
            print(game_names)
        try:
            game_index = int(input('qual destes você quer loadar? digite o número crrespondente\n'))
            query = """SELECT * FROM saved WHERE game_name = '{}'""".format(game_names[game_index][0])
            cursor2 = connection.cursor()
            cursor2.execute(query)
            data = cursor2.fetchall()
            print(data)
            print("deu certo")
            return data
        except IndexError:
            print("Não existe esse jogo")
        finally:
            cursor2.close()

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to insert record into saved table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    # save_file = generate_save_file(6, 794, [288, 268], [-0.7147161699707916, -0.22960815220284236])
    # save = get_save_file()
    # print(save)
    save = generate_save_file(6, 794, [288, 268], [-0.7147161699707916, -0.22960815220284236])
    save_file(save)
