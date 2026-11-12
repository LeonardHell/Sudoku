"""Randomized generation of completed Sudoku grids and unique puzzles."""

import random

from .board import Board
from .solver import (
    _build_masks,
    _candidate_mask,
    count_solutions
)

# Default clue counts used by the named puzzle difficulty levels.
DIFFICULTY_CLUES = {
    "easy": 40,
    "medium": 32,
    "hard": 25,
}

def _generate_solution(values: list[list[int]]) -> bool:
    """Fill an in-place grid using randomized backtracking.

    Candidate digits are shuffled before trying them; failed branches reset
    the cell to zero. Returns whether a complete solution was found.
    """

    row_masks, column_masks, block_masks = _build_masks(values)
    return _generate_solution_with_masks(
        values, row_masks, column_masks, block_masks
    )


def _generate_solution_with_masks(
    values: list[list[int]],
    row_masks: list[int],
    column_masks: list[int],
    block_masks: list[int],
) -> bool:
    """Fill the grid while maintaining used-digit masks incrementally."""
    empty_position = _find_empty_position(values)
    if empty_position is None:
        return True

    row, column = empty_position
    block = (row // 3) * 3 + column // 3
    candidates = _candidate_mask(
        row, column, row_masks, column_masks, block_masks
    )

    numbers = []
    while candidates:
        bit = candidates & -candidates
        candidates ^= bit
        numbers.append(bit)
    # Shuffling changes the search order, producing varied valid solutions.
    random.shuffle(numbers)

    for bit in numbers:
        values[row][column] = bit.bit_length()
        row_masks[row] |= bit
        column_masks[column] |= bit
        block_masks[block] |= bit

        if _generate_solution_with_masks(
            values, row_masks, column_masks, block_masks
        ):
            return True

        # The recursive branch failed; restore the grid and its masks.
        values[row][column] = 0
        row_masks[row] ^= bit
        column_masks[column] ^= bit
        block_masks[block] ^= bit

    return False


def _find_empty_position(
    values: list[list[int]],
) -> tuple[int, int] | None:
    """Return the first empty cell in row-major order, or ``None`` if full."""

    for row in range(9):
        for column in range(9):
            if values[row][column] == 0:
                return row, column

    return None


def generate_solution() -> Board:
    """Create an empty grid, fill it with randomized backtracking, and wrap it.

    The returned board is complete and satisfies the Sudoku constraints.
    """

    values = [[0 for _ in range(9)] for _ in range(9)]

    _generate_solution(values)

    return Board(values)

def generate_puzzle(
    clues: int | None = None,
    difficulty: str | None = None,
    max_attempts: int = 100,
) -> Board:
    """Generate a Sudoku puzzle with a unique solution.

    A completed grid is generated first. Cells are then considered in random
    order and removed only when the remaining puzzle still has exactly one
    solution. If a full pass cannot reach the requested clue count, the process
    retries with a new completed grid until ``max_attempts`` is exhausted.

    Args:
        clues: Number of given digits to retain. Defaults to 35.
        difficulty: Named level selecting its configured clue count. Cannot be
            supplied together with ``clues``.
        max_attempts: Maximum number of completed grids to try.

    Returns:
        A board with the requested clue count and exactly one solution.

    Raises:
        ValueError: If options conflict or their values are outside supported
            ranges.
        RuntimeError: If no puzzle with the requested clue count is generated
            within ``max_attempts``.
    """

    if clues is not None and difficulty is not None:
        raise ValueError("clues and difficulty cannot both be set simultaneously. Set EITHER clues OR diffuculty")

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

        # Random removal order gives different puzzles from the same solution.
        random.shuffle(positions)

        current_clues = 81

        for row, column in positions:
            if current_clues <= clues:
                break

            original_value = values[row][column]
            values[row][column] = 0

            puzzle = Board(values)

            # Keep a removal only if it preserves exactly one solution.
            if count_solutions(puzzle, limit=2) == 1:
                current_clues -= 1
            else:
                # Restore the clue when removing it makes the puzzle ambiguous.
                values[row][column] = original_value
        if current_clues == clues:
            return Board(values)

    raise RuntimeError( f"Could not generate a Sudoku with {clues} clues " f"after {max_attempts} attempts." )
