from socket import *
from _thread import *
from table import Table
import sys
import dill as pickle

SERVER = "192.168.1.206"
PORT = 5555
clients = []
s = socket(AF_INET, SOCK_STREAM)
count = 0
table = Table()
game_start = False

try:
    s.bind((SERVER, PORT))

except error as e:
    str(e)

s.listen()
connections = dict()

def transition(player):
    if table.state == 'PREFLOP':
        table.players[player.id - 1].cards = table.deck.deal_cards(2)
        table.blinds(player.id)

    elif table.state == 'FLOP':
        pass
    elif table.state == 'TURN':
        pass
    elif table.state == "RIVER":
        pass


def update(conn):
    global count
    id = count
    print(f'id: {id}')
    conn.send(pickle.dumps(True))
    try:
        while True:


            opp_id = 1 if id == 4 else 2

            data = pickle.loads(conn.recv(2048))
            if data == "opp":

                conn.send(pickle.dumps(table.players[opp_id - 1]))
    except:
        pass

def thread(conn):
    global count
    id = count

    if id == 1:
        cards =  ((150, 500), (200, 500))
        chips = (1000, 600)
        bet = ((400, 600), (600, 600), (800, 600))

    elif id == 2:
        cards = ((150, 100), (200, 100))
        chips = (1000, 150)
        bet = ((400, 200), (600, 200), (600, 200))

    pos = {"chips": chips, "cards": cards, 'bet': bet}

    conn.send(pickle.dumps(pos))
    player = table.addPlayer(pos)

    connections[id] = conn

    #if len(connections) == 2:
        #connections[1].send(pickle.dumps(False))


    while True:

        data = pickle.loads(conn.recv(2048))

        if data == "check_player":
            if len(connections) == 2:
                conn.send(pickle.dumps(False))
            else:
                conn.send(pickle.dumps(True))

        if data == "state":
            conn.send(pickle.dumps(table.state))

        if data == 'transition':
            transition(player)
            conn.send(pickle.dumps(True))


        if data == "player":
            conn.send(pickle.dumps(table.players[id - 1]))






count = 0
while True:

    conn, addr = s.accept()

    print(f'Player {count} connected')
    count += 1
    if count < 3:

        start_new_thread(thread, (conn, ))
    else:

        start_new_thread(update, (conn, ))
