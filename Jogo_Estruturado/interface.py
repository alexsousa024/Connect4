import pygame
import sys
import math
from Jogo1 import *
# Initialize Pygame
pygame.init()

# Define colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)

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

C = math.sqrt(2)



class Menu: 
    def draw_menu(self,screen):
        screen.fill((200, 200, 200))  # Define a cor de fundo da tela

        # Configura a fonte do título para uma fonte diferente e desenha o título
        title_font = pygame.font.SysFont("comicsansms", 60)  # Altera para "comicsansms" e aumenta o tamanho
        title_text = title_font.render("Connect 4", True, (0, 0, 0))  # Cor do texto do título (preto)
        title_rect = title_text.get_rect(center=(width // 2, 50))
        screen.blit(title_text, title_rect)

        # Configurações para os modos de jogo
        font = pygame.font.SysFont("Arial", 36)  # Fonte para os modos de jogo
        menu_bg_color = (70, 70, 70)  # Altera para cinza escuro
        text_color = (255, 255, 255)  # Cor do texto (branco)
        modes = ["Player vs Player", "Player vs CPU", "CPU vs CPU"]
        mode_rects = []

        for i, mode in enumerate(modes):
            # Calcula a posição e tamanho do retângulo para cada modo
            rect_x = (width - (width // 2)) // 2  # Centraliza o retângulo
            rect_y = 150 + i * 100 - 10
            rect_width = width // 2
            rect_height = 60

            # Desenha o retângulo de fundo para cada modo de jogo
            mode_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(screen, menu_bg_color, mode_rect)
            mode_rects.append(mode_rect)

            # Renderiza e desenha o texto do modo de jogo sobre o retângulo
            text = font.render(mode, True, text_color)
            text_rect = text.get_rect(center=(width // 2, 150 + i * 100))
            screen.blit(text, text_rect)

        pygame.display.update()
        return mode_rects


    def menu_screen(self):

        running = True
        mode_rects = self.draw_menu(screen)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for i, rect in enumerate(mode_rects):
                        if rect.collidepoint(x, y):
                            return i  # Retorna o índice do modo selecionado


            pygame.display.update()

    def algorithm_screen(self):
            running = True
            mode_rects = self.draw_algorithm_menu(screen)

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        for i, rect in enumerate(mode_rects):
                            if rect.collidepoint(x, y):
                                return i  # Retorna o índice do modo selecionado

                pygame.display.update()
    def draw_algorithm_menu(self, screen):
        screen.fill((200, 200, 200))  # Fundo

        # Título do submenu
        title_font = pygame.font.SysFont("comicsansms", 40)
        title_text = title_font.render("Escolha o Algoritmo", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(width // 2, 50))
        screen.blit(title_text, title_rect)

        # Opções de algoritmo
        algorithms = ["A*", "Monte Carlo"]
        algorithm_rects = []

        for i, algorithm in enumerate(algorithms):
            rect_x = (width - (width // 3)) // 2
            rect_y = 150 + i * 100
            rect_width = width // 3
            rect_height = 50

            # Desenha retângulo para cada algoritmo
            algorithm_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(screen, (70, 70, 70), algorithm_rect)
            algorithm_rects.append(algorithm_rect)

            # Texto para cada algoritmo
            font = pygame.font.SysFont("Arial", 28)
            text = font.render(algorithm, True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, 150 + i * 100))
            screen.blit(text, text_rect)

        pygame.display.update()

        return algorithm_rects

    
    

board = Board()



# No início do seu script, após inicializar o Pygame
Inicio = Menu()

mode_index = Inicio.menu_screen()

a_star = Heuristica_AStar()

Mcts = monte_carlo_tree_search(); 

if mode_index == 1 or mode_index == 2:
    algorithm_index = Inicio.algorithm_screen() 

# Main game loop
    
while not board.game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if mode_index == 0:  # Player vs Player
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                col = int(x_pos // SQUARESIZE)
                if board.drop_pieces(board.turn + 1, col):
                    if board.win(board.turn + 1):
                        print(f"Player {board.turn + 1} wins!")
                        board.game_over = True
                    board.turn = 1 - board.turn  # Troca de turnos

        elif mode_index == 1:  # Player vs CPU
            if board.turn == 0:  # Turno do jogador humano
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos = event.pos[0]
                    col = int(x_pos // SQUARESIZE)
                    if board.drop_pieces(1, col):
                        if board.win(1):
                            print("Player 1 wins!")
                            board.game_over = True
                        board.turn = 1 - board.turn  # Troca para o turno da CPU
            else:  # Turno da CPU
                if algorithm_index == 0:
                    col2 = a_star.astar_algorithm(board, 2)
                elif algorithm_index == 1: 
                    
                    col2 = Mcts.mcts(board, 2,simulations = 10000)
                    
                if board.drop_pieces(2, col2):
                    if board.win(2):
                        print("CPU wins!")
                        board.game_over = True
                    board.turn = 1 - board.turn  # Troca para o turno do jogador

        elif mode_index == 2:  # CPU vs CPU
            pygame.time.wait(100)  # Adiciona um pequeno delay para tornar as jogadas visíveis
            if(algorithm_index == 0):
                col = a_star.astar_algorithm(board, board.turn + 1)

            if board.drop_pieces(board.turn + 1, col):

                if board.win(board.turn + 1):

                    print(f"CPU {board.turn + 1} wins!")
                    board.game_over = True
                board.turn = 1 - board.turn  # Troca de turnos entre as CPUs

        draw_board(board)

        if board.is_full():
            print("The game is a draw!")
            board.game_over = True

        pygame.display.update()

        

pygame.time.wait(3000)  # Espera um pouco antes de fechar o jogo


pygame.quit()
