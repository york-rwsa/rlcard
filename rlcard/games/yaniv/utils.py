import os
import json
import numpy as np
from collections import OrderedDict
from copy import copy
from rlcard.games.yaniv.card import YanivCard
import rlcard

ASSAF_PENALTY = 30
INITIAL_NUMBER_OF_CARDS = 5

PICKUP_TOP_DISCARD_ACTION = "pickup_top_discard"
PICKUP_BOTTOM_DISCARD_ACTION = "pickup_bottom_discard"
DRAW_CARD_ACTION = "draw_card"
YANIV_ACTION = "yaniv"

ROOT_PATH = rlcard.__path__[0]

pickup_actions = [
    PICKUP_TOP_DISCARD_ACTION,
    PICKUP_BOTTOM_DISCARD_ACTION,
    DRAW_CARD_ACTION,
]
# a map of abstract action to its index and a list of abstract action
with open(
    os.path.join(ROOT_PATH, "games/yaniv/jsondata/discard_actions.json"), "r"
) as file:
    DISCARD_ACTIONS = json.load(file, object_pairs_hook=OrderedDict)
    DISCARD_ACTION_LIST = list(DISCARD_ACTIONS.keys())

    ACTION_SPACE = OrderedDict()
    ACTION_SPACE.update(DISCARD_ACTIONS)

    for action in pickup_actions:
        ACTION_SPACE.update({action: len(ACTION_SPACE)})

    ACTION_SPACE.update({YANIV_ACTION: len(ACTION_SPACE)})
    ACTION_LIST = list(ACTION_SPACE.keys())

def get_hand_score(cards: list[YanivCard]) -> int:
    """Judge the score of a given cards set

    Args:
        cards (list): a list of cards

    Returns:
        score (int): the score of the given cards set
    """

    score = 0
    for card in cards:
        score += card.get_score()

    return score

def cardlist_to_action(cards: list[YanivCard]) -> str:
    return "".join([str(c) for c in cards])

def cards_to_list(cards: list[YanivCard]) -> list[str]:
    return [
        str(c) for c in sorted(cards, key=lambda x: (x.suit, x.get_rank_as_int()))
    ]

def cards_to_str(cards: list[YanivCard]) -> str:
    return "".join(cards_to_list(cards))


def init_deck() -> list[YanivCard]:
    return [YanivCard(suit, rank) for suit in YanivCard.suits for rank in YanivCard.ranks]
