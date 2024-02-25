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
        print(self.board)
    #Escolher a peca
    
    #Funcao que coloca a peca escolhida no tabuleiro 
        
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
    
    #Condicoes quando ganha um player

    def win(self,player): 
        #Verificar horizontal
        for c in range(COL_COUNT-3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == player and self.board[r][c+1] == player and self.board[r][c+1] == player and self-board[r][c+1] == player:
                    return True
        #Verificar vertical
                
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == player and self.board[r+1][c] == player and self.board[r+2][c] and self.board[r+3][c] == player: 
                    return True
        #Verificar diagonal com declive positivo
        for c in range(COL_COUNT - 3):
            for r in range(ROW_COUNT -3):
                if self.board[r][c] == player and self.board[r+1][c+1] == player and self.board[r+2][c+2] == player and self.board[r+3][c+3] == player: 
                    return True 
        #Verificar diagonal com decline negativo 
        for c in range(COL_COUNT - 3):
            for r in range(3,ROW_COUNT):
                if self.board[r][c] == player and self.board[r-1][c+1] == player and self.board[r-2][c+2] == player and self.board[r-3][c+3] == player: 
                    return True
                
        return False 
                


board = Board()
board.print_board()


while not game_over:

    if board.player ==  1:
        play = int(input("Player 1 choose where to play (0-6):"))
        if board.drop_pieces(1,play):
            if board.win(board.player):
                print("Player 1 Wins!")
                game_over = 1
            board.print_board()
            board.player = 2
    else:
        play = int(input("Player 2 choose where to play (0-6):"))
        if board.drop_pieces(2, play):
            if board.win(board.player):
                print("Player 2 Wins!")
                game_over = 1 
            board.print_board()
            board.player = 1
