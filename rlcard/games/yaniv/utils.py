import os
import json
import numpy as np
from collections import OrderedDict

import rlcard

ASSAF_PENALTY = 30

ROOT_PATH = rlcard.__path__[0]

pickup_actions = ["pickup_top_discard", "pickup_bottom_discard", "draw_card"]
# a map of abstract action to its index and a list of abstract action
with open(
    os.path.join(ROOT_PATH, "games/yaniv/jsondata/discard_actions.json"), "r"
) as file:
    ACTION_SPACE = json.load(file, object_pairs_hook=OrderedDict)
    for action in pickup_actions:
        ACTION_SPACE.update({action: len(ACTION_SPACE)})

    ACTION_SPACE.update({"yaniv": len(ACTION_SPACE)})
    ACTION_LIST = list(ACTION_SPACE.keys())

rank2score = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}

rank2int = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
}

def get_hand_score(cards):
    """Judge the score of a given cards set

    Args:
        cards (list): a list of cards

    Returns:
        score (int): the score of the given cards set
    """

    score = 0
    for card in cards:
        score += rank2score[card.rank]

    return score

def cardlist_to_action(cards):
    return  "".join([c.suit+c.rank for c in cards])

def straight_to_action(straight):
    suit = straight[0].suit
    for c in straight[1:]:
        if c.suit != suit:
            raise ValueError("striaght is not straight")
    
    return suit + "".join([c.rank for c in straight])