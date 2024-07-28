import pygame
import sys

# Define constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BROWN = (139, 69, 19)
LIGHT_BROWN = (245, 222, 179)

def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'bp', 'br', 'bn', 'bb', 'bq', 'bk']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'assets/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))
    return images

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def draw_board(window):
    colors = [LIGHT_BROWN, DARK_BROWN]
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            pygame.draw.rect(window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(window, board, images):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "--":
                window.blit(images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess')

    images = load_images()

    board = [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
    ]

    while True:
        handle_events()
        draw_board(window)
        draw_pieces(window, board, images)
        pygame.display.flip()
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()
