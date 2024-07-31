import pygame
import sys

# Define constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 105, 153)
LIGHT_BLUE = (230, 247, 255)
HIGHLIGHT_COLOR1 = (255, 179, 179)
HIGHLIGHT_COLOR2 = (255, 102, 102)
PIECE_COLOR = (102, 153, 255)

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

    #Checking if Pawn is Promoting
    if end[0] == 0 and piece == 'wp':
        board[end[0]][end[1]] = 'wq'

    if end[0] == 7 and piece == 'bp':
        board[end[0]][end[1]] = 'bq'

# Possible Moves
def highlight_moves(board, coords):
    piece = board[coords[0]][coords[1]]
    highlights = []

    if piece == 'wp':
        if coords[0] == 6 and board[coords[0] - 1][coords[1]] == '--':
            highlights.append((coords[0] - 1, coords[1]))
            if board[coords[0] - 2][coords[1]] == '--':
                highlights.append((coords[0] - 2, coords[1]))

        elif board[coords[0] - 1][coords[1]] == '--':
            highlights.append((coords[0] - 1, coords[1]))

        if coords[1] + 1 < 8 and board[coords[0] - 1][coords[1] + 1] != "--" and board[coords[0] - 1][coords[1] + 1][0] == 'b':
            highlights.append((coords[0] - 1, coords[1] + 1))

        if coords[1] - 1 >= 0 and board[coords[0] - 1][coords[1] - 1] != "--" and board[coords[0] - 1][coords[1] - 1][0] == 'b':
            highlights.append((coords[0] - 1, coords[1] - 1))

    elif piece == 'bp':
        if coords[0] == 1 and board[coords[0] + 1][coords[1]] == '--':
            highlights.append((coords[0] + 1, coords[1]))   
            if board[coords[0] + 2][coords[1]] == '--':
                highlights.append((coords[0] + 2, coords[1]))

        else:
            if board[coords[0] + 1][coords[1]] == '--':
                highlights.append((coords[0] + 1, coords[1]))

        if coords[1] + 1 < 8 and board[coords[0] + 1][coords[1] + 1] != "--" and board[coords[0] + 1][coords[1] + 1][0] == 'w':
            highlights.append((coords[0] + 1, coords[1] + 1))

        if coords[1] - 1 >= 0 and board[coords[0] + 1][coords[1] - 1] != "--" and board[coords[0] + 1][coords[1] - 1][0] == 'w':
            highlights.append((coords[0] + 1, coords[1] - 1))
        
    elif piece[1] == 'r':
        row, col = coords[0] + 1, coords[1]
        opponent = "w" if piece[0] == "b" else "b"

        while row <= 7:
            if board[row][col] == "--":
                highlights.append((row,col))
                row += 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break

        row, col = coords[0] - 1, coords[1]
        while row >= 0:
            if board[row][col] == "--":
                highlights.append((row,col))
                row -= 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break

        row, col = coords[0], coords[1] - 1
        while col >= 0:
            if board[row][col] == "--":
                highlights.append((row,col))
                col -= 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break

        row, col = coords[0], coords[1] + 1
        while col <= 7:
            if board[row][col] == "--":
                highlights.append((row,col))
                col += 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break

    return highlights

def draw_board(window, highlights,selected=None):
    colors = [LIGHT_BLUE, DARK_BLUE]
    for row in range(ROWS):
        for col in range(COLS):
            if (row, col) in highlights:
                color = [HIGHLIGHT_COLOR1,HIGHLIGHT_COLOR2][(row + col) % 2]
            else:
                color = colors[(row + col) % 2]
            
            if selected and (row,col) == selected:
                color = PIECE_COLOR

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
        draw_board(window, highlights,selected)
        draw_pieces(window, board, images)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
