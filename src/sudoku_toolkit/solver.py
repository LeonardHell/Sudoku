from .board import Board
from .validator import is_valid


def solve(board: Board) -> Board | None:
    """Solve a Sudoku board using backtracking.

    Return a solved Board if a solution exists.
    Return None if the Sudoku has no solution.
    """
    if not is_valid(board):
        return None

    values = [row.copy() for row in board.values]

    if _solve_values(values):
        return Board(values)

    return None


def _solve_values(values: list[list[int]]) -> bool:
    """Recursively solve the Sudoku using backtracking."""

    empty_position = _find_empty_position(values)

    if empty_position is None:
        return True

    row, column = empty_position

    for number in range(1, 10):
        if _is_valid_move(values, row, column, number):
            values[row][column] = number

            if _solve_values(values):
                return True

            values[row][column] = 0

    return False

def _get_possible_values(
    values: list[list[int]],
    row: int,
    column: int,
) -> list[int]:
    """Return the possible values for a position."""

    possible_values = []

    for number in range(1, 10):
        if _is_valid_move(values, row, column, number):
            possible_values.append(number)

    return possible_values

def _find_empty_position(
    values: list[list[int]],
) -> tuple[int, int] | None:
    """Return the empty position with the fewest possible values."""

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

                if len(options) == 1:
                    return best_position

    return best_position

def _is_valid_move(
    values: list[list[int]],
    row: int,
    column: int,
    number: int,
) -> bool:
    """Return whether a number can be placed at a given position."""

    # Check the row
    if number in values[row]:
        return False

    # Check the column
    for current_row in range(9):
        if values[current_row][column] == number:
            return False

    # Check the 3x3 block
    block_row = (row // 3) * 3
    block_column = (column // 3) * 3

    for current_row in range(block_row, block_row + 3):
        for current_column in range(block_column, block_column + 3):
            if values[current_row][current_column] == number:
                return False

    return True

def count_solutions(board: Board, limit: int = 2) -> int:
    """Count the number of solutions of a Sudoku board.

    Stop searching once the number of solutions reaches limit.
    """
    if not is_valid(board):
            return 0
    
    values = [row.copy() for row in board.values]
    
    return _count_solutions(values, limit)


def _count_solutions(values: list[list[int]], limit: int) -> int:
    """Count solutions, stopping once the specified limit is reached."""

    if limit <= 0:
        return 0

    empty_position = _find_empty_position(values)

    if empty_position is None:
        return 1

    row, column = empty_position
    solution_count = 0

    for number in range(1, 10):
        if _is_valid_move(values, row, column, number):
            values[row][column] = number

            solution_count += _count_solutions(values, limit - solution_count,)

            values[row][column] = 0

            if solution_count >= limit:
                return solution_count

    return solution_count
