import random

""" protocol game:
        def whose_turn(history)

        def deal()

        def get_actions_available(history)
        """

class Khun: #implements game
    @staticmethod
    def deal():
        return ''.join(random.sample('JQK', 3))[:2]

    @staticmethod
    def whose_turn(history):
        return (len(history) + 1)%2

    @staticmethod
    def value(card):
        if card == 'Q':
            return 1
        elif card == 'K':
            return 2
        else:
            return 0

    @staticmethod
    def get_actions_available(history):
        if history == '':
            return 'D'
        if history[2:] == 'pp':
            return 2*(Khun.value(history[0]) > Khun.value(history[1])) - 1
        elif history[-2:] == 'bb':
            return 4*(Khun.value(history[0]) > Khun.value(history[1])) - 2
        elif history[2:] == 'bp':
            return -1
        elif history[2:] == 'pbp':
            return 1
        else:
            return ['p', 'b']

class KhunNCards: #implements game
    def __init__(self, N):
        if N > 13:
            N = 13
        elif N < 3:
            N = 3
        self.N = N

    def deal(self):
        cards = 'AKQJT98765432'[:self.N]
        return ''.join(random.sample(cards, self.N))[:2]

    @staticmethod
    def whose_turn(history):
        return (len(history) + 1)%2

    @staticmethod
    def value(card):
        if card == 'A':
            return 14
        elif card == 'K':
            return 13
        elif card == 'Q':
            return 12
        elif card == 'J':
            return 11
        elif card == 'T':
            return 10
        else:
            return int(card)

    @staticmethod
    def get_actions_available(history):
        if history == '':
            return 'D'
        if history[2:] == 'pp':
            return 2*(KhunNCards.value(history[0]) > KhunNCards.value(history[1])) - 1
        elif history[-2:] == 'bb':
            return 4*(KhunNCards.value(history[0]) > KhunNCards.value(history[1])) - 2
        elif history[2:] == 'bp':
            return -1
        elif history[2:] == 'pbp':
            return 1
        else:
            return ['p', 'b']

class KhunNCardsRaise(KhunNCards): #implements game
    def __init__(self, N):
        KhunNCards.__init__(self, N)

    @staticmethod
    def whose_turn(history):
        return (len(history) + 1)%2

    @staticmethod
    def get_actions_available(history):
        if history == '':
            return 'D'
        elif history[-1] == 'c':
            best = 2*(KhunNCardsRaise.value(history[0]) > KhunNCardsRaise.value(history[1])) - 1
            if history[-2] == 'b':
                return 2*best
            elif history[-2] == 'r':
                return 3*best
            else:
                return best
        elif history[-1] == 'f':
            num_actions = len(history[2:])
            winner = 2*(num_actions%2) - 1
            if history[-2] == 'r':
                return 2*winner
            else:
                return winner
        elif history[-1] == 'b':
            return ['f', 'c', 'r']
        elif history[-1] == 'r':
            return ['f', 'c']
        elif len(history) == 2:
            return ['p', 'b']
        else:
            return ['c', 'b']

