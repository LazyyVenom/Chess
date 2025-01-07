# For Deadfish interpreter
from typing import List
from valid_moves_check import Valid_Moves
import random
from board_utils import move_piece, check
import copy


class DeadFish:
    def __init__(self, version_idx: int):
        self.version_idx = version_idx
        self.king_moved = False
        self.left_rook_moved = False
        self.right_rook_moved = False

    def move(self, board: List[List[str]], deadfish_color: str) -> List[List[str]]:
        board = board[::-1]
        possible_pieces = []

        for row, board_row in enumerate(board):
            for col, piece in enumerate(board_row):
                if piece[0] == deadfish_color:
                    possible_pieces.append((row, col))

        # for piece in possible_pieces:
        while True:
            piece = random.choice(possible_pieces)
            row, col = piece
            piece = board[row][col]

            if piece[1] == "p":
                valid_moves = Valid_Moves.check_pawn(board, (row, col), deadfish_color)
            elif piece[1] == "n":
                valid_moves = Valid_Moves.check_knight(
                    board, (row, col), deadfish_color
                )
            elif piece[1] == "b":
                valid_moves = Valid_Moves.check_bishop(
                    board, (row, col), deadfish_color
                )
            elif piece[1] == "r":
                valid_moves = Valid_Moves.check_rook(board, (row, col), deadfish_color)
            elif piece[1] == "q":
                valid_moves = Valid_Moves.check_queen(board, (row, col), deadfish_color)
            elif piece[1] == "k":
                valid_moves = Valid_Moves.check_king(
                    board,
                    (row, col),
                    deadfish_color,
                    (
                        not self.king_moved,
                        not self.left_rook_moved,
                        not self.right_rook_moved,
                    ),
                )
            else:
                raise ValueError("Invalid piece")

            new_valid_moves = valid_moves.copy()

            opp_color = "w" if deadfish_color == "b" else "b"

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
                    elif row == 7 and not self.right_rook_moved:
                        self.right_rook_moved = True

                # Checking if king moved
                if board[row][col][1] == "k":
                    self.king_moved = True

                board = move_piece(board, (row, col), move)
                return board[::-1]

        return board[::-1]