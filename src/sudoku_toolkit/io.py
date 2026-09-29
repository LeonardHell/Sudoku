import csv
from pathlib import Path

from .board import Board


def _create_board(rows):
    """Create a Board after validating its dimensions and values."""

    if len(rows) != 9:
        raise ValueError(
            "A Sudoku board must contain exactly 9 rows."
        )

    if any(len(row) != 9 for row in rows):
        raise ValueError(
            "Each Sudoku row must contain exactly 9 values."
        )

    if any(
        value < 0 or value > 9
        for row in rows
        for value in row
    ):
        raise ValueError(
            "Sudoku values must be between 0 and 9."
        )

    return Board(rows)


def load_txt(filename):
    """Load a Sudoku board from a text file."""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            rows = []

            for line in file:
                line = line.strip()

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


def load_csv(filename):
    """Load a Sudoku board from a CSV file."""

    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = []

            for row in reader:
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

def load_board(filename):
    """Load a Sudoku board from a supported file format."""

    extension = Path(filename).suffix.lower()

    if extension == ".txt":
        return load_txt(filename)

    if extension == ".csv":
        return load_csv(filename)

    raise ValueError(
        "Unsupported file format. "
        "Supported formats are: .txt, .csv"
    )

def save_txt(board, filename):
    """Save a Sudoku board to a text file."""

    with open(filename, "w", encoding="utf-8") as file:
        for row in board.values:
            file.write(" ".join(str(value) for value in row) + "\n")


def save_csv(board, filename):
    """Save a Sudoku board to a CSV file."""

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(board.values)

def save_board(board, filename):
    """Save a Sudoku board to a supported file format."""

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
