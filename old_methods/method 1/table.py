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
    def addPlayer(self, poscards, poschips, posbet):
        self.count += 1
        self.players.append(Player(self.count, poscards, poschips, posbet))

        return self.players[-1]

    def change_dealer(self):
        self.dealer += 1
        if self.dealer >= len(self.players):
            self.dealer = 0
        return self.dealer
