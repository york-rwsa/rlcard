import numpy as np

from rlcard.envs import Env
from rlcard.games.yaniv import Game, utils


# for two player
class YanivEnv(Env):
    def __init__(self, config):
        self.name = "yaniv"
        self.game = Game()
        super().__init__(config)
        self.state_shape = [6, 52]

    def _extract_state(self, state):
        if self.game.is_over():
            return {
                "obs": np.array([utils.encode_cards([]) for _ in range(7)]),
                "legal_actions": self._get_legal_actions(),
            }

        discard_pile = self.game.round.discard_pile
        if self.game.round.discarding:
            last_discard = discard_pile[-1]
        else:
            last_discard = discard_pile[-2]

        available_discard = set([last_discard[0], last_discard[-1]])
        deadcards = [c for d in discard_pile for c in d if c not in available_discard]

        current_player = self.game.players[self.game.round.current_player]
        next_player = self.game.players[self.game.round.get_next_player()]
        known_cards = self.game.round.known_cards[next_player.get_player_id()]
        unknown_cards = self.game.round.dealer.deck + [
            c for c in next_player.hand if c not in known_cards
        ]

        card_obs = [
            current_player.hand,
            available_discard,
            deadcards,
            known_cards,
            unknown_cards,
        ]
        opponent_hand_size = np.zeros(52)
        opponent_hand_size[len(next_player.hand)] = 1
        obs = list(map(utils.encode_cards, card_obs)) + [opponent_hand_size]

        extracted_state = {"obs": np.array(obs), "legal_actions": self._get_legal_actions()}

        if self.allow_raw_data:
            extracted_state['raw_obs'] = state
            extracted_state['raw_legal_actions'] = [
                a for a in state['legal_actions']]

        if self.record_action:
            extracted_state['action_record'] = self.action_recorder
        
        return extracted_state

    def get_payoffs(self):
        return np.array(self.game.get_payoffs())

    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        if action_id in legal_ids:
            return utils.ACTION_LIST[action_id]
        else:
            raise Exception("decode_action: unknown action_id={}".format(action_id))

    def _get_legal_actions(self):
        legal_actions = self.game.get_legal_actions()
        legal_ids = [utils.ACTION_SPACE[action] for action in legal_actions]
        return legal_ids

    def _load_model(self):
        """Load pretrained/rule model

        Returns:
            model (Model): A Model object
        """
        raise NotImplementedError