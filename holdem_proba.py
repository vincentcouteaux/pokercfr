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

def is_full(hand):
#check for full
    out = []
    nb_sort = {}
    for card in hand:
        if card.value in nb_sort:
            nb_sort[card.value]+= 1
        else:
            nb_sort[card.value]=1

    b = [];
    p = [];
    for i in nb_sort:
        if nb_sort[i] ==3:
            b.append(i)

    for j in nb_sort:
        if nb_sort[j] ==2:
            p.append(j)
    p.sort(reverse = True)

    if b!=[] and p!=[]:
        out+=b
        out.append(p[0])

    return out


def is_pair(hand):
    for i in nb_sort:
        if nb_sort[i] == 2:
            out.append(i)

    nb_sort = sorted(nb_sort, reverse=True)
    if out != []:
        nb_sort.remove(out[0])
        out += nb_sort[:3]
    return out

def is_double_pair(hand):
    buckets = {}
    for card in hand:
        if card.value in buckets:
            buckets[card.value] += 1
        else:
            buckets[card.value]=1
    out = []
    kicker = 1
    for v in sorted(buckets, reverse = True):
        if buckets[v] == 2 and len(out) < 2:
            out.append(v)
        elif v > kicker:
            kicker = v
    if len(out) == 2:
        return out + [kicker]
    else:
        return []

def has_nothing(hand):
    values = []
    for card in hand:
        values.append(card.value)
    values.sort()
    return values[:5]

def compare_combination(comb1, comb2):
    for k in range(len(comb1)):
        if comb1[k] > comb2[k]:
            return 1
        if comb1[k] < comb2[k]:
            return -1
    return 0

def get_combination(hand):
    values = is_straight_flush(hand)
    if values != []:
        return 8, values
    values = is_quad(hand)
    if values != []:
        return 7, values
    values = is_full(hand)
    if values != []:
        return 6, values
    values = is_flush(hand)
    if values != []:
        return 5, values
    values = is_straight(hand)
    if values != []:
        return 4, values
    values = is_trips(hand)
    if values != []:
        return 3, values
    values = is_double_pair(hand)
    if values != []:
        return 2, values
    values = is_pair(hand)
    if values != []:
        return 1, values
    return 0, has_nothing(hand)


if __name__ == "__main__":

    hand = string2hand("JhAsAd3h4c5sQc")
    print(is_pair(hand))
    print(is_double_pair(hand))

    hand = string2hand("JhAsAd3h4c5sJc")
    print(is_pair(hand))
    print(is_double_pair(hand))
