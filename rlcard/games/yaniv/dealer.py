
from rlcard.utils import init_54_deck
from rlcard.core import Card
from typing import List

class YanivDealer(object):
    ''' Initialize a uno dealer class
    '''
    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_54_deck() # type: List[Card]
        self.shuffle()

    def shuffle(self):
        ''' Shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_card(self) -> Card:
        ''' Deal one card from the deck

        Returns:
            (Card): The drawn card from the deck
        '''
        return self.deck.pop()

