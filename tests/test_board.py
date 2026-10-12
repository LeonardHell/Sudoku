import pytest

from sudoku_toolkit import Board

@pytest.mark.parametrize("row_count", [8, 10])
def test_board_rejects_wrong_number_of_rows(row_count):
    """A board must have exactly nine rows."""

    values = [[0] * 9 for _ in range(row_count)]

    with pytest.raises(ValueError, match="exactly 9 rows"):
        Board(values)


@pytest.mark.parametrize("column_count", [8, 10])
def test_board_rejects_wrong_number_of_columns(column_count):
    """Every row must have exactly nine cells."""

    values = [[0] * 9 for _ in range(9)]
    values[4] = [0] * column_count

    with pytest.raises(ValueError, match="exactly 9 values"):
        Board(values)


@pytest.mark.parametrize("value", [-1, 10])
def test_board_rejects_values_outside_range(value):
    """Cell values must be between zero and nine."""

    values = [[0] * 9 for _ in range(9)]
    values[0][0] = value

    with pytest.raises(ValueError, match="between 0 and 9"):
        Board(values)


@pytest.mark.parametrize("value", [1.5, "5", None, True, False])
def test_board_rejects_non_integer_values(value):
    """Only integers are accepted, excluding booleans."""

    values = [[0] * 9 for _ in range(9)]
    values[0][0] = value

    with pytest.raises(ValueError, match="must be integers"):
        Board(values)


@pytest.mark.parametrize("value", [0, 9])
def test_board_accepts_boundary_values(value):
    """Both endpoints of the allowed range are accepted."""

    values = [[0] * 9 for _ in range(9)]
    values[0][0] = value

    board = Board(values)

    assert board.get(0, 0) == value


@pytest.mark.parametrize("value", [-1, 10])
def test_set_rejects_values_outside_range(value):
    """Setting an out-of-range value must fail."""

    board = Board([[0] * 9 for _ in range(9)])

    with pytest.raises(ValueError, match="between 0 and 9"):
        board.set(0, 0, value)


@pytest.mark.parametrize("value", [1.5, "5", None, True, False])
def test_set_rejects_non_integer_values(value):
    """Setting a non-integer value must fail."""

    board = Board([[0] * 9 for _ in range(9)])

    with pytest.raises(ValueError, match="must be integers"):
        board.set(0, 0, value)


@pytest.mark.parametrize(
    "row, column",
    [(-1, 0), (9, 0), (0, -1), (0, 9)],
)
def test_set_rejects_indices_outside_board(row, column):
    """Negative indices must not silently access another cell."""

    board = Board([[0] * 9 for _ in range(9)])

    with pytest.raises(IndexError, match="between 0 and 8"):
        board.set(row, column, 5)


def test_rejected_set_does_not_change_board():
    """A rejected update must preserve the previous cell value."""

    board = Board([[0] * 9 for _ in range(9)])
    board.set(0, 0, 5)

    with pytest.raises(ValueError):
        board.set(0, 0, 10)

    assert board.get(0, 0) == 5


def test_board_copies_input_rows():
    """Changing the original input must not change the board."""

    values = [[0] * 9 for _ in range(9)]
    board = Board(values)

    values[0][0] = 9

    assert board.get(0, 0) == 0

def test_board_can_be_created():
    values = [[0] * 9 for _ in range(9)]

    board = Board(values)

    assert board.values == values


def test_board_value_can_be_read():
    values = [[0] * 9 for _ in range(9)]
    values[2][4] = 7

    board = Board(values)

    assert board.get(2, 4) == 7


def test_board_value_can_be_changed():
    values = [[0] * 9 for _ in range(9)]

    board = Board(values)
    board.set(2, 4, 7)

    assert board.get(2, 4) == 7

def test_board_str():
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
