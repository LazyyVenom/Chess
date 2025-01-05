#For Deadfish interpreter
from typing import List, Callable
from valid_moves_check import Valid_Moves
import random
from board_utils import move_piece

def deadfish(board: List[List[str]],deadfish_color: str ,deciding_function: Callable):
    board = board[::-1]
    possible_pieces = []

    for row, board_row in enumerate(board):
        for col, piece in enumerate(board_row):
            if piece[0] == deadfish_color:
                possible_pieces.append((row,col))

    # for piece in possible_pieces:
    while True:
        piece = random.choice(possible_pieces)
        row, col = piece
        piece = board[row][col]

        if piece[1] == 'p':
            valid_moves = Valid_Moves.check_pawn(board, (row, col), deadfish_color)
        elif piece[1] == 'n':
            valid_moves = Valid_Moves.check_knight(board, (row, col), deadfish_color)
        elif piece[1] == 'b':
            valid_moves = Valid_Moves.check_bishop(board, (row, col), deadfish_color)
        elif piece[1] == 'r':
            valid_moves = Valid_Moves.check_rook(board, (row, col), deadfish_color)
        elif piece[1] == 'q':
            valid_moves = Valid_Moves.check_queen(board, (row, col), deadfish_color)
        elif piece[1] == 'k':
            valid_moves = Valid_Moves.check_king(board, (row, col), deadfish_color)
        else:
            raise ValueError('Invalid piece')
        
        # for move in valid_moves:
        if valid_moves:
            move = random.choice(valid_moves)

            board = move_piece(board, (row, col), move)
            return board[::-1]

    return board
