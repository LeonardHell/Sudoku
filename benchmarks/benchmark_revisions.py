"""Compare Sudoku search and validation across two repository revisions."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from collections.abc import Generator
from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
import platform
import random
import statistics
import subprocess
import sys
import tarfile
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from sudoku_toolkit import Board as CurrentBoard
from sudoku_toolkit.solver import (
    count_solutions as current_count_solutions,
    solve as current_solve,
)
from sudoku_toolkit.validator import is_valid as current_is_valid

BASELINE_COMMIT = "7731443"
SEED = 42

PUZZLES: dict[str, list[list[int]]] = {
    "classic-30-clue": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ],
    "seed-42-35-clue": [
        [4, 9, 0, 3, 0, 1, 0, 5, 0],
        [0, 0, 0, 0, 8, 0, 2, 0, 0],
        [0, 7, 1, 0, 6, 9, 0, 8, 0],
        [0, 0, 0, 6, 3, 0, 9, 0, 0],
        [6, 2, 9, 0, 0, 8, 0, 3, 0],
        [0, 0, 3, 0, 5, 0, 1, 0, 6],
        [0, 3, 6, 1, 4, 5, 0, 0, 0],
        [0, 1, 0, 0, 9, 0, 0, 0, 0],
        [9, 0, 2, 0, 7, 0, 5, 0, 0],
    ],
    "seed-42-25-clue": [
        [8, 0, 0, 0, 0, 1, 0, 4, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 8, 7, 0, 0, 2],
        [0, 2, 0, 0, 0, 6, 0, 0, 7],
        [0, 7, 0, 0, 0, 0, 5, 0, 1],
        [6, 0, 8, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 4, 0, 2, 0, 0],
        [0, 8, 0, 0, 7, 0, 9, 0, 0],
        [0, 0, 0, 0, 2, 3, 0, 8, 0],
    ],
    "multiple-solution-21-clue": [
        [0, 0, 0, 0, 5, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 0, 0, 0, 7],
        [1, 5, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 5, 0],
        [2, 0, 0, 5, 0, 3, 0, 0, 9],
        [0, 0, 0, 7, 0, 9, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 5],
        [7, 1, 0, 0, 2, 0, 0, 9, 0],
    ],
    "sparse-multiple-solution-7-clue": [
        [5, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [2, 0, 0, 0, 8, 0, 0, 0, 0],
    ],
}


@contextmanager
def _load_baseline_package(source_root: Path) -> Generator[ModuleType, None, None]:
    """Load the historical package from the pinned commit in an isolated name."""
    archive = subprocess.run(
        ["git", "archive", BASELINE_COMMIT, "src/sudoku_toolkit"],
        cwd=source_root,
        check=True,
        capture_output=True,
    )
    with tempfile.TemporaryDirectory(prefix="sudoku-baseline-") as directory:
        with tarfile.open(fileobj=BytesIO(archive.stdout)) as source_archive:
            source_archive.extractall(directory)
        package_path = (
            Path(directory) / "src" / "sudoku_toolkit"
        )
        package_name = "sudoku_toolkit_baseline"
        spec = spec_from_file_location(
            package_name,
            package_path / "__init__.py",
            submodule_search_locations=[str(package_path)],
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load baseline package {BASELINE_COMMIT}")
        package = module_from_spec(spec)
        sys.modules[package_name] = package
        spec.loader.exec_module(package)
        yield package


def _numpy_candidates(
    grid: Any,
    row: int,
    column: int,
    numpy: ModuleType,
) -> list[int]:
    """Return legal digits using NumPy row, column, and block arrays."""
    block_row = (row // 3) * 3
    block_column = (column // 3) * 3
    used = numpy.concatenate(
        (
            grid[row, :],
            grid[:, column],
            grid[block_row:block_row + 3, block_column:block_column + 3].ravel(),
        )
    )
    digits = numpy.arange(1, 10)
    return digits[~numpy.isin(digits, used)].tolist()


def numpy_is_valid(board: Any, numpy: ModuleType) -> bool:
    """Check board structure and Sudoku rules with NumPy operations."""
    try:
        board.validate_structure()
    except ValueError:
        return False

    grid = numpy.asarray(board.values)
    units = [
        *grid,
        *grid.T,
        *grid.reshape(3, 3, 3, 3).transpose(0, 2, 1, 3).reshape(9, 9),
    ]
    for unit in units:
        nonzero = unit[unit != 0]
        if numpy.unique(nonzero).size != nonzero.size:
            return False
    return True


def numpy_solve(board: Any, numpy: ModuleType) -> Any | None:
    """Solve a board using NumPy arrays for candidate and MRV operations."""
    if not numpy_is_valid(board, numpy):
        return None

    grid = numpy.array(board.values, dtype=int, copy=True)

    def search() -> bool:
        best_position = None
        best_candidates = None
        for row, column in numpy.argwhere(grid == 0):
            candidates = _numpy_candidates(grid, int(row), int(column), numpy)
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_position = (int(row), int(column))
                best_candidates = candidates
                if len(candidates) <= 1:
                    break

        if best_position is None:
            return True
        if not best_candidates:
            return False

        row, column = best_position
        for number in best_candidates:
            grid[row, column] = number
            if search():
                return True
            grid[row, column] = 0
        return False

    if search():
        return type(board)(grid.tolist())
    return None


def numpy_count_solutions(
    board: Any, numpy: ModuleType, limit: int = 2
) -> int:
    """Count solutions up to ``limit`` using NumPy candidate operations."""
    if limit <= 0 or not numpy_is_valid(board, numpy):
        return 0

    grid = numpy.array(board.values, dtype=int, copy=True)

    def search(remaining: int) -> int:
        if remaining <= 0:
            return 0

        best_position = None
        best_candidates = None
        for row, column in numpy.argwhere(grid == 0):
            candidates = _numpy_candidates(grid, int(row), int(column), numpy)
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_position = (int(row), int(column))
                best_candidates = candidates
                if len(candidates) <= 1:
                    break

        if best_position is None:
            return 1
        if not best_candidates:
            return 0

        row, column = best_position
        solution_count = 0
        for number in best_candidates:
            grid[row, column] = number
            solution_count += search(remaining - solution_count)
            grid[row, column] = 0
            if solution_count >= remaining:
                break
        return solution_count

    return search(limit)


def _median_microseconds_per_call(
    operation: Callable[[], object], repeats: int, iterations: int
) -> float:
    """Return the median per-call time measured over repeated batches."""
    operation()
    durations = []
    for _ in range(repeats):
        start = time.perf_counter_ns()
        for _ in range(iterations):
            operation()
        durations.append((time.perf_counter_ns() - start) / iterations / 1_000)
    return statistics.median(durations)


def _preserves_clues(puzzle: list[list[int]], solution: Any) -> bool:
    """Return whether a solved board retains every nonempty given value."""
    return all(
        value == 0 or solution.values[row][column] == value
        for row, values in enumerate(puzzle)
        for column, value in enumerate(values)
    )


def _assert_solved(
    name: str,
    puzzle: list[list[int]],
    solution: Any,
    validator: Callable[[Any], bool],
) -> None:
    """Reject missing, incomplete, invalid, or clue-changing solver results."""
    assert solution is not None, f"{name}: solver returned no solution"
    assert validator(solution), f"{name}: solver returned an invalid board"
    assert all(0 not in row for row in solution.values), (
        f"{name}: solver returned an incomplete board"
    )
    assert _preserves_clues(puzzle, solution), (
        f"{name}: solver changed a given value"
    )


def run_benchmarks(
    seed: int,
    repeats: int,
    search_iterations: int,
    validator_iterations: int,
    numpy: ModuleType | None,
) -> None:
    """Load the baseline and compare solving/counting/validation methods."""
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if branch != "project-revision":
        raise RuntimeError(
            "Run this benchmark from the project-revision branch; "
            f"the current branch is {branch or '(detached HEAD)'}."
        )

    current_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    baseline_commit = subprocess.run(
        ["git", "rev-parse", BASELINE_COMMIT],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    dirty_tree = bool(
        subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )
    puzzles = list(PUZZLES.items())
    random.Random(seed).shuffle(puzzles)

    print(f"Python: {platform.python_version()} ({platform.platform()})")
    print(f"Current code: project-revision @ {current_commit}")
    print(f"Baseline code: main @ {baseline_commit}")
    print(
        f"Puzzle-order seed: {seed}; repeats: {repeats}; "
        f"search iterations/batch: {search_iterations}; "
        f"validator iterations/batch: {validator_iterations}"
    )
    if dirty_tree:
        print(
            "WARNING: working tree has uncommitted changes; current-code "
            "results include the working tree."
        )
    if numpy is not None:
        print(f"NumPy: {numpy.__version__}")
    print("The 35- and 25-clue boards were generated sequentially")
    print("with random.seed(42), then stored here as fixed puzzle data.")
    print("\nPuzzles (0 means empty):")
    for name, values in puzzles:
        clues = sum(value != 0 for row in values for value in row)
        print(f"\n{name} ({clues} clues)")
        print("\n".join(" ".join(map(str, row)) for row in values))

    invalid_values = [row.copy() for row in PUZZLES["classic-30-clue"]]
    invalid_values[0][2] = 5
    validation_puzzles = {
        **dict(puzzles),
        "duplicate-invalid": invalid_values,
    }
    expected_solution_counts = {
        "classic-30-clue": 1,
        "seed-42-35-clue": 1,
        "seed-42-25-clue": 1,
        "multiple-solution-21-clue": 2,
        "sparse-multiple-solution-7-clue": 2,
    }

    with _load_baseline_package(REPOSITORY_ROOT) as baseline:
        baseline_solver = import_module("sudoku_toolkit_baseline.solver")
        baseline_validator = import_module("sudoku_toolkit_baseline.validator")

        print("\nSearch timings (median milliseconds per call):")
        print(
            "Puzzle | operation | baseline ms | current ms | NumPy ms "
            "| baseline/current | current/NumPy"
        )
        for name, values in puzzles:
            current_board = CurrentBoard(values)
            baseline_board = baseline.Board(values)
            numpy_solve_call = (
                (lambda: numpy_solve(current_board, numpy))
                if numpy is not None
                else None
            )
            numpy_count_call = (
                (
                    lambda: numpy_count_solutions(
                        current_board, numpy, limit=2
                    )
                )
                if numpy is not None
                else None
            )
            operations: tuple[
                tuple[
                    str,
                    Callable[[], object],
                    Callable[[], object],
                    Callable[[], object] | None,
                ],
                ...,
            ] = (
                (
                    "solve",
                    lambda: baseline_solver.solve(baseline_board),
                    lambda: current_solve(current_board),
                    numpy_solve_call,
                ),
                (
                    "count(limit=2)",
                    lambda: baseline_solver.count_solutions(
                        baseline_board, limit=2
                    ),
                    lambda: current_count_solutions(current_board, limit=2),
                    numpy_count_call,
                ),
            )
            for label, baseline_call, current_call, numpy_call in operations:
                baseline_result = baseline_call()
                current_result = current_call()
                if label == "solve":
                    _assert_solved(
                        name,
                        values,
                        baseline_result,
                        baseline_validator.is_valid,
                    )
                    _assert_solved(name, values, current_result, current_is_valid)
                    if numpy_call is not None:
                        numpy_result = numpy_call()
                        _assert_solved(
                            name, values, numpy_result, current_is_valid
                        )
                else:
                    expected_count = expected_solution_counts[name]
                    assert baseline_result == expected_count, (
                        f"{name}: baseline counted {baseline_result}, "
                        f"expected {expected_count}"
                    )
                    assert current_result == expected_count, (
                        f"{name}: current counted {current_result}, "
                        f"expected {expected_count}"
                    )
                    if numpy_call is not None:
                        numpy_result = numpy_call()
                        assert numpy_result == expected_count, (
                            f"{name}: NumPy counted {numpy_result}, "
                            f"expected {expected_count}"
                        )

                baseline_ms = _median_microseconds_per_call(
                    baseline_call, repeats, search_iterations
                ) / 1_000
                current_ms = _median_microseconds_per_call(
                    current_call, repeats, search_iterations
                ) / 1_000
                numpy_ms = (
                    _median_microseconds_per_call(
                        numpy_call, repeats, search_iterations
                    ) / 1_000
                    if numpy_call is not None
                    else None
                )
                numpy_text = f"{numpy_ms:.3f}" if numpy_ms is not None else "not run"
                current_numpy = (
                    f"{current_ms / numpy_ms:.2f}x"
                    if numpy_ms
                    else "not run"
                )
                print(
                    f"{name:32} {label:15} {baseline_ms:11.3f} "
                    f"{current_ms:10.3f} {numpy_text:>8} "
                    f"{baseline_ms / current_ms:16.2f}x "
                    f"{current_numpy:>14}"
                )

        print(
            f"\nValidator timings (median microseconds/call; "
            f"{validator_iterations} calls per batch):"
        )
        print(
            "Puzzle | baseline us | current us | NumPy us "
            "| baseline/current | current/NumPy"
        )
        for name, values in validation_puzzles.items():
            current_board = CurrentBoard(values)
            baseline_board = baseline.Board(values)
            calls: list[tuple[str, Callable[[], bool]]] = [
                (
                    "baseline",
                    lambda: baseline_validator.is_valid(baseline_board),
                ),
                ("current", lambda: current_is_valid(current_board)),
            ]
            if numpy is not None:
                calls.append(
                    ("NumPy", lambda: numpy_is_valid(current_board, numpy))
                )

            expected = calls[0][1]()
            for label, call in calls[1:]:
                assert call() == expected, (
                    f"{name}: {label} validator disagrees with baseline"
                )
            timings = [
                _median_microseconds_per_call(
                    call, repeats, validator_iterations
                )
                for _, call in calls
            ]
            numpy_us = timings[2] if numpy is not None else None
            numpy_text = f"{numpy_us:8.3f}" if numpy_us is not None else "not run"
            current_numpy = (
                f"{timings[1] / numpy_us:14.2f}x"
                if numpy_us
                else "not run"
            )
            print(
                f"{name:32} {timings[0]:11.3f} {timings[1]:10.3f} "
                f"{numpy_text:>8} {timings[0] / timings[1]:16.2f}x "
                f"{current_numpy:>14}"
            )


def main() -> None:
    """Parse benchmark settings and run the measurements."""
    try:
        numpy = import_module("numpy")
    except ImportError:
        numpy = None

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--search-iterations", type=int, default=5)
    parser.add_argument("--validator-iterations", type=int, default=100)
    args = parser.parse_args()
    if (
        args.repeats < 1
        or args.search_iterations < 1
        or args.validator_iterations < 1
    ):
        parser.error("repeats and iteration counts must be positive")
    run_benchmarks(
        args.seed,
        args.repeats,
        args.search_iterations,
        args.validator_iterations,
        numpy,
    )


if __name__ == "__main__":
    main()
