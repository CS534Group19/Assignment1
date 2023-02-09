import sys
import time

# Hill Climbing param order -> board_file_name.csv run_time
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

# print(puzzle)

def hillClimb(start: Board, timer):
    """Static method to run hill climbing
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
    bestH = 999 # currently best found h_val
    bestMoves = [] # list of the best moves to be printed

    repeatNum = 150 # number of repeats we want to run
    trialTime = timer/repeatNum
    repeatCounter = 0

    # while not over max repeats
    while ((repeatCounter < repeatNum) and open):
        runtime = 0
        found = False
        current_board = open.pop(0)
        repeatCounter += 1

        # while time hasnt run out and end not found
        while (runtime < trialTime and (not found)):
            tic = time.perf_counter()

            #if finds a solution or local min
            if (current_board.h_val == 0):
                found = True
                # check if the found h_val is better than the current best
                if current_board.h_val <= bestH:
                    # get the list of moves
                    moves = []
                    while current_board.parent is not None:
                        moves.append(current_board.move)
                        current_board = current_board.parent
                    moves.reverse()
                    bestMoves = moves

            # Assign all possible children to the current board
            populate_children(current_board)
            sortedList = current_board.children
            sortedList.sort(reverse = True, key=getHVal)
            if (sortedList[0].h_val <= current_board.h_val):
                open.append(sortedList[0])
                
            else:
                found = True
                    # check if the found h_val is better than the current best
                if current_board.h_val < bestH:
                    # get the list of moves
                    moves = []
                    while current_board.parent is not None:
                        moves.append(current_board.move)
                        current_board = current_board.parent
                    moves.reverse()
                    bestMoves = moves        



            toc = time.perf_counter()
            runtime += toc - tic
    for move in bestMoves:
        print(move)
    
hillClimb(parent, 1200)
