def _unit_is_valid(values):
    """Check whether a row, column, or block contains no duplicates."""
    numbers = [value for value in values if value != 0]
    return len(numbers) == len(set(numbers))


def is_valid(board):
    """Check whether a Sudoku board satisfies the Sudoku rules."""

    # Check rows
    for row in board.values:
        if not _unit_is_valid(row):
            return False

    # Check columns
    for column in zip(*board.values):
        if not _unit_is_valid(column):
            return False

    # Check 3x3 blocks
    for row_start in range(0, 9, 3):
        for column_start in range(0, 9, 3):
            block = []

            for row in range(row_start, row_start + 3):
                for column in range(column_start, column_start + 3):
                    block.append(board.values[row][column])

            if not _unit_is_valid(block):
                return False

    return True
