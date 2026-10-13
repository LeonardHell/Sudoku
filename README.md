# Sudoku Toolkit

A Python library and command-line tool for validating, solving, and generating standard 9x9 Sudoku puzzles.

## Features

- Validate board dimensions, cell values, and Sudoku rules.
- Solve puzzles using backtracking with a Minimum Remaining Values heuristic.
- Count solutions up to a specified limit.
- Generate complete Sudoku solutions.
- Generate puzzles with a unique solution.
- Choose a difficulty level or an exact number of clues.
- Load and save boards in TXT and CSV formats.
- Run an automated test suite.

## Requirements and installation

The project requires Python 3.10 or newer.

Windows is the tested platform. Other operating systems have not been tested.

The library has no third-party runtime dependencies. Testing uses pytest and pytest-cov, available through the optional test dependencies.

### Windows PowerShell

Clone the repository:

```powershell
git clone https://github.com/LeonardHell/Sudoku.git
cd Sudoku
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the package in editable mode:

```powershell
python -m pip install -e .
```

To also install the testing dependencies:

```powershell
python -m pip install -e ".[test]"
```

Run the following commands from the activated virtual environment.

## Command-line interface

The `sudoku` command provides four subcommands: `generate`, `puzzle`, `validate`, and `solve`.

Display the available commands:

```powershell
sudoku --help
```

Display help for a specific command:

```powershell
sudoku puzzle --help
```

### Generate a complete solution

```powershell
sudoku generate
sudoku generate --output solution.csv
```

### Generate a puzzle

Generate a puzzle with the default number of 35 clues:

```powershell
sudoku puzzle
```

Choose a difficulty level or an exact clue count:

```powershell
sudoku puzzle --difficulty medium
sudoku puzzle --clues 35
```

Save the puzzle:

```powershell
sudoku puzzle --difficulty easy --output puzzle.txt
```

`--difficulty` and `--clues` cannot be used together.

### Validate a puzzle

```powershell
sudoku validate puzzle.txt
```

The command reports whether the loaded board satisfies the Sudoku rules. File loading also checks dimensions and allowed values.

A valid board may contain empty cells and is not necessarily solvable.

### Solve a puzzle

```powershell
sudoku solve puzzle.txt
sudoku solve puzzle.txt --output solution.csv
```

If the board is invalid or unsolvable, the command prints:

```text
The Sudoku has no solution.
```

### Complete example

```powershell
sudoku puzzle --difficulty easy --output puzzle.txt
sudoku validate puzzle.txt
sudoku solve puzzle.txt --output solution.csv
sudoku validate solution.csv
```

When `--output` is omitted, generated boards and solutions are printed to the terminal. With `--output`, they are saved as TXT or CSV files.

The destination directory must already exist. Saving to an existing file overwrites its contents.

Invalid arguments and handled file or generation errors are reported without a traceback and terminate the command with exit code 2. An invalid Sudoku reported by `validate`, or a puzzle with no solution reported by `solve`, currently produces a message without a nonzero exit code.

## File formats

Boards contain exactly nine rows and nine integer values per row. Allowed values are 0-9, where `0` represents an empty cell.

### TXT

Values are separated by whitespace. Save the following example as `puzzle.txt`:

```text
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
```

### CSV

Values are separated by commas. Files must not contain a header. For example, the first row of the board above becomes:

```text
5,3,0,0,7,0,0,0,0
```

Both formats require the complete nine-row board. Empty lines are ignored.

The formatted terminal display containing `|` and `------` is not a supported input format. Use `--output` or the file-saving functions to create a loadable file.

## Python API

### Create and edit a board

```python
from sudoku_toolkit import Board

