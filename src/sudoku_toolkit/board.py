class Board:
    """Representation of a 9x9 Sudoku board. Zero denotes an empty cell."""

    def __init__(self, values):
        self.values = [list(row) for row in values]
        self.validate_structure()

    def validate_structure(self):
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
                if type(value) is not int:
                    raise ValueError(
                        "Sudoku values must be integers."
                    )

                if not 0 <= value <= 9:
                    raise ValueError(
                        "Sudoku values must be between 0 and 9."
                    )

    def get(self, row, column):
        """Return the value at the given position."""
        return self.values[row][column]

    def set(self, row, column, value):
        """Set a cell to an integer between 0 and 9."""

        if type(value) is not int:
            raise ValueError("Sudoku values must be integers.")

        if not 0 <= value <= 9:
            raise ValueError("Sudoku values must be between 0 and 9.")

        if not 0 <= row < 9 or not 0 <= column < 9:
            raise IndexError("Cell indices must be between 0 and 8.")

        self.values[row][column] = value

    def __str__(self):
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
