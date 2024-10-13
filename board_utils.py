import pygame

DARK_BLUE = (0, 105, 153)
LIGHT_BLUE = (230, 247, 255)
HIGHLIGHT_COLOR1 = (255, 179, 179)
HIGHLIGHT_COLOR2 = (255, 102, 102)
PIECE_PLACEMENT_COLOR = (102, 153, 255)
SQUARE_SIZE = 75

def draw_board(window, highlights,selected=None):
    colors = [LIGHT_BLUE, DARK_BLUE]
    for row in range(8):
        for col in range(8):
            if (row, col) in highlights:
                color = [HIGHLIGHT_COLOR1,HIGHLIGHT_COLOR2][(row + col) % 2]
            else:
                color = colors[(row + col) % 2]
            
            if selected and (row,col) == selected:
                color = PIECE_PLACEMENT_COLOR

            pygame.draw.rect(window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
