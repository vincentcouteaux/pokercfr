import numpy as np
import random

#Player 0 has the button
#Player 1 is UTG
# An history is for instance 'JQpb', button has card J, utg has card Q, button passes, utg bets

debug = False

def deal():
    return ''.join(random.sample('JQK', 3))[:2]

def whose_turn(history):
    return (len(history) + 1)%2

def value(card):
    if card == 'Q':
        return 1
    elif card == 'K':
        return 2
    else:
        return 0

def button_beats(card1, card2):
    return value(card1) > value(card2)

def get_actions_available(history):
    if history == '':
        return 'D'
    if history[2:] == 'pp':
        return 2*(value(history[0]) > value(history[1])) - 1
    elif history[-2:] == 'bb':
        return 4*(value(history[0]) > value(history[1])) - 2
    elif history[2:] == 'bp':
        return -1
    elif history[2:] == 'pbp':
        return 1
    else:
        return ['p', 'b']

def history_to_info_set(history, player_index):
    pos = 1 - player_index
    return history[:pos] + history[(pos+1):]


#strategy = {}
#cumulated_regret = {}

def cfr(history, player, t, pi1, pi2, strategy, cumulated_regret, cumulated_strat):
    actions = get_actions_available(history)
    if debug:
        print('** history: {0}, actions: {1}'.format(history, actions))
    if type(actions) == int:
        if player == 0:
            return actions
        else:
            return -actions
    player_turn = whose_turn(history)
    number_actions = len(actions)
    v_sigma = 0
    v_sigmaI = np.zeros(number_actions)
    info_set = history_to_info_set(history, player_turn)
    if len(strategy) <= t:
        strategy.append({})
    if info_set not in strategy[t]:
        strategy[t][info_set] = np.ones(number_actions) / number_actions
        cumulated_regret[info_set] = np.zeros(number_actions);
        cumulated_strat[info_set] = np.zeros(number_actions);
    for i, a in enumerate(actions):
        if player_turn == 0:
            v_sigmaI[i] = cfr(history + a, player, t, strategy[t][info_set][i]*pi1, pi2,
                    strategy, cumulated_regret, cumulated_strat)
        else:
            v_sigmaI[i] = cfr(history + a, player, t, pi1, strategy[t][info_set][i]*pi2,
                    strategy, cumulated_regret, cumulated_strat)
        v_sigma += strategy[t][info_set][i]*v_sigmaI[i]
    if player_turn == player:
        if player == 0: # zero or 1 ????
            pii = pi1
            pim = pi2
        else:
            pii = pi2
            pim = pi1
        if debug:
            print('history: {0}, v_sigmaI: {1}, v_sigma: {2}'.format(history, v_sigmaI, v_sigma))
        cumulated_regret[info_set] += pim*(v_sigmaI - v_sigma)
        cumulated_strat[info_set] += pii*strategy[t][info_set]
        bigR = np.maximum(cumulated_regret[info_set], np.zeros(number_actions))
        sumBigR = np.sum(bigR)
        if len(strategy) <= t+1:
            strategy.append(strategy[t])
        if debug:
            print('cumulated_regret: {0}, sumBigR: {1}'.format(cumulated_regret[info_set], sumBigR))
        if sumBigR > 0:
            strategy[t+1][info_set] = bigR / sumBigR
        else:
            strategy[t+1][info_set] = np.ones(number_actions) / number_actions
    return v_sigma

def get_optimal_strat(T):
    strategy = []
    cumulated_regret = {}
    cumulated_strategy = {}
    for t in range(T):
        cards = deal()
        if debug:
            print("player 0")
        cfr(cards, 0, t, 1, 1, strategy, cumulated_regret, cumulated_strategy)
        if debug:
            print("player 1")
        cfr(cards, 1, t, 1, 1, strategy, cumulated_regret, cumulated_strategy)
    for infoset in cumulated_strategy:
        cumulated_strategy[infoset] /= np.sum(cumulated_strategy[infoset])
    return cumulated_strategy

if __name__ == "__main__":
    if debug:
        T = 10
    else:
        T = 10000
    strategy = get_optimal_strat(T)
    print(strategy)
    print("J: pass = %.2f, bet = %.2f" % (strategy["J"][0],strategy["J"][1]))
    print("K: pass = %.2f, bet = %.2f" % (strategy["K"][0],strategy["K"][1]))
    print("Jp: pass = %.2f, bet = %.2f" % (strategy["Jp"][0], strategy["Jp"][1]))
    print("Qb: pass = %.2f, bet = %.2f" % (strategy["Qb"][0], strategy["Qb"][1]))
