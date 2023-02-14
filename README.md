## CS534 - ARTIFICIAL INTELLIGENCE
    # Group 19
    - Michael Alicea, malicea2@wpi.edu
    - Cutter Beck, cjbeck@wpi.edu
    - Jeffrey Davis, jrdavis2@wpi.edu
    - Oliver Shulman, ohshulman@wpi.edu
    - Edward Smith, essmith@wpi.edu

-------------------------------------------------------------------------------------------------------------------------------------
| ## PROGRAM SPECIFICATIONS
-------------------------------------------------------------------------------------------------------------------------------------
    - This program is coded in Python 3.10.9, but higher versions will work as well
    - Using the UTF-8-sig Encoding (based on Professor Beck's example files)
    - This program can be run using the terminal command permutations, one each for project part
-------------------------------------------------------------------------------------------------------------------------------------
| ## PROGRAM EXECUTION
------------------------------------------------------------------------------------------------------------------------------------- 
    # RUNNING PART 1 - A* Search
        1. To run A* Search:
            1.1 - Run from command line
                1.1.1 - COMMAND: `python astar.py path_to_board.csv heuristic tile_weight?`
                    1.1.1.1
                        - path_to_board.csv: the path location of the board CSV file the algorithm will search
                        - heuristic: one of `sliding` or `greedy`
                            - **`sliding` will run this version of A* for Part 1**
                        - tile_weight?: one of `True` or `False`
                1.1.2 - This will run the A* Search with either a weighted heuristic (true) or 
                                                                an unweighted heuristic (false)
        2. Output from A* Search:
            2.1 - Moves
                The exact moves necessary to solve the board state
            2.2 - Nodes Expanded
                The total number of nodes expanded during the search for the goal
            2.3 - Moves Required
                The total number of moves required to reach the goal
            2.4 - Solution Cost
                The total cost of the moves adjusted for the tile weights
            2.5 - Estimated Branching Factor
                The average number of branches from a parent node to a child node during the search.
                This is computed with the formula (total # of expanded nodes) ^ (1 / solution node depth)
-------------------------------------------------------------------------------------------------------------------------------------
    # RUNNING PART 2 - Hill Climbing
        1. To run Hill Climbing:
            1.1 - Run from command line
                1.1.1 - COMMAND: `python greedy_hillclimbing.py path_to_board.csv time`
                    1.1.1.1
                        - path_to_board.csv: the path location of the board CSV file the algorithm will search
                        - time: a value in seconds, can be an integer or float as it is cast to float during execution
        2. Output from Hill Climbing:
            2.1 - Moves
                The exact moves necessary to solve the board state
            2.2 - Nodes Expanded
                The total number of nodes expanded during the search for the goal
            2.3 - Moves Required
                The total number of moves required to reach the goal
            2.4 - Solution Cost
                The total cost of the moves adjusted for the tile weights
            2.5 - Estimated Branching Factor
                The average number of branches from a parent node to a child node during the search.
                This is computed with the formula (total # of expanded nodes) ^ (1 / solution node depth)
-------------------------------------------------------------------------------------------------------------------------------------
    # RUNNING PART 3 - Modified A* Search
        1. To run Modifed A* Search:
            1.1 - Run from command line
                1.1.1 - COMMAND: `python astar.py path_to_board.csv heuristic tile_weight?`
                    1.1.1.1
                        - path_to_board.csv: the path location of the board CSV file the algorithm will search
                        - heuristic: one of `sliding` or `greedy`
                            - **`greedy` will run this modified version of A for Part 3**
                        - tile_weight?: one of `True` or `False`
                1.1.2 - This will run the modified A* Search with either a weighted greedy heuristic (`True`) or 
                                                                         an unweighted greedy heuristic (`False`)
        2. Output from Modified A* Search:
            2.1 - Moves
                The exact moves necessary to solve the board state
            2.2 - Nodes Expanded
                The total number of nodes expanded during the search for the goal
            2.3 - Moves Required
                The total number of moves required to reach the goal
            2.4 - Solution Cost
                The total cost of the moves adjusted for the tile weights
            2.5 - Estimated Branching Factor
                The average number of branches from a parent node to a child node during the search.
                This is computed with the formula (total # of expanded nodes) ^ (1 / solution node depth)
-------------------------------------------------------------------------------------------------------------------------------------
| ## PROGRAM NOTES
-------------------------------------------------------------------------------------------------------------------------------------    
    # PART 0 - New Board Data Structure
        0.1 - Reads a .csv file into a square 2d array, interpretting 'B' as 0
        0.2 - This board acts as the start state or parent
        0.3 - The board goal(s) are computed from the initial board with a simple shuffle
            0.3.1 - The front state is represented by the zeros in the front
            0.3.2 - The back state is represented by the zeros in the back
        0.4 - To determine possible moves (children), each 0 is examined
            0.4.1 - For each non-0 neighbor in a cardinal direction of a zero, 
                0.4.1.1 - A new child board is created swapping the zero with its neighbor
            0.4.2 - This new child board is assigned its parent
            0.4.3 - The effort of this child is computed as the weight of the swapped neighbor
    	    0.4.4 - The plain English reprentation of this movement is stored within the child
            0.4.5 - The heuristic effort is computed as the sum of each tile's Manhattan distance to the goal
            0.4.6 - The total estimated effort is computed as a sum of the tile movement weight and heurisitic effort
        0.6 - Repeat steps 0.2 - 0.4 to build the entire tree of possible board states

-------------------------------------------------------------------------------------------------------------------------------------    
    # PART 1 - A* Search
        1.1 - Reads command line argument #2 - (sliding)
            1.1.1 - If this is not sliding, it will instead run PART 3's Modified A* Search
        1.2 - Reads command line argument #3 - (true/false) 
            1.2.1 - If true, the sliding heuristic utilized will take into account the tile weights
            1.2.2 - If false, the sliding heuristic utilized will not take into account the tile weights 
        1.3 - Begins an A* Search by building a board using the New Board data structure
        1.4 - Devises a priority queue in which a board and its children are enqueued based on their total estimated effort
            1.4.1 - Pops the best board from the queue and expands it
            1.4.2 - Enqueues the board's children
            1.4.3 - Seperately records metadata on the search (# of nodes expanded, node depth, total compute time)
        1.5 - Repeats 1.4 until heurisitic value of a board equals 0 (every board tile is in its place)
	    1.6 - Backtracks from the goal back to start using the parent-child relation, archiving each movement's move from 0.4.4
        1.7 - Reports the metadata from the A* Search via output

-------------------------------------------------------------------------------------------------------------------------------------
    # PART 2 - Hill Climbing
        2.1 - Reads command line argument #2 - (xxxx)  
            2.1.1 - xxxx is understood to be the total allowed time in REAL SECONDS
        2.2 - For the allotted time:
            2.2.1 - The program will make a set number of random restarts
            2.2.2 - From each restart, the program performs simulated annealling 
            2.2.3 - The rate at which the temperature decreases changes proportionally to the total amount of available compute time
            2.2.4 - If goal is reached, the search succeeds
            2.2.5 - Otherwise the search has failed
        2.3 - If the search succeeded
            2.3.1 - The program will output the successful moves to the target
            2.3.2 - The program will output the metadata of the search
        2.4 - If the search failed 
            2.4.1 - The program will output the board at which it was currently when the time expanded
            2.4.2 - The program will output the metadata of the search

-------------------------------------------------------------------------------------------------------------------------------------
    # PART 3 - Modified A* Search
        3.1 - Reads command line argument #2 - (greedy)
            3.1.1 - If this is not greedy, it will instead run PART 1's A* Search
        3.2 - Reads command line argument #3 - (true/false) 
            3.2.1 - If true, the greedy heuristic utilized will take into account the tile weights
            3.2.2 - If false, the greedy heuristic utilized will not take into account the tile weights 
        3.3 - Begins a Modified A* Search by building a board using the New Board data structure
            3.3.1 - The Board is modified slightly, with the heurisitic value being caluated using the new algorithm:
            3.3.2 - NEW HEURISTIC:
            *************************************************************************************************
            3.3.3 - For each board, the total heuristic cost is computed as f(n) = g(n) + h(n) where:
                g(n) = weight of the moved tile
                h(n) = the effort required to perform a successful greedy hill climb for 3 boards with sideways moves
            *************************************************************************************************
        3.4 - Devises a priority queue in which a board and its children are enqueued based on their total estimated effort
            3.4.1 - Pops the best board from the queue and expands it
            3.4.2 - Enqueues the board's children
            3.4.3 - Seperately records metadata on the search (# of nodes expanded, node depth, total compute time)
        3.5 - Repeats 1.4 until heurisitic value of a board equals 0 (every board tile is in its place)
	    3.6 - Backtracks from the goal back to start using the parent-child relation, archiving each movement's move from 0.4.4
        3.7 - Reports the metadata from the Modifed A* Search via output
