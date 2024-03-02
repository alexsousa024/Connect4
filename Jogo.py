import numpy as np
import pygame
import sys
from algoritmos import Connect4Game 
import heapq
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
        self.turn = 1  # Player 1 starts

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
                if self.board[r][c] == player and self.board[r+1][c] == player and self.board[r+2][c] and self.board[r+3][c] == player: 
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


    #Escolher a peca

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

IA = Connect4Game(1,2,board.board, 0)

#Algoritmo A*
def astar_algorithm(self):
        start_state = self.board

        priority_queue = [(0,start_state)]
        visited_states = set()

        while priority_queue:
            current_cost, current_state = heapq.heappop(priority_queue)
            

            if board.is_full or board.game_over:
                return 
            
            if current_state in visited_states:
                continue

            visited_states.add(current_state)

            sucessors = self.generate_sucessors(current_state)

            for successor_state in sucessors:
                heuristic = self.heuristic_function(successor_state)
                cost_to_sucessor = self.cost_function(successor_state)
                total_cost = heuristic + cost_to_sucessor + current_cost

                heapq.heappush(priority_queue, (total_cost, successor_state))

def generate_sucessors(self):
    sucessors = []
    for col in range(COL_COUNT):
        if self.board.valid_col(col):
            new_board = copy.deepcopy(self.board)
            new_board.drop_pieces(self.turn, col)

            new_game = Connect4Game(self.player_1, self.player_2, new_board, self.depth +1)
            new_game.switch_players()
            sucessors.append(new_game)
    return sucessors


def switch_players(self):
    self.turn = 3 - self.turn



#Funcao da heuristica #1 


# Main game loop
while not board.game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_pos = event.pos[0]
            col = int(x_pos // SQUARESIZE)


            if board.turn == 1:
                if board.drop_pieces(1, col):
                    print(IA.final_heuristic_1(1,2))
                    board.print_board() 
                    if board.win(1):
                        print("Player 1 wins!")
                        board.game_over = True
                    board.turn = 3 - board.turn  # Switch turns
            else:
                if board.drop_pieces(2, col):
                    print(IA.final_heuristic_1(1,2))
                    board.print_board()
                    if board.win(2):
                        print("Player 2 wins!")
                        board.game_over = True
                    board.turn = 3 - board.turn  # Switch turns

    draw_board(board)  # Draw the board state at every loop iteration
    
    if board.is_full():
        print("The game is a draw!")
        board.game_over = True


pygame.time.wait(3000)  # Delay to see the final board state before closing
pygame.quit()


