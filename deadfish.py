# For Deadfish interpreter
from typing import List
from valid_moves_check import Valid_Moves
import random
from board_utils import move_piece, check, valid_move_decider
import copy
import threading
from multiprocessing import Process

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
        processes = []
        stalemate_condition = True

        def process_stalemate_piece(board, piece):
            test_board = copy.deepcopy(board)
            valid_moves = valid_move_decider(test_board, piece, (not self.king_moved,not self.left_rook_moved,not self.right_rook_moved))
            
            valid_moves_test = valid_moves.copy()
            for move in valid_moves_test:
                test_board = copy.deepcopy(board)
                test_board = self.move(test_board, piece, move)
                if self.inCheck(test_board):
                    valid_moves.remove(move)

            if valid_moves:
                for process in processes:
                    process.terminate()
                    global stalemate_condition
                    stalemate_condition = False
                return False
            
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece[0] == self.deadfish_color:
                    pieces.append((row,col))

        for piece in pieces:
            processes.append(Process(target=process_stalemate_piece, args=(board, piece)))
        
        for process in processes:
            process.start()
        
        for process in processes:
            process.join()

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
                if self.inCheck(temp_board[::-1]):
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

                board = self.move(board, (row, col), move)
                return board[::-1]

        return board[::-1]
    