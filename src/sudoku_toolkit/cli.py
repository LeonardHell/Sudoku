import argparse

from .io import load_board, save_board
from .generator import generate_puzzle, generate_solution
from .solver import solve
from .validator import is_valid


def _load_board(filename, parser):
    """Load a Sudoku board and report errors through argparse."""

    try:
        return load_board(filename)
    except ValueError as error:
        parser.error(str(error))


def _save_board(board, filename, parser):
    """Save a Sudoku board and report errors through argparse."""

    try:
        save_board(board, filename)
    except ValueError as error:
        parser.error(str(error))


def main():
    parser = argparse.ArgumentParser(
        description="Solve, validate, and generate Sudoku puzzles."
    )

    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a solved Sudoku."
    )

    generate_parser.add_argument(
        "--output",
        help="Save the Sudoku to a file."
    )

    puzzle_parser = subparsers.add_parser(
        "puzzle",
        help="Generate a Sudoku puzzle."
    )

    puzzle_parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        help="Difficulty level."
    )

    puzzle_parser.add_argument(
        "--clues",
        type=int,
        help="Number of clues to keep."
    )

    puzzle_parser.add_argument(
        "--output",
        help="Save the Sudoku to a file."
    )

    solve_parser = subparsers.add_parser(
        "solve",
        help="Solve a Sudoku puzzle."
    )

    solve_parser.add_argument(
        "filename",
        help="Path to the Sudoku file."
    )

    solve_parser.add_argument(
        "--output",
        help="Save the solution to a file."
    )

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a Sudoku puzzle."
    )

    validate_parser.add_argument(
        "filename",
        help="Path to the Sudoku file."
    )

    args = parser.parse_args()

    if args.command == "generate":
        board = generate_solution()

        if args.output:
            _save_board(board, args.output, parser)
        else:
            print(board)

    elif args.command == "puzzle":
        try:
            if args.clues is not None:
                board = generate_puzzle(clues=args.clues)
            else:
                board = generate_puzzle(
                    difficulty=args.difficulty
                )
        except ValueError as error:
            parser.error(str(error))

        if args.output:
            _save_board(board, args.output, parser)
        else:
            print(board)

    elif args.command == "solve":
        board = _load_board(args.filename, parser)
        solution = solve(board)

        if solution is None:
            print("The Sudoku has no solution.")
        elif args.output:
            _save_board(solution, args.output, parser)
        else:
            print(solution)

    elif args.command == "validate":
        board = _load_board(args.filename, parser)

        if is_valid(board):
            print("The Sudoku is valid.")
        else:
            print("The Sudoku is invalid.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
