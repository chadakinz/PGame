
import random
import numpy as np
class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number


class Deck:
    def __init__(self):
        self.cards = list()
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        for suit in suits:
            for i in range(2, 15):
                self.cards.append(Card(suit, i))
        self._removedCards = []
        #self._cards = {'Clubs': {}, 'Spades': {}, 'Hearts': {}, 'Diamonds': {}}


        #for i in self._cards.keys():
            #for x in range(2, 15):
                #self._cards[i].add(x)
    def remove_card(self, card):
        self.cards.remove(card)
        self._removedCards.append(card)

    def deal_cards(self, num):
        cards = []
        np.random.shuffle(self.cards)
        print(self.cards)
        for i in range(num):
            x = random.choice(self.cards)
            cards.append(x)
            self.remove_card(x)
        return cards
    def choose_cards(self):
        pass

    def shuffle(self):
        if len(self._removedCards) == 0:
            np.random.shuffle(self.cards)
        else:
            for i in self._removedCards:
                self.cards.append(i)
            self._removedCards = []
            np.random.shuffle(self.cards)

    def __str__(self):
        deck = ""
        deck += f'CARDS INSIDE: {len(self.cards)}'
        for i in self.cards:
            deck += f'Suit: {i.suit} - Number: {i.number}\n'

        return deck

