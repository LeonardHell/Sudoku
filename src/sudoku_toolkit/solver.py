from .board import Board
from .validator import is_valid


def solve(board):
    """Solve a Sudoku board using backtracking.

    Return a solved Board if a solution exists.
    Return None if the Sudoku has no solution.
    """
    values = [row.copy() for row in board.values]

    if not is_valid(Board(values)):
        return None

    if _solve_values(values):
        return Board(values)

    return None


def _solve_values(values):
    """Recursively solve the Sudoku using backtracking."""

    empty_position = _find_empty_position(values)

    if empty_position is None:
        return True

    row, column = empty_position

    for number in range(1, 10):
        values[row][column] = number

        if is_valid(Board(values)):
            if _solve_values(values):
                return True

        values[row][column] = 0

    return False


def _find_empty_position(values):
    """Return the position of the first empty cell, or None."""
    for row in range(9):
        for column in range(9):
            if values[row][column] == 0:
                return row, column

    return None
