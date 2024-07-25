from deck import Deck
from player import Player
from list import List
from phevaluator.evaluator import evaluate_cards
import math
class Table():
    def __init__(self):
        self.deck  = Deck()
        self.players = []
        self.pot = 0
        self.count = 0
        self.dealer = 0
        self.pot = 0
        self.raise_ = 100
        self.state = 'PREFLOP'
        self.board = []
        self.raise_tot = 150
        self.first_act = False
        self.shove = False
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
    def blinds(self):
        print(f'Blinds are set!')
        for id in range(len(self.players)):
            if id  == self.dealer:
                self.players[id].chips -= 50
                self.players[id].raise_tot += 50
                self.pot += 50



            else:
                self.players[id].chips -= 100
                self.players[id].raise_tot += 100
                self.pot += 100

    def reset(self):
        self.change_dealer()
        self.deck.replace_cards()
        for i in range(len(self.players)):
            self.players[i].cards = None
            self.players[i].raise_tot = 0

        self.board = []
        self.state = 'PREFLOP'
        self.pot = 0
        self.raise_ = 100

    def transition(self):
        if self.state == 'PREFLOP':
            for i in range(len(self.players)):
                self.players[i].cards = self.deck.deal_cards(2)
            self.blinds()
            self.state = 'FLOP'



        elif self.state == 'FLOP':
            print(f'pot amount when entering flop: {self.pot}')

            for i in range(len(self.players)):
                self.players[i].raise_tot = 0

            burn_card = self.deck.deal_cards(1)
            self.board = self.deck.deal_cards(3)
            self.state = 'TURN'

        elif self.state == 'TURN':
            burn_card = self.deck.deal_cards(1)
            for i in range(len(self.players)):
                self.players[i].raise_tot = 0
            self.board.append(self.deck.deal_cards(1)[0])
            self.state = 'RIVER'

        elif self.state == 'RIVER':
            burn_card = self.deck.deal_cards(1)
            for i in range(len(self.players)):
                self.players[i].raise_tot = 0
            self.board.append(self.deck.deal_cards(1)[0])
            self.state = 'GO_NEXT'
        elif self.state == 'GO_NEXT':
            winner = self.evaluate()
            if winner == 1:
                self.players[0].chips += self.pot
            elif winner == 2:
                self.players[1].chips += self.pot
            else:
                chips = math.floor(self.pot/2)
                remainder = self.pot - (2 * chips)
                for i in range(len(self.players)):
                    self.players[i].chips += chips
                self.players[0].chips += remainder
            self.reset()
            for i in range(len(self.players)):
                self.players[i].cards = self.deck.deal_cards(2)
            self.blinds()
            self.state = 'FLOP'
        self.raise_ = 100
        self.first_act = False




    def evaluate(self):
        suit = {'Clubs': 'c', 'Hearts': 'h', 'Spades': 'S', 'Diamonds': 'd'}
        rank = {i:i for i in range(2, 10)}
        rank2 = {10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        rank.update(rank2)
        player1 = self.players[0].cards + self.board
        player2 = self.players[1].cards + self.board
        print(rank)
        print(self.board)
        print(player1)
        print(player2)
        for i in range(len(player1)):

            player1[i] = str(rank[player1[i].number]) + str(suit[player1[i].suit])
            player2[i] = str(rank[player2[i].number]) + str(suit[player2[i].suit])

        p1 = evaluate_cards(player1[0], player1[1], player1[2], player1[3], player1[4], player1[5], player1[6])
        p2 = evaluate_cards(player2[0], player2[1], player2[2], player2[3], player2[4], player2[5], player2[6])
        if p1 < p2: return self.players[0].id
        elif p1 > p2: return self.players[1].id
        else: return 3
    def all_in(self):
        while len(self.board) <= 5:
            self.board += self.deck.deal_cards(1)

        winner = self.evaluate()

        if winner == 1:
            self.players[0].chips += self.pot
        elif winner == 2:
            self.players[1].chips += self.pot
        else:
            chips = math.floor(self.pot / 2)
            remainder = self.pot - (2 * chips)
            for i in range(len(self.players)):
                self.players[i].chips += chips
            self.players[0].chips += remainder
        if self.players[0].chips != 0 and self.players[1].chips != 0:
            self.reset()
        else:
            return True

    pass