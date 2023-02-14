# Author: Jeff Davis, Mike Alicea
# Adapted by Cutter Beck
# Updated: 2/13/2023

import sys
import time
from initialization import Initialization
from new_board import *

# Hill Climbing param order -> board_file_name.csv run_time
# Params stored in sys.argv array, sys.argv[0] is the name of the Python file being executed
arg_board_csv = str(sys.argv[1])
arg_run_time = float(sys.argv[2])

# Create a new N-Puzzle
puzzle = Initialization(arg_board_csv)
# Get the two possible goal states
zeroes_in_front_goal = puzzle.front_goal
zeroes_in_back_goal = puzzle.back_goal

# Make the starting board (makes use of default None for weighted and heuristic in the Board constructor)
parent = Board(puzzle.board_array_2D, zeroes_in_front_goal, zeroes_in_back_goal)

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
    goal = False

    start_time = time.perf_counter()
    current_time = time.perf_counter()
    while not goal:
        if (current_board.board_array == current_board.goal):
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
            goal = True
            break
        if (current_time - start_time < max_time):
            trial_time_total = 0.0
            trial_counter += 1

            trial_start_time = time.perf_counter()

            current_board = open.pop(0)

            # DELAYED HERE
            current_time = time.perf_counter()
        if populate_children(current_board, True, start_time, current_time, max_time):
                print("\nOut of time")
                print("Printing partial moves...")
                moves = []
                while current_board.parent is not None:
                    moves.append(current_board.move)
                    current_board = current_board.parent
                moves.reverse()
                for move in moves:
                    print(move)
                break

            current_board.children.sort(key = lambda child:child.h_val)
            open.append(current_board.children[0])
            nodes_expanded.append(current_board)

            trial_end_time = time.perf_counter()
            trial_time_total += trial_end_time - trial_start_time
            
            if trial_time_total <= trial_time: # new trial if trial time overdone
                print("Restarting from best node")
        else:
            # get the list of moves
            print("\nOut of time")
            print("Printing partial moves...")
            moves = []
            while current_board.parent is not None:
                moves.append(current_board.move)
                current_board = current_board.parent
            moves.reverse()
            for move in moves:
                print(move)
            break
        current_time = time.perf_counter()

# Time the total length of running hill climbing
start_time = time.perf_counter()
hillClimb(parent, arg_run_time, 15)
end_time = time.perf_counter()
print(f"\nSearch took {end_time - start_time:0.4f} seconds")
