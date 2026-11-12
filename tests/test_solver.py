"""Tests for Sudoku solving, move selection, and solution counting."""

import pytest

from sudoku_toolkit import Board
from sudoku_toolkit.validator import is_valid
from sudoku_toolkit.solver import (
    solve,
    _get_possible_values,
    _find_empty_position,
    count_solutions,
    _is_valid_move,
    _count_solutions_with_masks
)

def test_solver_solves_sudoku(valid_puzzle_board: Board) -> None:
    """Given a solvable Sudoku puzzle,
    When the puzzle is solved,
    Then a complete valid solution is returned."""

    solved_board = solve(valid_puzzle_board)

    assert solved_board is not None
    assert is_valid(solved_board)


def test_solver_preserves_given_values(valid_puzzle_values: list[list[int]]) -> None:
    """Given a solvable Sudoku puzzle with prefilled values,
    When the puzzle is solved,
    Then all prefilled values are preserved."""

    board = Board(valid_puzzle_values)
    solved_board = solve(board)

    for row in range(9):
        for column in range(9):
            if valid_puzzle_values[row][column] != 0:
                assert solved_board.get(row, column) == valid_puzzle_values[row][column]


def test_solver_returns_none_for_unsolvable_sudoku(
    duplicate_in_row_board: Board,
) -> None:
    """Given an inconsistent Sudoku puzzle,
    When the puzzle is solved,
    Then no solution is returned."""

    assert solve(duplicate_in_row_board) is None

def test_solver_does_not_modify_original_board(valid_puzzle_board: Board) -> None:
    """Given a Sudoku puzzle,
    When the puzzle is solved,
    Then the original board remains unchanged."""

    original_values = [row.copy() for row in valid_puzzle_board.values]

    solve(valid_puzzle_board)

    assert valid_puzzle_board.values == original_values

def test_solver_accepts_solved_board(solved_board: Board) -> None:
    """Given an already solved Sudoku,
    When the puzzle is solved,
    Then the same solved board is returned."""

    board = solved_board
    solved_solved_board = solve(board)

    assert solved_solved_board is not None
    assert solved_solved_board.values == solved_board.values

def test_solve_returns_none_for_unsolvable_board(
    valid_unsolvable_board: Board,
) -> None:
    """Given a valid but unsolvable Sudoku puzzle,
    When the puzzle is solved,
    Then no solution is returned."""

    assert is_valid(valid_unsolvable_board)
    assert solve(valid_unsolvable_board) is None

def test_is_valid_move_rejects_column_conflict(
    valid_puzzle_values: list[list[int]],
) -> None:
    """Given a candidate value already present in the column,
    When the move is checked,
    Then the move is rejected."""

    assert not _is_valid_move(valid_puzzle_values, 0, 2, 8)

def test_is_valid_move_rejects_row_conflict(
    valid_puzzle_values: list[list[int]],
) -> None:
    """Given a candidate value already present in the row,
    When the move is checked,
    Then the move is rejected."""

    assert not _is_valid_move(valid_puzzle_values, 0, 2, 7)

def test_is_valid_move_rejects_block_conflict(
    valid_puzzle_values: list[list[int]],
) -> None:
    """Given a candidate value already present in the block,
    When the move is checked,
    Then the move is rejected."""

    assert not _is_valid_move(valid_puzzle_values, 0, 2, 6)

def test_get_possible_values(valid_puzzle_values: list[list[int]]) -> None:
    """Given a Sudoku board and an empty cell with one valid candidate,
    When possible values are retrieved for the cell,
    Then only that candidate is returned."""

    assert _get_possible_values(valid_puzzle_values, 4, 4) == [5]

def test_find_empty_position_uses_mrv(valid_puzzle_values: list[list[int]]) -> None:
    """Given a Sudoku board with empty cells,
    When an empty position is selected,
    Then a position with the fewest possible values is returned."""

    position = _find_empty_position(valid_puzzle_values)

    assert position in [(4, 4), (6, 5), (6, 8), (7, 7)]

def test_count_solutions_no_solution(duplicate_in_row_board: Board) -> None:
    """Given an invalid Sudoku board,
    When its solutions are counted,
    Then the count is zero."""

    assert count_solutions(duplicate_in_row_board) == 0


def test_count_solutions_one_solution(valid_puzzle_board: Board) -> None:
    """Given a Sudoku board with one solution,
    When its solutions are counted,
    Then the count is one."""

    assert count_solutions(valid_puzzle_board) == 1

def test_count_solutions_multiple_solutions(
    empty_board: Board,
    sparse_multiple_solution_board: Board,
) -> None:
    """Given Sudoku boards with multiple solutions,
    When their solutions are counted up to the limit,
    Then the limit is returned for each board."""

    assert count_solutions(empty_board, limit=2) == 2
    assert count_solutions(sparse_multiple_solution_board, limit=2) == 2

def test_count_solutions_does_not_exceed_limit(
    multiple_solution_board: Board,
) -> None:
    """Given a Sudoku with more solutions than the counting limit,
    When its solutions are counted,
    Then the count does not exceed the limit."""

    assert count_solutions(multiple_solution_board, limit=2) == 2

def test_count_solution_returns_0(multiple_solution_board: Board) -> None:
    """Given a Sudoku and a solution-count limit of zero,
    When its solutions are counted,
    Then the count is zero."""

    assert count_solutions(multiple_solution_board, limit=0) == 0

@pytest.mark.parametrize("number", [0, 10])
def test_is_valid_move_rejects_out_of_range_number(
    valid_puzzle_values: list[list[int]], number: int
) -> None:
    """Given a candidate outside the allowed range,
    When the move is checked,
    Then the move is rejected."""
    assert not _is_valid_move(valid_puzzle_values, 0, 2, number)

def test_count_solutions_with_zero_internal_limit(empty_board: Board) -> None:
    """Given an empty board and a zero solution limit,
    When the internal solution counter is called,
    Then the count is zero."""
    masks = [0] * 9
    assert _count_solutions_with_masks(
        empty_board.values, 0, masks, masks.copy(), masks.copy()
    ) == 0
