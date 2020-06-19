from unittest import TestCase, main
from unittest.mock import patch

from player import Player
from arena import attackRolls

def fixedroller(low, high):
    result = max(low, high-2)
    return result

class TestBattle(TestCase):
    
    @patch('arena.roll', side_effect=fixedroller)
    def test_battle(self, mock_roll):
        verbose = False
        winner = Player(name="winner", maxhp=30, ac=15, attacks=[[0,1,6,4]], detailedTracking=verbose)
        loser = Player(name="loser", maxhp=20, ac=15, attacks=[[0,1,6,0]], detailedTracking=verbose)
        attackRolls(winner, loser, verbose)
        self.assertEqual(winner.hp, 30)
        self.assertEqual(loser.hp, 12)
        attackRolls(loser, winner, verbose)
        self.assertEqual(winner.hp, 26)
        self.assertEqual(loser.hp, 12)
    
if __name__ == '__main__':
    main()