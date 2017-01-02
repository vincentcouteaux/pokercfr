from holdem_proba import *
import numpy as np
from scipy.misc import comb
import csv

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def get_pocket_id(card1, card2):
    if card1.value == card2.value:
        return card1.value - 2
    v1 = max(card1.value, card2.value)-2
    v2 = min(card1.value, card2.value)-2
    ind = 13 + v1*(v1-1)/2 + v2
    if card1.color == card2.color:
        return ind+78
    return ind

def estimate_hand_strength(pocket, community, iterations):
    pocket_id = get_pocket_id(pocket[0], pocket[1])
    comb = get_combination(pocket+community)
    deck = string2hand(deck_str)
    n_to_draw = 7 - len(community)
    for card in pocket+community:
        deck = card.remove_from(deck)
    wins = 0
    ties = 0
    for k in range(iterations):
        shuffle(deck)
        cards = deck[:n_to_draw]
        hand1 = pocket + community + cards[2:]
        hand2 = cards + community
        c = compare(hand1, hand2)
        if c == 1:
            wins += 1
        elif c == 0:
            ties += 1
    return (float(wins) + float(ties)/2)

def estimate_hand_strength_preflop(pocket, filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        card1 = pocket[0]
        card2 = pocket[1]

        if card1.value<=card2.value:
            pair = hand2string([card1])[0] + hand2string([card2])[0]
        else:
            pair = hand2string([card2])[0] + hand2string([card1])[0]
        if card1.value == card2.value:
            for row in reader:
                if row[0] == pair:
                    strength = float(row[1]) + float(row[3])/2
        elif card1.color == card2.color:
            for row in reader:
                if row[0][:2] == 'su':
                    if row[0][-2:] == pair:
                        strength = float(row[1]) + float(row[3])/2
        else :
            for row in reader:
                if row[0][:2] == 'un':
                    if row[0][-2:] == pair:
                	    strength = float(row[1]) + float(row[3])/2
    return strength

if __name__ == "__main__":
    #hand = string2hand("8hTh9hJhQh")
    #print(estimate_hand_strength(string2hand("AhAc"), string2hand("AsAdKc"), 1000))
    hand = string2hand("Tc4h")
    print(estimate_hand_strength_preflop(hand, 'results'))

