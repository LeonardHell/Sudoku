"""Shared Sudoku board fixtures for the test suite."""

import pytest

from sudoku_toolkit import Board


@pytest.fixture
def valid_puzzle_values():
    """Return a fresh copy of the common solvable Sudoku puzzle values."""
    return [
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


@pytest.fixture
def valid_puzzle_board(valid_puzzle_values):
    """Return a fresh Board containing the common solvable puzzle."""
    return Board(valid_puzzle_values)


@pytest.fixture
def empty_board():
    """Return a fresh board with all cells empty."""
    return Board([[0] * 9 for _ in range(9)])


@pytest.fixture
def duplicate_in_row_board(valid_puzzle_values):
    """Return a puzzle with a duplicate value in the first row."""
    valid_puzzle_values[0][7] = 5
    return Board(valid_puzzle_values)


@pytest.fixture
def duplicate_in_column_board(valid_puzzle_values):
    """Return a puzzle with a duplicate value in the first column."""
    valid_puzzle_values[6][0] = 5
    return Board(valid_puzzle_values)


@pytest.fixture
def duplicate_in_block_board(valid_puzzle_values):
    """Return a puzzle with a duplicate value in the top-left block."""
    valid_puzzle_values[0][2] = 6
    return Board(valid_puzzle_values)


@pytest.fixture
def valid_unsolvable_board():
    """Return a structurally and rule-valid puzzle that has no solution."""
    return Board([
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])


@pytest.fixture
def multiple_solution_board():
    """Return a sparse puzzle with more than one valid completion."""
    return Board([
        [0, 0, 0, 0, 5, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 0, 0, 0, 7],
        [1, 5, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 5, 0],
        [2, 0, 0, 5, 0, 3, 0, 0, 9],
        [0, 0, 0, 7, 0, 9, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 5],
        [7, 1, 0, 0, 2, 0, 0, 9, 0],
    ])


@pytest.fixture
def sparse_multiple_solution_board():
    """Return a very sparse board with multiple valid completions."""
    return Board([
        [5, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [2, 0, 0, 0, 8, 0, 0, 0, 0],
    ])

@pytest.fixture
def solved_board():
    """Return a solved Sudoku board."""
    return Board([
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9],
        ])
