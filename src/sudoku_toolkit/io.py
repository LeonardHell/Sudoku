"""Read and write Sudoku boards in whitespace-delimited text and CSV formats."""

import csv
from collections.abc import Iterable
from os import PathLike
from pathlib import Path

from .board import Board


def _create_board(rows: Iterable[Iterable[int]]) -> Board:
    """Construct a board from rows, applying the board's structure checks."""

    board = Board(rows)
    board.validate_structure()
    return board


def load_txt(filename: str | PathLike[str]) -> Board:
    """Load a Sudoku board whose rows contain whitespace-separated integers.

    Blank lines are ignored. Missing files and non-numeric cells raise
    ``ValueError``; malformed dimensions or values are rejected by ``Board``.
    """

    try:
        with open(filename, "r", encoding="utf-8") as file:
            rows = []

            for line in file:
                line = line.strip()

                # Ignore blank or whitespace-only lines rather than treating them as rows.
                if not line:
                    continue

                try:
                    values = [int(value) for value in line.split()]
                except ValueError:
                    raise ValueError(
                        "Text file contains non-numeric values."
                    )

                rows.append(values)

    except FileNotFoundError:
        raise ValueError(f"File not found: {filename}")

    return _create_board(rows)


def load_csv(filename: str | PathLike[str]) -> Board:
    """Load a Sudoku board whose rows contain comma-separated integers.

    Empty rows are ignored. Missing files and non-numeric cells raise
    ``ValueError``; malformed dimensions or values are rejected by ``Board``.
    """

    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = []

            for row in reader:
                # csv.reader represents a completely blank line as an empty row.
                if not row:
                    continue

                try:
                    values = [int(value.strip()) for value in row]
                except ValueError:
                    raise ValueError(
                        "CSV file contains non-numeric values."
                    )

                rows.append(values)

    except FileNotFoundError:
        raise ValueError(f"File not found: {filename}")

    return _create_board(rows)

def load_board(filename: str | PathLike[str]) -> Board:
    """Choose a text or CSV loader from the filename's extension.

    The extension is case-insensitive. Unsupported extensions raise
    ``ValueError``.
    """

    extension = Path(filename).suffix.lower()

    if extension == ".txt":
        return load_txt(filename)

    if extension == ".csv":
        return load_csv(filename)

    raise ValueError(
        "Unsupported file format. "
        "Supported formats are: .txt, .csv"
    )

def save_txt(board: Board, filename: str | PathLike[str]) -> None:
    """Write each board row as space-separated values to a text file."""

    with open(filename, "w", encoding="utf-8") as file:
        for row in board.values:
            file.write(" ".join(str(value) for value in row) + "\n")


def save_csv(board: Board, filename: str | PathLike[str]) -> None:
    """Write each board row as a CSV record."""

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(board.values)

def save_board(board: Board, filename: str | PathLike[str]) -> None:
    """Choose a text or CSV writer from the filename's extension.

    The extension is case-insensitive. Unsupported extensions raise
    ``ValueError``.
    """

    extension = Path(filename).suffix.lower()

    if extension == ".txt":
        save_txt(board, filename)
        return

    if extension == ".csv":
        save_csv(board, filename)
        return

    raise ValueError(
        "Unsupported file format. "
        "Supported formats are: .txt, .csv"
    )
