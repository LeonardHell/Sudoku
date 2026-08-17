from sudoku_toolkit import Board


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