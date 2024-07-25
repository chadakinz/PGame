import pickle
class Player:
    def __init__(self, name, pos):
        self.isdealer = False
        self.chips = 1000
        self.id = name
        self.cards = None
        self.show_cards = False
        self.isTurn = False
        self.pos = pos
        self.defer = False




