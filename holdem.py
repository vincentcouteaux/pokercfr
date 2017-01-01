from ars import *
from holdem_proba import *

class HoldemHU: #implements game
    @staticmethod
    def deal():
        deck = string2hand(deck_str)
        shuffle(deck)
        return(deck[:4])

