import pygame
import sys

# Define constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BROWN = (139, 69, 19)
LIGHT_BROWN = (245, 222, 179)

# Load images
def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'bp', 'br', 'bn', 'bb', 'bq', 'bk']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'assets/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))
    return images

# Handle events
def handle_events(selected, board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
            if selected:
                if (row, col) != selected:
                    move_piece(board, selected, (row, col))
                selected = None
            else:
                if board[row][col] != "--":
                    selected = (row, col)
    return selected

# Move pieces
def move_piece(board, start, end):
    piece = board[start[0]][start[1]]
    board[start[0]][start[1]] = "--"
    board[end[0]][end[1]] = piece

# Draw the board
def draw_board(window):
    colors = [LIGHT_BROWN, DARK_BROWN]
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            pygame.draw.rect(window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw the pieces
def draw_pieces(window, board, images):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "--":
                window.blit(images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Main function
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

    selected = None

    clock = pygame.time.Clock()
    while True:
        selected = handle_events(selected, board)
        draw_board(window)
        draw_pieces(window, board, images)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
