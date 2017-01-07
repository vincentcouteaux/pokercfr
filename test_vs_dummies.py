import numpy as np
from cfr_holdem import *
from holdem import *

def draw(p):
    r = np.random.rand()
    c = np.cumsum(p)
    i = 0
    while r >= c[i]:
        i += 1
    return i

_, strategy, _ = load_obj('hulhe_cumstrat')
strategy = cum_strat2strat(strategy)

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
iterations = 50
game = HoldemHU()
for k in range(iterations):
    history = game.deal()
    actions = game.get_actions_available(history)
    while type(actions) != int:
        if actions == 'D':
            history += game.deal_cards(history)
            actions = game.get_actions_available(history)
        turn = game.whose_turn(history)
        if turn == 1:
            a = draw(caller[tuple(holdem_history_to_info_set(history, turn))])
        else:
            a = draw(strategy[tuple(holdem_history_to_info_set(history, turn))])
        history += actions[a]
        actions = game.get_actions_available(history)
    gain += actions
    #print(actions)
    #print_history(history)
print(float(actions)/iterations)
