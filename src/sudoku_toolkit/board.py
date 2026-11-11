"""Data model and basic operations for a 9x9 Sudoku board."""

from collections.abc import Iterable


class Board:
    """Representation of a 9x9 Sudoku board.

    The public ``values`` attribute stores nine mutable rows of nine integers.
    Values range from 1 to 9, and zero denotes an empty cell.
    """

    def __init__(self, values: Iterable[Iterable[int]]) -> None:
        """Copy and validate the supplied rows and cell values.

        Raises:
            ValueError: If the input is not a 9x9 grid of integers from 0 to 9.
        """
        # Copy each row so later edits to the caller's input cannot change this board.
        self.values = [list(row) for row in values]
        self.validate_structure()

    def validate_structure(self) -> None:
        """Reject malformed grids and values outside the allowed range."""

        if len(self.values) != 9:
            raise ValueError(
                "A Sudoku board must contain exactly 9 rows."
            )

        if any(len(row) != 9 for row in self.values):
            raise ValueError(
                "Each Sudoku row must contain exactly 9 values."
            )

        for row in self.values:
            for value in row:
                # bool is an int subclass, but True/False are not Sudoku digits.
                if type(value) is not int:
                    raise ValueError(
                        "Sudoku values must be integers."
                    )

                if not 0 <= value <= 9:
                    raise ValueError(
                        "Sudoku values must be between 0 and 9."
                    )

    def get(self, row: int, column: int) -> int:
        """Return the value at the zero-based row and column."""
        return self.values[row][column]

    def set(self, row: int, column: int, value: int) -> None:
        """Set a cell after checking its value and board coordinates.

        Raises:
            ValueError: If ``value`` is not an integer from 0 to 9.
            IndexError: If either coordinate is outside the board.
        """

        if type(value) is not int:
            raise ValueError("Sudoku values must be integers.")

        if not 0 <= value <= 9:
            raise ValueError("Sudoku values must be between 0 and 9.")

        if not 0 <= row < 9 or not 0 <= column < 9:
            raise IndexError("Cell indices must be between 0 and 8.")

        self.values[row][column] = value

    def __str__(self) -> str:
        """Return a formatted string representation of the Sudoku board."""

        lines = []

        for row_index, row in enumerate(self.values):
            if row_index > 0 and row_index % 3 == 0:
                lines.append("------+-------+------")

            row_values = []

            for column_index, value in enumerate(row):
                if column_index > 0 and column_index % 3 == 0:
                    row_values.append("|")

                row_values.append(str(value))

            lines.append(" ".join(row_values))

        return "\n".join(lines)
