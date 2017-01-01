from ars import *
from holdem_proba import *

class HoldemHU: #implements game
    @staticmethod
    def deal():
        deck = string2hand(deck_str)
        shuffle(deck)
        return(deck[:4])

    @staticmethod
    def deal_cards(history):
        deck = string2hand(deck_str)
        cards_dealt = 0
        for c in history:
            if isinstance(c, Card):
                cards_dealt += 1
                deck = c.remove_from(deck)
        shuffle(deck)
        if cards_dealt == 0:
            return(deck[:4])
        elif cards_dealt == 4:
            return(deck[:3])
        else:
            return [deck[0]]

    @staticmethod
    def whose_turn(history):
        actions = 0
        for c in history:
            if not isinstance(c, Card):
                actions += 1
        return actions%2

    @staticmethod
    def get_actions_available(history):
        if len(history) == 4:
            return ['c', 'r']
        pocket0 = history[:2]
        pocket1 = history[2:4]
        community = []
        bet = [1, 2] # player 0 bets 1 blind, player 1 bets 2 blind
        turn = 0
        for i, c in enumerate(history[4:]):
            if isinstance(c, Card):
                community.append(c)
            else:
                if c == 'f':
                    return (2*turn - 1)*(bet[0] + bet[1] - bet[1 - turn])
                elif c == 'p':
                    turn = 1 - turn
                elif c == 'b':
                    bet[turn] += 1
                    turn = 1 - turn
                elif c == 'r':
                    bet[turn] += 2
                    turn = 1 - turn
                elif c == 'c':
                    if history[3+i] != 'p':
                        bet[turn] += 1
                    turn = 1 - turn
        if isinstance(history[-1], Card):
            return ['p', 'b']
        if history[-1] == 'p':
            return  ['c', 'b']
        if history[-1] == 'r':
            return ['c', 'f']
        if history[-1] == 'b':
            return ['f', 'c', 'r']
        if history[-1] == 'c':
            if len(community) < 5:
                return 'D'
            if len(community) == 5:
                winner = compare(pocket0 + community, pocket1 + community)
                return bet[0] *  winner # both bet the same

def generate_random_history():
    hu = HoldemHU()
    h=hu.deal()
    print(hand2string(h))
    actions = hu.get_actions_available(h)
    while type(actions) != int:
        print(actions)
        if actions == 'D':
            cards = hu.deal_cards(h)
            print(hand2string(cards))
            h += cards
        else:
            h.append(np.random.choice(actions))
        actions = hu.get_actions_available(h)
    print_history(h)
    print('player {} wins {}'.format(-0.5*np.sign(actions) + 0.5, abs(actions)))

def print_history(h):
    print('dealer has {}, utg has {}'.format(hand2string(h[:2]), hand2string(h[2:4])))
    turn = 0
    for c in h[4:]:
        if isinstance(c, Card):
            print(hand2string([c]))
        else:
            print('Player {} does {}'.format(turn, c))
            turn = 1 - turn

if __name__ == "__main__":
    hu = HoldemHU()
    h = hu.deal()
    print(hand2string(h))
    h += hu.deal_cards(h)
    print(hand2string(h))
    h += hu.deal_cards(h)
    print(hand2string(h))
    h += hu.deal_cards(h)
    print(hand2string(h))
    generate_random_history()
