from cfr_holdem import *
from ars import *

game = HoldemHU()

strategy = load_obj('hulhe_strat1')
print(strategy)

human_stack = 10
ai_stack = 10

command = 'a'
human_dealer = True

def draw(p):
    r = np.random.rand()
    c = np.cumsum(p)
    i = 0
    while r >= c[i]:
        i += 1
    return i

while command != 'n':
    history = game.deal()
    actions = game.get_actions_available(history)

    if human_dealer:
        print('Your cards are {0}'.format(hand2string(history[:2])))
        human_to_play = True
    else:
        print('Your cards are {0}'.format(hand2string(history[2:4])))
        human_to_play = False
    while type(actions) != int:
        if not human_to_play:
            ai_info = holdem_history_to_info_set(history,1*human_dealer)
            #print("ai info: {0}, strategy: {1}".format(ai_info, strategy[ai_info]))
            if actions != 'D':
                human_to_play = True
                c = draw(strategy[tuple(ai_info)])
                history.append(actions[c])
                print('ai played {0}'.format(actions[c]))
            actions = game.get_actions_available(history)
            if actions == 'D':
                cards = game.deal_cards(history)
                history += cards
                print(hand2string(cards))
        else:
            if actions != 'D':
                human_to_play = False
                print('You can play: {0}'.format(actions))
                c = raw_input()
                history.append(c)
            actions = game.get_actions_available(history)
            if actions == 'D':
                cards = game.deal_cards(history)
                history += cards
                print(hand2string(cards))
    if not human_dealer:
        actions = -actions
    human_stack += actions
    ai_stack -= actions
    print("oppenent shows {0}".format(hand2string(history[2*human_dealer: 2*(human_dealer+1)])))
    print("your stack: {0}, opponent stack: {1}".format(human_stack, ai_stack))
    print("rematch ? 'y' yes, 'n' no")
    command = raw_input()
    print("\n\n\n")
    human_dealer = not human_dealer
