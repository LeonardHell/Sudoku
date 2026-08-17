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
        