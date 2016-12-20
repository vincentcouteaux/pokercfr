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

def hand2string(hand):
    s = ""
    for card in hand:
        s = s+str(card.value)
        if card.color == Color.spade:
            s = s+'s'
        elif card.color == Color.heart:
            s = s+'h'
        elif card.color == Color.diamond:
            s = s+'d'
        else:
            s = s+'c'
    return s

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
    for i in sorted(nb_sort, reverse=True):
        if nb_sort[i] == 3:
            b.append(i)
    if b == []:
        return []
    del nb_sort[b[0]]
    for j in sorted(nb_sort, reverse=True):
        if nb_sort[j] >= 2:
            p.append(j)
    if p == []:
        return []
    p.sort(reverse = True)
    b.sort(reverse = True)
    out.append(b[0])
    if len(b) > 1 and b[1] > p[0]:
            out.append(b[1])
    else:
        out.append(p[0])
    return out


def is_pair(hand):
    nb_sort = {}
    for card in hand:
        if card.value in nb_sort:
            nb_sort[card.value]+= 1
        else:
            nb_sort[card.value]=1
    out = []
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
    if type(comb1) == int:
        if comb1 > comb2:
            return 1
        elif comb1 < comb2:
            return -1
        else:
            return 0
    if (len(comb1) != len(comb2)):
        print('{}, {}'.format(comb1, comb2))
        return -5
    for k in range(len(comb1)):
        if comb1[k] > comb2[k]:
            return 1
        elif comb1[k] < comb2[k]:
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

def compare(hand1, hand2):
    """! return 1 if hand1 betas hand2, -1 if hand2 beats hand1, 0 for a split pot """
    c1, v1 = get_combination(hand1)
    c2, v2 = get_combination(hand2)
    if (c1 > c2):
        return 1
    elif (c2 > c1):
        return -1
    else:
        c = compare_combination(v1, v2)
        if c == -5:
            print(c1)
        return c

deck_str = "2h3h4h5h6h7h8h9hThJhQhKhAh2s3s4s5s6s7s8s9sTsJsQsKsAs2d3d4d5d6d7d8d9dTdJdQdKdAd2c3c4c5c6c7c8c9cTcJcQcKcAc"

def next_draw(draw, maxi):
    size = len(draw)
    k = size - 1
    from_last = 0
    while draw[k] == maxi - from_last:
        k -= 1
        from_last += 1
    if k == -1:
        return []
    draw[k] += 1
    c=1
    #while k < len(draw) - 1 and draw[k] < maxi - size + k + 1:
    while k < len(draw) - 1 and draw[k] + c <= maxi - size + k + 2:
        draw[k+1] = draw[k] + c
        k+=1
        c+=1
    return draw

def probability_to_win(card1, card2):
    deckstr = deck_str.replace(card1, '')
    deckstr = deckstr.replace(card2, '')
    deck = string2hand(deckstr)
    draw = range(7)
    pocket = string2hand(card1) + string2hand(card2)
    wins = 0
    loss = 0
    draws = 0
    print(len(deck))
    while draw != []:
        cards = [deck[i] for i in draw]
        hand1 = pocket + cards[2:]
        hand2 = cards
        c = compare(hand1, hand2)
        if c == 1:
            wins += 1
        elif c == -1:
            loss += 1
        else:
            draws += 1
        draw = next_draw(draw, 49)
    return wins, loss, draws

def estimate_proba(card1, card2, T):
    deckstr = deck_str.replace(card1, '')
    deckstr = deckstr.replace(card2, '')
    deck = string2hand(deckstr)
    pocket = string2hand(card1) + string2hand(card2)
    wins = 0
    loss = 0
    draws = 0
    for k in range(T):
        cards = list(np.random.choice(deck, 7))
        hand1 = pocket + cards[2:]
        hand2 = cards
        c = compare(hand1, hand2)
        if c == 1:
            wins += 1
        elif c == -1:
            loss += 1
        else:
            draws += 1
    T = float(T)
    return wins/T, loss/T, draws/T

def value_to_char(value):
    if value == 14:
        return 'A'
    elif value == 13:
        return 'K'
    elif value == 12:
        return 'Q'
    elif value == 11:
        return 'J'
    elif value == 10:
        return 'T'
    else:
        return str(value)

def estimate_all_preflop_probas(T):
    #suited_cards:
    pocket = [0, 1]
    while pocket != []:
        card1 = pocket[0] + 2
        card2 = pocket[1] + 2
        card1 = value_to_char(card1) + 'h'
        card2 = value_to_char(card2) + 'h'
        wins, losses, draws = estimate_proba(card1, card2, T)
        print('suited {}{}, {}, {}, {}'.format(card1[0], card2[0], wins, losses, draws))
        pocket=next_draw(pocket, 12)
    #unsuited_cards:
    pocket = [0, 1]
    while pocket != []:
        card1 = pocket[0] + 2
        card2 = pocket[1] + 2
        card1 = value_to_char(card1) + 'h'
        card2 = value_to_char(card2) + 'c'
        wins, losses, draws = estimate_proba(card1, card2, T)
        print('unsuited {}{}, {}, {}, {}'.format(card1[0], card2[0], wins, losses, draws))
        pocket=next_draw(pocket, 12)
    #pairs:
    for k in range(2, 15):
        card1 = value_to_char(k) + 'h'
        card2 = value_to_char(k) + 'c'
        wins, losses, draws = estimate_proba(card1, card2, T)
        print('{}{}, {}, {}, {}'.format(card1[0], card2[0], wins, losses, draws))


if __name__ == "__main__":

    hand = string2hand("JhAsAd3h4c5sQc")
    print(is_pair(hand))
    print(is_double_pair(hand))

    hand = string2hand("JhAsAd3h4c5sJc")
    print(is_pair(hand))
    print(is_double_pair(hand))

    print(compare(string2hand("JhJsJcQh2hQcQs"), string2hand("JhJsJcQh2hQc4c")))

    draw = [45, 46, 47, 48, 49, 50, 51]
    #draw = range(7)
    for k in range(5):
        draw = next_draw(draw, 52)
        print(draw)

    print(estimate_proba("As", "Ac", 10000))
    estimate_all_preflop_probas(10000)
