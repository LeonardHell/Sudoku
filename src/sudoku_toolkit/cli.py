import argparse

from .io import _create_board, load_txt, load_csv, load_board, save_board, save_csv, save_txt
from .board import Board
from .generator import generate_puzzle, generate_solution
from .solver import solve
from .validator import is_valid


def main():
    parser = argparse.ArgumentParser(
        description="Solve, validate, and generate Sudoku puzzles."
    )

    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a solved Sudoku."
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

    solve_parser = subparsers.add_parser(
        "solve",
        help="Solve a Sudoku puzzle."
    )

    solve_parser.add_argument(
        "filename",
        help="Path to the Sudoku file."
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
        print(board)

    elif args.command == "puzzle":
        if args.clues is not None:
            board = generate_puzzle(clues=args.clues)
        else:
            board = generate_puzzle(difficulty=args.difficulty)

        print(board)

    elif args.command == "solve":
        board = load_board(args.filename)
        solution = solve(board)

        if solution is None:
            print("The Sudoku has no solution.")
        else:
            print(solution)

    elif args.command == "validate":
        board = load_board(args.filename)

        if is_valid(board):
            print("The Sudoku is valid.")
        else:
            print("The Sudoku is invalid.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
