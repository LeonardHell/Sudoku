"""Tests for CLI commands, argument handling, output, and error reporting."""

import argparse
import sys
import runpy
import pytest
from pathlib import Path

from sudoku_toolkit import Board, cli
from sudoku_toolkit.solver import is_valid


def test_generate_command(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    valid_puzzle_board: Board,
) -> None:
    """Given the generate command with no output path,
    When the CLI runs,
    Then the generated Sudoku is printed."""

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "generate"]
    )

    monkeypatch.setattr(
        cli,
        "generate_solution",
        lambda: valid_puzzle_board
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == str(valid_puzzle_board) + "\n"


def test_generate_with_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    valid_puzzle_board: Board,
) -> None:
    """Given the generate command with an output path,
    When the CLI runs,
    Then the generated Sudoku is saved to that path."""

    output_file = tmp_path / "solution.txt"

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "generate", "--output", str(output_file)]
    )

    monkeypatch.setattr(
        cli,
        "generate_solution",
        lambda: valid_puzzle_board
    )

    saved = {}

    def fake_save_board(board, filename):
        """Record the board and destination passed to the save operation."""
        saved["board"] = board
        saved["filename"] = filename

    monkeypatch.setattr(
        cli,
        "save_board",
        fake_save_board
    )

    cli.main()

    assert saved["board"] is valid_puzzle_board
    assert saved["filename"] == str(output_file)


def test_puzzle_command(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    valid_puzzle_board: Board,
) -> None:
    """Given the puzzle command with default options,
    When the CLI runs,
    Then the generated puzzle is printed."""

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "puzzle"]
    )

    monkeypatch.setattr(
        cli,
        "generate_puzzle",
        lambda difficulty=None: valid_puzzle_board
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == str(valid_puzzle_board) + "\n"


def test_puzzle_with_difficulty(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    valid_puzzle_board: Board,
) -> None:
    """Given the puzzle command with a difficulty option,
    When the CLI runs,
    Then the requested difficulty is used and the puzzle is printed."""

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "puzzle", "--difficulty", "hard"]
    )

    def fake_generate_puzzle(difficulty=None):
        """Check the requested difficulty and return the shared test board."""
        assert difficulty == "hard"
        return valid_puzzle_board

    monkeypatch.setattr(
        cli,
        "generate_puzzle",
        fake_generate_puzzle
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == str(valid_puzzle_board) + "\n"


def test_puzzle_with_clues(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    valid_puzzle_board: Board,
) -> None:
    """Given the puzzle command with a clue-count option,
    When the CLI runs,
    Then the requested clue count is used and the puzzle is printed."""

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "puzzle", "--clues", "30"]
    )

    def fake_generate_puzzle(clues=None):
        """Check the requested clue count and return the shared test board."""
        assert clues == 30
        return valid_puzzle_board

    monkeypatch.setattr(
        cli,
        "generate_puzzle",
        fake_generate_puzzle
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == str(valid_puzzle_board) + "\n"


def test_puzzle_with_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    valid_puzzle_board: Board,
) -> None:
    """Given the puzzle command with an output path,
    When the CLI runs,
    Then the generated puzzle is saved to that path."""

    output_file = tmp_path / "puzzle.txt"

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "puzzle", "--output", str(output_file)]
    )

    monkeypatch.setattr(
        cli,
        "generate_puzzle",
        lambda difficulty=None: valid_puzzle_board
    )

    saved = {}

    def fake_save_board(board, filename):
        """Record the board and destination passed to the save operation."""
        saved["board"] = board
        saved["filename"] = filename

    monkeypatch.setattr(
        cli,
        "save_board",
        fake_save_board
    )

    cli.main()

    assert saved["board"] is valid_puzzle_board
    assert saved["filename"] == str(output_file)


def test_solve_command(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    valid_puzzle_board: Board,
) -> None:
    """Given the solve command with a solvable input file,
    When the CLI runs,
    Then the solved Sudoku is printed."""

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "solve", "puzzle.txt"]
    )

    monkeypatch.setattr(
        cli,
        "load_board",
        lambda filename: valid_puzzle_board
    )

    monkeypatch.setattr(
        cli,
        "solve",
        lambda board: valid_puzzle_board
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == str(valid_puzzle_board) + "\n"


def test_solve_unsolvable(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    valid_puzzle_board: Board,
) -> None:
    """Given the solve command with an unsolvable input file,
    When the CLI runs,
    Then a no-solution message is printed."""

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "solve", "puzzle.txt"]
    )

    monkeypatch.setattr(
        cli,
        "load_board",
        lambda filename: valid_puzzle_board
    )

    monkeypatch.setattr(
        cli,
        "solve",
        lambda board: None
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == "The Sudoku has no solution.\n"


def test_solve_with_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    valid_puzzle_board: Board,
) -> None:
    """Given the solve command with an output path,
    When the CLI runs,
    Then the solved Sudoku is saved to that path."""

    output_file = tmp_path / "solution.txt"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "sudoku",
            "solve",
            "puzzle.txt",
            "--output",
            str(output_file)
        ]
    )

    monkeypatch.setattr(
        cli,
        "load_board",
        lambda filename: valid_puzzle_board
    )

    monkeypatch.setattr(
        cli,
        "solve",
        lambda board: valid_puzzle_board
    )

    saved = {}

    def fake_save_board(board, filename):
        """Record the board and destination passed to the save operation."""
        saved["board"] = board
        saved["filename"] = filename

    monkeypatch.setattr(
        cli,
        "save_board",
        fake_save_board
    )

    cli.main()

    assert saved["board"] is valid_puzzle_board
    assert saved["filename"] == str(output_file)


