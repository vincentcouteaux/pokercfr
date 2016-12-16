from cfr import *

strategy = get_optimal_strat()

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

while command != 'e':
    print('type "e" any time to exit')
    history = deal()
    actions = get_actions_available(history)
    if human_dealer:
        print('Your card is {0}'.format(history[0]))
        human_to_play = False
    else:
        print('Your card is {0}'.format(history[1]))
        human_to_play = True
    while type(actions) != int:
        if not human_to_play:
            ai_info = history_to_info_set(history,1)
            c = draw(strategy[ai_info])
            history += actions[c]
            print('ai played {0}'.format(actions[c]))
            actions = get_actions_available(history)
            human_to_play = True
        else:
            print('You can play: {0}'.format(actions))
            c = raw_input()
            history += c
            actions = get_actions_available(history)
            human_to_play = False
    if not human_dealer:
        actions = -actions
    human_stack += actions
    ai_stack -= actions
    print("oppenent shows {0}".format(history[1*human_dealer]))
    print("your stack: {0}, opponent stack: {0}".format(human_stack, ai_stack))
    print("rematch ? a yes, e no")
    command = raw_input()
    human_dealer = not human_dealer