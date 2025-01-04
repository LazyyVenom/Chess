#For checking specific moves for a piece
from typing import List

class Valid_Moves:
    @staticmethod
    def check_pawn(board: List[List[str]], coords: tuple, player: str):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []

        if player != piece_color:
            return possible_moves
    
        if board[coords[0] - 1][coords[1]] == '--':
            possible_moves.append((coords[0] - 1, coords[1]))

        if coords[0] == 6 and board[coords[0] - 2][coords[1]] == '--':
            possible_moves.append((coords[0] - 2, coords[1]))
        
        if board[coords[0] - 1][coords[1] - 1][0] != player and board[coords[0] - 1][coords[1] - 1] != '--':
            possible_moves.append((coords[0] - 1, coords[1] - 1))
        
        if board[coords[0] - 1][coords[1] + 1][0] != player and board[coords[0] - 1][coords[1] + 1] != '--':
            possible_moves.append((coords[0] - 1, coords[1] + 1))
        
        return possible_moves
    
    @staticmethod
    def check_knight(board: List[List[str]], coords: tuple, player: str):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []
        
        if player != piece_color:
            return possible_moves
        
        if coords[0] - 2 >= 0 and coords[1] - 1 >= 0 and board[coords[0] - 2][coords[1] - 1][0] != player:
            possible_moves.append((coords[0] - 2, coords[1] - 1))
            

        return []
    
    @staticmethod
    def check_king(board: List[List[str]], coords: tuple, player: str):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []
        
        if player != piece_color:
            return possible_moves
        
        return []

    @staticmethod
    def check_queen(board: List[List[str]], coords: tuple, player: str):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []
        
        if player != piece_color:
            return possible_moves
        
        return []

    @staticmethod
    def check_rook(board: List[List[str]], coords: tuple, player: str):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []
        
        if player != piece_color:
            return possible_moves
        
        return []

    @staticmethod
    def check_bishop(board: List[List[str]], coords: tuple, player: str):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []
        
        if player != piece_color:
            return possible_moves
        
        return []