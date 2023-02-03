import csv

class NPuzzle():
    def __init__(self, board_file):
        self.board_file = board_file
        self.start_state = Board(self.create_board_array())

    def create_board_array(self):
        board_array = []
        with open(self.board_file, newline='', encoding='utf-8-sig') as board:
            reader = csv.reader(board, delimiter=",")
            for row in reader:
                board_array.append(row)
        return board_array

    def __str__(self):
        return str(self.start_state)


class Board():
    def __init__(self, board_array):
        self.board_array = board_array
        self.side_length = len(self.board_array)
        self.tiles = self.tile_board()
        self.goal = self.sort_tiles()
        # Set of child boards
        self.child_states = []
        self.total_heuristic = self.sum_board()


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
        for i in range(1, len(numeric_sort)):
            key = numeric_sort[i]
            j = i - 1
            while j >= 0 and key.current_value < numeric_sort[j].current_value:
                numeric_sort[j + 1] = numeric_sort[j]
                j -= 1
            numeric_sort[j + 1] = key

        sorted_int_list = [tile.current_value for tile in numeric_sort]
        new_tiles = []
        index = 0
        for i in range(self.side_length):
            for j in range(self.side_length):
                new_tiles.append(Tile(i, j, index, sorted_int_list[index]))
                index += 1
        return new_tiles

    def sum_board(self):
        sum = 0
        for tile in self.tiles:
            sum += min(tile.back_h_val, tile.front_h_val)

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