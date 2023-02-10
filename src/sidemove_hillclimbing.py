import sys
import time
from initialization import Initialization
from new_board import *

# Hill Climbing param order -> board_file_name.csv run_time
# Params stored in sys.argv array, sys.argv[0] is the name of the Python file being executed
# arg_board_csv = str(sys.argv[1])
# arg_run_time = float(sys.argv[2]) # in seconds

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

arg_board_csv = BOARD_3
arg_run_time = 90 # in seconds

# Create a new N-Puzzle
puzzle = Initialization(arg_board_csv)
# Get the two possible goal states
zeroes_in_front_goal = puzzle.front_goal
zeroes_in_back_goal = puzzle.back_goal

# Make the starting board (makes use of default None for weighted and heuristic in the Board constructor)
parent = Board(puzzle.board_array_2D, zeroes_in_front_goal, zeroes_in_back_goal)

# TODO Search performs better weighted
def hillClimb(start: Board, max_time: float, repeats: int):
    """Static method to run hill climbing
    ### Parameters
    - start: the starting Board for the search

    ### Returns
    - nothing, but prints to the console
    """
    # Get all possible moves for the start state
    start.set_zero_neighbors()
    # Begin search
    current_board: Board = start
    open = [start] # tracks children being searched
    nodes_expanded = []

    trial_time = max_time / repeats

    trial_counter = 0
    trial_time_total = 0.0

    # TODO make sure code breaks at time limit
    start_time = time.perf_counter()
    while True:
        current_time = time.perf_counter()
        if (current_board.board_array ==  current_board.goal):
            print("\nReached goal state")
            cost = current_board.effort
            final_depth = current_board.node_depth
            moves = []
            while current_board.parent is not None:
                moves.append(current_board.move)
                current_board = current_board.parent
            moves.reverse()
            for move in moves:
                print(move)

            print(f"\nNodes expanded: {len(nodes_expanded)}")
            print(f"Moves required: {len(moves)}")
            print(f"Solution Cost: {cost}")
            if final_depth != 0:
                print(f"Estimated branching factor {len(nodes_expanded)**(1/final_depth):0.3f}")
        if (current_time - start_time < max_time): # haven't overdone the time limit
            trial_start_time = time.perf_counter()
            trial_counter += 1

            current_board = open.pop(0)
            populate_children(current_board)

            for child in current_board.children:
                if child.board_array not in [board.board_array for board in open]:
                    open.append(child)
            open.sort(reverse = True, key = lambda child:child.h_val)

            nodes_expanded.append(current_board)

            trial_end_time = time.perf_counter()
            trial_time_total += trial_end_time - trial_start_time
            if (trial_time_total > trial_time): # new trial if trial time overdone
                print("Restarting from next best node")
                trial_time_total = 0.0
        else:
            # get the list of moves
            print("\nOut of time")
            cost = current_board.effort
            final_depth = current_board.node_depth
            moves = []
            while current_board.parent is not None:
                moves.append(current_board.move)
                current_board = current_board.parent
            moves.reverse()
            for move in moves:
                print(move)

            print(f"\nNodes expanded: {len(nodes_expanded)}")
            print(f"Moves required: {len(moves)}")
            print(f"Solution Cost: {cost}")
            if final_depth != 0:
                print(f"Estimated branching factor {len(nodes_expanded)**(1/final_depth):0.3f}")
            break

# Time the total length of running hill climbing
start_time = time.perf_counter()
hillClimb(parent, arg_run_time, 15)
end_time = time.perf_counter()
print(f"\nSearch took {end_time - start_time:0.4f} seconds")
