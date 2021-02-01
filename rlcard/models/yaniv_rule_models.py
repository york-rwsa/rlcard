import numpy as np
import rlcard

from rlcard.models.model import Model
import rlcard.games.yaniv.utils as utils

from operator import methodcaller


class YanivNoviceRuleAgent(object):
    """
    Agent always discards highest action value

    """

    def __init__(self):
        self.use_raw = False # TODO: convert to use raw, as much easeir to read

    @staticmethod
    def step(state):
        """Predict the action given the current state.
            Novice strategy:
                Discard stage:
                    - Yaniv if can and opponenets hand is less than my hand
                    - discard highest scoring combination of cards
                Pickup stage:
                    - draw
                    - unless ace or 2


        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted
        """
        legal_actions = state["legal_actions"]
        decoded_legals = [utils.ACTION_LIST[a] for a in legal_actions]

        # picking up
        if utils.DRAW_CARD_ACTION in decoded_legals:
            availcards = utils.decode_cards(state["obs"][1])
            actions = []
            if availcards[0].get_score() <= 2:
                actions.append(utils.ACTION_SPACE[utils.PICKUP_TOP_DISCARD_ACTION])

            if len(availcards) == 2 and availcards[1].get_score() <= 2:
                actions.append(utils.ACTION_SPACE[utils.PICKUP_BOTTOM_DISCARD_ACTION])

            # otherwise
            if len(actions) == 0:
                actions = [utils.ACTION_SPACE[utils.DRAW_CARD_ACTION]]

            return np.random.choice(actions)

        # discarding
        actions = []
        if utils.ACTION_SPACE[utils.YANIV_ACTION] in legal_actions:
            hand = utils.decode_cards(state["obs"][0])
            handscore = sum(map(methodcaller("get_score"), hand))
            known_cards = utils.decode_cards(state["obs"][3])
            known_score = sum(map(methodcaller("get_score"), known_cards))
            if handscore < known_score:
                actions.append(utils.ACTION_SPACE[utils.YANIV_ACTION])

        legal_discard_actions = [
            a for a in legal_actions if a != utils.ACTION_SPACE[utils.YANIV_ACTION]
        ]
        legal_discards = [utils.ACTION_LIST[a] for a in legal_discard_actions]
        discard_scores = list(map(utils.score_discard_action, legal_discards))
        max_discard = max(discard_scores)
        best_discards = [
            legal_discard_actions[i]
            for i, ds in enumerate(discard_scores)
            if ds == max_discard
        ]
        actions.extend(best_discards)

        return np.random.choice(actions)

    def eval_step(self, state):
        """Predict the action given the current state for evaluation.
            Since the agents is not trained, this function is equivalent to step function.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted by the agent
            probabilities (list): The list of action probabilities
        """
        probabilities = []
        return self.step(state), probabilities


class YanivNoviceRuleModel(Model):
    """Yaniv Rule Model"""

    def __init__(self):
        """Load pre-trained model"""
        super().__init__()
        env = rlcard.make("yaniv")
        rule_agent = YanivNoviceRuleAgent()
        self.rule_agents = [rule_agent for _ in range(env.player_num)]

    @property
    def agents(self):
        """Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        """
        return self.rule_agents
