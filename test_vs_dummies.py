import numpy as np
from cfr_holdem import *
from holdem import *
from abstract import *
import matplotlib.pyplot as plt

def draw(p):
    r = np.random.rand()
    c = np.cumsum(p)
    i = 0
    while r >= c[i]:
        i += 1
    return i

#_, strategy, _ = load_obj('hulhe_cumstrat')
#strategy = cum_strat2strat(strategy)
strategy = get_optimal_strat(AbstractPoker(10), 10000)
strategy.update(get_optimal_strat(PreflopPoker(10), 10000))

caller = {}
for k in range(10):
    caller[(k, 'pre')] = np.array([0., 1., 0.])
    caller[(k, 'c', 'pre')] = np.array([1., 0.])
    caller[(k, 'r', 'pre')] = np.array([1., 0.])
    caller[(k, 'c', 'r', 'pre')] = np.array([1., 0.])
    caller[(k,)] = np.array([1., 0.])
    caller[(k, 'p')] = np.array([1., 0.])
    caller[(k, 'b')] = np.array([0., 1., 0.])
    caller[(k, 'p', 'b')] = np.array([1., 0.])

gain = 0
iterations = 100
game = HoldemHU()
gain = np.zeros(iterations)
for k in range(iterations):
    history = game.deal()
    actions = game.get_actions_available(history)
    strat_deal = 0
    while type(actions) != int:
        if actions == 'D':
            history += game.deal_cards(history)
            actions = game.get_actions_available(history)
        turn = game.whose_turn(history)
        info = holdem_history_to_info_set(history, turn)
        if info[0] == 10:
            print_history(history)
            info[0] = 9
        if turn == strat_deal:
            a = draw(caller[tuple(info)])
        else:
            a = draw(strategy[tuple(info)])
        history += actions[a]
        actions = game.get_actions_available(history)
    gain[k] = (1 - 2*strat_deal) * actions
    strat_deal = 1 - strat_deal
    #print(actions)
    #print_history(history)
plt.plot(np.cumsum(gain))
plt.show()
