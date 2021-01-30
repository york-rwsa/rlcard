import unittest
import numpy as np

from rlcard.games.yaniv import Round, Game, utils


class TestYanivRound(unittest.TestCase):
    def test_get_player_num(self):
        game = Game()
        player_num = game.get_player_num()
        self.assertEqual(player_num, 2)

        game = Game(3)
        player_num = game.get_player_num()
        self.assertEqual(player_num, 3)

    def test_get_action_num(self):
        game = Game()
        action_num = game.get_action_num()
        self.assertEqual(action_num, 488)

    def test_init_game(self):
        game = Game()
        state, current_player = game.init_game()
        self.assertEqual(current_player, 0)
        for player in game.players:
            self.assertEqual(len(player.hand), utils.INITIAL_NUMBER_OF_CARDS)
        self.assertEqual(len(game.round.discard_pile), 1)
        self.assertEqual(len(game.round.discard_pile[0]), 1)
    
    def test_step(self):
        game = Game()
        _, current_player = game.init_game()

        # discard first
        action = np.random.choice([a for a in game.get_legal_actions() if a != 'yaniv'])
        self.assertNotIn(action, utils.pickup_actions)
        self.assertIn(action, utils.ACTION_LIST)
        _, next_player = game.step(action)
        self.assertEqual(next_player, current_player)

        # then pickup
        action = np.random.choice(game.get_legal_actions())
        self.assertIn(action, utils.pickup_actions)
        _, next_player = game.step(action)
        self.assertEqual(next_player, (current_player + 1) % game.get_player_num())
        
    def test_proceed_game(self):
        game = Game()
        game.init_game()
        while not game.is_over():
            legal_actions = game.get_legal_actions()
            action = np.random.choice(legal_actions)
            self.assertIn(action, utils.ACTION_LIST)
            _, _ = game.step(action)

        self.assertEqual(game.actions[-1], 'yaniv')
        
if __name__ == "__main__":
    unittest.main()
