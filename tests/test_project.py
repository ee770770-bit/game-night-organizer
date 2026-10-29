"""
tests/test_project.py - 6 בדיקות יחידה מקיפות למערכת.
להרצה: python -m unittest discover -s tests -v
"""
import unittest
from games_data import get_initial_games, add_game, validate_game_data
from recommender import rank_games, filter_games
from search_reports import search_by_tag

class TestGameNightOrganizer(unittest.TestCase):

    def setUp(self):
        self.sample_games = [
            {"id": "g1", "name": "Game Alpha", "min_players": 2, "max_players": 4, "duration": 30, "tags": ["strategy"]},
            {"id": "g2", "name": "Game Beta", "min_players": 4, "max_players": 6, "duration": 60, "tags": ["party"]},
            {"id": "g3", "name": "Game Gamma", "min_players": 2, "max_players": 4, "duration": 45, "tags": ["strategy", "party"]}
        ]

    def test_01_normal_recommendation_ranking(self):
        ranked = rank_games(self.sample_games, players_count=3, max_time=50, preferred_tags=["strategy"])
        self.assertEqual(len(ranked), 2)
        # Game Gamma אמור לצאת ראשון (ציון תגית + זמן קרוב יותר ל-50)
        self.assertEqual(ranked[0]["game"]["id"], "g3")
        self.assertTrue(ranked[0]["score"] > ranked[1]["score"])

    
    def test_02_empty_dataset_handling(self):
        ranked = rank_games([], players_count=4, max_time=60, preferred_tags=["party"])
        self.assertEqual(ranked, [])

    def test_03_invalid_game_data_rejected(self):
        invalid_game = {
            "id": "bad_game",
            "name": "שגיאה",
            "min_players": 5,
            "max_players": 3, 
            "duration": 30,
            "tags": ["party"]
        }
        is_valid, msg = validate_game_data(invalid_game, self.sample_games)
        self.assertFalse(is_valid)
        with self.assertRaises(ValueError):
            add_game(self.sample_games, invalid_game)

    def test_04_exact_boundary_limits(self):
        eligible = filter_games(self.sample_games, players_count=4, max_time=30)
        self.assertEqual(len(eligible), 1)
        self.assertEqual(eligible[0]["id"], "g1")

    def test_05_tie_breaking_logic(self):
        tied_games = [
            {"id": "t1", "name": "B Game", "min_players": 2, "max_players": 4, "duration": 30, "tags": ["fun"]},
            {"id": "t2", "name": "A Game", "min_players": 2, "max_players": 4, "duration": 40, "tags": ["fun"]}
        ]
        ranked = rank_games(tied_games, players_count=3, max_time=60, preferred_tags=["fun"])
        self.assertEqual(ranked[0]["game"]["id"], "t2")
        self.assertEqual(ranked[1]["game"]["id"], "t1")

    def test_06_immutability_and_state_consistency(self):
        original_count = len(self.sample_games)
        new_game = {"id": "g4", "name": "Game Delta", "min_players": 2, "max_players": 2, "duration": 15, "tags": ["fast"]}
        updated = add_game(self.sample_games, new_game)
        
        self.assertEqual(len(self.sample_games), original_count)
        self.assertEqual(len(updated), original_count + 1)

if __name__ == "__main__":
    unittest.main()
