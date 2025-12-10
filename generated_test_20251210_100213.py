import sys
from pathlib import Path
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / 'py-tic-tac-toe'))
import pytest
from unittest.mock import patch
from Main import TicTacToe
import random

@pytest.fixture
def game():
    """Provides a TicTacToe instance for each test."""
    return TicTacToe()

def test_initialization(game):
    """Test that the board is an empty list initially."""
    assert game.board == []

def test_create_board(game):
    """Test that create_board initializes a 3x3 board with dashes."""
    game.create_board()
    assert len(game.board) == 3
    for row in game.board:
        assert len(row) == 3
        assert all(cell == '-' for cell in row)

@pytest.mark.parametrize("randint_return, expected_player", [(0, 'O'), (1, 'X')])
def test_get_random_first_player_and_start_assignment(game, randint_return, expected_player):
    """Test that get_random_first_player returns a valid choice."""
    with patch('random.randint', return_value=randint_return):
        # The start method uses get_random_first_player, so we test its effect here
        # without running the full game loop.
        game.create_board()
        player = 'X' if game.get_random_first_player() == 1 else 'O'
        assert player == expected_player

def test_get_random_first_player_range(game):
    """Test that the random player is either 0 or 1."""
    player_choice = game.get_random_first_player()
    assert player_choice in [0, 1]

def test_fix_spot(game):
    """Test that fix_spot correctly places a player's mark on the board."""
    game.create_board()
    game.fix_spot(1, 1, 'X')
    assert game.board[1][1] == 'X'
    game.fix_spot(0, 2, 'O')
    assert game.board[0][2] == 'O'

@pytest.mark.parametrize("current_player, next_player", [('X', 'O'), ('O', 'X')])
def test_swap_player_turn(game, current_player, next_player):
    """Test that swap_player_turn correctly switches between 'X' and 'O'."""
    assert game.swap_player_turn(current_player) == next_player

def test_is_board_filled_false(game):
    """Test is_board_filled returns False for an empty or partially filled board."""
    game.create_board()
    assert not game.is_board_filled()
    game.fix_spot(0, 0, 'X')
    assert not game.is_board_filled()

def test_is_board_filled_true(game):
    """Test is_board_filled returns True for a full board."""
    game.board = [
        ['X', 'O', 'X'],
        ['O', 'X', 'O'],
        ['O', 'X', 'O']
    ]
    assert game.is_board_filled()

@pytest.mark.parametrize("player", ['X', 'O'])
class TestPlayerWins:
    def test_row_win(self, game, player):
        """Test player win condition for a complete row."""
        game.create_board()
        for i in range(3):
            game.board[1][i] = player
        assert game.has_player_won(player)

    def test_column_win(self, game, player):
        """Test player win condition for a complete column."""
        game.create_board()
        for i in range(3):
            game.board[i][2] = player
        assert game.has_player_won(player)

    def test_main_diagonal_win(self, game, player):
        """Test player win condition for the main diagonal."""
        game.create_board()
        for i in range(3):
            game.board[i][i] = player
        assert game.has_player_won(player)

    def test_anti_diagonal_win(self, game, player):
        """Test player win condition for the anti-diagonal."""
        game.create_board()
        for i in range(3):
            game.board[i][2 - i] = player
        assert game.has_player_won(player)

def test_no_win_condition(game):
    """Test has_player_won returns False when there is no winner."""
    game.board = [
        ['X', 'O', 'X'],
        ['X', 'O', 'O'],
        ['O', 'X', 'X']
    ]
    assert not game.has_player_won('X')
    assert not game.has_player_won('O')

def test_show_board(game, capsys):
    """Test that show_board prints the board to stdout."""
    game.board = [
        ['X', 'O', '-'],
        ['-', 'X', '-'],
        ['-', '-', 'O']
    ]
    game.show_board()
    captured = capsys.readouterr()
    expected_output = "X O -\n- X -\n- - O\n\n"
    assert captured.out == expected_output