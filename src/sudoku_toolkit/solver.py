"""Backtracking Sudoku solver and solution counter."""

from .board import Board
from .validator import is_valid


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

    empty_position = _find_empty_position(values)

    # No empty cell means every cell has been assigned consistently.
    if empty_position is None:
        return True

    row, column = empty_position

    for number in range(1, 10):
        if _is_valid_move(values, row, column, number):
            values[row][column] = number

            if _solve_values(values):
                return True

            # This candidate led to a dead end; clear it before trying the next.
            values[row][column] = 0

    return False

def _get_possible_values(
    values: list[list[int]],
    row: int,
    column: int,
) -> list[int]:
    """List digits that can be placed at a position without a rule conflict."""

    possible_values = []

    for number in range(1, 10):
        if _is_valid_move(values, row, column, number):
            possible_values.append(number)

    return possible_values

def _find_empty_position(
    values: list[list[int]],
) -> tuple[int, int] | None:
    """Select an empty cell with the minimum remaining legal candidates.

    Returns ``None`` when the grid has no empty cells. The selected cell gives
    the backtracking search its most constrained next choice.
    """

    best_position = None
    fewest_options = 10

    for row in range(9):
        for column in range(9):
            if values[row][column] != 0:
                continue

            options = _get_possible_values(values, row, column)

            if len(options) < fewest_options:
                fewest_options = len(options)
                best_position = (row, column)

                # One candidate is the minimum possible, so no better cell exists.
                if len(options) == 1:
                    return best_position

    return best_position

def _is_valid_move(
    values: list[list[int]],
    row: int,
    column: int,
    number: int,
) -> bool:
    """Check a candidate against its row, column, and 3x3 block."""

    if number in values[row]:
        return False

    for current_row in range(9):
        if values[current_row][column] == number:
            return False

    # Integer division maps each coordinate to the top-left corner of its block.
    block_row = (row // 3) * 3
    block_column = (column // 3) * 3

    for current_row in range(block_row, block_row + 3):
        for current_column in range(block_column, block_column + 3):
            if values[current_row][current_column] == number:
                return False

    return True

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


def _count_solutions(values: list[list[int]], limit: int) -> int:
    """Recursively count grid completions, stopping at the remaining limit."""

    if limit <= 0:
        return 0

    empty_position = _find_empty_position(values)

    # A full valid grid contributes one solution to its caller's count.
    if empty_position is None:
        return 1

    row, column = empty_position
    solution_count = 0

    for number in range(1, 10):
        if _is_valid_move(values, row, column, number):
            values[row][column] = number

            # Pass only the number of additional solutions still needed.
            solution_count += _count_solutions(values, limit - solution_count,)

            # Counting explores alternatives on the same mutable working grid.
            values[row][column] = 0

            if solution_count >= limit:
                return solution_count

    return solution_count
