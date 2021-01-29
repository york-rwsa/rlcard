import unittest
import numpy as np

from rlcard.games.yaniv.round import YanivRound
from rlcard.games.yaniv.player import YanivPlayer
from rlcard.core import Card


class TestYanivRound(unittest.TestCase):
    # def setUp(self):
    #     self.round = YanivRound(None, 1, None)

    def test_get_legal_actions(self):
        rnd = YanivRound(None, 1, None)
        player = YanivPlayer(1, None)
        player.hand = [
            Card("S", "T"),
            Card("S", "1"),
            Card("D", "T"),
            Card("S", "J"),
            Card("S", "Q"),
        ]

        actions = rnd.get_legal_actions([player], 0)
        self.assertIn("DTST", actions)
        self.assertIn("STJQ", actions)
        self.assertIn("ST", actions)
        self.assertIn("DT", actions)
        self.assertEqual(7, len(actions))

        player.hand = [
            Card("S", "9"),
            Card("S", "T"),
            Card("S", "J"),
            Card("S", "Q"),
        ]

        actions = rnd.get_legal_actions([player], 0)
        self.assertIn("S9TJQ", actions)
        self.assertIn("STJQ", actions)
        self.assertIn("S9TJ", actions)
        self.assertEqual(7, len(actions))

        player.hand = [
            Card("S", "8"),
            Card("S", "9"),
            Card("S", "T"),
            Card("S", "J"),
            Card("S", "Q"),
        ]

        actions = rnd.get_legal_actions([player], 0)
        self.assertIn("S89TJQ", actions)
        self.assertIn("S9TJQ", actions)
        self.assertIn("S89TJ", actions)
        self.assertIn("STJQ", actions)
        self.assertIn("S9TJ", actions)
        self.assertIn("S89T", actions)
        self.assertEqual(11, len(actions))

        player.hand = [Card("S", "1")]
        actions = rnd.get_legal_actions([player], 0)
        self.assertIn("yaniv", actions)
        self.assertIn("S1", actions)
        self.assertEqual(2, len(actions))


if __name__ == "__main__":
    unittest.main()
