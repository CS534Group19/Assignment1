import copy
import Integer

class Board():
    """Holds a given state of the game, assumes a square board
    ### Parameters:
    - board_array: 2D array holding the current values on the board
    - children: 1D array holding child states -> Board objects
    - parent: the parent state of the board -> is a Board object
    - effort: the node depth of the state used in A* heuristic calculations
    - move: String representation of the move the board made
    - zero_neighbors: a list of tuples holding the (x,y) coordinate of a 0 and the (x,y) coordinate of the neighbor as a tuple (0_x, 0_y, neighbor_x, neighbor_y)
    """
    def __init__(self, board_array):
        self.board_array = board_array
        self.children = []
        self.parent = None
        self.effort = 0
        self.node_depth = 0
        self.move = ""
        # List of possible moves
        self.zero_neighbors = []

    def __str__(self):
        return str(self.board_array)

    # Neighbor tuple form (0_x, 0_y, neighbor_x, neighbor_y)
    def set_zero_neighbors(self):
        zeroes = []
        for x in range(len(self.board_array)):
            for y in range(len(self.board_array)):
                if self.board_array[x][y] == 0:
                    # Up
                    deltaY = y+1
                    if deltaY >= 0 and deltaY < len(self.board_array):
                        zeroes.append((x, y, x, deltaY))
                    # Down
                    deltaY = y-1
                    if deltaY >= 0 and deltaY < len(self.board_array):
                        zeroes.append((x, y, x, deltaY))
                    # Left
                    deltaX = x-1
                    if deltaX >= 0 and deltaX < len(self.board_array):
                        zeroes.append((x, y, deltaX, y))
                    # Right
                    deltaX = x+1
                    if deltaX >= 0 and deltaX < len(self.board_array):
                        zeroes.append((x, y, deltaX, y))
        self.zero_neighbors = zeroes

    def populate_children(parent_board):
        """Static method to populate a parent node with children
        Parameters
        - parent_board: Board object
        """
        for move in parent_board.zero_neighbors:
            child = copy.deepcopy(parent_board)
            child.parent_board = parent_board

            # Zero coordinates
            x0 = move[0]
            y0 = move[1]
            # Neighbor coordinates
            x1 = move[2]
            y1 = move[3]

            # Compute string representation of the board move
            if (y1-y0) == 1:  #Means there was dy up
                child.move = f"Moved {parent_board.board_array[x1][y1]} up ;)"
            elif (y1-y0) == -1:  #Means there was dy down
                child.move = f"Moved {parent_board.board_array[x1][y1]} down ;)"    
            elif (x1-x0) == -1:  #Means there was dx left
                child.move = f"Moved {parent_board.board_array[x1][y1]} left ;)"   
            else:
                child.move = f"Moved {parent_board.board_array[x1][y1]} right ;)"

            # Swap the zero and the value
            val = parent_board.board_array[x1][y1]
            child.board_array[x0][y0] = val
            child.board_array[x1][y1] = 0   

            # Record traverse effort 
            if (False):   # FIX LATER WITH "Weight param"
                child.effort = parent_board.effort + 1*val
            else:
                child.effort = parent_board.effort + 1

            # Record child node depth
            child.node_depth = parent_board.node_depth + 1

            # Update neighbors for new board
            child.set_zero_neighbors()

            parent_board.children.append(child)

    # TODO Spencer will write
    def getHVal_Astar(board):
        sum = 0
        for row in board.board_array:
            for val in row:
                sum += 9000 # Will do maths
        return sum

    # Selects a parent's favorite child
    def find_next_best_move_AStar(self):
        min = Integer.MAX_VALUE
        favorite_Child = None
        for child in self.children:
            h_val = Board.getHVal_Astar(child)
            if (h_val + child.effort < min):
                min = h_val + child.effort
                favorite_Child = child
        return (h_val, favorite_Child)







