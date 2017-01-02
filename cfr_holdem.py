import numpy as np
import random
import os.path
from khun import *
from ars import *
from holdem_proba import *
from holdem import *

#Player 0 has the button
#Player 1 is UTG
#A history has the form ['card1P0','card2P0','card1P1','card2P1','action','action',...]
#Its length is variable and ends with a final state

def holdem_history_to_info_set(history, player_index):
    iterations = 500
    pos = 1 - player_index
    full_info_set = history[:2*pos] + history[2*(pos+1):]
    cards = []
    for c in full_info_set:
        if isinstance (c, Card):
            cards.append(c)
    #print(hand2string(cards))
    pocket = cards [:2]
    #print(hand2string(pocket))
    community  = cards[2:]
    #print(hand2string(community))
    if len(cards) == 2:
        strength = estimate_hand_strength_preflop(pocket, 'results')
    else:
        strength = estimate_hand_strength(pocket, community, iterations)
    #print(strength)
    i = len(history)
    while not isinstance(history[i-1], Card):
        i = i-1
    info_set = [int(10*strength/iterations)] + history[i:]
    if len(cards) == 2:
        info_set.append('pre')
    return info_set

if __name__ == "__main__":
	pocketP0 = string2hand('7c7h')
	pocketP1 = string2hand('2h3d')
	community = string2hand('AdAcKh')
	history = pocketP0 + pocketP1 + ['p','b','b'] + community
	info_set = holdem_history_to_info_set(history, 0)

np.seterr(all='raise')

def holdem_cfr_2p(game, history, player, pi1, pi2, strategy, cumulated_regret, cumulated_strat):
    actions = game.get_actions_available(history)
    if type(actions) == int:
        if player == 0:
            return actions
        else:
            return -actions
    if actions == 'D':
    	history += game.deal_cards(history)
        actions = game.get_actions_available(history)

    player_turn = game.whose_turn(history)
    number_actions = len(actions)
    v_sigma = 0
    v_sigmaI = np.zeros(number_actions)
    info_set = tuple(holdem_history_to_info_set(history, player_turn))
    if info_set not in strategy:
        strategy[info_set] = np.ones(number_actions) / number_actions
        cumulated_regret[info_set] = np.zeros(number_actions);
        cumulated_strat[info_set] = np.zeros(number_actions);
    for i, a in enumerate(actions):
        if player_turn == 0:
            v_sigmaI[i] = holdem_cfr_2p(game, history + [a], player, strategy[info_set][i]*pi1, pi2,
                    strategy, cumulated_regret, cumulated_strat)
        else:
            v_sigmaI[i] = holdem_cfr_2p(game, history + [a], player, pi1, strategy[info_set][i]*pi2,
                    strategy, cumulated_regret, cumulated_strat)
        v_sigma += strategy[info_set][i]*v_sigmaI[i]
    if player_turn == player:
        if player == 0: # zero or 1 ????
            pii = pi1
            pim = pi2
        else:
            pii = pi2
            pim = pi1
        if cumulated_regret[info_set].shape != v_sigmaI.shape:
            print(info_set)
            print(actions)
        cumulated_regret[info_set] += pim*(v_sigmaI - v_sigma)
        cumulated_strat[info_set] += pii*strategy[info_set]
        bigR = np.maximum(cumulated_regret[info_set], np.zeros(number_actions))
        sumBigR = np.sum(bigR)
        if sumBigR > 0:
            strategy[info_set] = bigR / sumBigR
        else:
            strategy[info_set] = np.ones(number_actions) / number_actions
    return v_sigma


def get_optimal_strat(game, T):
    strategy = {}
    cumulated_regret = {}
    cumulated_strategy = {}
    for t in range(T):
        print(t)
        cards = game.deal()
        holdem_cfr_2p(game, cards, 0, 1, 1, strategy, cumulated_regret, cumulated_strategy)
        holdem_cfr_2p(game, cards, 1, 1, 1, strategy, cumulated_regret, cumulated_strategy)
    for infoset in cumulated_strategy:
        if np.sum(cumulated_strategy[infoset]) <= 0.:
            nb_actions = cumulated_strategy[infoset].size
            cumulated_strategy[infoset] = np.ones(nb_actions)/nb_actions
        else:
            cumulated_strategy[infoset] /= np.sum(cumulated_strategy[infoset])
    return cumulated_strategy

if __name__ == "__main__":
    filename = 'hulhe_strat1'
    strat = get_optimal_strat(HoldemHU(), 10)
    save_obj(strat, filename)
    print(strat)
