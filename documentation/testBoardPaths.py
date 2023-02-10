# Boards for testing in the command line

# Professor Beck's boards (haven't run either of these)
BOARD_1 = "../documentation/test_boards/board1.csv" # not solvable according to https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
BOARD_2 = "../documentation/test_boards/board2.csv" # solvable according to https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/

# Cutter Beck's boards
BOARD_3 = "../documentation/test_boards/board3.csv" # ~0.2 seconds, 4 moves, 8 nodes, 18 cost, branching factor 1.7
BOARD_4 = "../documentation/test_boards/board4.csv" # ~22 seconds, 6 moves, 52 nodes, 26 cost, branching factor 1.9
BOARD_5 = "../documentation/test_boards/board5.csv" # ~418.7 seconds, or ~7 min, 5 moves, 25 nodes, 60 cost, branching factor 1.9
BOARD_6 = "../documentation/test_boards/board6.csv" # ~10.5 seconds, 3 moves, 14 nodes, 18 cost, branching factor 2.4
BOARD_7 = "../documentation/test_boards/board7.csv" # ~3.8 seconds, 4 moves, 14 nodes, 46 cost, branching factor 1.9

# ^^ current times are based on unweighted heuristic