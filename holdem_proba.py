import numpy as np
from scipy.misc import comb

class Color:
    spade = 0
    heart = 1
    diamond = 2
    club = 3

class CardValue:
    A = 14
    K = 13
    Q = 12
    J = 11
    T = 10

class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

def string2hand(string):
    out = []
    for c in xrange(0, len(string), 2):
        value, color = string[c:c+2]
        if value == 'A':
            value = CardValue.A
        elif value == 'K':
            value = CardValue.K
        elif value == 'Q':
            value = CardValue.Q
        elif value == 'J':
            value = CardValue.J
        elif value == 'T':
            value = CardValue.T
        else:
            value = int(value)
        if color == 's':
            color = Color.spade
        if color == 'h':
            color = Color.heart
        if color == 'd':
            color = Color.diamond
        if color == 'c':
            color = Color.club
        out.append(Card(value, color))
    return out

def hand_value(hand):
    #check for flush:
    color_sort = {Color.spade: [], Color.heart: [], Color.diamond: [], Color.club: []}
    for card in hand:
        color_sort[card.color].append(card.value)
    for color in color_sort:
        if len(color_sort[color]) >= 5: #Flush
            if CardValue.A in color_sort[color]:
                color_sort[color].append[1]
            color_sort[color].sort()
            #check for straight flush
            if sum(np.array(color_sort[color]+[0]) -
                    np.array([0]+color_sort[color]) == 1) >= 4:
                return max(color_sort[color]) #Straight flush !!
    return 0


def is_quad(hand):
    #check for quad
    out = []
    nb_sort = {}
    for card in hand:
        if card.value in nb_sort:
            nb_sort[card.value]+= 1
        else:
            nb_sort[card.value]=1

    for i in nb_sort:
        if nb_sort[i] == 4:
            out.append(i) #value of the quad

    a = sorted(nb_sort, reverse=True)
    if out != []:
        if a[0] == out[0]:
            out.append(a[1]) #value of the kicker
        else:
            out.append(a[0]) #value of the kicker

    return out
        

            


if __name__ == "__main__":
    hand = string2hand("5s5c5d5hJs3s2s")
    print(hand)
    print(is_quad(hand))





