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
