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

        board = board
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
        print("Move Selected")

        move_piece(board, (row, col), best_move)

        return board[::-1]


def deadfish_v1_eval(board: List[List[str]], deadfish: DeadFish):
    """
    Deadfish Version 1 AI (For Deciding Moves)
    """
    best_move = None
    eval_board = copy.deepcopy(board)
    best_score = -1000000
    
    for row in range(8):
        for col in range(8):
            piece = eval_board[row][col]
            if piece[0] == deadfish.deadfish_color:
                valid_moves = valid_move_decider(eval_board, (row, col), (not deadfish.king_moved, not deadfish.left_rook_moved, not deadfish.right_rook_moved))

                for move in valid_moves:
                    temp_board = copy.deepcopy(eval_board)
                    temp_board = move_piece(temp_board, (row, col), move)
                    if deadfish.inCheck(temp_board):
                        valid_moves.remove(move)

                for move in valid_moves:
                    temp_board = copy.deepcopy(eval_board)
                    temp_board = move_piece(temp_board, (row, col), move)
                    score = 0

                    for row in range(8):
                        for col in range(8):
                            piece = temp_board[row][col]
                            if piece[0] == deadfish.deadfish_color:
                                score += points_per_piece[piece[1]]
                            elif piece != '--':
                                score -= points_per_piece[piece[1]]

                    if score > best_score:
                        best_score = score
                        best_move = (row, col, move)

    return best_move