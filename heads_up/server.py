#FIXME not good for memory to use *
from socket import *
from _thread import *
from table import Table
import sys
import dill as pickle

SERVER = "192.168.1.196"
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
'''This thread sends constant information about the elements of the current game being run to each client'''
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

                    conn.send(pickle.dumps((opp, player, table.pot, table.raise_, table.board)))
    except:
        pass


"""This thread takes the action made by the user and passes it to the table to update the game attributes"""
def thread(conn, player):
    global data, player_turn, round

    connections[player.id] = conn
    opp_id = 1 if player.id == 2 else 2
    print(f'Connection saved: {connections[player.id]} For player: {player.id}')


    while True:

        try:
            data = pickle.loads(conn.recv(2048))
        except:
            continue
        player, action = data[0], data[1]
        table.players[player.id - 1] = player

        print(f'Data received: {data}')

        if action == "Fold":
            print(f'Folded Player {opp_id} wins {table.pot} chips')
            print(f'Chips before: {table.players[opp_id - 1].chips}')
            conn.send(pickle.dumps(True))
            table.players[opp_id - 1].chips += table.pot
            print(f'Chips after: {table.players[opp_id -1].chips}')
            table.pot = 0
            table.reset()

            round = False


        if action == "Raise":

            raise_amnt = table.players[player.id - 1].raise_tot - table.players[opp_id - 1].raise_tot

            if raise_amnt > table.raise_:
                table.raise_ = raise_amnt

            table.pot += table.players[player.id - 1].raise_amnt
            conn.send(pickle.dumps(False))
            player_turn = False
            if table.first_act == False:
                table.first_act = True

        if action == 'Call':

            call_amnt = table.players[opp_id - 1].raise_tot - table.players[player.id - 1].raise_tot
            print(f'Player {opp_id}raised, the call amount is {call_amnt}')
            table.players[player.id - 1].chips -= call_amnt
            table.players[player.id - 1].raise_tot += call_amnt
            table.pot += call_amnt
            if table.shove or table.players[player.id - 1].chips <= 0:
                table.shove = False
                x = table.all_in()
                if x:
                    return

            conn.send(pickle.dumps(True))

            if table.first_act == False:
                player_turn = False

                table.first_act = True
            else:

                round = False

                #turn ends



        if action == "Check":
            conn.send(pickle.dumps(table.players[player.id - 1]))
            if table.first_act == False:
                table.first_act = True
                player_turn = False
            else:
                round = False

        if action == 'All_In':
            if table.players[player.id - 1].raise_tot - table.players[opp_id - 1].raise_tot > table.players[opp_id - 1].chips :
                table.raise_ = table.players[opp_id - 1].chips
                table.pot += table.players[opp_id - 1].chips
                table.players[player.id -1].chips += table.players[player.id - 1].raise_amnt - table.raise_
            else:
                table.raise_ = table.players[player.id - 1].raise_amnt
                table.pot += table.players[player.id - 1].raise_amnt
            table.shove = True
            #table.all_in()
            player_turn = False
            if table.first_act == False:
                table.first_act = True

            pass





#FIXME fix variables and try to find an easier solution

'''
This thread keeps the game running. It is responsible for transitioning 
rounds and sending information to the client when it is its turn to bet

One poker game consists of multiple rounds, where each round has 4 states: preflop, flop, turn, river. 
When a round ends we restart the round loop, and when a player turn ends we go through the list of players
to find the next players turn

'''
def game():
    global player_turn, round

    while True:
        print(f'Transitioning!')
        round = True
        table.transition()
        table.first_act = False

        while round:
            #FIXME only works for two players
            ''' This tracks the dealers position so we know which player is first to act'''
            if table.dealer == 0:
                player_list = table.players
            else:
                player_list = reversed(table.players)
            '''
            
                If a player finishes their turn we find the next player to act
            '''
            for i in player_list:

                table.players[i.id - 1].isTurn = True

                player_turn = True

                connections[i.id].send(pickle.dumps('bet'))

                """After information is sent we wait until the player finishes their turn"""""
                while player_turn:

                    if round == False:
                        break

                    else:
                        table.players[i.id - 1].isTurn = False
                        continue

                else:
                    continue
                break
            else:
                continue
            break







data = None
player_turn = True
round = True
val3 = True
count = 0



'''
Main thread that handles connections. when a connection joins the server it states a purpose which is handled by the server,
the purposes are listed as such: 

opp (#FIXME should not be named opp): Start a thread that sends constant information of the table to the client so it 
can display contents on the screen

player: This thread initializes information about the player; it gives them their ID and card position #FIXME 
(This method only works for 2 players)

else #FIXME (This should be named beter for organization) : This starts a thread connected to an individual client that handles information 
about the betting action of the player

Finally, if there are 2 players, we start the game thread that cycles through the rounds and sends information 
to the clients when it is their turn to act
'''
while True:

    conn, addr = s.accept()

    purpose = pickle.loads(conn.recv(2048))
    print(f'Connected by : {addr} with conn: {conn} with intent: {purpose}')


    if purpose[1] == "opp":
        conn.send(pickle.dumps(None))
        start_new_thread(update, (conn, purpose[0].id, ))

    #fixme can use len of players table to find the position of the current connecting player
    elif purpose[1] == "player":
        count += 1
        print(f'Count: {count}')
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
    #FIXME only works for two players
    if count == 2 and val3:
        print(f'Starting new thread')
        start_new_thread(game, ())
        val3 = False