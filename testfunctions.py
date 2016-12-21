from holdem_proba import *
from random import shuffle

def get_random_hand():
    deck = string2hand(deck_str)
    cards = list(np.random.choice(deck, 9))
    shuffle(cards)
    j1 = cards[:2]
    j2 = cards[2:4]
    flop = cards[4:]
    return j1, j2, flop

def test_n_hands(n):
    for k in range(n):
        j1, j2, flop = get_random_hand()
        hand1 = j1+flop
        hand2 = j2+flop
        c1, v1 = get_combination(hand1)
        c2, v2 = get_combination(hand2)
        res = compare(hand1, hand2)
        print("flop is: {}, {} has {},{}, vs: {} has {},{}: {}".format(hand2string(flop), hand2string(j1),
            comb_id_to_string(c1), v1, hand2string(j2), comb_id_to_string(c2), v2, res))

def comb_id_to_string(c):
    if c==8:
        return 'Straight flush'
    if c==7:
        return 'quads'
    if c==6:
        return 'full'
    if c==5:
        return 'flush'
    if c==4:
        return 'straight'
    if c==3:
        return 'trips'
    if c==2:
        return 'double pair'
    if c==1:
        return 'pair'
    return 'nothing'

if __name__ == "__main__":
    test_n_hands(10)
