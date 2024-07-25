from deck import Deck
from player import Player
class Table():
    def __init__(self):
        self.deck  = Deck()
        self.players = []
        self.pot = 0
        self.count = 0
        self.dealer = 0
        self.pot = 0
        self.call_amnt = 0
        self.state = 'PREFLOP'
        self.board = []
    def addPlayer(self, pos):
        self.count += 1
        self.players.append(Player(self.count, pos))
        if self.count == 1:
            self.players[0].isdealer = True
            self.players[0].isTurn = True


        return self.players[-1]

    def change_dealer(self):
        self.dealer += 1
        if self.dealer >= len(self.players):
            self.dealer = 0
        return self.dealer
    def blinds(self, id):
        if self.players[id - 1].isdealer == True:
            self.players[id - 1].chips -= 50
        else:
            self.players[id - 1].chips -= 100

