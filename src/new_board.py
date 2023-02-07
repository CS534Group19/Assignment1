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
    - effort: the node depth of the state used in A* heuristic calculations
    - move: String representation of the move the board made
    - zero_neighbors: a list of tuples holding the (x,y) coordinate of a 0 and the (x,y) coordinate of the neighbor as a tuple (0_x, 0_y, neighbor_x, neighbor_y)
    - h_val: the heuristic value of the board
    """
    def __init__(self, board_array: list[list[int]], goal: list[list[int]]):
        self.board_array = board_array
        self.goal = goal
        self.children: list[Board] = []
        self.parent = None
        self.effort = 0
        self.node_depth = 0
        self.move = ""
        # List of possible moves
        self.zero_neighbors = self.set_zero_neighbors()
        self.h_val: int = self.getHVal()

    def __str__(self):
        return str(self.board_array)

    # Neighbor tuple form (0_x, 0_y, neighbor_x, neighbor_y)
    def set_zero_neighbors(self) -> list[tuple]:
        zeroes = []
        for x in range(len(self.board_array)):
            for y in range(len(self.board_array)):
                if self.board_array[x][y] == 0:
                    # Up
                    delta_y = y+1
                    if delta_y >= 0 and delta_y < len(self.board_array):
                        zeroes.append((x, y, x, delta_y))
                    # Down
                    delta_y = y-1
                    if delta_y >= 0 and delta_y < len(self.board_array):
                        zeroes.append((x, y, x, delta_y))
                    # Left
                    delta_x = x-1
                    if delta_x >= 0 and delta_x < len(self.board_array):
                        zeroes.append((x, y, delta_x, y))
                    # Right
                    delta_x = x+1
                    if delta_x >= 0 and delta_x < len(self.board_array):
                        zeroes.append((x, y, delta_x, y))
        return zeroes

    @classmethod
    def populate_children(cls, parent_board):
        """Static method to populate a parent node with children
        Parameters
        - parent_board: Board object
        """
        for move in parent_board.zero_neighbors:
            child = copy.deepcopy(parent_board)
            child.parent_board = parent_board

            # Zero coordinates
            x_0 = move[0]
            y_0 = move[1]
            # Neighbor coordinates
            x_1 = move[2]
            y_1 = move[3]

            # Compute string representation of the board move
            if (y_1-y_0) == 1:  #Means there was dy up
                child.move = f"Moved {parent_board.board_array[x_1][y_1]} up ;)"
            elif (y_1-y_0) == -1:  #Means there was dy down
                child.move = f"Moved {parent_board.board_array[x_1][y_1]} down ;)"    
            elif (x_1-x_0) == -1:  #Means there was dx left
                child.move = f"Moved {parent_board.board_array[x_1][y_1]} left ;)"   
            else:
                child.move = f"Moved {parent_board.board_array[x_1][y_1]} right ;)"

            # Swap the zero and the value
            val = parent_board.board_array[x_1][y_1]
            child.board_array[x_0][y_0] = val
            child.board_array[x_1][y_1] = 0

            # Record traverse effort
            if (False):   # FIX LATER WITH "Weight param"
                child.effort = parent_board.effort + 1*val
            else:
                child.effort = parent_board.effort + 1

            # Record child node depth
            child.node_depth = parent_board.node_depth + 1

            # Update neighbors for new board
            child.set_zero_neighbors()

            child.h_val += child.node_depth

            parent_board.children.append(child)
        parent_board.children.sort(reverse=True, key=return_child_hval)

    def getHVal(self): # heuristic
        total: int = 0
        for i in range(1, len(self.board_array)**2):
            manhattan_distance = calculate_manhattan_dist_for_value(self.board_array, self.goal, i)
            if manhattan_distance != -1:
                total += manhattan_distance
        return total

    # Selects a parent's favorite child
    # def find_next_best_move_AStar(self):
    #     minimum: int = sys.maxsize
    #     favorite_child: Board = None
    #     for child in self.children:
    #         h_val: int = child.h_val
    #         if h_val + child.effort < minimum:
    #             minimum = h_val + child.effort
    #             favorite_child = child
    #     return (h_val, favorite_child)


def return_child_hval(child: Board) -> int:
    return child.h_val

def get_coords_for_val(board: list[list[int]], val: int) -> tuple:
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == val:
                return (x, y)
    return -1

def calculate_manhattan_dist_for_value(current_board: list[list[int]], goal_board: list[list[int]], val: int) -> int:
    # Find (x,y) coords for all current positions
    current_coords: tuple = get_coords_for_val(current_board, val)
    goal_coords: tuple = get_coords_for_val(goal_board, val)
    if current_coords == -1 or goal_coords == -1:
        return -1
    else:
        return abs(current_coords[0] - goal_coords[0]) + abs(current_coords[1] - goal_coords[1])
        