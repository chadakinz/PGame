from socket import *
from _thread import *
from table import Table
import sys
import dill as pickle

SERVER = "192.168.1.9"
PORT = 5556
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
def bet_phase(conn, id):
    conn.send(pickle.dumps(None))
    end = True
    first_act = False
    opp_id = 1 if id == 2 else 2
    while end:
        data = pickle.loads(conn.recv(2048))
        print(f'data0 = {data[0]}, data1 = {data[1]}')
        if data[1] == 'Reset':
            return

        if data[0] is None:
            continue

        table.players[id - 1] = data[0]


        if data[1] == 'Fold':
            print(f'someone folded')

            table.players[opp_id - 1].chips += table.pot
            table.pot = 0
            for i in connections.values():
                i.send(pickle.dumps('Reset'))
            table.reset()
            table.state = ('PREFLOP')
            return
        if data[1] == 'Call':
            call_amnt = table.pot - table.players[id - 1].raise_amnt
            print(f'call = {call_amnt}')
            table.players[id - 1].chips -= call_amnt
            table.pot += call_amnt
            for i in connections.values():
                i.send(pickle.dumps('Call'))

        if data[1] == 'Raise':
            if data[0].new_raise > table.raise_amnt:
                table.raise_amnt = data[0].new_raise

            table.players[id - 1].chips -= data[0].raise_amnt2
            table.pot += data[0].raise_amnt2

            if data[0].new_raise > table.raise_amnt:
                table.raise_amnt = data[0].new_raise
            for i in connections.values():
                i.send(pickle.dumps('Raise'))






        elif data[1] == 'raise':
            pass
        elif data[1] == 'check':
            pass
        elif data[1] == 'call':
            pass
    pass
def transition(player):
    if table.state == 'PREFLOP':
        table.players[player.id - 1].cards = table.deck.deal_cards(2)
        table.blinds(player.id)
        table.state = 'FLOP'

    elif table.state == 'FLOP':
        burn_cards = table.deck.deal_cards(1)
        flop = table.deck.deal_cards(3)
        table.board = flop
        table.raise_tot = 0
        table.raise_amnt = 100
        for i in range(len(table.players)):
            table.players[i].raise_amnt = 0
            table.players[i].raise_amnt2 = 0
            table.players[i].new_raise = 0
            if i == table.dealer:
                table.players[i].isTurn = False
            else:
                table.players[i].isTurn = True
        table.state = 'TURN'


        pass
    elif table.state == 'TURN':
        pass
    elif table.state == "RIVER":
        pass


def update(conn, id):


    try:

        while True:
            data = pickle.loads(conn.recv(2048))




            opp_id = 1 if id == 2 else 2


            if data == "opp":
                if len(table.players) < 2:
                    conn.send(pickle.dumps(False))
                else:
                    opp = table.players[opp_id - 1]
                    player = table.players[id - 1]

                    conn.send(pickle.dumps((opp, player, table.pot, table.raise_amnt, table.board)))
    except:
        pass

def thread(conn, player):


    connections[player.id] = conn

    #if len(connections) == 2:
        #connections[1].send(pickle.dumps(False))
    print(player)

    while True:


        data = pickle.loads(conn.recv(2048))
        print(f'Data received: {data}')


        if data == "check_players":
            if len(table.players) == 2:
                conn.send(pickle.dumps(False))
            else:
                conn.send(pickle.dumps(True))

        if data == "state":
            conn.send(pickle.dumps(table.state))

        if data == 'transition':
            transition(player)
            conn.send(pickle.dumps(True))


        if data == "player":
            conn.send(pickle.dumps(table.players[player.id - 1]))

        if data == 'betting':
            bet_phase(conn, player.id)







count = 0
while True:

    conn, addr = s.accept()
    print(f'Connection received')
    purpose = pickle.loads(conn.recv(2048))
    print(f'Connected by : {addr} with conn: {conn} with intent: {purpose}')




    if purpose[1] == "opp":
        conn.send(pickle.dumps(None))
        start_new_thread(update, (conn, purpose[0].id, ))

    #fixme can use len of players table to find the position of the current connecting player
    elif purpose[1] == "player":
        count += 1
        if count == 1:
            cards = ((150, 500), (200, 500))
            chips = (1000, 600)
            bet = ((400, 600), (600, 600), (800, 600))

        elif count == 2:
            cards = ((150, 100), (200, 100))
            chips = (1000, 150)
            bet = ((400, 200), (600, 200), (800, 200))

        pos = {"chips": chips, "cards": cards, 'bet': bet}

        player = table.addPlayer(pos)
        conn.send(pickle.dumps(player))
    else:
        conn.send(pickle.dumps(None))

        start_new_thread(thread, (conn, purpose[0], ))
