# testbreakthroughgame.py
# by: Bright Geofrey Kata

""" Tests for Implementation of Breakthrough game rules

Initial Board: White moves first.

    0   1   2   3   4   5   6   7
  +---+---+---+---+---+---+---+---+
0 | B | B | B | B | B | B | B | B |
  +---+---+---+---+---+---+---+---+
1 | B | B | B | B | B | B | B | B |
  +---+---+---+---+---+---+---+---+
2 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+
3 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+
4 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+
5 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+
6 | W | W | W | W | W | W | W | W |
  +---+---+---+---+---+---+---+---+
7 | W | W | W | W | W | W | W | W |
  +---+---+---+---+---+---+---+---+
"""

import unittest
from breakthroughgame import BreakthroughGame, Color


class TestBreakthroughGame(unittest.TestCase):
    def setUp(self):
        self.game = BreakthroughGame()

    def test_board_size(self):
        self.assertEqual(len(self.game.board), 8)
        for row in self.game.board:
            self.assertEqual(len(row), 8)

    def test_initial_board_setup(self):
        """Test initialization of board with black pawns at 0 and 1 and white pawns at 6 and 7"""
        # Test black pawns
        for col in range(8):
            self.assertEqual(self.game.board[0][col], Color.BLACK)
            self.assertEqual(self.game.board[1][col], Color.BLACK)
        # Test white pawns
        for col in range(8):
            self.assertEqual(self.game.board[6][col], Color.WHITE)
            self.assertEqual(self.game.board[7][col], Color.WHITE)
        # Test empty rows
        for row in range(2, 6):
            for col in range(8):
                self.assertIsNone(self.game.board[row][col])

        

    # Sprint 2
    def test_pawn_moves_forward_one_space(self):
        self.assertTrue(self.game.move((6, 0), (5, 0)))  # White pawn moves forward
        self.assertTrue(self.game.move((1, 0), (2, 0)))  # Black pawn moves forward

    def test_pawn_moves_diagonally_to_capture(self):
        self.game.board[5][1] = Color.BLACK  # Place black pawn in front of white pawn
        self.assertTrue(self.game.move((6, 0), (5, 1)))  # White pawn captures black pawn

    def test_pawn_cannot_move_backwards(self):
        self.assertFalse(self.game.move((6, 0), (7, 0)))  # White pawn tries to move backwards

    def test_pawn_cannot_move_to_the_side(self):
        self.assertFalse(self.game.move((6, 0), (6, 1)))  # White pawn tries to move sideways

    def test_pawn_cannot_move_diagonally_if_space_is_empty(self):
        self.assertFalse(self.game.move((6, 0), (5, 1)))  # White pawn tries to move diagonally to empty space

    def test_pawn_cannot_capture_same_color(self):
        self.game.board[5][1] = Color.WHITE  # Place white pawn in front of white pawn
        self.assertFalse(self.game.move((6, 0), (5, 1)))  # White pawn tries to capture white pawn

    def test_pawn_cannot_move_forward_if_space_is_occupied(self):
        self.game.board[5][0] = Color.BLACK  # Place black pawn in front of white pawn
        self.assertFalse(self.game.move((6, 0), (5, 0)))  # White pawn tries to move forward to occupied space

    def test_pawn_cannot_move_more_than_one_step(self):
        self.assertFalse(self.game.move((6, 0), (4, 0)))  # White pawn tries to move forward two spaces
        self.assertFalse(self.game.move((6, 0), (4, 2)))  # White pawn tries to move diagonally two spaces

    # Sprint 3
    def test_pawn_can_capture_opponent_piece(self):
        self.game.board[5][1] = Color.BLACK  # Place black pawn in front of white pawn
        self.assertTrue(self.game.move((6, 0), (5, 1)))  # White pawn captures black pawn
        self.assertIsNone(self.game.board[6][0])  # Original position is empty
        self.assertEqual(self.game.board[5][1], Color.WHITE)  # New position has white pawn

    def test_pawn_cannot_capture_same_color(self):
        self.game.board[5][1] = Color.WHITE  # Place white pawn in front of white pawn
        self.assertFalse(self.game.move((6, 0), (5, 1)))  # White pawn tries to capture white pawn

    def test_pawn_cannot_capture_if_space_is_empty(self):
        self.assertFalse(self.game.move((6, 0), (5, 1)))  # White pawn tries to move diagonally to empty space

    def test_pawn_cannot_capture_by_moving_forward(self):
        self.game.board[5][0] = Color.BLACK  # Place black pawn in front of white pawn
        self.assertFalse(self.game.move((6, 0), (5, 0)))  # White pawn tries to move forward to capture

    def test_capture_removes_opponent_piece(self):
        self.game.board[5][1] = Color.BLACK  # Place black pawn in front of white pawn
        self.assertTrue(self.game.move((6, 0), (5, 1)))  # White pawn captures black pawn
        self.assertIsNone(self.game.board[6][0])  # Original position is empty
        self.assertEqual(self.game.board[5][1], Color.WHITE)  # New position has white pawn
        self.assertNotEqual(self.game.board[5][1], Color.BLACK)  # Black pawn is removed from board

    def test_pawn_waits_for_player_move(self):
        self.assertFalse(self.game.move((6, 0), (5, 1)))  # White pawn does not automatically capture

    # Sprint 4
    def test_game_ends_when_pawn_reaches_opposite_end(self):
        """Set up board with a pawn at the second last row"""
        self.game.board[1][0] = Color.WHITE
        self.game.board[0][0] = None
        self.assertTrue(self.game.move((1, 0), (0, 0)))  # Move pawn to the last row

    def test_game_ends_when_all_pieces_captured(self):
        self.game.board = [[None for _ in range(8)] for _ in range(8)]
        self.game.board[7][0] = Color.WHITE
        self.game.board[0][0] = Color.BLACK



    def test_game_ends_when_no_valid_moves_left(self):
        self.game.board = [[None for _ in range(8)] for _ in range(8)]
        self.game.board[1][0] = Color.BLACK
        self.game.board[0][0] = Color.WHITE
        self.assertFalse(self.game.move((1, 0), (0, 0)))  # White captures black pawn

    def test_game_identifies_winner_when_game_ends(self):
        """ Setup board with a winning condition"""
        self.game.board[1][0] = Color.WHITE
        self.game.board[0][0] = None
        self.assertTrue(self.game.move((1, 0), (0, 0)))  # Move pawn to the last row
        self.assertEqual(self.game._winner, Color.WHITE)

    # Sprint 5
    def test_alternates_between_players(self):
        self.assertEqual(self.game.current_turn, Color.WHITE)
        self.assertTrue(self.game.move((6, 0), (5, 0)))  # White moves
        self.assertEqual(self.game.current_turn, Color.BLACK)
        self.assertTrue(self.game.move((1, 0), (2, 0)))  # Black moves
        self.assertEqual(self.game.current_turn, Color.WHITE)

    def test_not_allow_move_when_not_turn(self):
        self.assertEqual(self.game.current_turn, Color.WHITE)
        self.assertFalse(self.game.move((1, 0), (2, 0)))  # Black tries to move
        self.assertEqual(self.game.current_turn, Color.WHITE)

    def test_not_allow_wrong_piece_move(self):
        self.assertEqual(self.game.current_turn, Color.WHITE)
        self.assertFalse(self.game.move((1, 0), (2, 0)))  # Black piece move
        self.assertEqual(self.game.current_turn, Color.WHITE)

    def test_invalid_move_does_not_change_turn(self):
        self.assertEqual(self.game.current_turn, Color.WHITE)
        self.assertFalse(self.game.move((6, 0), (6, 0)))  # Invalid move
        self.assertEqual(self.game.current_turn, Color.WHITE)

    def test_not_allow_move_when_game_ended(self):
        self.game._winner = Color.WHITE  # Simulate game end
        self.assertFalse(self.game.move((6, 0), (5, 0)))  # Try to move after game end
        self.assertEqual(self.game._winner, Color.WHITE)


    # Sprint 6
    def test_move_outside_board(self):
        """ Test moving a piece outside the board boundaries"""
        self.assertFalse(self.game.is_valid_move((0, 0), (-1, 0)))  # Move off the top
        self.assertFalse(self.game.is_valid_move((0, 0), (0, -1)))  # Move off the left
        self.assertFalse(self.game.is_valid_move((7, 7), (8, 7)))  # Move off the bottom
        self.assertFalse(self.game.is_valid_move((7, 7), (7, 8)))  # Move off the right

if __name__ == "__main__":
    unittest.main()