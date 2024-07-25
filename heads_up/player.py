import pickle
class Player:
    def __init__(self, id, pos):
        self.isdealer = False
        self.chips = 1000
        self.raise_tot = 0
        self.raise_amnt = 0
        self.id = id
        self.cards = None
        self.show_cards = False
        self.isTurn = False
        self.pos = pos
    def raise_sequence(self, amount):
        self.raise_tot += amount
        self.chips -= amount
        self.raise_amnt = amount






