from typing import List
import pygame

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

def draw_board(window, valid_moves,selected=None):
    colors = [LIGHT_BLUE, DARK_BLUE]
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


def valid_move_decider(board: List[list[str]], piece_cord: tuple):
    valid_moves = []
    
    return valid_moves


def move_piece(board: List[list[str]], original_pos: tuple, new_pos: tuple):
    board[original_pos[0]][original_pos[1]] = board[new_pos[0]][new_pos[1]]
    return board

