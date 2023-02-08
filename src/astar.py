import sys
import time

# TODO make command line interface
# A* param order -> board_file_name.csv heuristic tile_weight?
# Params stored in sys.argv

from initialization import Initialization
from new_board import *

# Boards for testing
# Professor Beck's boards
BOARD_1 = "./documentation/test_boards/board1.csv" # not solvable according to https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
BOARD_2 = "./documentation/test_boards/board2.csv" # solvable according to https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/

# Cutter Beck's boards
BOARD_3 = "./documentation/test_boards/board3.csv" # ~0.2 seconds, 4 moves, 8 nodes, 18 cost, branching factor 1.7
BOARD_4 = "./documentation/test_boards/board4.csv" # ~22 seconds, 6 moves, 52 nodes, 26 cost, branching factor 1.9
BOARD_5 = "./documentation/test_boards/board5.csv" # ~418.7 seconds, or ~7 min, 5 moves, 25 nodes, 60 cost, branching factor 1.9
BOARD_6 = "./documentation/test_boards/board6.csv" # ~10.5 seconds, 3 moves, 14 nodes, 18 cost, branching factor 2.4
BOARD_7 = "./documentation/test_boards/board7.csv" # ~3.8 seconds, 4 moves, 14 nodes, 46 cost, branching factor 1.9


# Create a new N-Puzzle
puzzle = Initialization(BOARD_3)
# Get the two possible goal states
zeroes_in_front_goal = puzzle.front_goal
zeroes_in_back_goal = puzzle.back_goal

# Make the starting board
parent = Board(puzzle.board_array_2D, zeroes_in_back_goal)

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
    counter = 0

    while not goal:
        # PriorityQueue
        current_board = open.pop(0)
        # print([board.h_val for board in open])
        # print([board.f_val for board in open])
        counter += 1
        print(counter)
        # print(current_board.effort)
        # print(current_board.f_val)
        # print("\n")
        # open.clear() # removes all worse children from the stack (Is this necessary? Currently doesn't operate properly without it)

        if current_board.board_array == current_board.goal: # at goal state
            goal = True
            moves = []
            cost = current_board.effort
            final_depth = current_board.node_depth
            while current_board.parent is not None:
                moves.append(current_board.move)
                current_board = current_board.parent
            moves.reverse()
            for move in moves:
                print(move)

            print(f"\nNodes expanded: {len(closed)}")
            print(f"Moves required: {len(moves)}")
            print(f"Solution Cost: {cost}")
            if final_depth != 0:
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
        
            
    print("No solution found")
    return

tic = time.perf_counter()
search_tree(parent)
toc = time.perf_counter()
print(f"\nSearch took {toc - tic:0.4f} seconds")