board = Board([
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

print(board)
print(board.get(0, 0))
board.set(0, 2, 4)
```

`Board(values)` copies the supplied rows. Incorrect dimensions, non-integer values, booleans, and values outside 0-9 raise `ValueError`.

Cell indices are zero-based: rows and columns range from 0 to 8. `set()` rejects invalid values with `ValueError` and indices outside the board with `IndexError`.

Duplicate numbers are allowed when constructing or editing a board. Use `is_valid()` to check for Sudoku rule violations.

`board.validate_structure()` checks dimensions and allowed values, raising `ValueError` if these conditions are violated. It does not check Sudoku rule conflicts.

### Validate a Sudoku

```python
from sudoku_toolkit.validator import is_valid

valid = is_valid(board)
print(valid)
```

`is_valid()` returns `False` for invalid dimensions, invalid values, or duplicate nonzero values in a row, column, or 3x3 block.

It returns `True` for a board without these violations, including an empty board. It does not determine whether the puzzle is solvable or has a unique solution.

### Solve a Sudoku

```python
from sudoku_toolkit.solver import solve

solution = solve(board)

if solution is None:
    print("The Sudoku has no solution.")
else:
    print(solution)
```

`solve()` returns the first solved `Board` found. It returns `None` if the input board is invalid or the puzzle has no solution.

The input board is not modified.

### Count solutions

```python
from sudoku_toolkit.solver import count_solutions

number_of_solutions = count_solutions(board, limit=2)
print(number_of_solutions)
```

Use a positive integer for `limit`. Its default is 2.

The function counts solutions up to the specified limit. With `limit=2`:

- `0`: no solution.
- `1`: exactly one solution.
- `2`: at least two solutions.

The input board is not modified. Invalid boards return 0.

### Generate a complete Sudoku

```python
from sudoku_toolkit.generator import generate_solution

solution = generate_solution()
print(solution)
```

The function returns a random, valid, completely filled `Board`.

### Generate a Sudoku puzzle

```python
from sudoku_toolkit.generator import generate_puzzle

puzzle = generate_puzzle(difficulty="medium")
print(puzzle)
```

Alternatively, specify the exact number of clues:

```python
puzzle = generate_puzzle(clues=35)
```

Generated puzzles have exactly one solution.

The function signature is:

```python
generate_puzzle(clues=None, difficulty=None, max_attempts=100)
```

| Parameter | Meaning | Default |
|-----------|---------|---------|
| `clues` | Exact number of nonempty cells; use an integer from 17 to 81 | 35 when neither `clues` nor `difficulty` is supplied |
| `difficulty` | `easy`, `medium`, or `hard` | None |
| `max_attempts` | Maximum number of generation attempts; use a positive integer | 100 |

Difficulty levels correspond to the following clue counts:

| Difficulty | Given clues |
|------------|------------:|
| Easy | 40 |
| Medium | 32 |
| Hard | 25 |

These labels are based on clue count, not a formal assessment of solving difficulty.

`clues` and `difficulty` cannot both be supplied. Unsupported difficulty levels, clue counts outside the allowed range, and `max_attempts` below 1 raise `ValueError`.

If the requested clue count cannot be reached within `max_attempts`, the function raises `RuntimeError`.

Generation is random. Repeated calls generally produce different boards. The generator uses Python's `random` module; the API currently has no dedicated seed parameter.

### Load and save boards

```python
from sudoku_toolkit.io import load_board, save_board

board = load_board("puzzle.txt")
solution = solve(board)

if solution is not None:
    save_board(solution, "solution.csv")
```

`load_board()` and `save_board()` select the format from the file extension: `.txt` or `.csv`. Extension matching is case-insensitive.

Format-specific functions are also available:

```python
from sudoku_toolkit.io import load_txt, load_csv, save_txt, save_csv
```

Unsupported extensions and malformed input files raise `ValueError`. Missing input files are reported as `ValueError` by the loaders. Other file-access errors may raise `OSError`.

Saving overwrites an existing file. The destination directory must already exist.

## Implementation

The solver uses recursive backtracking. It selects an empty cell using a Minimum Remaining Values heuristic, prioritizing cells with few valid candidates, and tries numbers from 1 to 9.

If a candidate leads to a dead end, the solver restores the empty cell and tries another candidate.

Solution counting uses the same search strategy. Recursive calls receive the remaining solution limit, so the result cannot exceed the specified positive limit.

The generator creates a complete board using randomized backtracking. It then attempts to remove numbers in random order, keeping each removal only if the puzzle still has exactly one solution.

If an attempt cannot reach the requested clue count, generation restarts with a new complete board, up to `max_attempts`.

Board representation, rule validation, solving, generation, file operations, and the command-line interface are implemented in separate modules.

## Limitations

- Only standard 9x9 Sudoku boards with 3x3 blocks are supported.
- Difficulty is estimated from clue count.
- Low clue counts can require many attempts and are not guaranteed to be reached.
- Backtracking can be slow for difficult puzzles or large solution-count limits.
- The library does not provide a graphical interface or explanations of human solving techniques.
- Only Windows is currently tested.

## Testing

Install the test dependencies:

```powershell
python -m pip install -e ".[test]"
```

Run the complete test suite:

```powershell
python -m pytest
```

Run the tests with coverage measurement:

```powershell
python -m pytest --cov=sudoku_toolkit --cov-report=term-missing
```

The suite tests board input validation, Sudoku rules, solving, solution counting, generation, TXT/CSV file operations, and command-line behavior.

Regression tests cover the solution-count limit, directly modified invalid boards, conflicting CLI options, and handled CLI errors.

Randomized generation tests use a fixed seed. The exhausted-attempts error path is tested using a controlled replacement of solution counting.

## Project structure

```text
Sudoku/
├── src/
│   └── sudoku_toolkit/
│       ├── __init__.py
│       ├── board.py
│       ├── validator.py
│       ├── solver.py
│       ├── generator.py
│       ├── io.py
│       └── cli.py
├── tests/
│   ├── test_board.py
│   ├── test_validator.py
│   ├── test_solver.py
│   ├── test_generator.py
│   ├── test_io.py
│   └── test_cli.py
├── pyproject.toml
└── README.md
```
