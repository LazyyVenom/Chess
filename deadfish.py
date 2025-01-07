# For Deadfish interpreter
from typing import List
from valid_moves_check import Valid_Moves
import random
from board_utils import move_piece, check, valid_move_decider
import copy

class DeadFish:
    def __init__(self, version_idx: int, deadfish_color: str):
        self.version_idx = version_idx
        self.king_moved = False
        self.left_rook_moved = False
        self.right_rook_moved = False
        self.deadfish_color = deadfish_color

    def stalemate(self, board: List[List[str]]) -> bool:
        pieces = []

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece[0] == self.deadfish_color:
                    pieces.append((row,col))
        
        for piece in pieces:
            valid_moves = valid_move_decider(board, piece, (not self.king_moved,not self.left_rook_moved,not self.right_rook_moved))
            if valid_moves:
                return False

        return True

    def inCheck(self, board: List[List[str]]) -> bool:
        opp_color = "w" if self.deadfish_color == "b" else "b"

        pieces = []

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece[0] == opp_color:
                    pieces.append((row,col))
        
        for piece in pieces:
            valid_moves = valid_move_decider(board, piece, (not self.king_moved,not self.left_rook_moved,not self.right_rook_moved))
            for move in valid_moves:
                if board[move[0]][move[1]][1] == 'k':
                    return True

        return False

    def move(self, board: List[List[str]]) -> List[List[str]]:
        board = board[::-1]
        possible_pieces = []

        for row, board_row in enumerate(board):
            for col, piece in enumerate(board_row):
                if piece[0] == self.deadfish_color:
                    possible_pieces.append((row, col))

        # for piece in possible_pieces:
        while True:
            piece = random.choice(possible_pieces)
            row, col = piece

            valid_moves = valid_move_decider(board, piece, (not self.king_moved,not self.left_rook_moved,not self.right_rook_moved))

            new_valid_moves = valid_moves.copy()

            opp_color = "w" if self.deadfish_color == "b" else "b"

            for move in new_valid_moves:
                temp_board = copy.deepcopy(board)
                temp_board = move_piece(temp_board, (row, col), move)
                if check(temp_board[::-1], opp_color):
                    valid_moves.remove(move)

            # for move in valid_moves:
            if valid_moves:
                move = random.choice(valid_moves)

                # Checking if rook moved
                if board[row][col][1] == "r":
                    if col == 0 and not self.left_rook_moved:
                        self.left_rook_moved = True
                        print("Left rook moved")
                    elif row == 7 and not self.right_rook_moved:
                        self.right_rook_moved = True
                        print("Right rook moved")

                # Checking if king moved
                if board[row][col][1] == "k":
                    self.king_moved = True
                    print("King moved")

                board = move_piece(board, (row, col), move)
                return board[::-1]

        return board[::-1]