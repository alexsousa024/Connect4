from Jogo import *

class Connect4Game: 
    def __init__(self,player_1,player_2): 
        self.board = Board()   
        self.player_1 = player_1
        self.player_2 = player_2 

    
        

#POR A CONDICAO DE WINNING_MOVE 
#E POR NA HEURISTICA 
    def Scores(self,window,player_1,player_2):
        score = 0
        if window.count(player_1) == 3 and window.count(player_2) == 0: 
                    score -= 50
        elif window.count(player_1) == 2 and window.count(player_2) == 0: 
                    score -= 10
        elif window.count(player_1) == 1  and window.count(player_2) == 0: 
                    score -= 1
        elif window.count(player_1) == 0 and window.count(player_2) == 0: 
                    score += 0 
        elif window.count(player_1) == 0 and window.count(player_2) == 1: 
                    score += 1
        elif window.count(player_1) == 0 and window.count(player_2) == 2: 
                    score += 10
        elif window.count(player_1) == 0 and window.count(player_2) == 3: 
                    score += 50
        
        return score

    
            
    #Funcap de heurística #1 - Jananlas de 4 em 4 
    def evaluate_function_1(self,player_1,player_2):
        score = 0
        
        #horizontalmente
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT - 3): 
                window = board[r][c:c+4]
                
                score += self.Scores(window,self.player_1,self.player_2)
        
    
        #verticalmente
        for r in range(ROW_COUNT-3):
            for c in range(ROW_COUNT): 
                window = board[r][c:c+4]
                
                score += self.Scores(window,self.player_1,self.player_2)
