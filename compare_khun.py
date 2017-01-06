from cfr import *
from khun import *
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy as cp

def truth(alpha):
    s = {}
    s["J"] = np.array([1 - alpha, alpha])
    s["Q"] = np.array([1., 0.])
    s["K"] = np.array([1 - 3*alpha, 3*alpha])
    s["Jp"] = np.array([2./3, 1./3])
    s["Qp"] = np.array([1., 0.])
    s["Kp"] = np.array([0., 1.])
    s["Jb"] = np.array([1., 0.])
    s["Qb"] = np.array([2./3, 1./3])
    s["Kb"] = np.array([0., 1.])
    s["Jpb"] = np.array([1., 0.])
    s["Qpb"] = np.array([2./3 - alpha, alpha + 1./3])
    s["Kpb"] = np.array([0., 1.])
    return s

def distance(s1, s2):
    out = 0
    for i in s1:
        out += (s1[i][0] - s2[i][0])**2
    return out

def strat_diff_vs_it(game, T):
    strategy = {}
    cumulated_regret = {}
    cumulated_strategy = {}
    diff = np.zeros(T)
    for t in range(T):
        cards = game.deal()
        cfr_2p(game, cards, 0, 1, 1, strategy, cumulated_regret, cumulated_strategy)
        cfr_2p(game, cards, 1, 1, 1, strategy, cumulated_regret, cumulated_strategy)
        strat = cp(cumulated_strategy)
        if len(strat) >= 12:
            for infoset in strat:
                strat[infoset] /= np.sum(strat[infoset])
            diff[t] = distance(strat, truth(strat["J"][1]))
    return diff

if __name__ == "__main__":
    diff = strat_diff_vs_it(Khun(), 2000)
    plt.plot(diff)
    plt.ylabel("Sum of Squared Differences")
    plt.xlabel("games")
    plt.show()
