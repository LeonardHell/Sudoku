"""Tests for randomized solution and unique-puzzle generation."""

import pytest
import random
from collections.abc import Iterator

from sudoku_toolkit.validator import is_valid
from sudoku_toolkit.solver import count_solutions
from sudoku_toolkit import generator
from sudoku_toolkit.generator import (
    generate_solution,
    generate_puzzle,
)


@pytest.fixture(autouse=True)
def fixed_random_seed() -> Iterator[None]:
    """Make randomness reproducible without affecting other tests."""

    previous_state = random.getstate()
    random.seed(42)

    yield

    random.setstate(previous_state)

def test_generate_solution_is_valid() -> None:
    """Given a request for a solution,
    When a solution is generated,
    Then it is a valid completed board."""

    board = generate_solution()

    assert is_valid(board)

    for row in board.values:
        assert 0 not in row
        assert sorted(row) == list(range(1, 10))

def test_generate_solution_is_random() -> None:
    """Given a fixed initial random seed,
    When two solutions are generated successively,
    Then the solutions are different."""

    board_1 = generate_solution()
    board_2 = generate_solution()

    assert board_1.values != board_2.values

def test_generate_puzzle_is_valid() -> None:
    """Given a request for a puzzle with 35 clues,
    When the puzzle is generated,
    Then it is a valid Sudoku board."""

    board = generate_puzzle(clues=35)

    assert is_valid(board)


def test_generate_puzzle_has_correct_number_of_clues() -> None:
    """Given a request for a puzzle with 36 clues,
    When the puzzle is generated,
    Then it has exactly 36 clues."""

    board = generate_puzzle(clues=36)

    clues = sum(
        value != 0
        for row in board.values
        for value in row
    )

    assert clues == 36


def test_generate_puzzle_has_unique_solution() -> None:
    """Given a request for a puzzle,
    When the puzzle is generated and its solutions are counted,
    Then it has exactly one solution."""

    board = generate_puzzle()

    assert count_solutions(board, limit=2) == 1


def test_generate_puzzle_rejects_invalid_clues() -> None:
    """Given clue counts below or above the supported range,
    When a puzzle is generated,
    Then a ValueError is raised."""
    with pytest.raises(ValueError):
        generate_puzzle(clues=16)

    with pytest.raises(ValueError):
        generate_puzzle(clues=82)

def test_generate_easy_puzzle() -> None:
    """Given a request for an easy puzzle,
    When the puzzle is generated,
    Then it has 40 clues and one solution."""

    board = generate_puzzle(difficulty="easy")

    clues = sum(
        value != 0
        for row in board.values
        for value in row
    )

    assert clues == 40
    assert count_solutions(board, limit=2) == 1


def test_generate_medium_puzzle() -> None:
    """Given a request for a medium puzzle,
    When the puzzle is generated,
    Then it has 32 clues and one solution."""

    board = generate_puzzle(difficulty="medium")

    clues = sum(
        value != 0
        for row in board.values
        for value in row
    )

    assert clues == 32
    assert count_solutions(board, limit=2) == 1


def test_generate_hard_puzzle() -> None:
    """Given a request for a hard puzzle,
    When the puzzle is generated,
    Then it has 25 clues and one solution."""

    board = generate_puzzle(difficulty="hard")

    clues = sum(
        value != 0
        for row in board.values
        for value in row
    )

    assert clues == 25
    assert count_solutions(board, limit=2) == 1


def test_generate_puzzle_rejects_invalid_difficulty() -> None:
    """Given an unsupported difficulty,
    When a puzzle is generated,
    Then a ValueError is raised."""

    with pytest.raises(ValueError):
        generate_puzzle(difficulty="impossible")

def test_generate_puzzle_rejects_clues_and_difficulty() -> None:
    """Given both a clue count and a difficulty,
    When a puzzle is generated,
    Then a ValueError is raised."""

    with pytest.raises(ValueError):
        generate_puzzle(clues=30, difficulty='hard')

def test_generate_puzzle_rejects_invalid_max_attempts() -> None:
    """Given a maximum attempt count below one,
    When a puzzle is generated,
    Then a ValueError is raised."""

    with pytest.raises(ValueError):
        generate_puzzle(max_attempts=0)


def test_generate_puzzle_raises_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Given generation attempts that never produce a unique puzzle,
    When the maximum number of attempts is reached,
    Then a RuntimeError is raised."""

    monkeypatch.setattr(
        generator,
        "count_solutions",
        lambda board, limit=2: 2,
    )

    with pytest.raises(RuntimeError, match="after 2 attempts"):
        generator.generate_puzzle(clues=80, max_attempts=2)
