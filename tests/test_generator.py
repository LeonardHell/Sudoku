import pytest

from sudoku_toolkit.validator import is_valid
from sudoku_toolkit.solver import count_solutions
from sudoku_toolkit.generator import (
    generate_solution,
    generate_puzzle
)


def test_generate_solution_is_valid():
    """The generated Sudoku is a valid completed board."""

    board = generate_solution()

    assert is_valid(board)

    for row in board.values:
        assert 0 not in row
        assert sorted(row) == list(range(1, 10))

def test_generate_solution_is_random():
    """
    Generating solutions produces different boards.
    This test could in theory fail but is incredibly unlikely.
    """

    board_1 = generate_solution()
    board_2 = generate_solution()

    assert board_1.values != board_2.values

def test_generate_puzzle_is_valid():
    """The generated puzzle is a valid Sudoku board."""

    board = generate_puzzle(clues=35)

    assert is_valid(board)


def test_generate_puzzle_has_correct_number_of_clues():
    """The generated puzzle has the requested number of clues."""

    board = generate_puzzle(clues=36)

    clues = sum(
        value != 0
        for row in board.values
        for value in row
    )

    assert clues == 36


def test_generate_puzzle_has_unique_solution():
    """The generated puzzle has exactly one solution."""

    board = generate_puzzle()

    assert count_solutions(board, limit=2) == 1


def test_generate_puzzle_rejects_invalid_clues():
    """Invalid clue counts raise a ValueError."""
    with pytest.raises(ValueError):
        generate_puzzle(clues=16)

    with pytest.raises(ValueError):
        generate_puzzle(clues=82)

def test_generate_easy_puzzle():
    """An easy puzzle has 40 clues."""

    board = generate_puzzle(difficulty="easy")

    clues = sum(
        value != 0
        for row in board.values
        for value in row
    )

    assert clues == 40
    assert count_solutions(board, limit=2) == 1


def test_generate_medium_puzzle():
    """A medium puzzle has 32 clues."""

    board = generate_puzzle(difficulty="medium")

    clues = sum(
        value != 0
        for row in board.values
        for value in row
    )

    assert clues == 32
    assert count_solutions(board, limit=2) == 1


def test_generate_hard_puzzle():
    """A hard puzzle has 25 clues."""

    board = generate_puzzle(difficulty="hard")

    clues = sum(
        value != 0
        for row in board.values
        for value in row
    )

    assert clues == 25
    assert count_solutions(board, limit=2) == 1


def test_generate_puzzle_rejects_invalid_difficulty():
    """An invalid difficulty raises a ValueError."""

    with pytest.raises(ValueError):
        generate_puzzle(difficulty="impossible")
