import sys

# A* param order -> board_file_name.csv heuristic tile_weight?
# Params stored in sys.argv

from initialization import Initialization
from new_board import Board

BOARD_1 = "./documentation/test_boards/board1.csv"
BOARD_2 = "./documentation/test_boards/board2.csv"

# Create a new N-Puzzle
puzzle = Initialization(BOARD_1)
# Get the two possible goal states
zeroes_in_front_goal = puzzle.front_goal
zeroes_in_back_goal = puzzle.back_goal

# Make the starting board
parent = Board(puzzle.board_array_2D)
# print(parent.zero_neighbors) # should be empty

# Find all zeroes on the board and set their neighbors
parent.set_zero_neighbors()
# print(parent.zero_neighbors) # should no longer be empty


# Begin search
queueFIFO = []
# Find children
Board.populate_children(parent)

# Enque parent
queueFIFO.append(parent)

# Begin recursion
# Find best child
parent.find_next_best_move_AStar()
# Deque parent -> Put onto new stack
# Enque best child(becomes parent) children
# Repeat

# Add parent to other queue for backtracking

# while parent != None, backtrack from goal once goal is found


# print([str(child) for child in parent.children]) # expose the parent's children

