import numpy as np
from cfr_holdem import *
import matplotlib.pyplot as plt
from holdem_proba import next_draw
from abstract import *

#<<<<<<< HEAD
_, strategy, _ = load_obj('hulhe_cumstrat2')
strategy = cum_strat2strat(strategy)
print(strategy)
#=======
#_, strategy, _ = load_obj('hulhe_cumstrat')
#strategy = cum_strat2strat(strategy)
#print(strategy)
#strategy = get_optimal_strat(PreflopPoker(10), 20000)
#>>>>>>> 1263015c8ab8166c340bf20fa7c21c92985e42ad

def build_preflop_heatmap(strat):
    out = np.zeros((13, 13, 3))
    buckets = np.zeros((13, 13))
    pocket = [0, 1]
    while pocket != []:
        card1 = pocket[0] + 2
        card2 = pocket[1] + 2
        card1 = value_to_char(card1) + 'h'
        card2 = value_to_char(card2) + 'h'
        history = string2hand(card1 + card2 + "3s4s")
        info_set = holdem_history_to_info_set(history, 0)
        buckets[pocket[0], pocket[1]] = info_set[0]
        if tuple(info_set) in strat:
            out[pocket[0], pocket[1], :] = strat[tuple(info_set)]
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
        buckets[pocket[1], pocket[0]] = info_set[0]
        if tuple(info_set) in strat:
            out[pocket[1], pocket[0], :] = strat[tuple(info_set)]
        pocket=next_draw(pocket, 12)
    #pairs:
    for k in range(2, 15):
        card1 = value_to_char(k) + 'h'
        card2 = value_to_char(k) + 'c'
        history = string2hand(card1 + card2 + "3s4s")
        info_set = holdem_history_to_info_set(history, 0)
        buckets[k-2, k-2] = info_set[0]
        if tuple(info_set) in strat:
            out[k-2, k-2, :] = strat[tuple(info_set)]
    print(buckets)
    c = np.array(out[:,:,1])
    r = np.array(out[:,:,2])
    out[:,:,1] = r
    out[:,:,2] = c
    plt.imshow(out, interpolation='nearest')
    plt.show()

for k in range(10):
    if (k, 'pre') in strategy:
        print(k, strategy[(k, 'pre')])
build_preflop_heatmap(strategy)

