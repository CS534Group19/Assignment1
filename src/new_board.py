# Author: Cutter Beck
# Updated: 2/10/2023

import copy
import sys
import time

GREEDY_ITERS = 2

class Board():
    """Holds a given state of the game, assumes a square board
    ### Parameters:
    - board_array: 2D array holding the current values on the board
    - front_goal: 2D array holding the goal where 0s are in the top left
    - back_goal: 2D array holding the goal where 0s are in the bottom right
    - weighted: a boolean flag on whether the weighted or unweighted heuristic should be used
    - heuristic: a string flagging either sliding or greedy for the heurisitic to be used

    ### Attributes
    - goal: 2D array holding the chosen best goal state of the board
    - children: 1D array holding child states -> Board objects
    - parent: the parent state of the board -> is a Board object
    - node_depth: the depth of the tree the current board is at
    - move: String representation of the move the board made
    - zero_neighbors: a list of tuples holding the (x,y) coordinate of a 0 and the (x,y) coordinate of the neighbor as a tuple (0_x, 0_y, neighbor_x, neighbor_y)
    - f_val: the heuristic value of the board including board effort
    - h_val: the heuristic value of the board (either sliding or greedy)
    - effort: how much work was done for a board (summation of tile values moved)
    """
    def __init__(self, board_array: list[list[int]], front_goal: list[list[int]], back_goal: list[list[int]], weighted: str = None, heuristic: str = None):
        # Parameters
        self.board_array = board_array
        self.front_goal = front_goal
        self.back_goal = back_goal
        if weighted is None:
            self.weighted = None
        else:
            if weighted.lower() == "true":
                self.weighted = True
            else:
                self.weighted = False
        if heuristic is None:
            self.heuristic = None
        else:
            self.heuristic = heuristic
        # Attributes
        if self.heuristic == "sliding":
            self.goal = check_best_goal_state(self, self.front_goal, self.back_goal)
        else:
            self.goal = self.back_goal
        self.children: list[Board] = []
        self.parent = None
        self.node_depth = 0
        self.move = ""
        # List of possible moves
        self.zero_neighbors = []
        self.f_val: int = 0
        self.effort = 0
        if heuristic == "sliding":
            self.h_val = getHVal(self, self.goal)
        else:
            current = self
            effort_sum = 0
            children: Board = []
            for i in range(GREEDY_ITERS):
                children.append(produce_best_child(current))
                current = children[-1]
            for child in children:
                effort_sum += child.effort
            self.h_val = effort_sum

    def __str__(self):
        return str(self.board_array)

    # Neighbor tuple form (0_x, 0_y, neighbor_x, neighbor_y)
    def set_zero_neighbors(self) -> list[tuple]:
        zeroes = []
        for row in range(len(self.board_array)):
            for col in range(len(self.board_array)):
                if self.board_array[row][col] == 0:
                    # Up
                    delta_y = row+1
                    if delta_y >= 0 and delta_y < len(self.board_array):
                        if self.board_array[delta_y][col] != 0:
                            zeroes.append((col, row, col, delta_y))
                    # Down
                    delta_y = row-1
                    if delta_y >= 0 and delta_y < len(self.board_array):
                        if self.board_array[delta_y][col] != 0: 
                            zeroes.append((col, row, col, delta_y))
                    # Left
                    delta_x = col-1
                    if delta_x >= 0 and delta_x < len(self.board_array):
                        if self.board_array[row][delta_x] != 0:
                            zeroes.append((col, row, delta_x, row))
                    # Right
                    delta_x = col+1
                    if delta_x >= 0 and delta_x < len(self.board_array):
                        if self.board_array[row][delta_x] != 0:
                            zeroes.append((col, row, delta_x, row))
        self.zero_neighbors = zeroes


def populate_children(parent_board: Board, use_time: bool = False, program_start: float=0.0, function_start: float=0.0, max_time: float=0.0):
    """Static method to populate a parent node with children
    Parameters
    - parent_board: Board object
    """
    if function_start - program_start >= max_time and use_time:
        return True
    for move in parent_board.zero_neighbors:
        current_time = time.perf_counter()
        if current_time - program_start >= max_time and use_time:
            return True
        # Make new child
        # child = Board(parent_board.board_array, parent_board.goal)
        child = copy.deepcopy(parent_board)
        child.parent = parent_board
        child.node_depth = parent_board.node_depth + 1

        # Zero coordinates
        col_0 = move[0]
        row_0 = move[1]
        # Neighbor coordinates
        col_1 = move[2]
        row_1 = move[3]

        # Swap the zero and the value
        val = parent_board.board_array[row_1][col_1]
        child.board_array[row_0][col_0] = val
        child.board_array[row_1][col_1] = 0

        # Compute string representation of the board move
        if (row_1-row_0) == 1 and (col_1-col_0) == 0:
            child.move = f"Moved {parent_board.board_array[row_1][col_1]} up"
        elif (row_1-row_0) == -1 and (col_1-col_0) == 0:
            child.move = f"Moved {parent_board.board_array[row_1][col_1]} down"    
        elif (col_1-col_0) == 1 and (row_1-row_0) == 0:
            child.move = f"Moved {parent_board.board_array[row_1][col_1]} left"   
        elif (col_1-col_0) == -1 and (row_1-row_0) == 0:
            child.move = f"Moved {parent_board.board_array[row_1][col_1]} right"

        # Update neighbors for new board
        child.set_zero_neighbors()
        # Calculate the heuristic cost of the board
        child.effort = parent_board.effort + val
        if parent_board.heuristic == "sliding":
            child.h_val = getHVal(child, child.goal)
        elif parent_board.heuristic == "greedy":
            effort_sum = 0
            children: Board = []
            for i in range(GREEDY_ITERS):
                # print(child)
                children.append(produce_best_child(child))
                child = children[-1]
            for child in children:
                effort_sum += child.effort
            child.h_val = effort_sum
            children.clear()
        current_time = time.perf_counter()
        if current_time - program_start >= max_time and use_time:
            return True
        child.f_val = child.h_val + child.effort
        # Tell the parent it has children
        parent_board.children.append(child)

