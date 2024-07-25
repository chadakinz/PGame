from socket import *
from _thread import *
from table import Table

import sys
import dill as pickle
SERVER = "192.168.1.200"
PORT = 5555
clients = []
s = socket(AF_INET, SOCK_STREAM)
count = 0
table = Table()

try:
    s.bind((SERVER, PORT))

except error as e:
    str(e)

s.listen()
connections = dict()

def thread(conn):
    global count
    count += 1
    print(f'Count: {count}')
    id = count
    if id == 1:
        cards = (150, 500, 200, 500)
        chips = (1000, 600)
        bet = ((400, 600), (600, 600), (800, 600))
    elif id == 2:
        cards = (150, 100, 200, 100)
        chips = (1000, 150)
        bet = ((400, 200), (600, 200), (600, 200))




    player = table.addPlayer(cards, chips, bet)

    connections[player] = conn

    players = dict()
    conn.send(pickle.dumps("connection established"))
    print(f'Inside player {player.id} thread')

    while True:
        #print(f'Inside while loop')
        try:

            #print('Recieving data now...')
            data = pickle.loads(conn.recv(2048))
            #print(f'Data: {data}, dataType: {type(data)}')
            if type(data) == type(player):
                print(f'Updating players')
                for i in range(len(table.players)):
                    if table.players[i].id == data.id:
                        print(f'Player Chips before {table.players[i].chips}')
                        table.players[i] = data
                        player = data
                        print(f'Player Chips after {table.players[i].chips}')
                        conn.send(pickle.dumps(table.players[i]))


            #print(data)
            if data == "PREFLOP":
                for i in range(len(table.players)):
                    if i == table.dealer:
                        table.players[i].isdealer = True

                player.cards = table.deck.deal_cards(2)

                conn.send(pickle.dumps(player))




            if data == "update":

                if len(table.players) == 1:

                    conn.send(pickle.dumps(False))
                else:
                    #print(f'Length of table : {len(table.players)} where players: {table.players}')
                    for i in table.players:
                        if i.id == player.id:
                            pass
                        else:

                            players[i.id] = i



                    reply = players
                    conn.send(pickle.dumps(reply))
            if data == "player":
                #print(f'inside player')
                #print(pickle.pickles(player))
                conn.send(pickle.dumps(player))

            if not data:
                print("No data recieved")
                continue
            else:
                #print(f'Received: {data}')
                #print(f'Sending: {reply}')
                pass
            #conn.sendall(pickle.dumps("message sent."))
        except:
            #print('Connection interrupted')
            continue
    #conn.sendall(pickle.dumps(reply))
    print('Now closing connection')
    conn.close()


while True:

    conn, addr = s.accept()

    print(f'Player {count} connected')
    start_new_thread(thread, (conn, ))


