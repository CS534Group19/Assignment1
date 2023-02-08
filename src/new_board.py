import copy
import sys

class Board():
    """Holds a given state of the game, assumes a square board
    ### Parameters:
    - board_array: 2D array holding the current values on the board
    - goal: 2D array holding the goal state of the board

    ### Attributes
    - children: 1D array holding child states -> Board objects
    - parent: the parent state of the board -> is a Board object
    - node_depth: the depth of the tree the current board is at
    - move: String representation of the move the board made
    - zero_neighbors: a list of tuples holding the (x,y) coordinate of a 0 and the (x,y) coordinate of the neighbor as a tuple (0_x, 0_y, neighbor_x, neighbor_y)
    - f_val: the heuristic value of the board
    """
    def __init__(self, board_array: list[list[int]], goal: list[list[int]]):
        self.board_array = board_array
        self.goal = goal
        self.children: list[Board] = []
        self.parent = None
        self.node_depth = 0
        self.move = ""
        # List of possible moves
        self.zero_neighbors = []
        self.f_val: int = 0
        self.effort = 0

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
                        zeroes.append((col, row, col, delta_y))
                    # Down
                    delta_y = row-1
                    if delta_y >= 0 and delta_y < len(self.board_array):
                        zeroes.append((col, row, col, delta_y))
                    # Left
                    delta_x = col-1
                    if delta_x >= 0 and delta_x < len(self.board_array):
                        zeroes.append((col, row, delta_x, row))
                    # Right
                    delta_x = col+1
                    if delta_x >= 0 and delta_x < len(self.board_array):
                        zeroes.append((col, row, delta_x, row))
        self.zero_neighbors = zeroes


def populate_children(parent_board: Board):
    """Static method to populate a parent node with children
    Parameters
    - parent_board: Board object
    """
    for move in parent_board.zero_neighbors:
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
        # child.f_val = getHVal(child) + child.effort
        child.f_val = getHVal(child) + child.effort
        # Tell the parent it has children
        parent_board.children.append(child)
    # Sort the children to make sure the best gets explore first
    # parent_board.children.sort(key = lambda child : child.f_val)
    print([child.f_val for child in parent_board.children])

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

def calculate_manhattan_dist_for_value(current_board: list[list[int]], goal_board: list[list[int]], val: int) -> int:
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
        return abs(current_coords[0] - goal_coords[0]) + abs(current_coords[1] - goal_coords[1])

def getHVal(board_obj: Board): # heuristic
    """Static method to find the total heuristic value of a given board
    ### Parameters
    - board_obj: a Board object to be fitted with a heuristic value

    ### Returns
    - total: the heuristic cost of the board
    """
    total: int = 0
    for i in range(1, len(board_obj.board_array)**2):
        manhattan_distance = calculate_manhattan_dist_for_value(board_obj.board_array, board_obj.goal, i)
        if manhattan_distance != -1:
            total += manhattan_distance + i
    return total