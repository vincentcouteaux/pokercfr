import numpy as np
from holdem_proba import *
from cfr_holdem import *

class AbstractPoker:
    """ history = (bucket 0, bucket1, 'action1', 'action2') """
    def __init__(self, n_bucket):
        self.n_bucket = n_bucket

    def whose_turn(self,history):
        return (len(history)+1)%2

    def deal(self):
        return [np.random.randint(self.n_bucket), np.random.randint(self.n_bucket)]

    def get_actions_available(self,history):
        if len(history) == 2:
            return ['p', 'b']
        bet = [0, 0]
        for i, ac in enumerate(history[2:]):
            turn = self.whose_turn(history[:(i+2)])
            if ac == 'f':
                return (2*turn - 1)*bet[turn]
            elif ac == 'p':
                pass
            elif ac == 'b':
                bet[turn] += 1
            elif ac == 'r':
                bet[turn] += 2
            elif ac == 'c':
                if history[1+i] != 'p':
                    bet[turn] += 1
        if history[-1] == 'p':
            return ['c', 'b']
        if history[-1] == 'r':
            return ['c', 'f']
        if history[-1] == 'b':
            return ['f', 'c', 'r']
        if history[-1] == 'c':
            if history[0] == history[1]:
                winner = np.random.rand() > 0.5
            else:
                winner = np.random.rand() > history[0] / (history[0] + history[1])
            return bet[0] * winner

    def abstract_h2info(self, history):
        a = AbstractPoker(1)
        turn = 1 - a.whose_turn(history)
        return history[:turn] + history[(turn+1):]

def draw(p):
    r = np.random.rand()
    c = np.cumsum(p)
    i = 0
    while r >= c[i]:
        i += 1
    return i

class PreflopPoker:
    """ history = (bucket 0, bucket1, 'action1', 'action2') """
    def __init__(self, n_bucket):
        self.n_bucket = n_bucket

    def whose_turn(self,history):
        return len(history)%2

    def deal(self):
        probas = np.double(np.array([0, 0, 0, 248, 426, 436, 152, 6, 6]))
        probas /= np.sum(probas)
        return [draw(probas), draw(probas)]

    def get_actions_available(self,history):
        if len(history) == 2:
            return ['f', 'c', 'r']
        bet = [0, 0]
        for i, ac in enumerate(history[2:]):
            turn = self.whose_turn(history[:(i+2)])
            if ac == 'f':
                return (2*turn - 1)*bet[turn]
            elif ac == 'r':
                bet[turn] += 2
            elif ac == 'c':
                bet[turn] += 1
        if history[-1] == 'r':
            return ['c', 'f']
        if history[-1] == 'c':
            if type(history[-2]) == int:
                return ['c', 'r']
            else:
                if history[0] == history[1]:
                    winner = np.random.rand() > 0.5
                else:
                    winner = np.random.rand() > history[0] / (history[0] + history[1])
                return bet[0] * winner

    def abstract_h2info(self, history):
        a = AbstractPoker(1)
        turn = 1 - a.whose_turn(history)
        return history[:turn] + history[(turn+1):] + ['pre']

def abstract_cfr(game, history, player, pi1, pi2, strategy, cumulated_regret, cumulated_strat):
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
    info_set = tuple(game.abstract_h2info(history))
    if info_set not in strategy:
        strategy[info_set] = np.ones(number_actions) / number_actions
        cumulated_regret[info_set] = np.zeros(number_actions);
        cumulated_strat[info_set] = np.zeros(number_actions);
    for i, a in enumerate(actions):
        if player_turn == 0:
            v_sigmaI[i] = abstract_cfr(game, history + [a], player, strategy[info_set][i]*pi1, pi2,
                    strategy, cumulated_regret, cumulated_strat)
        else:
            v_sigmaI[i] = abstract_cfr(game, history + [a], player, pi1, strategy[info_set][i]*pi2,
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
        cards = game.deal()
        abstract_cfr(game, cards, 0, 1, 1, strategy, cumulated_regret, cumulated_strategy)
        abstract_cfr(game, cards, 1, 1, 1, strategy, cumulated_regret, cumulated_strategy)
    for infoset in cumulated_strategy:
        if np.sum(cumulated_strategy[infoset]) <= 0.:
            nb_actions = cumulated_strategy[infoset].size
            cumulated_strategy[infoset] = np.ones(nb_actions)/nb_actions
        else:
            cumulated_strategy[infoset] /= np.sum(cumulated_strategy[infoset])
    return cumulated_strategy

def get_bucket_probas():
    buckets = {}
    pocket = [0, 1]
    while pocket != []:
        card1 = pocket[0] + 2
        card2 = pocket[1] + 2
        card1 = value_to_char(card1) + 'h'
        card2 = value_to_char(card2) + 'h'
        history = string2hand(card1 + card2 + "3s4s")
        info_set = holdem_history_to_info_set(history, 0)
        if info_set[0] not in buckets:
            buckets[info_set[0]] = 0
        buckets[info_set[0]] += 4
        pocket=next_draw(pocket, 12)
    #unsuited_cards:
    pocket = [0, 1]
    while pocket != []:
        card1 = pocket[0] + 2
        card2 = pocket[1] + 2
        card1 = value_to_char(card1) + 'h'
        card2 = value_to_char(card2) + 'c'
        history = string2hand(card1 + card2 + "3s4s")
        info_set = holdem_history_to_info_set(history, 0)
        if info_set[0] not in buckets:
            buckets[info_set[0]] = 0
        buckets[info_set[0]] += 12
        pocket=next_draw(pocket, 12)
    #pairs:
    for k in range(2, 15):
        card1 = value_to_char(k) + 'h'
        card2 = value_to_char(k) + 'c'
        history = string2hand(card1 + card2 + "3s4s")
        info_set = holdem_history_to_info_set(history, 0)
        if info_set[0] not in buckets:
            buckets[info_set[0]] = 0
        buckets[info_set[0]] += 2
    print(buckets)

if __name__ == "__main__":
    #print(get_optimal_strat(PreflopPoker(10), 20000))
    get_bucket_probas()
