# breakthroughgame.py
# by: Bright Kata

""" Implementation of Breakthrough game rules

"""
from enum import Enum


class Color(Enum):
    BLACK = "BLACK"
    WHITE = "WHITE"


class BreakthroughGame:
    """Implementation of the rules of breakthrough.  Assumes an 8x8 board
    with rows and columns numbered 0--7. A location on the board is
    given as a pair: (row, column). Black pawns start on rows 0 and 1 while
    white pawns start on rows 6 and 7.

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

    def __init__(self):
        self.board = self.initialize_board()
        self.current_turn = Color.WHITE
        self._winner = None

    def initialize_board(self):
        """Initialize the game board with pieces in starting positions."""
        board = [[None for _ in range(8)] for _ in range(8)]
        for col in range(8):
            board[0][col] = Color.BLACK
            board[1][col] = Color.BLACK
            board[6][col] = Color.WHITE
            board[7][col] = Color.WHITE
        return board

    def __getitem__(self, loc):
        """Return owner of piece at loc (row, column).

        pre: loc is a valid (row, col) board location 
        post: result in [Color.BLACK, Color.WHITE, None]
        """
        row, col = loc
        return self.board[row][col]

    @property
    def player_in_turn(self):
        """Indicate the player that is in turn, i.e. allowed to move.

        post: result in [Color.BLACK, Color.WHITE]
        """
        return self.current_turn

    @property
    def winner(self):
        """The winner of the game.

        Note: value is None, if game is still in progress
        post: result in [Color.BLACK, Color.WHITE, None]
        """
        return self._winner

    def is_valid_move(self, fromloc, toloc):
        """Validate a move from fromloc to toloc.

        pre: fromloc and toloc are valid (row, column) board locations
        post: returns True if move is valid, False otherwise
        """
        from_row, from_col = fromloc
        to_row, to_col = toloc

        # Check if the move is within the board boundaries
        if not (0 <= from_row < 8 and 0 <= from_col < 8):
            return False
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            return False
        
        piece = self.board[from_row][from_col]
        target = self.board[to_row][to_col]

        # Check if the piece is not None
        if piece is None:
            return False

        # Check if it's the player's turn
        if piece != self.current_turn:
            return False

        if piece == Color.WHITE:
            if to_row == from_row - 1 and to_col == from_col and target is None:
                return True  # Move forward
            if to_row == from_row - 1 and abs(to_col - from_col) == 1 and target == Color.BLACK:
                return True  # Capture diagonally
        elif piece == Color.BLACK:
            if to_row == from_row + 1 and to_col == from_col and target is None:
                return True  # Move forward
            if to_row == from_row + 1 and abs(to_col - from_col) == 1 and target == Color.WHITE:
                return True  # Capture diagonally

        return False

    def move(self, fromloc, toloc):
        """Move piece from fromloc to toloc.

        pre: fromloc and toloc are valid (row, column) board locations
             and there is a piece at fromloc
        post: the move is performed
        note: move does not have to be valid
        """
        if self._winner is not None:
            print("Game has already ended.")
            return False

        if self.is_valid_move(fromloc, toloc):
            from_row, from_col = fromloc
            to_row, to_col = toloc

            self.board[to_row][to_col] = self.board[from_row][from_col]
            self.board[from_row][from_col] = None

            print(f"Moved piece from {fromloc} to {toloc}")

            if self.check_game_end():
                self._winner = self.current_turn
                print(f"Game ended. Winner: {self._winner}")
                return True

            self.switch_turn()
            return True
        else:
            print(f"Invalid move from {fromloc} to {toloc}")
            return False

    def check_game_end(self):
        """Check if the game has ended."""
        if self.check_pawn_reaches_opposite_end():
            self._winner = self.current_turn
            return True
        if self.check_all_pieces_captured():
            self._winner = self.current_turn
            return True
        if self.check_no_valid_moves():
            self._winner = self.current_turn
            return True
        return False

    def check_pawn_reaches_opposite_end(self):
        """Check if any pawn has reached the opposite end."""
        for col in range(8):
            if self.board[0][col] == Color.WHITE or self.board[7][col] == Color.BLACK:
                return True
        return False

    def check_all_pieces_captured(self):
        """Check if all pieces of one color are captured."""
        white_pieces = any(Color.WHITE in row for row in self.board)
        black_pieces = any(Color.BLACK in row for row in self.board)
        return not white_pieces or not black_pieces

    def check_no_valid_moves(self):
        """Check if there are no valid moves left for the current player."""
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == self.current_turn:
                    for d_row in [-1, 1]:
                        for d_col in [-1, 0, 1]:
                            if 0 <= row + d_row < 8 and 0 <= col + d_col < 8:
                                if self.is_valid_move((row, col), (row + d_row, col + d_col)):
                                    return False
        return True

    def switch_turn(self):
        """Switch the turn to the other player."""
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE