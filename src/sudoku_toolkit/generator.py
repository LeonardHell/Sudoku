import random

from .board import Board
from .solver import (
    _is_valid_move,
    count_solutions
)

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

def generate_puzzle(clues=35):
    """Generate a Sudoku puzzle with a unique solution.

    Args:
        clues: Number of given numbers that should remain in the puzzle.

    Returns:
        A Board containing a Sudoku puzzle with a unique solution.
    """

    if not 17 <= clues <= 81:
        raise ValueError("clues must be between 17 and 81")

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

    return Board(values)
