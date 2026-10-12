import pytest

from sudoku_toolkit import Board
from sudoku_toolkit.validator import is_valid


@pytest.mark.parametrize("value", [-1, 10, 1.5, "5", None, True])
def test_validator_rejects_board_with_modified_invalid_value(value):
    """Direct modification of values must not bypass validation."""

    board = Board([[0] * 9 for _ in range(9)])
    board.values[0][0] = value

    assert is_valid(board) is False


@pytest.mark.parametrize("row_count", [8, 10])
def test_validator_rejects_board_with_modified_row_count(row_count):
    """A modified row count must return False instead of crashing."""

    board = Board([[0] * 9 for _ in range(9)])
    board.values = [[0] * 9 for _ in range(row_count)]

    assert is_valid(board) is False


@pytest.mark.parametrize("column_count", [8, 10])
def test_validator_rejects_board_with_modified_column_count(column_count):
    """A modified row length must return False instead of crashing."""

    board = Board([[0] * 9 for _ in range(9)])
    board.values[4] = [0] * column_count

    assert is_valid(board) is False


def test_validator_accepts_empty_board():
    """Empty cells do not violate Sudoku rules."""

    board = Board([[0] * 9 for _ in range(9)])

    assert is_valid(board) is True

def test_valid_board_is_accepted():
    values = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    board = Board(values)

    assert is_valid(board)

def test_duplicate_in_row_is_rejected():
    values = [
        [5, 0, 0, 0, 7, 0, 0, 5, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    board = Board(values)

    assert not is_valid(board)

def test_duplicate_in_column_is_rejected():
    values = [
        [5, 0, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [5, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    board = Board(values)

    assert not is_valid(board)

def test_duplicate_in_block_is_rejected():
    values = [
        [5, 0, 6, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    board = Board(values)

    assert not is_valid(board)
