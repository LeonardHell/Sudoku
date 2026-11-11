"""Tests for Sudoku board construction, access, mutation, and formatting."""

import pytest

from sudoku_toolkit import Board

@pytest.mark.parametrize("row_count", [8, 10])
def test_board_rejects_wrong_number_of_rows(row_count):
    """Given a board with the wrong number of rows,
    When the board is created,
    Then a ValueError is raised."""

    values = [[0] * 9 for _ in range(row_count)]

    with pytest.raises(ValueError, match="exactly 9 rows"):
        Board(values)


@pytest.mark.parametrize("column_count", [8, 10])
def test_board_rejects_wrong_number_of_columns(column_count):
    """Given a board with a row of the wrong length,
    When the board is created,
    Then a ValueError is raised."""

    values = [[0] * 9 for _ in range(9)]
    values[4] = [0] * column_count

    with pytest.raises(ValueError, match="exactly 9 values"):
        Board(values)


@pytest.mark.parametrize("value", [-1, 10])
def test_board_rejects_values_outside_range(value):
    """Given a cell value outside the allowed range,
    When the board is created,
    Then a ValueError is raised."""

    values = [[0] * 9 for _ in range(9)]
    values[0][0] = value

    with pytest.raises(ValueError, match="between 0 and 9"):
        Board(values)


@pytest.mark.parametrize("value", [1.5, "5", None, True, False])
def test_board_rejects_non_integer_values(value):
    """Given a non-integer cell value,
    When the board is created,
    Then a ValueError is raised."""

    values = [[0] * 9 for _ in range(9)]
    values[0][0] = value

    with pytest.raises(ValueError, match="must be integers"):
        Board(values)


@pytest.mark.parametrize("value", [0, 9])
def test_board_accepts_boundary_values(value):
    """Given a cell value at either allowed endpoint,
    When the board is created,
    Then the value is accepted."""

    values = [[0] * 9 for _ in range(9)]
    values[0][0] = value

    board = Board(values)

    assert board.get(0, 0) == value


@pytest.mark.parametrize(
    "row, column",
    [(-1, 0), (9, 0), (0, -1), (0, 9)],
)
def test_set_rejects_indices_outside_board(row, column):
    """Given an index outside the board,
    When a cell is updated,
    Then an IndexError is raised."""

    board = Board([[0] * 9 for _ in range(9)])

    with pytest.raises(IndexError, match="between 0 and 8"):
        board.set(row, column, 5)


def test_set_rejects_non_integer_values():
    """Given a board and a non-integer cell value,
    When the cell is updated,
    Then a ValueError is raised."""

    board = Board([[0] * 9 for _ in range(9)])

    with pytest.raises(ValueError, match="must be integers"):
        board.set(0, 0, "5")


def test_rejected_set_does_not_change_board():
    """Given a cell with an existing value,
    When an invalid update is rejected,
    Then the existing value is unchanged."""

    board = Board([[0] * 9 for _ in range(9)])
    board.set(0, 0, 5)

    with pytest.raises(ValueError):
        board.set(0, 0, 10)

    assert board.get(0, 0) == 5


def test_board_copies_input_rows():
    """Given a board created from input rows,
    When the input is changed,
    Then the board remains unchanged."""

    values = [[0] * 9 for _ in range(9)]
    board = Board(values)

    values[0][0] = 9

    assert board.get(0, 0) == 0

def test_board_can_be_created():
    """Given valid board values,
    When a board is created,
    Then it stores those values."""

    values = [[0] * 9 for _ in range(9)]

    board = Board(values)

    assert board.values == values


def test_board_value_can_be_read():
    """Given a board with a populated cell,
    When that cell is read,
    Then its value is returned."""

    values = [[0] * 9 for _ in range(9)]
    values[2][4] = 7

    board = Board(values)

    assert board.get(2, 4) == 7


def test_board_value_can_be_changed():
    """Given an empty board,
    When one cell is updated,
    Then its new value can be read."""

    values = [[0] * 9 for _ in range(9)]

    board = Board(values)
    board.set(2, 4, 7)

    assert board.get(2, 4) == 7

def test_board_str():
    """Given a populated board,
    When it is converted to a string,
    Then it uses the expected Sudoku layout."""

    board = Board([
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
    ])

    expected = (
        "1 2 3 | 4 5 6 | 7 8 9\n"
        "4 5 6 | 7 8 9 | 1 2 3\n"
        "7 8 9 | 1 2 3 | 4 5 6\n"
        "------+-------+------\n"
        "2 3 4 | 5 6 7 | 8 9 1\n"
        "5 6 7 | 8 9 1 | 2 3 4\n"
        "8 9 1 | 2 3 4 | 5 6 7\n"
        "------+-------+------\n"
        "3 4 5 | 6 7 8 | 9 1 2\n"
        "6 7 8 | 9 1 2 | 3 4 5\n"
        "9 1 2 | 3 4 5 | 6 7 8"
    )

    assert str(board) == expected
