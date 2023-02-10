# Author: Cutter Beck
# Updated: 2/5/2023

import csv
import copy

class Initialization():
    """Black box to wrap all CSV handling and start and goal states
    ### Attributes
    - board_file: CSV file in the form of an N-Puzzle
    - board_array_2D: a 2D array created from the CSV file
    - side_length: one side dimension of the board
    - board_array_1D: a 1D array representation of the CSV-passed board
    - sorted_board_array_1D: the sorted 1D array representation of the CSV file
    - front_goal: 2D array, goal state with all zeroes in the top left
    - back_goal: 2D array, goal state with all zeroes in the bottom right
    """
    def __init__(self, board_file):
        self.board_file = board_file
        self.board_array_2D = self.get_start_state()
        self.side_length = len(self.board_array_2D)
        self.board_array_1D = self.twoD_to_oneD_board()
        self.sorted_board_array_1D = sorted(self.board_array_1D)
        self.front_goal = self.find_goal_state_front()
        self.back_goal = self.find_goal_state_end()

    def __str__(self):
        return str(self.board_array_2D)

    def get_start_state(self):
        """Converts the input from CSV to a 2D array
        """
        board_array = []
        with open(self.board_file, newline='', encoding='utf-8-sig') as board:
            reader = csv.reader(board, delimiter=",")
            for row in reader:
                temp_row = []
                for item in row:
                    if item == "B":
                        temp_row.append(0)
                    else:
                        temp_row.append(int(item))
                board_array.append(temp_row)
        return board_array

    def twoD_to_oneD_board(self):
        """Converts a 2D board into a 1D array representation
        """
        board = []
        for row in self.board_array_2D:
            for tile in row:
                board.append(tile)
        return board

    def make_2D(self, sorted_1D: list[int]):
        """
        ### Parameters
        - sorted_1D: a sorted 1D representation of a board

        ### Returns
        - 2D array of the sorted board
        """
        goal_1D = sorted_1D
        goal_2D = []
        index = 0
        for i in range(self.side_length):
            temp_row = []
            for j in range(self.side_length):
                temp_row.append(goal_1D[index])
                index += 1
            goal_2D.append(temp_row)
        return goal_2D

    def find_goal_state_front(self):
        """Returns a 2D array created from the sorted 1D array with all zeroes in the top left
        """
        return self.make_2D(self.sorted_board_array_1D)

    def find_goal_state_end(self):
        """Returns a 2D array created from a re-arranged sorted 1D array with all zeros in the bottom right
        """
        sorted_board = copy.deepcopy(self.sorted_board_array_1D)
        end_zeroes = 0
        for i in range(len(sorted_board)):
            if sorted_board[i] == 0:
                end_zeroes = i
        zero_list = sorted_board[0 : end_zeroes + 1]
        sorted_board = sorted_board[end_zeroes + 1:] + zero_list
        return self.make_2D(sorted_board)