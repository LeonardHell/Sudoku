import random

from .board import Board
from .solver import (
    _is_valid_move,
    count_solutions
)

DIFFICULTY_CLUES = {
    "easy": 40,
    "medium": 32,
    "hard": 25,
}

def _generate_solution(values):
    """Generate a random completed Sudoku grid."""

    empty_position = _find_empty_position(values)

    if empty_position is None:
        return True

    row, column = empty_position

    numbers = list(range(1, 10))
    random.shuffle(numbers)

    for number in numbers:
        if _is_valid_move(values, row, column, number):
            values[row][column] = number

            if _generate_solution(values):
                return True

            values[row][column] = 0

    return False


def _find_empty_position(values):
    """Find the next empty position."""

    for row in range(9):
        for column in range(9):
            if values[row][column] == 0:
                return row, column

    return None


def generate_solution():
    """Generate a completely solved Sudoku."""

    values = [[0 for _ in range(9)] for _ in range(9)]

    _generate_solution(values)

    return Board(values)

def generate_puzzle(clues=None, difficulty=None, max_attempts=100):
    """Generate a Sudoku puzzle with a unique solution.

    Args:
        clues: Number of given numbers that should remain in the puzzle. Default is 35.
        difficulty: Difficulty level ('easy', 'medium', or 'hard'). Doesn't overwirte number of clues
        max_attempts: Maximum number of gneration attempts.
        
    Returns:
        A Board containing a Sudoku puzzle with a unique solution.

    Raises:
        ValueError: If the difficulty, clues, or max_attempts are invalid.
        RuntimeError: If no suitable puzzle is found within max_attempts.
    """

    Default_clues = 35

    if clues is None:
        if difficulty is not None:
            if difficulty not in DIFFICULTY_CLUES:
                raise ValueError(
                    "difficulty must be 'easy', 'medium', or 'hard'"
                )

            clues = DIFFICULTY_CLUES[difficulty]

        else:
            clues = Default_clues

    if not 17 <= clues <= 81:
        raise ValueError("clues must be between 17 and 81")
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    for attempt in range(max_attempts):
        solution = generate_solution()

        values = [row.copy() for row in solution.values]

        positions = [
            (row, column)
            for row in range(9)
            for column in range(9)
        ]

        random.shuffle(positions)

        current_clues = 81

        for row, column in positions:
            if current_clues <= clues:
                break

            original_value = values[row][column]
            values[row][column] = 0

            puzzle = Board(values)

            if count_solutions(puzzle, limit=2) == 1:
                current_clues -= 1
            else:
                values[row][column] = original_value
        if current_clues == clues:
            return Board(values)

    raise RuntimeError( f"Could not generate a Sudoku with {clues} clues " f"after {max_attempts} attempts." )
