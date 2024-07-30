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
HIGHLIGHT_COLOR1 = (200, 100, 100)
HIGHLIGHT_COLOR2 = (200, 50, 50)

# Load images
def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'bp', 'br', 'bn', 'bb', 'bq', 'bk']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'assets/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))
    return images

# Handle events
def handle_events(selected, board, highlights):
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
                    highlights = []
                else:
                    selected = None
                    highlights = []
            else:
                if board[row][col] != "--":
                    selected = (row, col)
                    highlights = highlight_moves(board, selected)
    return selected, highlights

# Move pieces
def move_piece(board, start, end):
    piece = board[start[0]][start[1]]
    board[start[0]][start[1]] = "--"
    board[end[0]][end[1]] = piece

# Possible Moves
def highlight_moves(board, coords):
    piece = board[coords[0]][coords[1]]
    highlights = []
    if piece == 'wp':
        if coords[0] == 6:
            highlights = [(coords[0] - 1, coords[1]), (coords[0] - 2, coords[1])]
        else:
            highlights = [(coords[0] - 1, coords[1])]

        if coords[1] + 1 < 8 and board[coords[0] - 1][coords[1] + 1] != "--":
            highlights.append((coords[0] - 1, coords[1] + 1))

        if coords[1] - 1 >= 0 and board[coords[0] - 1][coords[1] - 1] != "--":
            highlights.append((coords[0] - 1, coords[1] - 1))

    elif piece == 'bp':
        if coords[0] == 1:
            highlights = [(coords[0] + 1, coords[1]), (coords[0] + 2, coords[1])]
        else:
            highlights = [(coords[0] + 1, coords[1])]

        if coords[1] + 1 < 8 and board[coords[0] + 1][coords[1] + 1] != "--":
            highlights.append((coords[0] + 1, coords[1] + 1))

        if coords[1] - 1 >= 0 and board[coords[0] + 1][coords[1] - 1] != "--":
            highlights.append((coords[0] + 1, coords[1] - 1))
        
    return highlights

# Draw the board
def draw_board(window, highlights):
    colors = [LIGHT_BROWN, DARK_BROWN]
    for row in range(ROWS):
        for col in range(COLS):
            if (row, col) in highlights:
                color = [HIGHLIGHT_COLOR1,HIGHLIGHT_COLOR2][(row + col) % 2]
            else:
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
    highlights = []

    clock = pygame.time.Clock()
    while True:
        selected, highlights = handle_events(selected, board, highlights)
        draw_board(window, highlights)
        draw_pieces(window, board, images)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
