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

def is_flush(hand):
    color_sort = {Color.spade: [], Color.heart: [], Color.diamond: [], Color.club: []}
    for card in hand:
        color_sort[card.color].append(card.value)
    for color in color_sort:
        if len(color_sort[color]) >= 5: #Flush
            color_sort[color].sort(reverse=True)
            return color_sort[color][:5]
    return []

def is_straight_flush(hand):
    color_sort = {Color.spade: [], Color.heart: [], Color.diamond: [], Color.club: []}
    for card in hand:
        color_sort[card.color].append(card.value)
    flush = []
    for color in color_sort:
        if len(color_sort[color]) >= 5: #Flush
            color_sort[color].sort(reverse=True)
            flush = color_sort[color]
    consecutive_connected = []
    for i, k in enumerate(flush[1:]):
        if k - flush[i] == -1:
            if consecutive_connected == []:
                consecutive_connected.append(flush[i])
            consecutive_connected.append(k)
            if len(consecutive_connected) == 5:
                return consecutive_connected
        else:
            consecutive_connected = []
    return []



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

if __name__ == "__main__":
    hand = string2hand("5s7hJs4s6s3s2h")
    print(hand)
    print(is_flush(hand))
    print(is_straight_flush(hand))

