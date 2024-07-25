import pickle
class Player:
    def __init__(self, name, poscards, poschips, posbet):
        self.isdealer = False
        self.chips = 1000
        self.id = name
        self.cards = None
        self.pos = {"chips": poschips, "cards": poscards, 'bet': posbet}
        self.show_cards = False




    def pickilize(self):
        self.cards = pickle.dumps(self.cards)

    def depickilize(self):
        self.cards = pickle.loads(self.cards)