def get_coords_for_val(board: list[list[int]], val: int):
    """Static method to find the (x,y) coordinates of the provided value
    ### Parameters
    - board: a 2D array representing a board state
    - val: the value being searched for

    ### Returns
    Either an (x,y) tuple if the value is on the board or -1 if it wasn't found
    """
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == val:
                return (x, y)
    return -1

def calculate_manhattan_dist_for_value(current_board: list[list[int]], goal_board: list[list[int]], val: int, weighted: bool) -> int:
    """Static method to compute the Manhattan distance for a given value
    ### Parameters
    - current_board: the current state of the board
    - goal_board: the goal state for the computation
    - val: the value the calculation is based on

    ### Returns
    - The integer Manhattan distance for the value to its goal location or -1 if the value isn't on the board
    """
    # Find (x,y) coords for all current positions
    current_coords: tuple = get_coords_for_val(current_board, val)
    goal_coords: tuple = get_coords_for_val(goal_board, val)
    if current_coords == -1 or goal_coords == -1:
        return -1
    else:
        if weighted == True:
            return abs(current_coords[0] - goal_coords[0]) + abs(current_coords[1] - goal_coords[1]) * (val**2)
        else:
            return abs(current_coords[0] - goal_coords[0]) + abs(current_coords[1] - goal_coords[1])

def getHVal(board_obj: Board, goal: list[list[int]]) -> int: # sliding heuristic
    """Static method to find the total heuristic value of a given board
    ### Parameters
    - board_obj: a Board object to be fitted with a heuristic value

    ### Returns
    - total: the heuristic cost of the board
    """
    total: int = 0
    for i in range(1, len(board_obj.board_array)**2):
        manhattan_distance = calculate_manhattan_dist_for_value(board_obj.board_array, goal, i, board_obj.weighted)
        if manhattan_distance != -1:
            total += manhattan_distance
    return total

def check_best_goal_state(board_obj: Board, front: list[list[int]], back: list[list[int]]) -> list[list[int]]:
    """Static method to find which goal state is best for the board
    ### Parameters
    - board_obj: a Board object to be fitted with a heuristic value
    - front: 2D array holding the goal where 0s are in the top left
    - back: 2D array holding the goal where 0s are in the bottom right
    """
    if board_obj.heuristic == "sliding":
        front_h_val = getHVal(board_obj, front)
        # print(f"Front h val: {front_h_val}")
        back_h_val = getHVal(board_obj, back)
        # print(f"Back h val: {back_h_val}")

    if back_h_val < front_h_val:
        return back
    elif front_h_val < back_h_val:
        return front
    else:
        return back

def produce_best_child(start: Board) -> Board:
    start.set_zero_neighbors()
    min_difference = sys.maxsize
    min_diff_index = 0
    for i in range(len(start.zero_neighbors)):
        # Zero coordinates
        x_0 = start.zero_neighbors[i][0]
        y_0 = start.zero_neighbors[i][1]
        # Neighbor coordinates
        x_1 = start.zero_neighbors[i][2]
        y_1 = start.zero_neighbors[i][3]

        manhattan = abs(x_1 - x_0) + abs(y_1 - y_0)
        if manhattan < min_difference:
            min_difference = manhattan
            min_diff_index = i
    child = copy.deepcopy(start)
    child.parent = start
    child.node_depth = start.node_depth + 1

    # Zero coordinates
    col_0 = start.zero_neighbors[min_diff_index][0]
    row_0 = start.zero_neighbors[min_diff_index][1]
    # Neighbor coordinates
    col_1 = start.zero_neighbors[min_diff_index][2]
    row_1 = start.zero_neighbors[min_diff_index][3]

    # Swap the zero and the value
    val = start.board_array[row_1][col_1]
    child.board_array[row_0][col_0] = val
    child.board_array[row_1][col_1] = 0

    # Compute string representation of the board move
    if (row_1-row_0) == 1 and (col_1-col_0) == 0:
        child.move = f"Moved {start.board_array[row_1][col_1]} up"
    elif (row_1-row_0) == -1 and (col_1-col_0) == 0:
        child.move = f"Moved {start.board_array[row_1][col_1]} down"    
    elif (col_1-col_0) == 1 and (row_1-row_0) == 0:
        child.move = f"Moved {start.board_array[row_1][col_1]} left"   
    elif (col_1-col_0) == -1 and (row_1-row_0) == 0:
        child.move = f"Moved {start.board_array[row_1][col_1]} right"

    # Update neighbors for new board
    child.set_zero_neighbors()
    # Calculate the heuristic cost of the board
    child.effort = (start.effort + val)
    # child.h_val = child.effort

    # child.f_val = child.h_val + child.effort
    # start.children.append(child)
    return child