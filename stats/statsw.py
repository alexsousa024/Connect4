from test_stats import *

def compare_algorithms(algorithm1, algorithm2):
    wins_algorithm1 = 0
    wins_algorithm2 = 0
    draws = 0
    
    # Play 7 games where algorithm1 starts
    
    for col in range(COL_COUNT):
        print(f"Game {col+1} - Algorithm 1 starts")
        board = Board()  # Initialize a new game board
        board.drop_pieces(2, col) # Drop a piece of the adversary in a column before starting the game
        board.print_board()
        print('\n')
        current_player = 1  # Algorithm 1 starts
        
        
        while not board.is_full() and not board.win(1) and not board.win(2):
            if current_player == 1:
                if algorithm1 == minimax:
                    move = algorithm1(board, 1, 2, 1)
                elif algorithm1 == astar_algorithm:
                    move = algorithm1(board,1)
                elif algorithm1 == monte_carlo_tree_search:
                    move = algorithm1(board, 1, simulations=10000)
                elif algorithm1 == negamax:
                    move = algorithm1(board, 5, 1)[1]
                else:
                    print("ERROR")
                    return 0
            else:
                if algorithm1 == minimax:
                    move = algorithm1(board, 1, 2, 2)
                elif algorithm1 == astar_algorithm:
                    move = algorithm1(board,2)
                elif algorithm1 == monte_carlo_tree_search:
                    move = algorithm1(board, 2, simulations=10000)
                elif algorithm1 == negamax:
                    move = algorithm1(board, 5, 2)[1]
                else:
                    print("ERROR")
                    return 0
            # Make the move on the board
            board.drop_pieces(current_player, move)
            board.print_board()
            print('\n')
            # Switch to the next player
            current_player = 3 - current_player
        # Determine the winner or if it's a draw
        if board.win(1):
            wins_algorithm1 += 1
            print(f"{algorithm1} wins")
        elif board.win(2):
            wins_algorithm2 += 1
            print(f"{algorithm2} wins")
        else:
            draws += 1
            print("Draw")
    
    # Play 7 games where algorithm2 starts
    for col in range(COL_COUNT):
        print(f"Game {col+1} - Algorithm 1 starts")
        board = Board()  # Initialize a new game board
        board.drop_pieces(1, col) # Drop a piece of the adversary in a column before starting the game
        board.print_board()
        print('\n')
        current_player = 2  # Algorithm 2 starts
        
        
        while not board.is_full() and not board.win(1) and not board.win(2):
            if current_player == 1:
                if algorithm1 == minimax:
                    move = algorithm1(board, 1, 2, 1)
                elif algorithm1 == astar_algorithm:
                    move = algorithm1(board,1)
                elif algorithm1 == monte_carlo_tree_search:
                    move = algorithm1(board, 1, simulations=10000)
                elif algorithm1 == negamax:
                    move = algorithm1(board, 5, 1)[1]
                else:
                    print("ERROR")
                    return 0
            else:
                if algorithm1 == minimax:
                    move = algorithm1(board, 1, 2, 2)
                elif algorithm1 == astar_algorithm:
                    move = algorithm1(board,2)
                elif algorithm1 == monte_carlo_tree_search:
                    move = algorithm1(board, 2, simulations=10000)
                elif algorithm1 == negamax:
                    move = algorithm1(board, 5, 2)[1]
                else:
                    print("ERROR")
                    return 0
            # Make the move on the board
            board.drop_pieces(current_player, move)
            board.print_board()
            print('\n')
            # Switch to the next player
            current_player = 3 - current_player
        # Determine the winner or if it's a draw
        if board.win(1):
            wins_algorithm1 += 1
            print(f"{algorithm1} wins")
        elif board.win(2):
            wins_algorithm2 += 1
            print(f"{algorithm2} wins")
        else:
            draws += 1
            print("Draw")
    
    # Print the results
    print("Results:")
    print(f"Algorithm 1 wins: {wins_algorithm1}")
    print(f"Algorithm 2 wins: {wins_algorithm2}")
    print(f"Draws: {draws}")

#compare_algorithms(astar_algorithm,astar_algorithm)
#compare_algorithms(astar_algorithm, minimax)
#compare_algorithms(astar_algorithm, monte_carlo_tree_search)
#compare_algorithms(astar_algorithm, negamax)

#compare_algorithms(minimax, minimax)
#compare_algorithms(minimax, monte_carlo_tree_search)
#compare_algorithms(minimax, negamax)

#ompare(monte_carlo_tree_search,monte_carlo_tree_search)
#compare_algorithms(monte_carlo_tree_search, negamax)

compare_algorithms(negamax,negamax)

