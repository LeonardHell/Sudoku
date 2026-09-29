import pytest

from sudoku_toolkit.board import Board
from sudoku_toolkit.io import (
    _create_board,
    load_txt,
    load_csv,
    load_board,
    save_txt,
    save_csv,
    save_board,
)


VALID_VALUES = [
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


def test_create_board():
    board = _create_board(VALID_VALUES)

    assert isinstance(board, Board)
    assert board.values == VALID_VALUES


def test_create_board_wrong_number_of_rows():
    values = VALID_VALUES[:-1]

    with pytest.raises(
        ValueError,
        match="exactly 9 rows"
    ):
        _create_board(values)


def test_create_board_wrong_number_of_columns():
    values = [row.copy() for row in VALID_VALUES]
    values[0] = values[0][:-1]

    with pytest.raises(
        ValueError,
        match="exactly 9 values"
    ):
        _create_board(values)


def test_create_board_invalid_value():
    values = [row.copy() for row in VALID_VALUES]
    values[0][0] = 10

    with pytest.raises(
        ValueError,
        match="between 0 and 9"
    ):
        _create_board(values)


def test_load_txt(tmp_path):
    filename = tmp_path / "puzzle.txt"

    filename.write_text(
        "5 3 0 0 7 0 0 0 0\n"
        "6 0 0 1 9 5 0 0 0\n"
        "0 9 8 0 0 0 0 6 0\n"
        "8 0 0 0 6 0 0 0 3\n"
        "4 0 0 8 0 3 0 0 1\n"
        "7 0 0 0 2 0 0 0 6\n"
        "0 6 0 0 0 0 2 8 0\n"
        "0 0 0 4 1 9 0 0 5\n"
        "0 0 0 0 8 0 0 7 9\n",
        encoding="utf-8",
    )

    board = load_txt(filename)

    assert board.values == VALID_VALUES


def test_load_txt_ignores_empty_lines(tmp_path):
    filename = tmp_path / "puzzle.txt"

    filename.write_text(
        "\n"
        "5 3 0 0 7 0 0 0 0\n"
        "6 0 0 1 9 5 0 0 0\n"
        "0 9 8 0 0 0 0 6 0\n"
        "8 0 0 0 6 0 0 0 3\n"
        "4 0 0 8 0 3 0 0 1\n"
        "7 0 0 0 2 0 0 0 6\n"
        "0 6 0 0 0 0 2 8 0\n"
        "0 0 0 4 1 9 0 0 5\n"
        "0 0 0 0 8 0 0 7 9\n"
        "\n",
        encoding="utf-8",
    )

    board = load_txt(filename)

    assert board.values == VALID_VALUES


def test_load_txt_non_numeric(tmp_path):
    filename = tmp_path / "puzzle.txt"

    filename.write_text(
        "5 3 0 0 7 0 0 0 X\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="non-numeric"
    ):
        load_txt(filename)


def test_load_txt_file_not_found(tmp_path):
    filename = tmp_path / "missing.txt"

    with pytest.raises(
        ValueError,
        match="File not found"
    ):
        load_txt(filename)


def test_load_csv(tmp_path):
    filename = tmp_path / "puzzle.csv"

    filename.write_text(
        "5,3,0,0,7,0,0,0,0\n"
        "6,0,0,1,9,5,0,0,0\n"
        "0,9,8,0,0,0,0,6,0\n"
        "8,0,0,0,6,0,0,0,3\n"
        "4,0,0,8,0,3,0,0,1\n"
        "7,0,0,0,2,0,0,0,6\n"
        "0,6,0,0,0,0,2,8,0\n"
        "0,0,0,4,1,9,0,0,5\n"
        "0,0,0,0,8,0,0,7,9\n",
        encoding="utf-8",
    )

    board = load_csv(filename)

    assert board.values == VALID_VALUES


def test_load_csv_non_numeric(tmp_path):
    filename = tmp_path / "puzzle.csv"

    filename.write_text(
        "5,3,0,0,7,0,0,0,X\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="non-numeric"
    ):
        load_csv(filename)


def test_load_board_txt(tmp_path):
    filename = tmp_path / "puzzle.txt"

    filename.write_text(
        "\n".join(
            " ".join(str(value) for value in row)
            for row in VALID_VALUES
        ),
        encoding="utf-8",
    )

    board = load_board(filename)

    assert board.values == VALID_VALUES


def test_load_board_csv(tmp_path):
    filename = tmp_path / "puzzle.csv"

    filename.write_text(
        "\n".join(
            ",".join(str(value) for value in row)
            for row in VALID_VALUES
        ),
        encoding="utf-8",
    )

    board = load_board(filename)

    assert board.values == VALID_VALUES


def test_load_board_unsupported_format(tmp_path):
    filename = tmp_path / "puzzle.json"
    filename.write_text("test", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="Unsupported file format"
    ):
        load_board(filename)


def test_save_txt(tmp_path):
    filename = tmp_path / "puzzle.txt"
    board = Board(VALID_VALUES)

    save_txt(board, filename)

    loaded_board = load_txt(filename)

    assert loaded_board.values == VALID_VALUES


def test_save_csv(tmp_path):
    filename = tmp_path / "puzzle.csv"
    board = Board(VALID_VALUES)

    save_csv(board, filename)

    loaded_board = load_csv(filename)

    assert loaded_board.values == VALID_VALUES


def test_save_board_txt(tmp_path):
    filename = tmp_path / "puzzle.txt"
    board = Board(VALID_VALUES)

    save_board(board, filename)

    assert load_board(filename).values == VALID_VALUES


def test_save_board_csv(tmp_path):
    filename = tmp_path / "puzzle.csv"
    board = Board(VALID_VALUES)

    save_board(board, filename)

    assert load_board(filename).values == VALID_VALUES


def test_save_board_unsupported_format(tmp_path):
    filename = tmp_path / "puzzle.json"
    board = Board(VALID_VALUES)

    with pytest.raises(
        ValueError,
        match="Unsupported file format"
    ):
        save_board(board, filename)
