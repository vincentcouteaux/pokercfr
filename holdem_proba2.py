from holdem_proba import *
from scipy.misc import comb
import numpy as np


def prob_to_have_straight_flush(high_card, having, without, n_to_draw):
    values = range(high_card-4, high_card+1)
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

def prob_to_make_quads(values, having, without, n_to_draw):
    for card in without:
        if card.value == values[0]:
            return 0.
    remaining_cards = 52 - len(having) - len(without)
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


if __name__ == "__main__":
    print(1/prob_to_have_straight_flush(14, [], [], 7))
    print(1/prob_to_have_straight_flush(14, string2hand("4h5h"), [], 5))
    print(1/prob_to_have_straight_flush(14, string2hand("ThJh"), [], 5))
    print(1/prob_to_have_straight_flush(14, string2hand("AhKh"), [], 5))
    print(1/prob_to_have_straight_flush(14, [], string2hand("ThJh"), 5))
    print(prob_to_have_straight_flush(14, string2hand("ThJhQhKhAh"), [], 2))
    print(1/prob_to_make_quads([14, 11], [], [], 7))
    print(1/prob_to_make_quads([14, 11], string2hand("AhAc"), [], 5))
    print(prob_to_make_quads([14, 11], [], string2hand("AhAc"), 5))
    print(1/prob_to_make_quads([14, 11], string2hand("AhJs"), [], 5))
    print(prob_to_make_quads([14, 11], string2hand("AhQs"), [], 5))


