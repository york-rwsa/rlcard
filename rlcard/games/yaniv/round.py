from rlcard.core import Card
import rlcard.games.yaniv.utils as utils
from rlcard.games.yaniv.player import YanivPlayer
from itertools import groupby
from operator import itemgetter


class YanivRound(object):
    def __init__(self, dealer, num_players, np_random):
        """Initialize the round class

        Args:
            dealer (object): the object of YanivDealer
            num_players (int): the number of players in game
        """
        self.np_random = np_random
        self.dealer = dealer
        self.current_player = 0
        self.num_players = num_players
        self.played_cards = []  # List[List[Card]]

        # discard first
        self.discarding = True

    def proceed_round(self, players, action):
        """Call other Classes's functions to keep one round running

        Args:
            player (object): YanivPlayer
            action (str): string of legal action
        """
        if action == "draw":
            self._perform_draw_action(players)
            return None
        player = players[self.current_player]

    def get_legal_actions(self, players: list[YanivPlayer], player_id):
        if not self.discarding:
            return utils.pickup_actions

        hand = players[player_id].hand
        legal_actions = []

        if utils.get_hand_score(hand) <= 7:
            legal_actions.append("yaniv")

        # can discard single cards
        for card in hand:
            legal_actions.append(card.suit + card.rank)

        suitKey = lambda c: c.suit
        rankKey = lambda c: utils.rank2int[c.rank]
        # groups of rank
        for rank, group in groupby(sorted(hand, key=rankKey), key=rankKey):
            cards = sorted(list(group), key=suitKey)

            if len(cards) == 1:
                continue

            if len(cards) == 2:
                legal_actions.append(utils.cardlist_to_action(cards))

            if len(cards) == 3:
                pass

        # straights
        for suit, group in groupby(sorted(hand, key=suitKey), key=suitKey):
            cards = sorted(group, key=rankKey)

            for _, straight in groupby(
                enumerate(cards), key=lambda x: x[0] - utils.rank2int[x[1].rank]
            ):
                straight = list(straight)
                if len(straight) < 3:
                    continue

                straight = [s[1] for s in straight]

                # whole straight
                legal_actions.append(utils.straight_to_action(straight))

                if len(straight) >= 4:
                    legal_actions.append(utils.straight_to_action(straight[0:3]))
                    legal_actions.append(utils.straight_to_action(straight[1:4]))

                if len(straight) == 5:
                    legal_actions.append(utils.straight_to_action(straight[2:5]))

                    legal_actions.append(utils.straight_to_action(straight[0:4]))
                    legal_actions.append(utils.straight_to_action(straight[1:5]))

        return legal_actions

    def get_state(self, players, player_id):
        """Get player's state

        Args:
            players (list): The list of UnoPlayer
            player_id (int): The id of the player
        """
        state = {}
        player = players[player_id]
        state["hand"] = cards2list(player.hand)
        state["target"] = self.target.str
        state["played_cards"] = cards2list(self.played_cards)
        others_hand = []
        for player in players:
            if player.player_id != player_id:
                others_hand.extend(player.hand)
        state["others_hand"] = cards2list(others_hand)
        state["legal_actions"] = self.get_legal_actions(players, player_id)
        state["card_num"] = []
        for player in players:
            state["card_num"].append(len(player.hand))
        return state

    def replace_deck(self):
        """Add cards have been played to deck"""
        self.dealer.deck.extend(self.played_cards)
        self.dealer.shuffle()
        self.played_cards = []

    def _perform_draw_action(self, players):
        if not self.dealer.deck:
            self.replace_deck()

        card = self.dealer.deck.pop()
        players[self.current_player].hand.append(card)

        # TODO deal with itsbah
