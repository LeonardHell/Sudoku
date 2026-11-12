"""Tests for reading and writing Sudoku boards in supported file formats."""

from pathlib import Path

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


def test_create_board(valid_puzzle_values: list[list[int]]) -> None:
    """Given valid Sudoku values,
    When a board is created from them,
    Then a Board containing those values is returned."""

    board = _create_board(valid_puzzle_values)

    assert isinstance(board, Board)
    assert board.values == valid_puzzle_values

def test_load_txt(tmp_path: Path, valid_puzzle_values: list[list[int]]) -> None:
    """Given a text file containing a Sudoku,
    When the file is loaded,
    Then the board values match the file."""

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

    assert board.values == valid_puzzle_values


def test_load_txt_ignores_empty_lines(
    tmp_path: Path, valid_puzzle_values: list[list[int]]
) -> None:
    """Given a text file containing a Sudoku and empty lines,
    When the file is loaded,
    Then the empty lines are ignored."""

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

    assert board.values == valid_puzzle_values


def test_load_txt_non_numeric(tmp_path: Path) -> None:
    """Given a text file containing a non-numeric cell,
    When the file is loaded,
    Then a ValueError is raised."""

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


def test_load_txt_file_not_found(tmp_path: Path) -> None:
    """Given a path to a missing text file,
    When the file is loaded,
    Then a ValueError is raised."""

    filename = tmp_path / "missing.txt"

    with pytest.raises(
        ValueError,
        match="File not found"
    ):
        load_txt(filename)


def test_load_csv(tmp_path: Path, valid_puzzle_values: list[list[int]]) -> None:
    """Given a CSV file containing a Sudoku,
    When the file is loaded,
    Then the board values match the file."""

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

    assert board.values == valid_puzzle_values


def test_load_csv_non_numeric(tmp_path: Path) -> None:
    """Given a CSV file containing a non-numeric cell,
    When the file is loaded,
    Then a ValueError is raised."""

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


def test_load_board_txt(
    tmp_path: Path, valid_puzzle_values: list[list[int]]
) -> None:
    """Given a text file containing a Sudoku,
    When the board is loaded by file format,
    Then the board values match the file."""

    filename = tmp_path / "puzzle.txt"

    filename.write_text(
        "\n".join(
            " ".join(str(value) for value in row)
            for row in valid_puzzle_values
        ),
        encoding="utf-8",
    )

    board = load_board(filename)

    assert board.values == valid_puzzle_values


def test_load_board_csv(
    tmp_path: Path, valid_puzzle_values: list[list[int]]
) -> None:
    """Given a CSV file containing a Sudoku,
    When the board is loaded by file format,
    Then the board values match the file."""

    filename = tmp_path / "puzzle.csv"

    filename.write_text(
        "\n".join(
            ",".join(str(value) for value in row)
            for row in valid_puzzle_values
        ),
        encoding="utf-8",
    )

    board = load_board(filename)

    assert board.values == valid_puzzle_values


def test_load_board_unsupported_format(tmp_path: Path) -> None:
    """Given a file with an unsupported extension,
    When the board is loaded,
    Then a ValueError is raised."""

    filename = tmp_path / "puzzle.json"
    filename.write_text("test", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="Unsupported file format"
    ):
        load_board(filename)


def test_save_txt(tmp_path: Path, valid_puzzle_values: list[list[int]]) -> None:
    """Given a Sudoku board and a text file path,
    When the board is saved and reloaded,
    Then the original board values are preserved."""

    filename = tmp_path / "puzzle.txt"
    board = Board(valid_puzzle_values)

    save_txt(board, filename)

    loaded_board = load_txt(filename)

    assert loaded_board.values == valid_puzzle_values


def test_save_csv(tmp_path: Path, valid_puzzle_values: list[list[int]]) -> None:
    """Given a Sudoku board and a CSV file path,
    When the board is saved and reloaded,
    Then the original board values are preserved."""

    filename = tmp_path / "puzzle.csv"
    board = Board(valid_puzzle_values)

    save_csv(board, filename)

    loaded_board = load_csv(filename)

    assert loaded_board.values == valid_puzzle_values


def test_save_board_txt(
    tmp_path: Path, valid_puzzle_values: list[list[int]]
) -> None:
    """Given a Sudoku board and a text file path,
    When the board is saved by file format and reloaded,
    Then the original board values are preserved."""

    filename = tmp_path / "puzzle.txt"
    board = Board(valid_puzzle_values)

    save_board(board, filename)

    assert load_board(filename).values == valid_puzzle_values


def test_save_board_csv(
    tmp_path: Path, valid_puzzle_values: list[list[int]]
) -> None:
    """Given a Sudoku board and a CSV file path,
    When the board is saved by file format and reloaded,
    Then the original board values are preserved."""

    filename = tmp_path / "puzzle.csv"
    board = Board(valid_puzzle_values)

    save_board(board, filename)

    assert load_board(filename).values == valid_puzzle_values


def test_save_board_unsupported_format(
    tmp_path: Path, valid_puzzle_values: list[list[int]]
) -> None:
    """Given a Sudoku board and a file path with an unsupported extension,
    When the board is saved,
    Then a ValueError is raised."""

    filename = tmp_path / "puzzle.json"
    board = Board(valid_puzzle_values)

    with pytest.raises(
        ValueError,
        match="Unsupported file format"
    ):
        save_board(board, filename)

def test_load_csv_skips_empty_rows(tmp_path: Path) -> None:
    """Given a CSV file containing an empty row,
    When the file is loaded,
    Then the empty row is skipped."""

    filename = tmp_path / "puzzle.csv"

    rows = [
        "5,3,0,0,7,0,0,0,0",
        "6,0,0,1,9,5,0,0,0",
        "0,9,8,0,0,0,0,6,0",
        "8,0,0,0,6,0,0,0,3",
        "4,0,0,8,0,3,0,0,1",
        "7,0,0,0,2,0,0,0,6",
        "0,6,0,0,0,0,2,8,0",
        "0,0,0,4,1,9,0,0,5",
        "0,0,0,0,8,0,0,7,9",
    ]

    filename.write_text(
        "\n".join(rows[:4]) + "\n\n" + "\n".join(rows[4:]),
        encoding="utf-8",
    )

    board = load_csv(filename)

    assert len(board.values) == 9
    assert board.values[0] == [5, 3, 0, 0, 7, 0, 0, 0, 0]

def test_load_csv_file_not_found(tmp_path: Path) -> None:
    """Given a path to a missing CSV file,
    When the file is loaded,
    Then a ValueError is raised."""

    filename = tmp_path / "missing.csv"

    with pytest.raises(
        ValueError,
        match="File not found",
    ):
        load_csv(filename)
