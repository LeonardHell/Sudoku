"""Validation of Sudoku board structure and row, column, and block rules."""

from collections.abc import Iterable

from .board import Board


def _unit_is_valid(values: Iterable[int]) -> bool:
    """Return whether non-empty values in one Sudoku unit are unique."""
    # Zero represents an empty cell and may appear multiple times in a unit.
    numbers = [value for value in values if value != 0]
    return len(numbers) == len(set(numbers))


def is_valid(board: Board) -> bool:
    """Check board structure and duplicates in every row, column, and block.

    Empty cells are allowed. A malformed board or a repeated non-zero value
    makes the board invalid.
    """

    try:
        board.validate_structure()
    except ValueError:
        # Invalid dimensions or cell values are validation failures, not crashes.
        return False
    
    # Check rows
    for row in board.values:
        if not _unit_is_valid(row):
            return False

    # Check columns
    # Unpacking rows transposes the grid so each resulting tuple is one column.
    for column in zip(*board.values):
        if not _unit_is_valid(column):
            return False

    # Check 3x3 blocks
    for row_start in range(0, 9, 3):
        for column_start in range(0, 9, 3):
            block = []

            for row in range(row_start, row_start + 3):
                for column in range(column_start, column_start + 3):
                    block.append(board.values[row][column])

            if not _unit_is_valid(block):
                return False

    return True
