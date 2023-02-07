import sys

# A* param order -> board_file_name.csv heuristic tile_weight?
# Params stored in sys.argv

from initialization import Initialization
from new_board import Board

BOARD_1 = "./documentation/test_boards/board1.csv"
BOARD_2 = "./documentation/test_boards/board2.csv"
BOARD_3 = "./documentation/test_boards/board3.csv"

# Create a new N-Puzzle
puzzle = Initialization(BOARD_3)
# Get the two possible goal states
zeroes_in_front_goal = puzzle.front_goal
zeroes_in_back_goal = puzzle.back_goal

# Make the starting board
parent = Board(puzzle.board_array_2D, zeroes_in_back_goal)

def search_tree(start: Board):
    # Begin search
    stack = [start]
    visited = []
    current_board: Board

    while stack:
        current_board = stack.pop()
        # Find the parent's children
        Board.populate_children(parent)
        print(current_board.board_array)
        print(current_board.move)

        if current_board.h_val == 0: # is goal state
            # Print moves
            moves = []
            while current_board.parent is not None:
                moves.append(current_board.move)
                current_board = current_board.parent
            for move in moves:
                print(move)
        if current_board.children:
            for child in current_board.children:
                if child not in visited:
                    stack.append(child)
                    visited.append(child)

    print("No solution found")

search_tree(parent)
