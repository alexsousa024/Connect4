import numpy as np 

game_over = 0
ROW_COUNT = 6
COL_COUNT = 7

class Board:
    #Método Construtor(Iniciador)
    def __init__(self):
        self.board = np.zeros((ROW_COUNT, COL_COUNT))
        self.column_heights = np.full(COL_COUNT, ROW_COUNT - 1, dtype=int)     #array com o numero de linhas desocupadas por coluna
        self.player = 1
    #Printar o Tabuleiro 
    def print_board(self):
        print(np.flip(self.board, 0))
    #Escolher a peca
        
    def drop_pieces(self, player , col):
        if self.valid_col( col ):
            height = self.column_heights[col] 
            self.board[height][col] = player
            self.column_heights[col] = height - 1
            return True
        else:
            print("Invalid move")
            return False

    def valid_col(self, col):
        if self.column_heights[col] == -1 :
            return False
        return True


board = Board()
board.print_board()


while not game_over:

    if board.player ==  1:
        play = int(input("Player 1 choose where to play (0-6):"))
        if board.drop_pieces(1,play):
            board.print_board()
            board.player = 2
    else:
        play = int(input("Player 2 choose where to play (0-6):"))
        if board.drop_pieces(2, play):
            board.print_board()
            board.player = 1