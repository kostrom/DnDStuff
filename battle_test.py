""" unit test for battle.py """
from unittest import TestCase, main
from unittest.mock import patch

from player import Player

from arena import attack_rolls

def fixedroller(count, die):
    """ this will replace the random die in our test """
    return count * max(1, die-2)

class TestBattle(TestCase):
    """ unit tests for the dnd5e battle simulator """

    @patch('arena.roll', side_effect=fixedroller)
    def test_battle(self, mock_roller):
        """ test the outcome of a mock battle with a fixed die"""
        verbose = False
        winner = Player(name="winner", maxhp=30, ac=15, attacks=[[0, 1, 6, 4]])
        loser = Player(name="loser", maxhp=20, ac=15, attacks=[[0, 1, 6, 0]])
        attack_rolls(winner, loser, verbose)
        self.assertEqual(winner.hp, 30)
        self.assertEqual(loser.hp, 12)
        self.assertEqual(mock_roller.call_count, 2)
        attack_rolls(loser, winner, verbose)
        self.assertEqual(winner.hp, 26)
        self.assertEqual(loser.hp, 12)
        self.assertEqual(mock_roller.call_count, 4)

if __name__ == '__main__':
    main()
