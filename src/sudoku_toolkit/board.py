class Board:
    """Representation of a 9x9 Sudoku board."""

    def __init__(self, values):
        self.values = [row.copy() for row in values]

    def get(self, row, column):
        """Return the value at the given position."""
        return self.values[row][column]

    def set(self, row, column, value):
        """Set a value at the given position."""
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
