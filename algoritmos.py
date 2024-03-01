import numpy as np

ROW_COUNT = 6
COL_COUNT = 7 

class Connect4Game: 
    def __init__(self,player_1,player_2,board): 
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2 

#POR A CONDICAO DE WINNING_MOVE 
#E POR NA HEURISTICA 
        
    #Funcao de Pontuacao base 
        
    def Scores(self, window):
        score = 0
        # Contar vitórias absolutas
        print("Window:", window)  # Debugging: Imprime a janela atual

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


    def board_evaluation(self,player_1,player_2):
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
                if self.board[r][c] == player_1:  # Posição ocupada pelo jogador 1
                    player_score -= board_score_matrix[r][c]
                elif self.board[r][c] == player_2:  # Posição ocupada pelo jogador 2
                    player_score += board_score_matrix[r][c]
        
        return player_score

    
            
    #Funcap de heurística #1 - Jananlas de 4 em 4 
    def evaluate_function_1(self):
        score = 0
        
        #horizontalmente
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT - 3): 
                window = self.board[r][c:c+4]
                
                score += self.Scores(window)
        
    
        #verticalmente
        for r in range(ROW_COUNT-3):
            for c in range(COL_COUNT): 
                window = np.array([self.board[r+i][c] for i in range(4)])
                
                score += self.Scores(window)

        #diagonalente com declive negativo 
        for r in range(ROW_COUNT-3):
            for c in range(COL_COUNT-3):
                window = np.array([self.board[r+i][c+i] for i in range(4)])
                score += self.Scores(window)

    # diagonalmente com declive positivo 
        for r in range(ROW_COUNT-3):
            for c in range(COL_COUNT-1, 2, -1):
                window = np.array([self.board[r+i][c-i] for i in range(4)])
                score += self.Scores(window)

        return score
    
    def final_heuristic_1(self,player_1, player_2):

        eval_score = self.evaluate_function_1()
        board_score = self.board_evaluation(player_1,player_2)
        

        total_score = eval_score + board_score

        
        return total_score

