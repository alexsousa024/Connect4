import numpy as np
import copy
import math 
import random

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
        #Verificar horizontal
        for c in range(COL_COUNT-3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == player and self.board[r][c+1] == player and self.board[r][c+2] == player and self.board[r][c+3] == player:
                    return True
        #Verificar vertical
                
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == player and self.board[r+1][c] == player and self.board[r+2][c] == player and self.board[r+3][c] == player: 
                    return True
                
        #Verificar diagonal com declive positivo
        
        for c in range(COL_COUNT - 3):
            for r in range(3,ROW_COUNT):
                if self.board[r][c] == player and self.board[r-1][c+1] == player and self.board[r-2][c+2] == player and self.board[r-3][c+3] == player: 
                    return True 
        #Verificar diagonal com decline negativo 
        for c in range(COL_COUNT - 3):
            for r in range(3):
                if self.board[r][c] == player and self.board[r+1][c+1] == player and self.board[r+2][c+2] == player and self.board[r+3][c+3] == player: 
                    return True
                
        return False 

    def is_full(self):
        return np.all(self.column_heights < 0)

    def print_board(self):

        print(self.board)

class Heuristica_AStar: 
    
    def Scores(self,window):
            score = 0
            # Contar vitórias absolutas
        
            #Mudar para float pq é como está o array numpy 
            player_1 = 1.0
            player_2 = 2.0
            if np.count_nonzero(window == player_2) == 4:
                score += 5120  # Vitória absoluta para o player_2 
                
            elif np.count_nonzero(window == player_1) == 4:
                
                score -= 5120  # Vitória absoluta para o player_1

            # Adaptação dos demais cálculos usando np.count_nonzero
            if np.count_nonzero(window == player_1) == 3 and np.count_nonzero(window == player_2) == 0: 
                score -= 500
            elif np.count_nonzero(window == player_1) == 2 and np.count_nonzero(window == player_2) == 0: 
                score -= 100
            elif np.count_nonzero(window == player_1) == 1 and np.count_nonzero(window == player_2) == 0: 
                score -= 10
            # Não é necessário tratar o caso de ambos 0, pois o score não muda
            elif np.count_nonzero(window == player_1) == 0 and np.count_nonzero(window == player_2) == 1: 
                score += 10
            elif np.count_nonzero(window == player_1) == 0 and np.count_nonzero(window == player_2) == 2: 
                score += 100
            elif np.count_nonzero(window == player_1) == 0 and np.count_nonzero(window == player_2) == 3: 
                score += 500

            return score


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
            
            # Iterar sobre o tabuleiro e calcular o score baseado em posições ocupadas
            for r in range(ROW_COUNT):
                for c in range(COL_COUNT):
                    if board[r][c] == player_1:  # Posição ocupada pelo jogador 1
                        player_score -= 5* board_score_matrix[r][c]
                    elif board[r][c] == player_2:  # Posição ocupada pelo jogador 2
                        player_score += 5 * board_score_matrix[r][c]
            
            return player_score

        
                
        #Funcao  de heurística #1 - Jananlas de 4 em 4 
    def evaluate_function_1(self,board):
            score = 0
            
            #horizontalmente
            for r in range(ROW_COUNT):
                for c in range(COL_COUNT - 3): 
                    window = board[r][c:c+4]
                    
                    score += self.Scores(window)
            
        
            #verticalmente
            for r in range(ROW_COUNT-3):
                for c in range(COL_COUNT): 
                    window = np.array([board[r+i][c] for i in range(4)])
                    
                    score += self.Scores(window)

            #diagonalente com declive negativo 
            for r in range(ROW_COUNT-3):
                for c in range(COL_COUNT-3):
                    window = np.array([board[r+i][c+i] for i in range(4)])
                    score += self.Scores(window)

        # diagonalmente com declive positivo 
            for r in range(ROW_COUNT-3):
                for c in range(COL_COUNT-1, 2, -1):
                    window = np.array([board[r+i][c-i] for i in range(4)])
                    score += self.Scores(window)

            return score
        
    def final_heuristic_1(self,board,player_1, player_2):

            eval_score = self.evaluate_function_1(board)
            board_score = self.board_evaluation(board,player_1,player_2)
            total_score = eval_score + board_score                           
            return total_score
    


    def astar_algorithm(self,board, player): 
        open_list = [(0, board, None)]  # Custo inicial, estado inicial, e nenhuma jogada ainda
        best_score = float('-inf')  # Inicializa a melhor pontuação como infinito negativo
        best_move = None  # Melhor movimento ainda não foi encontrado

        while open_list:
            _, current_board, move = open_list.pop(0)  # Remove o item com menor custo heurístico
            # Verifica se o movimento atual é melhor do que o melhor encontrado até agora
        
            current_score = self.final_heuristic_1(current_board.board,1,2)
            
            #print(current_score)
            if current_score > best_score:
                best_score = current_score
                best_move = move

            # Se o tabuleiro atual representa um estado de vitória, não precisamos continuar


            # Gera os sucessores do estado atual
            successors = self.generate_sucessors(current_board, player)
            #print(successors)

            i = 0

            for successor, succ_move in successors:
                # Calcula o custo heurístico para o sucessor
                #print(successor)
            
                heuristic = self.final_heuristic_1(successor,1, player)
                print(str(i) + " : " + str(heuristic))
                i += 1
                # Adiciona o sucessor à lista aberta
                open_list.append((heuristic, successor, succ_move))

            # Ordena a lista pelo custo heurístico para garantir que o próximo estado a ser explorado é o de menor custo
            open_list.sort(key=lambda x: x[0], reverse = True)
            a,b,c = open_list.pop(0)

            return c
        # Retorna a coluna do melhor movimento encontrado
        return best_move


    def generate_sucessors(self,board,player):
            sucessors = []
            for col in range(COL_COUNT):
                if board.valid_col(col):
                    new_board = copy.deepcopy(board)
                    new_board.drop_pieces(player, col)
                    sucessors.append((new_board.board,col))
            return sucessors
    
C = math.sqrt(2)
class Node:
    def __init__(self, board, player, move = None, parent=None):
        assert isinstance(board, Board)
        self.board = board  #Instancia da classe board 
        self.parent = parent
        self.children = []
        self.move = move
        self.wins = 0
        self.visits = 0
        self.player = player

    def is_leaf(self):
        if self.board.is_full():
            return True
        else:
            return False
        
    def generate_successors(self):
        successors = []
        for col in range(COL_COUNT):
            if self.board.valid_col(col):
                new_board = copy.deepcopy(self.board)
                new_board.drop_pieces(self.player, col)
                successors.append(Node(new_board, self.player,self))
        return successors
    
    def is_fully_expanded(self):
        possible_moves = self.generate_successors()

        print(len(self.children))

        print(len(possible_moves))

        return len(self.children) == len(possible_moves)
    
    def expand(self):
        possible_moves = self.generate_successors()
        for move in possible_moves: 
            self.children.append(move)
    

    def select_child(self):
        
        best_score = -float("inf")
        best_children = []
        unvisited_children = []

        for child in self.children:
            if child.visits == 0:
                unvisited_children.append(child)
            else:
                exploration_term = math.sqrt(math.log(self.visits +1) / child.visits)
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

class monte_carlo_tree_search:

    def mcts(self, board, player, simulations=100):
        root = Node(board,player)
        for _ in range(simulations):
            node = root
            # Selection
            
            while not node.is_leaf():
                if node.is_fully_expanded():
                    print("Nódulo Expandido")
                    node = node.select_child()
                else:
                    # Expansion
                    print("Expandiu")
                    node.expand()
                    node = node.children[-1]  # Choose the newest child
                    break

            # Simulation
                
            result = self.simulate_random_playout(node.board, player)


            # Backpropagation

            node.backpropagate(result)

        # After completing the simulations, choose the best move from the root node
        print(node.children)
        if node.children:
            best_child = max(node.children, key=lambda child: child.wins / child.visits if child.visits > 0 else 0)
            print(best_child.board)
            return best_child.move  # Return the move associated with the best child
        
    
    def simulate_random_playout(self, game_state, player):
        simulated_game = copy.deepcopy(game_state)
        current_player = player

        while not simulated_game.is_full() and not simulated_game.win(current_player):
            possible_moves = [col for col in range(COL_COUNT) if simulated_game.valid_col(col)]
            move = random.choice(possible_moves)
            simulated_game.drop_pieces(current_player, move)
            current_player = 1 if current_player == 2 else 2  # Switch player
            print(simulated_game.board)
        
        if simulated_game.win(current_player):
            return 1 if current_player == 2 else 0
        else:
            return 0.5  # Consider draw as half a win
