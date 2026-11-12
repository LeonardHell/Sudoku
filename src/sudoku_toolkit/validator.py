"""Validation of Sudoku board structure and row, column, and block rules."""

from collections.abc import Iterable

from .board import Board


def _unit_is_valid(values: Iterable[int]) -> bool:
    """Return whether non-empty values in one Sudoku unit are unique."""
    used_digits = 0
    for value in values:
        # Zero represents an empty cell and may appear multiple times in a unit.
        if value == 0:
            continue

        bit = 1 << (value - 1)
        if used_digits & bit:
            return False
        used_digits |= bit

    return True


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
    
    for row in board.values:
        if not _unit_is_valid(row):
            return False

    # Unpacking rows transposes the grid so each resulting tuple is one column.
    for column in zip(*board.values):
        if not _unit_is_valid(column):
            return False

    # Check blocks lazily to avoid allocating a temporary list for each one.
    for row_start in range(0, 9, 3):
        for column_start in range(0, 9, 3):
            block = (
                value
                for row in board.values[row_start:row_start + 3]
                for value in row[column_start:column_start + 3]
            )

            if not _unit_is_valid(block):
                return False

    return True
