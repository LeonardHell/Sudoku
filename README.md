# Sudoku Toolkit

A Python library for validating, solving, and generating Sudoku puzzles.

## Features

* **Validate** Sudoku boards
* **Solve** Sudoku puzzles using backtracking
* **Generate** complete Sudoku solutions
* **Generate** Sudoku puzzles with a unique solution
* **Check** whether a Sudoku has zero, one, or multiple solutions
* **Generate** puzzles with different difficulty levels
* **Customise** the number of given clues
* **Test** the library with an automated test suite

## Installation

Clone the repository:

```bash
git clone <https://github.com/LeonardHell/Sudoku.git>
cd Sudoku
```

Create and activate a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package in editable mode:

```bash
pip install -e .
```

## Usage

### Validate a Sudoku

```python
from sudoku_toolkit.board import Board
from sudoku_toolkit.validator import is_valid

board = Board([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
])

is_valid(board)
```

`is_valid()` returns `True` if the board satisfies the Sudoku rules and `False` otherwise.

### Solve a Sudoku

```python
from sudoku_toolkit.solver import solve

solution = solve(board)
```

`solve()` returns a solved `Board` if a solution exists. If the puzzle is invalid or has no solution, it returns `None`.

### Count solutions

```python
from sudoku_toolkit.solver import count_solutions

number_of_solutions = count_solutions(board, limit=2)
```

The function counts solutions up to the specified limit. Using `limit=2` allows you to distinguish between:

* `0` → no solution
* `1` → unique solution
* `2` → at least two solutions

### Generate a complete Sudoku

```python
from sudoku_toolkit.generator import generate_solution

solution = generate_solution()
```

Each call generates a random, valid, completely filled Sudoku board.

### Generate a Sudoku puzzle

```python
from sudoku_toolkit.generator import generate_puzzle

puzzle = generate_puzzle(difficulty="medium")
```

Available difficulty levels are:

```text
easy
medium
hard
```

You can also specify the desired number of clues directly:

```python
puzzle = generate_puzzle(clues=35)
```

Generated puzzles have a unique solution.

The current difficulty settings are based on the number of given clues:

| Difficulty | Given clues |
| ---------- | ----------: |
| Easy       |          40 |
| Medium     |          32 |
| Hard       |          25 |

These values are heuristic difficulty settings rather than a formal measure of Sudoku difficulty.

## Testing

The project uses `pytest` for automated testing.

Run the complete test suite with:

```bash
pytest
```

The test suite covers the board, validator, solver, solution counting, and generator functionality.

## Project Structure

```text
Sudoku/
│
├── src/
│   └── sudoku_toolkit/
│       ├── __init__.py
│       ├── board.py
│       ├── validator.py
│       ├── solver.py
│       └── generator.py
│
├── tests/
│   ├── test_board.py
│   ├── test_validator.py
│   ├── test_solver.py
│   └── test_generator.py
│
├── pyproject.toml
└── README.md
```

## Implementation

The solver uses a **backtracking algorithm**. Empty cells are filled recursively with valid candidates until a complete solution is found or all possibilities have been exhausted.

The generator first creates a complete valid Sudoku and then removes numbers while checking that the resulting puzzle still has a unique solution.

Solution counting stops after the specified limit is reached. This avoids unnecessary computation when only uniqueness needs to be determined.

## Current Limitations

* Difficulty is currently determined by the number of given clues.
* The solver uses backtracking rather than human-style Sudoku solving strategies.
* The generator may require multiple attempts to produce puzzles with a low number of clues.
* The project currently provides a Python API; a command-line interface is planned.
