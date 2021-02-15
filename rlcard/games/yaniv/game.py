from copy import deepcopy
import numpy as np

from rlcard.games.yaniv.dealer import YanivDealer
from rlcard.games.yaniv.player import YanivPlayer
from rlcard.games.yaniv.round import YanivRound
from rlcard.games.yaniv import utils


class YanivGame(object):
    def __init__(self, num_players=2, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = num_players
        self.payoffs = [0 for _ in range(self.num_players)]
        self.actions = []

        # default config
        self._end_after_n_deck_replacements = 0
        self._end_after_n_steps = 0
        self._early_end_reward = 0

    def init_game(self):
        """Initialize players and state

        Returns:
            (tuple): Tuple containing:
                (dict): The first state in one game
                (int): Current player's id
        """
        # Initalize payoffs
        self.payoffs = [0 for _ in range(self.num_players)]

        # Initialize a dealer that can deal cards
        self.dealer = YanivDealer(self.np_random)

        # Initialize four players to play the game
        self.players = [YanivPlayer(i, self.np_random) for i in range(self.num_players)]

        # Deal 5 cards to each player
        for _ in range(utils.INITIAL_NUMBER_OF_CARDS):
            for player in self.players:
                player.hand.append(self.dealer.draw_card())

        # Initialize a Round
        self.round = YanivRound(
            self.dealer,
            self.num_players,
            self.np_random,
        )
        self.round.flip_top_card()

        # Save the hisory for stepping back to the last state.
        self.history = []

        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id

    def configure(self, config):
        """Specifiy some game specific parameters, such as player number"""
        self._end_after_n_deck_replacements = config[
            "end_after_n_deck_replacements"
        ]
        self._end_after_n_steps = config["end_after_n_steps"]
        self._early_end_reward = config["early_end_reward"]

    def step(self, action):
        """Get the next state

        Args:
            action (str): A specific action

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        """

        if self.allow_step_back:
            # First snapshot the current state
            his_dealer = deepcopy(self.dealer)
            his_round = deepcopy(self.round)
            his_players = deepcopy(self.players)
            self.history.append((his_dealer, his_players, his_round))

        self.actions.append(action)
        self.round.proceed_round(self.players, action)
        player_id = self.round.current_player
        state = self.get_state(player_id)

        if self._end_after_n_steps > 0 and len(self.actions) >= self._end_after_n_steps:
            self.round.winner = -1
            self.round.is_over = True

        # end the game if repalce deck is required with everyone losing
        if (
            self._end_after_n_deck_replacements > 0
            and self.round.deck_replacements >= self._end_after_n_deck_replacements
        ):
            self.round.winner = -1
            self.round.is_over = True

        return state, player_id

    def step_back(self):
        """Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        """
        if not self.history:
            return False
        self.dealer, self.players, self.round = self.history.pop()
        return True

    def get_state(self, player_id):
        """Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        """
        state = self.round.get_state(self.players, player_id)
        state["player_num"] = self.get_player_num()
        state["current_player"] = self.round.current_player
        return state

    def get_payoffs(self):
        """Return the payoffs of the game
        1 if game won
        -(score / 50) otherwise

        Returns:
            (list): Each entry corresponds to the payoff of one player
        """
        self.payoffs = []
        if self.round.winner == -1:
            self.payoffs = [self._early_end_reward for _ in range(self.num_players)]
        else:
            for score in self.round.scores:
                if score == 0:
                    payoff = 1
                else:
                    payoff = -(score / 50)

                self.payoffs.append(payoff)

        return self.payoffs

    def get_legal_actions(self):
        """Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        """

        return self.round.get_legal_actions(self.players, self.round.current_player)

    def get_player_num(self):
        """Return the number of players in Limit Texas Hold'em

        Returns:
            (int): The number of players in the game
        """
        return self.num_players

    @staticmethod
    def get_action_num():
        """Return the number of applicable actions

        Returns:
            (int): The number of actions.
        """
        return len(utils.ACTION_LIST)

    def get_player_id(self):
        """Return the current player's id

        Returns:
            (int): current player's id
        """
        return self.round.current_player

    def is_over(self):
        """Check if the game is over

        Returns:
            (boolean): True if the game is over
        """
        return self.round.is_over


## For test
if __name__ == "__main__":
    # import time
    # random.seed(0)
    # start = time.time()
    game = YanivGame()
    for _ in range(1):
        state, button = game.init_game()
        print(button, state)
        i = 0
        while not game.is_over():
            i += 1
            legal_actions = game.get_legal_actions()
            print("legal_actions", legal_actions)
            action = np.random.choice(legal_actions)
            print("action", action)
            print()
            state, button = game.step(action)
            print(button, state)
        print(game.get_payoffs())
    print("step", i)
