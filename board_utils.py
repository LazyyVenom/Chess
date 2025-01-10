from typing import List
import pygame
from valid_moves_check import Valid_Moves
import threading
from copy import deepcopy

DARK_BLUE = (0, 105, 153)
LIGHT_BLUE = (230, 247, 255)
HIGHLIGHT_COLOR1 = (255, 179, 179)
HIGHLIGHT_COLOR2 = (255, 102, 102)
PIECE_PLACEMENT_COLOR = (102, 153, 255)
SQUARE_SIZE = 75
pygame.font.init()
player_info_font_primary = pygame.font.Font(None, 50)

def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'bp', 'br', 'bn', 'bb', 'bq', 'bk']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'assets/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))
    return images

images = load_images()

def draw_board(window, valid_moves,selected=None,player_color='w'):
    if player_color == 'b':
        colors = [LIGHT_BLUE, DARK_BLUE]
    else:
        colors = [DARK_BLUE, LIGHT_BLUE]
    for row in range(8):
        for col in range(8):
            if (row, col) in valid_moves:
                color = [HIGHLIGHT_COLOR1,HIGHLIGHT_COLOR2][(row + col) % 2]
            else:
                color = colors[(row + col) % 2]
            
            if selected and (row,col) == selected:
                color = PIECE_PLACEMENT_COLOR

            pygame.draw.rect(window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_players_info(screen,selected_color: str,selected_version: str):
    logo = pygame.image.load(f"assets/{selected_color}k.png")

    opp = 'b' if selected_color == 'w' else 'w'
    opp_logo = pygame.image.load(f"assets/{opp}k.png")

    screen.blit(opp_logo, (620, 100))
    screen.blit(player_info_font_primary.render(selected_version, True, (255, 255, 255)),(750,160))

    screen.blit(logo, (620, 400))
    screen.blit(player_info_font_primary.render("Player", True, (255, 255, 255)),(750,460))


def draw_pieces(screen,board: List[list[str]]):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece != '--':
                screen.blit(images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))


def valid_move_decider(board: List[list[str]], piece_cord: tuple, king_details: tuple = (True, True, True)):
    valid_moves = []

    if not piece_cord:
        return []
    
    piece = board[piece_cord[0]][piece_cord[1]]

    if piece[1] == 'p':
        valid_moves = Valid_Moves.check_pawn(board, piece_cord, piece[0])
    elif piece[1] == 'r':
        valid_moves = Valid_Moves.check_rook(board, piece_cord, piece[0])
    elif piece[1] == 'n':
        valid_moves = Valid_Moves.check_knight(board, piece_cord, piece[0])
    elif piece[1] == 'b':
        valid_moves = Valid_Moves.check_bishop(board, piece_cord, piece[0])
    elif piece[1] == 'q':
        valid_moves = Valid_Moves.check_queen(board, piece_cord, piece[0])
    elif piece[1] == 'k':
        valid_moves = Valid_Moves.check_king(board, piece_cord, piece[0], king_details[0], king_details[1], king_details[2])

    return valid_moves


def move_piece(board: List[list[str]], original_pos: tuple, new_pos: tuple):
    #Pawn Promotion
    if new_pos[0] == 0 and board[original_pos[0]][original_pos[1]][1] == 'p':
        board[new_pos[0]][new_pos[1]] = board[original_pos[0]][original_pos[1]][0] + 'q'
        board[original_pos[0]][original_pos[1]] = '--'

        return board
    
    #Castling Special Case
    global king_moved, left_rook_moved, right_rook_moved
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


def check(updated_board: List[list[str]], opp_color: str, DeadFish):
    pieces = []
    stop_event = threading.Event()
    threads = []

    def multi_thread_tester(board, piece):
        if stop_event.is_set():
            return
        
        valid_moves = valid_move_decider(updated_board, piece, (not DeadFish.king_moved,not DeadFish.left_rook_moved,not DeadFish.right_rook_moved))
        for move in valid_moves:
            if updated_board[move[0]][move[1]][1] == 'k':
                stop_event.set()
                return

    for row in range(8):
        for col in range(8):
            piece = updated_board[row][col]
            if piece[0] == opp_color:
                pieces.append((row,col))
    
    for piece in pieces:
        new_board = deepcopy(updated_board)
        new_board = move_piece(new_board, piece, piece)
        thread = threading.Thread(target=multi_thread_tester, args=(new_board, piece))
        threads.append(threads)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

    return stop_event.is_set()


def stalemate(board: List[list[str]], color: str):
    pieces = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece[0] == color:
                pieces.append((row,col))
    
    for piece in pieces:
        valid_moves = valid_move_decider(board, piece)
        if valid_moves:
            return False

    return True