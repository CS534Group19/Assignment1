from new_board import Board

def hill_heuristic(start: Board, goal_board: list[list[int]], max_iters: int):
    """Static method to run hill climbing
    ### Parameters
    - start: the starting Board for the search
    ### Returns
    - nothing, but prints to the console
    """
    # Get all possible moves for the start state
    start.set_zero_neighbors()
    # Begin search
    current_board: Board = start
    open = [start] # tracks children being searched
    nodes_expanded = []

    trial_counter = 0
    goal = False

    while not goal:
        if (current_board.board_array == goal_board):
            print("\nReached goal state")
            done_board = current_board
            cost = current_board.effort
            final_depth = current_board.node_depth
            moves = []
            while current_board.parent is not None:
                moves.append(current_board.move)
                current_board = current_board.parent
            moves.reverse()
            for move in moves:
                print(move)

            print(f"\nNodes expanded: {len(nodes_expanded)}")
            print(f"Moves required: {len(moves)}")
            print(f"Solution Cost: {cost}")
            if final_depth != 0:
                print(f"Estimated branching factor {len(nodes_expanded)**(1/final_depth):0.3f}")
            goal = True
            return done_board
        if (trial_counter <= max_iters):
            trial_counter += 1

            current_board = open.pop(0)

            populate_children(current_board)

            current_board.children.sort(key = lambda child:child.h_val)
            open.append(current_board.children[0])
            nodes_expanded.append(current_board)
        else:
            print("\nOut of moves")
            break
    if not goal:
        done_board = current_board
        cost = current_board.effort
        final_depth = current_board.node_depth
        moves = []
        while current_board.parent is not None:
            moves.append(current_board.move)
            current_board = current_board.parent
        moves.reverse()
        for move in moves:
            print(move)

        print(f"\nNodes expanded: {len(nodes_expanded)}")
        print(f"Moves required: {len(moves)}")
        print(f"Solution Cost: {cost}")
        if final_depth != 0:
            print(f"Estimated branching factor {len(nodes_expanded)**(1/final_depth):0.3f}")
        return done_board