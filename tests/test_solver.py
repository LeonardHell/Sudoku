from sudoku_toolkit import Board
from sudoku_toolkit.validator import is_valid
from sudoku_toolkit.solver import (
    solve,
    _get_possible_values,
    _find_empty_position,
    count_solutions,
    _is_valid_move
)

def test_solver_solves_sudoku():
    """Given a solvable Sudoku puzzle,
    When the puzzle is solved,
    Then a complete valid solution is returned."""

    values = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    board = Board(values)
    solved_board = solve(board)

    assert solved_board is not None
    assert is_valid(solved_board)


def test_solver_preserves_given_values():
    """Given a solvable Sudoku puzzle with prefilled values,
    When the puzzle is solved,
    Then all prefilled values are preserved."""

    values = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    board = Board(values)
    solved_board = solve(board)

    for row in range(9):
        for column in range(9):
            if values[row][column] != 0:
                assert solved_board.get(row, column) == values[row][column]


def test_solver_returns_none_for_unsolvable_sudoku():
    """Given an inconsistent Sudoku puzzle,
    When the puzzle is solved,
    Then no solution is returned."""

    values = [
        [5, 5, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    board = Board(values)

    assert solve(board) is None

def test_solver_does_not_modify_original_board():
    """Given a Sudoku puzzle,
    When the puzzle is solved,
    Then the original board remains unchanged."""

    values = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    board = Board(values)
    original_values = [row.copy() for row in board.values]

    solve(board)

    assert board.values == original_values

def test_solver_accepts_solved_board():
    """Given an already solved Sudoku,
    When the puzzle is solved,
    Then the same solved board is returned."""

    values = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    board = Board(values)
    solved_board = solve(board)

    assert solved_board is not None
    assert solved_board.values == values

def test_solve_returns_none_for_unsolvable_board():
    """Given a valid but unsolvable Sudoku puzzle,
    When the puzzle is solved,
    Then no solution is returned."""

    board = Board([
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    assert is_valid(board)
    assert solve(board) is None

def test_is_valid_move_rejects_column_conflict():
    """Given a candidate value already present in the column,
    When the move is checked,
    Then the move is rejected."""

    values = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    assert not _is_valid_move(values, 0, 2, 8)

def test_is_valid_move_rejects_row_conflict():
    """Given a candidate value already present in the row,
    When the move is checked,
    Then the move is rejected."""

    values = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    assert not _is_valid_move(values, 0, 2, 7)

def test_is_valid_move_rejects_block_conflict():
    """Given a candidate value already present in the block,
    When the move is checked,
    Then the move is rejected."""

    values = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    assert not _is_valid_move(values, 0, 2, 6)

def test_get_possible_values():
    """Given a Sudoku board and an empty cell with one valid candidate,
    When possible values are retrieved for the cell,
    Then only that candidate is returned."""

    values = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    assert _get_possible_values(values, 4, 4) == [5]

def test_find_empty_position_uses_mrv():
    """Given a Sudoku board with empty cells,
    When an empty position is selected,
    Then a position with the fewest possible values is returned."""

    values = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    position = _find_empty_position(values)

    assert position in [(4, 4), (6, 5), (6, 8), (7, 7)]

def test_count_solutions_no_solution():
    """Given an invalid Sudoku board,
    When its solutions are counted,
    Then the count is zero."""

    board = Board([
        [5, 3, 5, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ])

    assert count_solutions(board) == 0


def test_count_solutions_one_solution():
    """Given a Sudoku board with one solution,
    When its solutions are counted,
    Then the count is one."""

    board = Board([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ])

    assert count_solutions(board) == 1

def test_count_solutions_multiple_solutions():
    """Given Sudoku boards with multiple solutions,
    When their solutions are counted up to the limit,
    Then the limit is returned for each board."""

    board_empty = Board([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    board_scarse = Board([
        [5, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [2, 0, 0, 0, 8, 0, 0, 0, 0],
    ])

    assert count_solutions(board_empty, limit=2) == 2
    assert count_solutions(board_scarse, limit=2) == 2

def test_count_solutions_does_not_exceed_limit():
    """Given a Sudoku with more solutions than the counting limit,
    When its solutions are counted,
    Then the count does not exceed the limit."""

    board = Board([
        [0, 0, 0, 0, 5, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 0, 0, 0, 7],
        [1, 5, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 5, 0],
        [2, 0, 0, 5, 0, 3, 0, 0, 9],
        [0, 0, 0, 7, 0, 9, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 5],
        [7, 1, 0, 0, 2, 0, 0, 9, 0],
    ])

    assert count_solutions(board, limit=2) == 2

def test_count_solution_returns_0():
    """Given a Sudoku and a solution-count limit of zero,
    When its solutions are counted,
    Then the count is zero."""

    board = Board([
        [0, 0, 0, 0, 5, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 0, 0, 0, 7],
        [1, 5, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 5, 0],
        [2, 0, 0, 5, 0, 3, 0, 0, 9],
        [0, 0, 0, 7, 0, 9, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 5],
        [7, 1, 0, 0, 2, 0, 0, 9, 0],
    ])

    assert count_solutions(board, limit=0) == 0
