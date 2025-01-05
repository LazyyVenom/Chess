# For checking specific moves for a piece
from typing import List


class Valid_Moves:
    @staticmethod
    def check_pawn(board: List[List[str]], coords: tuple, player: str):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []

        if player != piece_color:
            return possible_moves

        if board[coords[0] - 1][coords[1]] == "--":
            possible_moves.append((coords[0] - 1, coords[1]))

        if coords[0] == 6 and board[coords[0] - 2][coords[1]] == "--":
            possible_moves.append((coords[0] - 2, coords[1]))

        if (
            -1 < coords[1] - 1
            and board[coords[0] - 1][coords[1] - 1][0] != player
            and board[coords[0] - 1][coords[1] - 1] != "--"
        ):
            possible_moves.append((coords[0] - 1, coords[1] - 1))

        if (
            coords[1] + 1 < 8
            and board[coords[0] - 1][coords[1] + 1][0] != player
            and board[coords[0] - 1][coords[1] + 1] != "--"
        ):
            possible_moves.append((coords[0] - 1, coords[1] + 1))

        return possible_moves

    @staticmethod
    def check_knight(board: List[List[str]], coords: tuple, player: str):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []

        if player != piece_color:
            return possible_moves

        if coords[0] - 2 >= 0:
            if coords[1] - 1 >= 0 and board[coords[0] - 2][coords[1] - 1][0] != player:
                possible_moves.append((coords[0] - 2, coords[1] - 1))

            if coords[1] + 1 < 8 and board[coords[0] - 2][coords[1] + 1][0] != player:
                possible_moves.append((coords[0] - 2, coords[1] + 1))

        if coords[0] + 2 < 8:
            if coords[1] - 1 >= 0 and board[coords[0] + 2][coords[1] - 1][0] != player:
                possible_moves.append((coords[0] + 2, coords[1] - 1))

            if coords[1] + 1 < 8 and board[coords[0] + 2][coords[1] + 1][0] != player:
                possible_moves.append((coords[0] + 2, coords[1] + 1))

        if coords[1] - 2 >= 0:
            if coords[0] - 1 >= 0 and board[coords[0] - 1][coords[1] - 2][0] != player:
                possible_moves.append((coords[0] - 1, coords[1] - 2))

            if coords[0] + 1 < 8 and board[coords[0] + 1][coords[1] - 2][0] != player:
                possible_moves.append((coords[0] + 1, coords[1] - 2))

        if coords[1] + 2 < 8:
            if coords[0] - 1 >= 0 and board[coords[0] - 1][coords[1] + 2][0] != player:
                possible_moves.append((coords[0] - 1, coords[1] + 2))

            if coords[0] + 1 < 8 and board[coords[0] + 1][coords[1] + 2][0] != player:
                possible_moves.append((coords[0] + 1, coords[1] + 2))

        return possible_moves

    @staticmethod
    def check_king(
        board: List[List[str]],
        coords: tuple,
        player: str,
        king_for_castling: bool = True,
        left_rook_for_castling: bool = True,
        right_rook_for_castling: bool = True,
    ):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []

        if player != piece_color:
            return possible_moves

        if coords[0] - 1 >= 0:
            if coords[1] - 1 >= 0 and board[coords[0] - 1][coords[1] - 1][0] != player:
                possible_moves.append((coords[0] - 1, coords[1] - 1))

            if board[coords[0] - 1][coords[1]][0] != player:
                possible_moves.append((coords[0] - 1, coords[1]))

            if coords[1] + 1 < 8 and board[coords[0] - 1][coords[1] + 1][0] != player:
                possible_moves.append((coords[0] - 1, coords[1] + 1))

        if coords[0] + 1 < 8:
            if coords[1] - 1 >= 0 and board[coords[0] + 1][coords[1] - 1][0] != player:
                possible_moves.append((coords[0] + 1, coords[1] - 1))

            if board[coords[0] + 1][coords[1]][0] != player:
                possible_moves.append((coords[0] + 1, coords[1]))

            if coords[1] + 1 < 8 and board[coords[0] + 1][coords[1] + 1][0] != player:
                possible_moves.append((coords[0] + 1, coords[1] + 1))

        if coords[1] - 1 >= 0 and board[coords[0]][coords[1] - 1][0] != player:
            possible_moves.append((coords[0], coords[1] - 1))

        if coords[1] + 1 < 8 and board[coords[0]][coords[1] + 1][0] != player:
            possible_moves.append((coords[0], coords[1] + 1))

        return possible_moves

    @staticmethod
    def check_queen(board: List[List[str]], coords: tuple, player: str):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []

        if player != piece_color:
            return possible_moves

        possible_moves += Valid_Moves.check_rook(board, coords, player)
        possible_moves += Valid_Moves.check_bishop(board, coords, player)

        return possible_moves

    @staticmethod
    def check_rook(board: List[List[str]], coords: tuple, player: str):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []

        if player != piece_color:
            return possible_moves

        if coords[0] - 1 >= 0:
            for i in range(coords[0] - 1, -1, -1):
                if board[i][coords[1]][0] == player:
                    break
                possible_moves.append((i, coords[1]))
                if board[i][coords[1]] != "--":
                    break

        if coords[0] + 1 < 8:
            for i in range(coords[0] + 1, 8):
                if board[i][coords[1]][0] == player:
                    break
                possible_moves.append((i, coords[1]))
                if board[i][coords[1]] != "--":
                    break

        if coords[1] - 1 >= 0:
            for i in range(coords[1] - 1, -1, -1):
                if board[coords[0]][i][0] == player:
                    break
                possible_moves.append((coords[0], i))
                if board[coords[0]][i] != "--":
                    break

        if coords[1] + 1 < 8:
            for i in range(coords[1] + 1, 8):
                if board[coords[0]][i][0] == player:
                    break
                possible_moves.append((coords[0], i))
                if board[coords[0]][i] != "--":
                    break

        return possible_moves

    @staticmethod
    def check_bishop(board: List[List[str]], coords: tuple, player: str):
        piece_color = board[coords[0]][coords[1]][0]
        possible_moves = []

        if player != piece_color:
            return possible_moves

        if coords[0] - 1 >= 0 and coords[1] - 1 >= 0:
            for i in range(1, min(coords[0], coords[1]) + 1):
                if board[coords[0] - i][coords[1] - i][0] == player:
                    break
                possible_moves.append((coords[0] - i, coords[1] - i))
                if board[coords[0] - i][coords[1] - i] != "--":
                    break

        if coords[0] - 1 >= 0 and coords[1] + 1 < 8:
            for i in range(1, min(coords[0], 8 - coords[1])):
                if board[coords[0] - i][coords[1] + i][0] == player:
                    break
                possible_moves.append((coords[0] - i, coords[1] + i))
                if board[coords[0] - i][coords[1] + i] != "--":
                    break

        if coords[0] + 1 < 8 and coords[1] - 1 >= 0:
            for i in range(1, min(8 - coords[0], coords[1] + 1)):
                if board[coords[0] + i][coords[1] - i][0] == player:
                    break
                possible_moves.append((coords[0] + i, coords[1] - i))
                if board[coords[0] + i][coords[1] - i] != "--":
                    break

        if coords[0] + 1 < 8 and coords[1] + 1 < 8:
            for i in range(1, min(8 - coords[0], 8 - coords[1])):
                if board[coords[0] + i][coords[1] + i][0] == player:
                    break
                possible_moves.append((coords[0] + i, coords[1] + i))
                if board[coords[0] + i][coords[1] + i] != "--":
                    break

        return possible_moves
