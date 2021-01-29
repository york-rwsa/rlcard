import unittest
import numpy as np

from rlcard.games.yaniv.round import YanivRound
from rlcard.games.yaniv.player import YanivPlayer
from rlcard.core import Card
import rlcard.games.yaniv.utils as utils


class TestYanivRound(unittest.TestCase):
    # def setUp(self):
    #     self.round = YanivRound(None, 1, None)

    def test_legal_pairs(self):
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

    def test_legal_trips(self):
        rnd = YanivRound(None, 1, None)
        player = YanivPlayer(1, None)
        player.hand = [
            Card("S", "1"),
            Card("D", "1"),
            Card("C", "1"),
        ]

        actions = rnd.get_legal_actions([player], 0)
        expectations = [
            "yaniv",
            "S1",
            "D1",
            "C1",
            "C1D1",
            "C1S1",
            "D1S1",
            "C1S1D1",
            "C1D1S1",
            "D1C1S1",
        ]
        for action in expectations:
            self.assertIn(action, actions)

        self.assertEqual(len(expectations), len(actions))

    def test_legal_quads(self):
        rnd = YanivRound(None, 1, None)
        player = YanivPlayer(1, None)
        player.hand = [
            Card("S", "1"),
            Card("D", "1"),
            Card("H", "1"),
            Card("C", "1"),
        ]

        actions = rnd.get_legal_actions([player], 0)
        expectations = [
            "yaniv",
            "S1",
            "D1",
            "H1",
            "C1",
            "C1D1",
            "C1H1",
            "C1S1",
            "D1H1",
            "D1S1",
            "H1S1",
            "D1C1H1",
            "C1D1H1",
            "C1H1D1",
            "D1C1S1",
            "C1D1S1",
            "C1S1D1",
            "H1C1S1",
            "C1H1S1",
            "C1S1H1",
            "H1D1S1",
            "D1H1S1",
            "D1S1H1",
            "C1H1S1D1",
            "C1D1S1H1",
            "C1D1H1S1",
            "D1C1S1H1",
            "D1C1H1S1",
            "H1C1D1S1",
        ]
        for action in expectations:
            self.assertIn(action, actions)

        self.assertEqual(len(expectations), len(actions))

    def test_legal_straights(self):
        rnd = YanivRound(None, 1, None)
        player = YanivPlayer(1, None)
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

    def test_get_legal_actions_pickup(self):
        rnd = YanivRound(None, 1, None)
        player = YanivPlayer(1, None)
        player.hand = [
            Card("S", "T"),
            Card("S", "1"),
            Card("D", "T"),
            Card("S", "Q"),
        ]
        rnd.discarding = False

        actions = rnd.get_legal_actions([player], 0)
        self.assertEqual(utils.pickup_actions, actions)


if __name__ == "__main__":
    unittest.main()
