from test import * 

def play_games(algorithm1, algorithm2):
    results = {'Algorithm 1': {'wins': 0, 'draws': 0},
               'Algorithm 2': {'wins': 0, 'draws': 0}}

    for i in range(COL_COUNT):
        print(f"Game {i+1} - Algorithm 1 starts")
        board = Board()
        board.drop_pieces(2,i)
        while not board.game_over:
            if board.turn == 0:
                if algorithm1 == minimax:
                    move = algorithm1(board, 1, 2, 1)
                elif algorithm1 == astar_algorithm:
                    move = algorithm1(board,1)
                elif algorithm1 == monte_carlo_tree_search:
                    move = algorithm1(board, 1, simulations=10000)
                elif algorithm1 == negamax:
                    move = algorithm1(board, 5, current_player)[1]
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
                    move = algorithm1(board, 5, current_player)[2]
                else:
                    print("ERROR")
                    return 0
            board.drop_pieces(board.turn + 1, move)
            board.turn = 1 - board.turn
        if board.win(1):
            results['Algorithm 1']['wins'] += 1
        elif board.win(2):
            results['Algorithm 2']['wins'] += 1
        else:
            results['Algorithm 1']['draws'] += 1
            results['Algorithm 2']['draws'] += 1
            

    for i in range(COL_COUNT):
        print(f"Game {i+1} - Algorithm 2 starts")
        board = Board()
        board.drop_pieces(1,i)
        while not board.game_over:
            if board.turn == 0:
                if algorithm1 == minimax:
                    move = algorithm1(board, 1, 2, 1)
                elif algorithm1 == astar_algorithm:
                    move = algorithm1(board,1)
                elif algorithm1 == monte_carlo_tree_search:
                    move = algorithm1(board, 1, simulations=10000)
                elif algorithm1 == negamax:
                    move = algorithm1(board, 5, current_player)[1]
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
                    move = algorithm1(board, 5, current_player)[2]
                else:
                    print("ERROR")
                    return 0
            board.drop_pieces(board.turn + 1, move)
            board.turn = 1 - board.turn
        if board.win(1):
            results['Algorithm 1']['wins'] += 1
        elif board.win(2):
            results['Algorithm 2']['wins'] += 1
        else:
            results['Algorithm 1']['draws'] += 1
            results['Algorithm 2']['draws'] += 1

    return results

# Example usage:
results = play_games(astar_algorithm, minimax)
print("Results:")
print(results)
