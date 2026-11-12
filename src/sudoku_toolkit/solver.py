"""Backtracking Sudoku solver and solution counter."""

from .board import Board
from .validator import is_valid

_ALL_DIGITS = (1 << 9) - 1


def _build_masks(
    values: list[list[int]],
) -> tuple[list[int], list[int], list[int]]:
    """Build row, column, and block masks for digits already in the grid."""
    row_masks = [0] * 9
    column_masks = [0] * 9
    block_masks = [0] * 9

    for row in range(9):
        for column in range(9):
            number = values[row][column]
            if number:
                bit = 1 << (number - 1)
                block = (row // 3) * 3 + column // 3
                row_masks[row] |= bit
                column_masks[column] |= bit
                block_masks[block] |= bit

    return row_masks, column_masks, block_masks


def _candidate_mask(
    row: int,
    column: int,
    row_masks: list[int],
    column_masks: list[int],
    block_masks: list[int],
) -> int:
    """Return the bit set of digits not yet used by a cell's peers."""
    block = (row // 3) * 3 + column // 3
    return _ALL_DIGITS & ~(
        row_masks[row] | column_masks[column] | block_masks[block]
    )


def solve(board: Board) -> Board | None:
    """Solve a board by recursively trying rule-compliant values.

    The search copies the board, selects an empty cell with the fewest legal
    candidates (MRV), and backtracks when a candidate leads to a dead end.
    Return a solved ``Board``, or ``None`` if the input is invalid or
    unsolvable. The input board is not modified.
    """
    if not is_valid(board):
        return None

    values = [row.copy() for row in board.values]

    if _solve_values(values):
        return Board(values)

    return None


def _solve_values(values: list[list[int]]) -> bool:
    """Fill a mutable grid recursively, undoing choices that lead to dead ends.

    Returns ``True`` as soon as a complete solution is found.
    """
    row_masks, column_masks, block_masks = _build_masks(values)
    return _solve_values_with_masks(
        values, row_masks, column_masks, block_masks
    )


def _solve_values_with_masks(
    values: list[list[int]],
    row_masks: list[int],
    column_masks: list[int],
    block_masks: list[int],
) -> bool:
    """Search candidate branches while updating the occupancy masks in place."""
    position, candidates = _find_empty_position_with_candidates(
        values, row_masks, column_masks, block_masks
    )

    # No empty cell means every cell has been assigned consistently.
    if position is None:
        return True
    if candidates == 0:
        return False

    row, column = position
    block = (row // 3) * 3 + column // 3

    while candidates:
        bit = candidates & -candidates
        candidates ^= bit
        values[row][column] = bit.bit_length()
        row_masks[row] |= bit
        column_masks[column] |= bit
        block_masks[block] |= bit

        if _solve_values_with_masks(
            values, row_masks, column_masks, block_masks
        ):
            return True

        # Undo the placement in both the grid and the cached constraint masks.
        values[row][column] = 0
        row_masks[row] ^= bit
        column_masks[column] ^= bit
        block_masks[block] ^= bit

    return False


def _get_possible_values(
    values: list[list[int]],
    row: int,
    column: int,
) -> list[int]:
    """List digits that can be placed at a position without a rule conflict."""
    row_masks, column_masks, block_masks = _build_masks(values)
    candidates = _candidate_mask(
        row, column, row_masks, column_masks, block_masks
    )
    possible_values = []

    while candidates:
        bit = candidates & -candidates
        candidates ^= bit
        possible_values.append(bit.bit_length())

    return possible_values


def _find_empty_position_with_candidates(
    values: list[list[int]],
    row_masks: list[int],
    column_masks: list[int],
    block_masks: list[int],
) -> tuple[tuple[int, int] | None, int]:
    """Select an empty cell with the fewest candidates and return its mask."""
    best_position = None
    best_candidates = 0
    fewest_options = 10

    for row in range(9):
        for column in range(9):
            if values[row][column] != 0:
                continue

            candidates = _candidate_mask(
                row, column, row_masks, column_masks, block_masks
            )
            option_count = candidates.bit_count()

            if option_count < fewest_options:
                best_position = (row, column)
                best_candidates = candidates
                fewest_options = option_count

                # One candidate is the minimum possible; zero means this branch fails.
                if option_count <= 1:
                    return best_position, best_candidates

    return best_position, best_candidates


def _find_empty_position(
    values: list[list[int]],
) -> tuple[int, int] | None:
    """Select an empty cell with the minimum remaining legal candidates.

    Returns ``None`` when the grid has no empty cells. The selected cell gives
    the backtracking search its most constrained next choice.
    """
    row_masks, column_masks, block_masks = _build_masks(values)
    position, _ = _find_empty_position_with_candidates(
        values, row_masks, column_masks, block_masks
    )
    return position


def _is_valid_move(
    values: list[list[int]],
    row: int,
    column: int,
    number: int,
) -> bool:
    """Check a candidate against its row, column, and 3x3 block."""
    if not 1 <= number <= 9:
        return False

    bit = 1 << (number - 1)
    row_masks, column_masks, block_masks = _build_masks(values)
    block = (row // 3) * 3 + column // 3
    return not (
        row_masks[row] & bit
        or column_masks[column] & bit
        or block_masks[block] & bit
    )


def count_solutions(board: Board, limit: int = 2) -> int:
    """Count solutions without modifying the input board.

    Search stops when ``limit`` solutions are found, which is useful for
    distinguishing zero, one, or multiple solutions without enumerating all
    possibilities. Invalid boards return zero.
    """
    if not is_valid(board):
        return 0

    values = [row.copy() for row in board.values]
    return _count_solutions(values, limit)


def _count_solutions(
    values: list[list[int]],
    limit: int,
) -> int:
    """Recursively count grid completions, stopping at the remaining limit."""
    if limit <= 0:
        return 0

    row_masks, column_masks, block_masks = _build_masks(values)
    return _count_solutions_with_masks(
        values, limit, row_masks, column_masks, block_masks
    )


def _count_solutions_with_masks(
    values: list[list[int]],
    limit: int,
    row_masks: list[int],
    column_masks: list[int],
    block_masks: list[int],
) -> int:
    """Count candidate branches using masks shared across recursive calls."""
    if limit <= 0:
        return 0

    position, candidates = _find_empty_position_with_candidates(
        values, row_masks, column_masks, block_masks
    )

    # A full valid grid contributes one solution to its caller's count.
    if position is None:
        return 1
    if candidates == 0:
        return 0

    row, column = position
    block = (row // 3) * 3 + column // 3
    solution_count = 0

    while candidates and solution_count < limit:
        bit = candidates & -candidates
        candidates ^= bit
        values[row][column] = bit.bit_length()
        row_masks[row] |= bit
        column_masks[column] |= bit
        block_masks[block] |= bit

        # Pass only the number of additional solutions still needed.
        solution_count += _count_solutions_with_masks(
            values,
            limit - solution_count,
            row_masks,
            column_masks,
            block_masks,
        )

        # Restore the working grid so the next candidate explores a clean branch.
        values[row][column] = 0
        row_masks[row] ^= bit
        column_masks[column] ^= bit
        block_masks[block] ^= bit

    return solution_count
