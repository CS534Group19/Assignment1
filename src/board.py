# DEPRECATED

# Author: Cutter Beck
# Updated: 2/3/2023

import csv

class NPuzzle():
    def __init__(self, board_file):
        self.board_file = board_file
        self.state = Board(self.create_board_array())

    def create_board_array(self):
        board_array = []
        with open(self.board_file, newline='', encoding='utf-8-sig') as board:
            reader = csv.reader(board, delimiter=",")
            for row in reader:
                board_array.append(row)
        return board_array

    def __str__(self):
        return str(self.state)


class Board():
    def __init__(self, board_array):
        # The original array passed from the csv, 2D array
        self.board_array = board_array
        # One side dimension of the board
        self.side_length = len(self.board_array)
        # Tile the board with the start state
        self.tiles = self.tile_board()
        # Stores the numerical values of the tiles, lowest to highest
        self.sorted_ints = self.sort_tiles()
        # Zeroes at the start of the board
        self.front_goal = self.front_sort_tiles()
        print([str(tile) for tile in self.front_goal])
        # Zeroes at the end of the board
        self.back_goal = self.back_sort_tiles()
        print([str(tile) for tile in self.back_goal])
        self.total_heuristic = self.sum_board()
        self.effort = 0
        self.parent = None
        # String representation of what happened in the board
        self.move = "No Move"


    def tile_board(self):
        tiles = []
        row_counter = 0
        index = 0
        for row in self.board_array:
            col_counter = 0
            for col in row:
                if col != "B":
                    tiles.append(Tile(row_counter, col_counter, index, int(col)))
                else:
                    tiles.append(Tile(row_counter, col_counter, index))
                col_counter += 1
                index += 1
            row_counter += 1
        return tiles
            
    def sort_tiles(self):
        numeric_sort = [tile for tile in self.tiles]
        # Insertion sort the board by tile value
        for i in range(1, len(numeric_sort)):
            key = numeric_sort[i]
            j = i - 1
            while j >= 0 and key.current_value < numeric_sort[j].current_value:
                numeric_sort[j + 1] = numeric_sort[j]
                j -= 1
            numeric_sort[j + 1] = key
        # Extract integer current values from the tiles
        sorted_int_list = [tile.current_value for tile in numeric_sort]
        return sorted_int_list

    def front_sort_tiles(self):
        sorted_int_list = self.sorted_ints
        # Make a new list of tiles with proper end coordinates, zeroes at the start of the list
        new_tiles = []
        index = 0
        for i in range(self.side_length):
            for j in range(self.side_length):
                new_tiles.append(Tile(i, j, index, sorted_int_list[index]))
                index += 1
        return new_tiles

    def back_sort_tiles(self):
        sorted_int_list = self.sorted_ints
        # Order zeroes to end of list
        end_zeroes = 0
        for i in range(len(sorted_int_list)):
            if sorted_int_list[i] == 0:
                end_zeroes = i
        zero_list = sorted_int_list[0 : end_zeroes + 1]
        sorted_int_list = sorted_int_list[end_zeroes + 1:] + zero_list
        # Make a new list of tiles with proper end coordinates, zeroes at the end of the list
        new_tiles = []
        index = 0
        for i in range(self.side_length):
            for j in range(self.side_length):
                new_tiles.append(Tile(i, j, index, sorted_int_list[index]))
                index += 1
        return new_tiles


    def __str__(self):
        for tile in self.tiles:
            print(tile)
        return "Board printed"

class Tile():
    def __init__(self, position_x, position_y, tile_index, current_value=0, front_h_val=-1, back_h_val=-1):
        # (X,Y) position of the tile on the board
        self.position_x = position_x
        self.position_y = position_y
        # Value of the tile (absolute position)
        self.tile_index = tile_index
        # The value held by the tile
        self.current_value = current_value
        # All blanks at the start of the board
        self.front_h_val = front_h_val
        # All blanks at the end of the board
        self.back_h_val = back_h_val

    def __str__(self):
        return str((self.position_x, self.position_y, self.current_value))