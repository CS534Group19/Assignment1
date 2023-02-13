# Author: Cutter Beck
# Updated: 2/10/2023

import time
from new_board import *
from initialization import Initialization

# # A* param order -> board_file_name.csv heuristic tile_weight?
# # Params stored in sys.argv array, sys.argv[0] is the name of the Python file being executed
# arg_board_csv = sys.argv[1]
# arg_heuristic = sys.argv[2]
# arg_weighted = sys.argv[3]

# # Create a new N-Puzzle
# puzzle = Initialization(arg_board_csv)
# # Get the two possible goal states
# zeroes_in_front_goal = puzzle.front_goal
# zeroes_in_back_goal = puzzle.back_goal

# # Make the starting board
# parent = Board(puzzle.board_array_2D, zeroes_in_front_goal, zeroes_in_back_goal, arg_weighted, arg_heuristic)

def modified_astar(start: Board):
    """Static method to run an A* search
    ### Parameters
    - start: the starting Board for the search

    ### Returns
    - nothing, but prints to the console
    """
    # Get all possible moves for the start state
    start.set_zero_neighbors()
    # Begin search
    current_board: Board
    open = [start] # tracks children being searched
    open_boards = [start.board_array]
    closed: list[Board] = [] # tracks expanded nodes
    goal: bool = False
    counter = 0

    while True:
        # PriorityQueue
        current_board = open.pop(0)
        counter += 1
        # print(counter)

        if current_board.board_array == current_board.goal: # at goal state
            moves = []
            cost = current_board.effort
            final_depth = current_board.node_depth
            # Collect moves from goal back up tree to start state
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

        # Assign greedy child to board children
        populate_children(current_board)
        for child in current_board.children:
            # Put all children on the priority queue as long as that child state has not already been placed on the queue
            if child.board_array not in [board.board_array for board in open]:
                open.append(child)
                open_boards.append(child.board_array)

        # Added expanded board to closed for counting later
        closed.append(current_board)
        # Prioritize the best children on the queue first
        open.sort(key = lambda child:child.f_val)

# # Track the time it takes the algorithm to complete
# start_time = time.perf_counter()
# modified_astar(parent)
# end_time = time.perf_counter()
# print(f"\nSearch took {end_time - start_time:0.4f} seconds")