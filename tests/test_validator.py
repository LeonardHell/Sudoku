"""Tests for board structure and Sudoku rule validation."""

import pytest

from sudoku_toolkit.validator import is_valid


@pytest.mark.parametrize("value", [-1, 10, 1.5, "5", None, True])
def test_validator_rejects_board_with_modified_invalid_value(value, empty_board):
    """Given a board whose cell was modified to an invalid value,
    When the board is validated,
    Then it is rejected."""

    empty_board.values[0][0] = value

    assert is_valid(empty_board) is False


@pytest.mark.parametrize("row_count", [8, 10])
def test_validator_rejects_board_with_modified_row_count(row_count, empty_board):
    """Given a board whose row count was modified,
    When the board is validated,
    Then it is rejected without raising an error."""

    empty_board.values = [[0] * 9 for _ in range(row_count)]

    assert is_valid(empty_board) is False


@pytest.mark.parametrize("column_count", [8, 10])
def test_validator_rejects_board_with_modified_column_count(
    column_count,
    empty_board,
):
    """Given a board whose row length was modified,
    When the board is validated,
    Then it is rejected without raising an error."""

    empty_board.values[4] = [0] * column_count

    assert is_valid(empty_board) is False


def test_validator_accepts_empty_board(empty_board):
    """Given an empty board,
    When the board is validated,
    Then it is accepted."""

    assert is_valid(empty_board) is True

def test_valid_board_is_accepted(valid_puzzle_board):
    """Given a board with no rule violations,
    When the board is validated,
    Then it is accepted."""

    assert is_valid(valid_puzzle_board)

def test_duplicate_in_row_is_rejected(duplicate_in_row_board):
    """Given a board with a duplicate value in a row,
    When the board is validated,
    Then it is rejected."""

    assert not is_valid(duplicate_in_row_board)

def test_duplicate_in_column_is_rejected(duplicate_in_column_board):
    """Given a board with a duplicate value in a column,
    When the board is validated,
    Then it is rejected."""

    assert not is_valid(duplicate_in_column_board)

def test_duplicate_in_block_is_rejected(duplicate_in_block_board):
    """Given a board with a duplicate value in a block,
    When the board is validated,
    Then it is rejected."""

    assert not is_valid(duplicate_in_block_board)
