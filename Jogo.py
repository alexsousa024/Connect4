import numpy as np
import pygame
import sys
#from algoritmos import Connect4Game 
import copy 

# Initialize Pygame
pygame.init()

# Define colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game settings
ROW_COUNT = 6
COL_COUNT = 7
SQUARESIZE = 100

width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)

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
    
   




def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r+1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int((r+1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board.board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2),  int((r+1) * SQUARESIZE + SQUARESIZE / 2)) , RADIUS)
            elif board.board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), int((r+1)* SQUARESIZE + SQUARESIZE / 2))  , RADIUS)
    pygame.display.update()


board = Board()




def Scores(window):
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


def board_evaluation(board,player_1,player_2):
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
                    player_score -= 10* board_score_matrix[r][c]
                elif board[r][c] == player_2:  # Posição ocupada pelo jogador 2
                    player_score += 10* board_score_matrix[r][c]
        
        return player_score

    
            
    #Funcap de heurística #1 - Jananlas de 4 em 4 
def evaluate_function_1(board):
        score = 0
        
        #horizontalmente
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT - 3): 
                window = board[r][c:c+4]
                
                score += Scores(window)
        
    
        #verticalmente
        for r in range(ROW_COUNT-3):
            for c in range(COL_COUNT): 
                window = np.array([board[r+i][c] for i in range(4)])
                
                score += Scores(window)

        #diagonalente com declive negativo 
        for r in range(ROW_COUNT-3):
            for c in range(COL_COUNT-3):
                window = np.array([board[r+i][c+i] for i in range(4)])
                score += Scores(window)

    # diagonalmente com declive positivo 
        for r in range(ROW_COUNT-3):
            for c in range(COL_COUNT-1, 2, -1):
                window = np.array([board[r+i][c-i] for i in range(4)])
                score += Scores(window)

        return score
    
def final_heuristic_1(board,player_1, player_2):

        eval_score = evaluate_function_1(board)
        board_score = board_evaluation(board,player_1,player_2)
        total_score = eval_score + board_score                           
        return total_score

def astar_algorithm(board, player):
    open_list = [(0, board, None)]  # Custo inicial, estado inicial, e nenhuma jogada ainda
    best_score = float('-inf')  # Inicializa a melhor pontuação como infinito negativo
    best_move = None  # Melhor movimento ainda não foi encontrado

    while open_list:
        _, current_board, move = open_list.pop(0)  # Remove o item com menor custo heurístico
        # Verifica se o movimento atual é melhor do que o melhor encontrado até agora
       
        current_score = final_heuristic_1(current_board.board,1,2)
        
        #print(current_score)
        if current_score > best_score:
            best_score = current_score
            best_move = move

        # Se o tabuleiro atual representa um estado de vitória, não precisamos continuar


        # Gera os sucessores do estado atual
        successors = generate_sucessors(current_board, player)
        #print(successors)

        i = 0

        for successor, succ_move in successors:
            # Calcula o custo heurístico para o sucessor
            #print(successor)
        
            heuristic = final_heuristic_1(successor,1, player)
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


def generate_sucessors(board,player):
        sucessors = []
        for col in range(COL_COUNT):
            if board.valid_col(col):
                new_board = copy.deepcopy(board)
                new_board.drop_pieces(player, col)
                sucessors.append((new_board.board,col))
        return sucessors

# Main game loop
while not board.game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_pos = event.pos[0]
            col = int(x_pos // SQUARESIZE)
            

            if board.turn == 0:
                if board.drop_pieces(1, col):
                    print(final_heuristic_1(board.board,1,2))
                    board.print_board() 
                    if board.win(1):
                        print("Player 1 wins!")
                        board.game_over = True
                    board.turn = 1 - board.turn  # Switch turns
            else:
                col2 = astar_algorithm(board,2)
                print(col2)
                if board.drop_pieces(2, col2):
                    heuristic_value = final_heuristic_1(board.board, 1, 2)
                    print("heuristica final:", heuristic_value)
                    board.print_board()
                    if board.win(2):
                        print("Player 2 wins!")
                        board.game_over = True
                    board.turn = 1 - board.turn  # Switch turns

    draw_board(board)  # Draw the board state at every loop iteration
    
    if board.is_full():
        print("The game is a draw!")
        board.game_over = True


pygame.time.wait(3000)  # Delay to see the final board state before closing
pygame.quit()



