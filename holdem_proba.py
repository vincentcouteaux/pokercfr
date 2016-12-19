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
    if 14 in flush:
        flush.append(1)
    flush = list(set(flush))
    flush.sort(reverse=True)
    for i, k in enumerate(flush[1:]):
        if k - flush[i] == -1:
            if consecutive_connected == []:
                consecutive_connected.append(flush[i])
            consecutive_connected.append(k)
            if len(consecutive_connected) == 5:
                return consecutive_connected[0]
        else:
            consecutive_connected = []
    return []


def is_straight(hand):
    values = []
    for card in hand:
        values.append(card.value)
    if 14 in values:
        values.append(1)
    values = list(set(values))
    values.sort(reverse=True)
    consecutive_connected = []
    for i, k in enumerate(values[1:]):
        if k - values[i] == -1:
            if consecutive_connected == []:
                consecutive_connected.append(values[i])
            consecutive_connected.append(k)
            if len(consecutive_connected) == 5:
                return consecutive_connected[0]
        else:
            consecutive_connected = []
    return []


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

def is_trips(hand):
    #check for trips
    out = []
    nb_sort = {}
    for card in hand:
        if card.value in nb_sort:
            nb_sort[card.value]+= 1
        else:
            nb_sort[card.value]=1

    for i in nb_sort:
        if nb_sort[i] ==3:
            out.append(i)

    a = sorted(nb_sort, reverse=True)
    if out != []:
        a.remove(out[0])
        out += a[:2]
    return out



if __name__ == "__main__":
    
    hand = string2hand("JhTh5c2sQdKhAh")
    print(is_straight(hand))
    print(is_straight_flush(hand))

    hand = string2hand("3h4h5h2hQd6cAh")
    print(is_straight(hand))
    print(is_straight_flush(hand))


