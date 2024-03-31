import numpy as np
import copy
import math 
import random
import pygame
import sys


# Game settings
ROW_COUNT = 6
COL_COUNT = 7
SQUARESIZE = 100


class Board:
    def __init__(self):
        self.board = np.zeros((ROW_COUNT, COL_COUNT))
        self.column_heights = np.full(COL_COUNT, ROW_COUNT - 1, dtype=int)
        self.game_over = False
        self.turn = 0  # Player 1 starts
        self.winning_pieces = []  # List to store winning pieces coordinates

    def drop_pieces(self, player , col):
        if self.valid_col(col):
            height = self.column_heights[col]
            self.board[height][col] = player
            self.column_heights[col] = height-1
            return True
        else:
            print("Invalid move")
            return False
        
    def valid_col(self, col):
        if self.column_heights[col] == -1 :
            return False
        return True
    
    def win(self,player): 

        # Check horizontal
        for c in range(COL_COUNT-3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == player and self.board[r][c+1] == player and self.board[r][c+2] == player and self.board[r][c+3] == player:
                    self.winning_pieces = [[r, c], [r, c + 1], [r, c + 2], [r, c + 3]]
                    return True

        # Check vertical
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == player and self.board[r+1][c] == player and self.board[r+2][c] == player and self.board[r+3][c] == player: 
                    self.winning_pieces = [[r, c], [r + 1, c], [r + 2, c], [r + 3, c]]
                    return True
                
        # Check diagonal with positive slope
        for c in range(COL_COUNT - 3):
            for r in range(3,ROW_COUNT):
                if self.board[r][c] == player and self.board[r-1][c+1] == player and self.board[r-2][c+2] == player and self.board[r-3][c+3] == player: 
                    self.winning_pieces = [[r, c], [r - 1, c + 1], [r - 2, c + 2], [r - 3, c + 3]]
                    return True 
                    
        # Check diagonal with negative slope
        for c in range(COL_COUNT - 3):
            for r in range(3):
                if self.board[r][c] == player and self.board[r+1][c+1] == player and self.board[r+2][c+2] == player and self.board[r+3][c+3] == player: 
                    self.winning_pieces = [[r, c], [r + 1, c + 1], [r + 2, c + 2], [r + 3, c + 3]]
                    return True
                
        return False 

    def is_full(self):
        return np.all(self.column_heights < 0)

    def print_board(self):

        print(self.board)



class Heuristic: 
    
    def Scores(self,window,player_1, player_2):

            # Count absolute victories
            score = 0
            
            # Change to float bc thats how the numpy array is

            if np.count_nonzero(window == player_2) == 4:
                score += 100000  # Absolute victory for Player 2
                
            elif np.count_nonzero(window == player_1) == 4:
                score -= 80000  # Absolute victory for Player 1

            # Adaptation of the calculations using np.count_nonzero
            if np.count_nonzero(window == player_1) == 3 and np.count_nonzero(window == player_2) == 0: 
                score -= 500
            elif np.count_nonzero(window == player_1) == 2 and np.count_nonzero(window == player_2) == 0: 
                score -= 100
            elif np.count_nonzero(window == player_1) == 1 and np.count_nonzero(window == player_2) == 0: 
                score -= 10

            # Not necessary to treat the case of both 0, as the score does not change

            elif np.count_nonzero(window == player_1) == 0 and np.count_nonzero(window == player_2) == 1: 
                score += 10
            elif np.count_nonzero(window == player_1) == 0 and np.count_nonzero(window == player_2) == 2: 
                score += 100
            elif np.count_nonzero(window == player_1) == 0 and np.count_nonzero(window == player_2) == 3: 
                score += 500
    
            return score

    # Useful function for the first moves of the game
    def board_evaluation(self,board,player_1,player_2):

            board_score_matrix = np.array([
                [3, 4, 5, 7, 5, 4, 3],
                [4, 6, 8, 10, 8, 6, 4],
                [5, 8, 11, 13, 11, 8, 5],
                [5, 8, 11, 13, 11, 8, 5],
                [4, 6, 8, 10, 8, 6, 4],
                [3, 4, 5, 7, 5, 4, 3]
            ])
            
            player_score = 0 
            
            # Iterate over the board and calculate the score based on occupied positions
            for r in range(ROW_COUNT):
                for c in range(COL_COUNT):
                    if board[r][c] == player_1:  # Position occupied by Player 1
                        player_score -= board_score_matrix[r][c]
                    elif board[r][c] == player_2:  # Position occupied by player 2
                        player_score += board_score_matrix[r][c]
            
            return player_score

        
    # Heuristic function - 4 by 4 windows
    def evaluate_function_1(self,board,player_1,player_2):

            score = 0
            
            # Horizontally
            for r in range(ROW_COUNT):
                for c in range(COL_COUNT - 3): 
                    window = board[r][c:c+4]
                    score += self.Scores(window,player_1,player_2)
            
        
            # Vertically
            for r in range(ROW_COUNT-3):
                for c in range(COL_COUNT): 
                    window = np.array([board[r+i][c] for i in range(4)])
                    score += self.Scores(window,player_1,player_2)

            # Diagonally with positive slope
            for r in range(ROW_COUNT-3):
                for c in range(COL_COUNT-1, 2, -1):
                    window = np.array([board[r+i][c-i] for i in range(4)])
                    score += self.Scores(window,player_1,player_2)

            # Diagonally with negative slope
            for r in range(ROW_COUNT-3):
                for c in range(COL_COUNT-3):
                    window = np.array([board[r+i][c+i] for i in range(4)])
                    score += self.Scores(window,player_1,player_2)

            return score
        

    def final_heuristic(self,board,player1, player2):
        
            eval_score = self.evaluate_function_1(board,player1,player2)
            board_score = self.board_evaluation(board,player1,player2)
            total_score = eval_score + board_score                           
            return total_score


heuristic = Heuristic()

def astar_algorithm(board, player): 
    open_list = [(0, board, None)]  # Initial cost, initial state, and no plays done yet
    best_score = float('-inf')  # Initializes the best score to negative infinity
    best_move = None  # Best move hasn't been found yet

    while open_list:

        # Remove the item with the lowest heuristic cost
        _, current_board, move = open_list.pop(0)  

        # Checks if the current movement is better than the best found so far
        current_score = heuristic.final_heuristic(current_board.board,3-player,player)
        
        if current_score > best_score:
            best_score = current_score
            best_move = move

        # If the current board represents a winning state, we do not need to continue


        # Generates the successors of the current state
        successors = generate_sucessors(current_board, player)
        

        i = 0

        for successor, succ_move in successors:

            # Calculate the heuristic cost for the successor
            heuristic_astar = heuristic.final_heuristic(successor,3-player, player)
            i += 1

            # Add successor to the open list
            open_list.append((heuristic_astar, successor, succ_move))

        # Sorts the list by heuristic cost to ensure that the next state to be explored is the one with the lowest cost
        open_list.sort(key=lambda x: x[0], reverse = True)
        a,b,c = open_list.pop(0)

        return c

    # Returns the column of the best movement found
    return best_move


def generate_sucessors(board,player):
        sucessors = []
        for col in range(COL_COUNT):
            if board.valid_col(col):
                new_board = copy.deepcopy(board)
                new_board.drop_pieces(player, col)
                sucessors.append((new_board.board,col))
        return sucessors

C = 0.5
class Node:
    def __init__(self, board, player, move = None , parent=None):
        assert isinstance(board, Board)
        self.board = board  #Instancia da classe board 
        self.parent = parent
        self.children = []
        self.move = move
        self.wins = 0
        self.visits = 0
        self.player = player

    def is_leaf(self):
        if (len(self.children) == 0) or self.board.win(1) or self.board.win(2) or self.board.is_full():
            return True
        else:
            return False
        
    def generate_successors(self):
        successors = []
        for col in range(COL_COUNT):
            if self.board.valid_col(col):
                new_board = copy.deepcopy(self.board)
                new_board.drop_pieces(self.player, col)
                successors.append(Node(new_board, self.player, col, self))
        return successors
    
    def is_fully_expanded(self):
        possible_moves = self.generate_successors()
        
        return len(possible_moves) == len(self.children)
    
    def expand(self):
        # Identifica as jogadas possíveis que ainda não foram exploradas
        unexplored_moves = [col for col in range(COL_COUNT) if self.board.valid_col(col) and all(col != child.move for child in self.children)]
        
        if unexplored_moves:
            # Escolhe uma jogada não explorada aleatoriamente para a expansão
            move = random.choice(unexplored_moves)
            
            # Cria uma cópia do estado do tabuleiro e aplica a jogada escolhida
            new_board = copy.deepcopy(self.board)
            new_board.drop_pieces(self.player, move)
            
            # Cria um novo nó filho com o estado resultante e adiciona à lista de filhos
            new_node = Node(board=new_board, player=self.player, move=move, parent=self)
            self.children.append(new_node)
            
            # Retorna o novo nó para que seja utilizado na simulação
            return new_node
        
        # Retorna None se não houver mais movimentos não exploradoss
        return None

    def select_child(self):
        
        best_score = -float("inf")
        best_children = []
        unvisited_children = []

        for child in self.children:
            if child.visits == 0:
                unvisited_children.append(child)
            else:
                exploration_term = math.sqrt((math.log(self.visits+1)*2) / child.visits)
                score = child.wins / child.visits + C * exploration_term
                if  score == best_score:
                    best_score = score
                    best_children = [child]
                elif score > best_score:
                    best_score = score
                    best_children = [child]
            if len(unvisited_children) > 0:
                return random.choice(unvisited_children)
        return random.choice(best_children)
    
    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent is not None:
            self.parent.backpropagate(result)

def monte_carlo_tree_search(board, player, simulations):

    # Passo 1: Inicialize a árvore
    root = Node(board, player)
    root.expand()  # Isso gera os primeiros sucessores (os 7 nós, assumindo um tabuleiro de Connect Four)
    
    # Passo 2: Simulações iniciais para os primeiros nós
    initial_simulations_per_node = 5
    for initial_node in root.children[:7]:  # Assumindo que você quer fazer isso apenas para os primeiros 7 nós
        for _ in range(initial_simulations_per_node):
            result = simulate_random_playout(initial_node.board, player)
            initial_node.backpropagate(result)

    for _ in range(simulations):
        
        node = root
        # Selection
        while not node.is_leaf():
            if not node.is_fully_expanded():
                node = node.expand()
                break
            else:
                node = node.select_child()
            
        if node is not None:
            result = simulate_random_playout(node.board, player)

            node.backpropagate(result)

    best_ratio = -float("inf")
    best_move = None
    for child in root.children:
        if child.visits > 0:
            ratio = child.wins / child.visits
            
        else:
            ratio = 0
        if ratio > best_ratio:
            best_ratio = ratio
            best_move = child.move
    
    # Retorna o movimento do melhor filho
    return best_move
    

def simulate_random_playout(game_state, player):
    simulated_game = copy.deepcopy(game_state)
    current_player = player

    while not simulated_game.is_full() and not simulated_game.win(current_player):
        possible_moves = [col for col in range(COL_COUNT) if simulated_game.valid_col(col)]
        move = random.choice(possible_moves)
        simulated_game.drop_pieces(current_player, move)
        if simulated_game.win(current_player):
            return 1 if current_player == player else 0
        current_player = 1 if current_player == 2 else 2  # Switch player
    
    if simulated_game.win(current_player):
        return 1 if current_player == player else 0
    else:
        return 0.5 # Consider draw as half a win

def minimax(board, depth, player_1, player_2, current_player, alpha=float('-inf'), beta=float('inf')):
    if board.is_full() or board.win(player_1) or board.win(player_2) or depth == 0:
        return heuristic.final_heuristic(board.board, player_1, player_2), -1

    maximizing_player = current_player == player_2
    if maximizing_player:
        max_eval = float('-inf')
        best_col = None
        for col in range(COL_COUNT):
            if board.valid_col(col):
                new_board = copy.deepcopy(board)
                new_board.drop_pieces(current_player, col)
                eval, _ = minimax(new_board, depth - 1, player_1, player_2, player_1, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_col = col
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval, best_col
    else:  # Minimizing player
        min_eval = float('inf')
        best_col = None
        for col in range(COL_COUNT):
            if board.valid_col(col):
                new_board = copy.deepcopy(board)
                new_board.drop_pieces(current_player, col)
                eval, _ = minimax(new_board, depth - 1, player_1, player_2, player_2, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_col = col
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval, best_col

def negamax(board, depth,player, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or board.is_full() or board.win(player):
        
        return heuristic.final_heuristic(board.board, 1, 2) * (-1 if player == 1 else 1), -1

    max_eval = float('-inf')
    player_move = -1

    for col in range(COL_COUNT):
        if board.valid_col(col):
            new_board = copy.deepcopy(board)
            new_board.drop_pieces(player, col)
            eval, _ = negamax(new_board, depth - 1, 3 - player, -beta, -alpha)
            eval = -eval  
            
            if eval > max_eval:
                max_eval = eval
                player_move = col

            alpha = max(alpha, eval)
            if alpha >= beta:
                break

    return max_eval, player_move
