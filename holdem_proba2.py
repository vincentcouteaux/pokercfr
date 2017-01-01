from holdem_proba import *
from scipy.misc import comb
import numpy as np


def prob_to_have_straight_flush(high_card, having, without):
    values = range(high_card-4, high_card+1)
    n_to_draw = 7 - len(having)
    number_of_draws = 0
    n_known_cards = len(having) + len(without)
    for color in range(4):
        needed_cards = []
        n_needed = 5
        possible = True
        for v in values:
            needed_cards.append(Card(v, color))
        for card in without:
            if card.is_in(needed_cards):
                possible = False #we can't make that straight flush
        if not possible:
            continue
        for card in having:
            if card.is_in(needed_cards):
                n_needed -= 1
        number_of_draws += comb(52  - n_needed - n_known_cards, n_to_draw - n_needed, exact=True)
    return float(number_of_draws)/comb(52 - n_known_cards, n_to_draw, exact=True)

def prob_to_make_quads(values, having, without):
    for card in without:
        if card.value == values[0]:
            return 0.
    remaining_cards = 52 - len(having) - len(without)
    n_to_draw = 7 - len(having)
    chosen_cards = 0
    n_possible_draws = 0
    n_to_make_quad = 4
    for card in having:
        if card.value == values[0]:
            n_to_make_quad -= 1
    chosen_cards += n_to_make_quad #we chose the cards to make the quad
    remaining_cards -= n_to_make_quad
    n_possible_draws = 1
    kicker_needed = True # False if we already have it in one in our hand
    for card in having:
        if card.value == values[1]:
            kicker_needed = False
    if kicker_needed:
        possible_kickers = 4
        for card in without:
            if card.value == values[1]:
                possible_kickers -= 1
        chosen_cards += 1 #we chose the kicker
        remaining_cards -= 1
        n_possible_draws *= comb(possible_kickers, 1, exact=True)
    #remove from the deck the cards above the kicker
    number_of_cards_above = 4*(14-values[1])
    if values[0] > values[1]:
        number_of_cards_above -= 4
    for card in having:
        if card.value != values[0] and card.value > values[1]:
            return 0. # the kicker would be that card
    for card in without:
        if card.value != values[0] and card.value > values[1]:
            number_of_cards_above -= 1
    remaining_cards -= number_of_cards_above
    n_possible_draws *= comb(remaining_cards, n_to_draw - chosen_cards, exact=True)
    return float(n_possible_draws)/comb(52-len(having)-len(without), n_to_draw, exact=True)

def prob_to_make_full(values, having, without):
    #3 way to make a full: 1 trip, 1 pair, 2 different cards
    remaining_cards = 52 - len(having) - len(without) # remaining unknown cards
    n_remain_trip_cards = 4 # number of trip cards remaining in the deck
    n_trip_cards_to_get = 3 # number of trip cards to draw
    n_remain_pair_cards = 4 # number of pair cards remaining in the deck
    n_pair_cards_to_get = 2
    for card in having:
        if card.value == values[0]:
            n_remain_trip_cards -= 1
            n_trip_cards_to_get -= 1
        elif card.value == values[1]:
            n_remain_pair_cards -= 1
            n_pair_cards_to_get -= 1
    for card in without:
        if card.value == values[0]:
            n_remain_trip_cards -= 1
        elif card.value == values[1]:
            n_remain_pair_cards -= 1
    number_of_draws = comb(n_remain_trip_cards, n_trip_cards_to_get, exact=True)
    number_of_draws *= comb(n_remain_pair_cards, n_pair_cards_to_get, exact=True)
    remaining_cards -= n_trip_cards_to_get
    n_remain_trip_cards -= n_trip_cards_to_get
    remaining_cards -= n_pair_cards_to_get
    n_remain_pair_cards -= n_pair_cards_to_get
    number_of_draws *= comb(remaining_cards - n_remain_trip_cards - n_remain_pair_cards, 2, exact=True) # We choose the two other card.
    #2 trips, 1 other card
    n_pair_cards_to_get += 1
    number_of_draws1 = comb(n_remain_trip_cards, n_trip_cards_to_get, exact=True)
    number_of_draws1 *= comb(n_remain_pair_cards, n_pair_cards_to_get, exact=True)
    remaining_cards -= 1
    n_remain_pair_cards -= 1
    number_of_draws1 *= remaining_cards - n_remain_trip_cards - n_remain_pair_cards
    #1 trip, 2 pairs
    number_of_draws2 = comb(n_remain_trip_cards, n_trip_cards_to_get, exact=True)
    n_pair_cards_to_get -= 1
    number_of_draws2 *= comb(n_remain_pair_cards, n_pair_cards_to_get, exact=True)
    possible_2nd_pairs = range(2, values[1]) # number of possible second pair
    for card in having:
        if card.value in possible_2nd_pairs:
            possible_2nd_pairs.remove(card.value)
    for card in without:
        if card.value in possible_2nd_pairs:
            possible_2nd_pairs.remove(card.value)
    number_of_draws2 *= len(possible_2nd_pairs)

def probability_to_draw(n_cards, card_sets):
    """ n_cards is a list of lists where n_cards[i] is the list of number of cards we can choose in card_sets[i]
    card_sets is the list of set of cards """
    number_of_draws = 1
    for i, l in enumerate(n_cards):
        number_of_sets = 0
        for n in l:
            number_of_sets += comb(card_sets[i], n)
        number_of_draws *= number_of_sets


if __name__ == "__main__":
    print(1/prob_to_have_straight_flush(14, [], []))
    print(1/prob_to_have_straight_flush(14, string2hand("4h5h"), []))
    print(1/prob_to_have_straight_flush(14, string2hand("ThJh"), []))
    print(1/prob_to_have_straight_flush(14, string2hand("AhKh"), []))
    print(1/prob_to_have_straight_flush(14, [], string2hand("ThJh")))
    print(prob_to_have_straight_flush(14, string2hand("ThJhQhKhAh"), []))
    print(1/prob_to_make_quads([14, 11], [], []))
    print(1/prob_to_make_quads([14, 11], string2hand("AhAc"), []))
    print(prob_to_make_quads([14, 11], [], string2hand("AhAc")))
    print(1/prob_to_make_quads([14, 11], string2hand("AhJs"), []))
    print(prob_to_make_quads([14, 11], string2hand("AhQs"), []))


