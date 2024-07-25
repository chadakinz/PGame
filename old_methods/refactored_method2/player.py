import pickle
class Player:
    def __init__(self, id, pos):
        self.isdealer = False
        self.chips = 1000
        self.raise_amnt = 0
        self.id = id
        self.cards = None
        self.show_cards = False
        self.isTurn = False
        self.pos = pos
        self.new_raise = 0
        self.raise_amnt2 = 0




