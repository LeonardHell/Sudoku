import sys

from sudoku_toolkit.board import Board
from sudoku_toolkit import cli


VALID_BOARD = Board([
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


def test_generate_command(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "generate"]
    )

    monkeypatch.setattr(
        cli,
        "generate_solution",
        lambda: VALID_BOARD
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == str(VALID_BOARD) + "\n"


def test_puzzle_command(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "puzzle"]
    )

    monkeypatch.setattr(
        cli,
        "generate_puzzle",
        lambda difficulty=None: VALID_BOARD
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == str(VALID_BOARD) + "\n"


def test_puzzle_with_difficulty(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "puzzle", "--difficulty", "hard"]
    )

    def fake_generate_puzzle(difficulty=None):
        assert difficulty == "hard"
        return VALID_BOARD

    monkeypatch.setattr(
        cli,
        "generate_puzzle",
        fake_generate_puzzle
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == str(VALID_BOARD) + "\n"


def test_puzzle_with_clues(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "puzzle", "--clues", "30"]
    )

    def fake_generate_puzzle(clues=None):
        assert clues == 30
        return VALID_BOARD

    monkeypatch.setattr(
        cli,
        "generate_puzzle",
        fake_generate_puzzle
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == str(VALID_BOARD) + "\n"


def test_solve_command(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "solve", "puzzle.txt"]
    )

    monkeypatch.setattr(
        cli,
        "load_board",
        lambda filename: VALID_BOARD
    )

    monkeypatch.setattr(
        cli,
        "solve",
        lambda board: VALID_BOARD
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == str(VALID_BOARD) + "\n"


def test_solve_unsolvable(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "solve", "puzzle.txt"]
    )

    monkeypatch.setattr(
        cli,
        "load_board",
        lambda filename: VALID_BOARD
    )

    monkeypatch.setattr(
        cli,
        "solve",
        lambda board: None
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == "The Sudoku has no solution.\n"


def test_validate_valid(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "validate", "puzzle.txt"]
    )

    monkeypatch.setattr(
        cli,
        "load_board",
        lambda filename: VALID_BOARD
    )

    monkeypatch.setattr(
        cli,
        "is_valid",
        lambda board: True
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == "The Sudoku is valid.\n"


def test_validate_invalid(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "validate", "puzzle.txt"]
    )

    monkeypatch.setattr(
        cli,
        "load_board",
        lambda filename: VALID_BOARD
    )

    monkeypatch.setattr(
        cli,
        "is_valid",
        lambda board: False
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == "The Sudoku is invalid.\n"


def test_no_command(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku"]
    )

    cli.main()

    captured = capsys.readouterr()

    assert "usage:" in captured.out
    assert "generate" in captured.out
    assert "puzzle" in captured.out
    assert "solve" in captured.out
    assert "validate" in captured.out
