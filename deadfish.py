# For Deadfish interpreter
from typing import List
import random
from board_utils import move_piece,  valid_move_decider
import copy
import threading
from piece_points_maps import pieces_points_map

points_per_piece = {
    "p": 100,
    "n": 300,
    "b": 300,
    "r": 500,
    "q": 900,
    "k": 10000
}

class DeadFish:
    def __init__(self, version_idx: int, deadfish_color: str):
        self.version_idx = version_idx
        self.king_moved = False
        self.left_rook_moved = False
        self.right_rook_moved = False
        self.deadfish_color = deadfish_color

    def move(self, board, original_pos, new_pos):
        #Pawn Promotion
        if new_pos[0] == 0 and board[original_pos[0]][original_pos[1]][1] == 'p':
            board[new_pos[0]][new_pos[1]] = board[original_pos[0]][original_pos[1]][0] + 'q'
            board[original_pos[0]][original_pos[1]] = '--'

            return board
        
        #Castling Special Case
        if board[original_pos[0]][original_pos[1]][1] == 'k' and abs(original_pos[1] - new_pos[1]) == 2:
            if new_pos[1] == 1:
                board[new_pos[0]][2] = board[new_pos[0]][0]
                board[new_pos[0]][0] = '--'
                board[new_pos[0]][new_pos[1]] = board[original_pos[0]][original_pos[1]]
                board[original_pos[0]][original_pos[1]] = '--'

            else:
                board[new_pos[0]][4] = board[new_pos[0]][7]
                board[new_pos[0]][7] = '--'
                board[new_pos[0]][new_pos[1]] = board[original_pos[0]][original_pos[1]]
                board[original_pos[0]][original_pos[1]] = '--'
            
            return board

        board[new_pos[0]][new_pos[1]] = board[original_pos[0]][original_pos[1]]
        board[original_pos[0]][original_pos[1]] = '--'

        return board

    def stalemate(self, board: List[List[str]]) -> bool:
        pieces = []
        threads = []
        stalemate_condition = True
        stalemate_lock = threading.Lock()
        
        def thread_stalemate_piece(board, piece):
            nonlocal stalemate_condition
            test_board = copy.deepcopy(board)
            valid_moves = valid_move_decider(test_board, piece, (not self.king_moved, not self.left_rook_moved, not self.right_rook_moved))
            
            valid_moves_test = valid_moves.copy()
            for move in valid_moves_test:
                test_board = copy.deepcopy(board)
                test_board = self.move(test_board, piece, move)
                if self.inCheck(test_board):
                    valid_moves.remove(move)

            if valid_moves:
                with stalemate_lock:
                    stalemate_condition = False

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece[0] == self.deadfish_color:
                    pieces.append((row, col))

        for piece in pieces:
            thread = threading.Thread(target=thread_stalemate_piece, args=(board, piece))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()

        return stalemate_condition

    def inCheck(self, board: List[List[str]]) -> bool:
        stop_event = threading.Event()
        threads = []

        def multi_thread_tester(board, piece):
            if stop_event.is_set():
                return
            
            test_board = copy.deepcopy(board)
            valid_moves = valid_move_decider(test_board, piece, (not self.king_moved, not self.left_rook_moved, not self.right_rook_moved))
            
            for move in valid_moves:
                if test_board[move[0]][move[1]][1] == 'k':
                    stop_event.set()
                    return

        opp_color = "w" if self.deadfish_color == "b" else "b"
        
        pieces = []

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece[0] == opp_color:
                    pieces.append((row, col))

        for piece in pieces:
            threads.append(threading.Thread(target=multi_thread_tester, args=(board, piece)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return stop_event.is_set()


    def make_decision(self, board: List[List[str]]) -> List[List[str]]:
        board = board[::-1]
        
        row, col, best_move =  deadfish_v1_eval(board, self)

        # Checking if rook moved
        if board[row][col][1] == "r":
            if col == 0 and not self.left_rook_moved:
                self.left_rook_moved = True
            elif row == 7 and not self.right_rook_moved:
                self.right_rook_moved = True

        # Checking if king moved
        if board[row][col][1] == "k":
            self.king_moved = True

        move_piece(board, (row, col), best_move)

        return board[::-1]


def deadfish_v1_eval(board: List[List[str]], deadfish: DeadFish, depth: int = 3, alpha: int = -100000, beta: int = 100000, maximizing_player: bool = True):
    """
    Deadfish Version 1 AI (For Deciding Moves) with Alpha-Beta Pruning and Multithreading
    """
    def evaluate_board(board: List[List[str]], deadfish: DeadFish) -> int:
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece[0] == deadfish.deadfish_color:
                    score += points_per_piece[piece[1]]
                elif piece != '--':
                    score -= points_per_piece[piece[1]]
                
                piece_position_factor = pieces_points_map[piece[1]][row][col] if piece != '--' else 0
                score += piece_position_factor
        return score

    def minimax(board: List[List[str]], depth: int, alpha: int, beta: int, maximizing_player: bool, deadfish: DeadFish) -> int:
        if depth == 0 or deadfish.stalemate(board):
            return evaluate_board(board, deadfish)

        if maximizing_player:
            max_eval = -100000
            possible_pieces = [(row, col) for row in range(8) for col in range(8) if board[row][col][0] == deadfish.deadfish_color]
            for piece_row, piece_col in possible_pieces:
                valid_moves = valid_move_decider(board, (piece_row, piece_col), (not deadfish.king_moved, not deadfish.left_rook_moved, not deadfish.right_rook_moved))
                for move in valid_moves:
                    temp_board = copy.deepcopy(board)
                    temp_board = move_piece(temp_board, (piece_row, piece_col), move)
                    if deadfish.inCheck(temp_board):
                        continue
                    eval = minimax(temp_board, depth - 1, alpha, beta, False, deadfish)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = 100000
            opp_color = "w" if deadfish.deadfish_color == "b" else "b"
            possible_pieces = [(row, col) for row in range(8) for col in range(8) if board[row][col][0] == opp_color]
            for piece_row, piece_col in possible_pieces:
                valid_moves = valid_move_decider(board, (piece_row, piece_col), (not deadfish.king_moved, not deadfish.left_rook_moved, not deadfish.right_rook_moved))
                for move in valid_moves:
                    temp_board = copy.deepcopy(board)
                    temp_board = move_piece(temp_board, (piece_row, piece_col), move)
                    if deadfish.inCheck(temp_board):
                        continue
                    eval = minimax(temp_board, depth - 1, alpha, beta, True, deadfish)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    overall_best_move = None
    overall_best_score = -100000
    possible_pieces = [(row, col) for row in range(8) for col in range(8) if board[row][col][0] == deadfish.deadfish_color]

    threads = []
    results = []

    def thread_worker(piece_row, piece_col):
        nonlocal overall_best_move, overall_best_score, alpha, beta
        valid_moves = valid_move_decider(board, (piece_row, piece_col), (not deadfish.king_moved, not deadfish.left_rook_moved, not deadfish.right_rook_moved))
        for move in valid_moves:
            temp_board = copy.deepcopy(board)
            temp_board = move_piece(temp_board, (piece_row, piece_col), move)
            if deadfish.inCheck(temp_board):
                continue
            score = minimax(temp_board, depth - 1, alpha, beta, False, deadfish)
            if score > overall_best_score:
                overall_best_score = score
                overall_best_move = (piece_row, piece_col, move)

    for piece_row, piece_col in possible_pieces:
        thread = threading.Thread(target=thread_worker, args=(piece_row, piece_col))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return overall_best_move