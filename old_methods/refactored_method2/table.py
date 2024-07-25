from deck import Deck
from player import Player
class Table():
    def __init__(self):
        self.deck  = Deck()
        self.players = []
        self.pot = 0
        self.count = 0
        self.dealer = 1
        self.pot = 0
        self.raise_amnt = 100
        self.state = 'PREFLOP'
        self.board = []
        self.raise_tot = 150
    def addPlayer(self, pos):
        self.count += 1
        self.players.append(Player(self.count, pos))
        if self.count == 1:
            self.players[0].isdealer = True
            self.players[0].isTurn = True


        return self.players[-1]

    #Fixme method only works for 2 players
    def change_dealer(self):
        self.dealer = 1 if self.dealer == 0 else 0
        first_act = 1 if self.dealer == 0 else 0
        self.players[first_act].isTurn = True

        return self.dealer
    def blinds(self, id):
        if id - 1 == self.dealer:
            self.players[id - 1].chips -= 100
            self.players[id - 1].raise_amnt += 100
            self.pot += 100


        else:
            self.players[id - 1].chips -= 50
            self.players[id - 1].raise_amnt += 50
            self.pot += 50

    def reset(self):
        self.change_dealer()
        self.deck.replace_cards()
        for i in range(len(self.players)):
            self.players[i].cards = None
            self.players[i].raise_amnt = 0

        self.board = []