def test_validate_valid(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    valid_puzzle_board: Board,
) -> None:
    """Given the validate command with a valid Sudoku file,
    When the CLI runs,
    Then a valid-status message is printed."""

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "validate", "puzzle.txt"]
    )

    monkeypatch.setattr(
        cli,
        "load_board",
        lambda filename: valid_puzzle_board
    )

    monkeypatch.setattr(
        cli,
        "is_valid",
        lambda board: True
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == "The Sudoku is valid.\n"


def test_validate_invalid(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    valid_puzzle_board: Board,
) -> None:
    """Given the validate command with an invalid Sudoku file,
    When the CLI runs,
    Then an invalid-status message is printed."""

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "validate", "puzzle.txt"]
    )

    monkeypatch.setattr(
        cli,
        "load_board",
        lambda filename: valid_puzzle_board
    )

    monkeypatch.setattr(
        cli,
        "is_valid",
        lambda board: False
    )

    cli.main()

    captured = capsys.readouterr()

    assert captured.out == "The Sudoku is invalid.\n"


def test_no_command(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Given the CLI is invoked without a command,
    When the CLI runs,
    Then usage information and available commands are displayed."""

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


def test_save_board_error(
    monkeypatch: pytest.MonkeyPatch, valid_puzzle_board: Board
) -> None:
    """Given a save operation that raises a ValueError,
    When the CLI saves the board,
    Then the CLI exits with an error."""

    parser = cli.argparse.ArgumentParser()

    def fake_save_board(board, filename):
        """Simulate a save failure for an unsupported file format."""
        raise ValueError("Unsupported file format")

    monkeypatch.setattr(
        cli,
        "save_board",
        fake_save_board
    )

    with pytest.raises(SystemExit):
        cli._save_board(
            valid_puzzle_board,
            "puzzle.json",
            parser
        )

def test_load_board_unsupported_format(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Given an input file with an unsupported format,
    When the CLI loads the board,
    Then it exits with an error listing supported formats."""

    filename = tmp_path / "puzzle.xlsx"
    parser = argparse.ArgumentParser()

    with pytest.raises(SystemExit) as error:
        cli._load_board(filename, parser)

    assert error.value.code == 2

    captured = capsys.readouterr()
    assert "Unsupported file format" in captured.err
    assert "Supported formats are: .txt, .csv" in captured.err

def test_puzzle_generation_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Given the puzzle command with an invalid clue count,
    When the CLI runs,
    Then it exits with an error describing the allowed range."""

    monkeypatch.setattr(
        "sys.argv",
        ["sudoku-toolkit", "puzzle", "--clues", "10"]
    )

    with pytest.raises(SystemExit) as error:
        cli.main()

    assert error.value.code == 2

    captured = capsys.readouterr()
    assert "clues must be between 17 and 81" in captured.err

def test_cli_entry_point_without_command(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Given the module entry point is invoked without a command,
    When the module runs,
    Then usage information and commands are displayed."""

    monkeypatch.setattr(sys, "argv", ["sudoku-toolkit"])
    monkeypatch.delitem(
        sys.modules, "sudoku_toolkit.cli", raising=False
    )

    runpy.run_module("sudoku_toolkit.cli", run_name="__main__")

    captured = capsys.readouterr()
    assert "usage:" in captured.out.lower()
    assert "generate" in captured.out
    assert "solve" in captured.out

@pytest.mark.parametrize(
    "options",
    [
        ["--clues", "40", "--difficulty", "hard"],
        ["--difficulty", "hard", "--clues", "40"],
    ],
)

def test_puzzle_rejects_clues_and_difficulty(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    options: list[str],
) -> None:
    """Given the puzzle command with both clues and difficulty options,
    When the CLI runs,
    Then it exits with an error without generating a puzzle."""

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "puzzle", *options],
    )

    def unexpected_generation(*args, **kwargs):
        """Fail if conflicting arguments reach puzzle generation."""
        pytest.fail("Generation must not run with conflicting options.")

    monkeypatch.setattr(
        cli,
        "generate_puzzle",
        unexpected_generation,
    )

    with pytest.raises(SystemExit) as error:
        cli.main()

    assert error.value.code == 2

    captured = capsys.readouterr()
    assert "not allowed with argument" in captured.err
    assert "--clues" in captured.err
    assert "--difficulty" in captured.err

def test_save_reports_missing_directory_without_traceback(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    valid_puzzle_board: Board,
) -> None:
    """Given an output path whose directory does not exist,
    When the CLI saves the board,
    Then it exits with a readable error and no traceback."""

    filename = tmp_path / "missing_directory" / "solution.txt"
    parser = argparse.ArgumentParser()

    with pytest.raises(SystemExit) as error:
        cli._save_board(valid_puzzle_board, filename, parser)

    assert error.value.code == 2

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert repr(str(filename)) in captured.err
    assert "Traceback" not in captured.err

def test_puzzle_generation_failure_is_reported(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Given puzzle generation that raises a RuntimeError,
    When the CLI runs,
    Then it exits with a readable error and no traceback."""

    monkeypatch.setattr(
        sys,
        "argv",
        ["sudoku", "puzzle"],
    )

    def failed_generation(*args, **kwargs):
        """Simulate puzzle generation exhausting its attempts."""
        raise RuntimeError("Could not generate a Sudoku.")

    monkeypatch.setattr(
        cli,
        "generate_puzzle",
        failed_generation,
    )

    with pytest.raises(SystemExit) as error:
        cli.main()

    assert error.value.code == 2

    captured = capsys.readouterr()
    assert "Could not generate a Sudoku." in captured.err
    assert "Traceback" not in captured.err
