import sys
import time

# TODO make command line interface
# A* param order -> board_file_name.csv heuristic tile_weight?
# Params stored in sys.argv

from initialization import Initialization
from new_board import *

# Boards for testing
BOARD_1 = "./documentation/test_boards/board1.csv"
BOARD_2 = "./documentation/test_boards/board2.csv"
BOARD_3 = "./documentation/test_boards/board3.csv" # easy 4 move
BOARD_4 = "./documentation/test_boards/board4.csv" # becomes hard 6 move, starts just alternating

# Whether the algorithm should put the zeroes at the end of the goal board or not
BACK = True

# Create a new N-Puzzle
puzzle = Initialization(BOARD_4)
# Get the two possible goal states
zeroes_in_front_goal = puzzle.front_goal
zeroes_in_back_goal = puzzle.back_goal

# Make the starting board
if BACK:
    parent = Board(puzzle.board_array_2D, zeroes_in_back_goal)
else:
    parent = Board(puzzle.board_array_2D, zeroes_in_front_goal)

def search_tree(start: Board):
    """Static method to run an A* search
    ### Parameters
    - start: the starting Board for the search

    ### Returns
    - nothing, but prints to the console
    """
    # Preliminary setup
    start.set_zero_neighbors()
    # Begin search
    current_board: Board
    open = [start] # tracks children being searched
    closed: list[Board] = [] # tracks expanded nodes
    goal: bool = False

    while not goal:
        # PriorityQueue
        current_board = open.pop(0)
        # print(current_board.effort)
        # print(current_board.f_val)
        # print("\n")
        # open.clear() # removes all worse children from the stack (Is this necessary? Currently doesn't operate properly without it)

        if current_board.board_array == current_board.goal: # at goal state
            goal = True
            moves = []
            cost = 0
            final_depth = current_board.node_depth
            while current_board.parent is not None:
                moves.append(current_board.move)
                cost += current_board.effort
                current_board = current_board.parent
            moves.reverse()
            for move in moves:
                print(move)

            print(f"\nNodes expanded: {len(closed)}")
            print(f"Moves required: {len(moves)}")
            print(f"Solution Cost: {cost}")
            print(f"Estimated branching factor {len(closed)**(1/final_depth):0.3f}")
            return

        # Assign all possible children to the current board
        populate_children(current_board)
        for child in current_board.children:
            if child.board_array not in [board.board_array for board in open]:
                open.append(child)

        # Added expanded board to closed for counting later
        closed.append(current_board)
        open.sort(key = lambda child:child.f_val)
        print([board.h_val for board in open])
        print([board.f_val for board in open])
        print("\n")
        
            
    print("No solution found")
    return

tic = time.perf_counter()
search_tree(parent)
toc = time.perf_counter()
print(f"\nSearch took {toc - tic:0.4f} seconds")
