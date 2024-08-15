from typing import List
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
PIECE_PLACEMENT_COLOR = (102, 153, 255)

b_king_available = True
b_l_rook_available = True
b_rook_available = True
w_king_available = True
w_l_rook_available = True
w_rook_available = True

# Load images
def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'bp', 'br', 'bn', 'bb', 'bq', 'bk']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'assets/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))
    return images

# Handle events
def handle_events(selected, board, highlights,turn):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
            if selected:
                if (row, col) != selected:
                    turn = move_piece(board, selected, (row, col),highlights,turn)
                    selected = None
                    highlights = []
                else:
                    selected = None
                    highlights = []
            else:
                if board[row][col] != "--":
                    if turn and board[row][col][0] == "w":
                        selected = (row, col)
                        highlights = highlight_moves(board, selected)

                    elif not turn and board[row][col][0] == "b":
                        selected = (row, col)
                        highlights = highlight_moves(board, selected)

    return selected, highlights, turn

# Move pieces
def move_piece(board, start, end, highlights, turn):
    if end not in highlights:
        return turn

    piece = board[start[0]][start[1]]
    board[start[0]][start[1]] = "--"
    board[end[0]][end[1]] = piece

    #Checking if Pawn is Promoting
    if end[0] == 0 and piece == 'wp':
        board[end[0]][end[1]] = 'wq'

    if end[0] == 7 and piece == 'bp':
        board[end[0]][end[1]] = 'bq'

    #Castling Limiter Here
    if piece[1] == 'k':
        if piece[0] == 'b':
            b_king_available = False
        else:
            w_king_available = False

    #Checking if its Castling.
    if piece == 'wk':
        if start == (7,4) and end == (7,2):
            board[7][0] = "--"
            board[7][3] = "wr"
        elif start == (7,4) and end == (7,6):
            board[7][7] = "--"
            board[7][5] = "wr"
    
    elif piece == 'bk':
        if start == (0,4) and end == (0,2):
            board[0][0] = "--"
            board[0][3] = "br"
        elif start == (0,4) and end == (0,6):
            board[0][7] = "--"
            board[0][5] = "br"

    if piece[1] == 'r':
        if piece[0] == 'b':
            if start == (0,0):
                b_l_rook_available = False
            elif start == (0,7):
                b_rook_available = False

        else:
            if start == (7,0):
                b_l_rook_available = False
            elif start == (7,7):
                b_rook_available = False

    return not turn

def king_can_be_captured(king_cords, board: List[list[str]],highlights: List[tuple]):
    opp_color = 'w' if board[king_cords[0]][king_cords[1]][0] == 'b' else 'b'
    king_color = board[king_cords[0]][king_cords[1]][0]
    old_highlights = highlights.copy()

    old_board = board.copy()

    for king_move in old_highlights:
        board[king_cords[0]][king_cords[1]] == '--'
        board[king_move[0]][king_move[1]] == f'{king_color}k'

        for i in range(8):
            for j in range(8):
                if board[i][j][1] == 'k':
                    continue

                if board[i][j][0] == opp_color:
                    opp_moves = highlight_moves(board,(i,j))
                    print(board[i][j])
                    print(opp_moves)
                    print(king_move)
                    if king_move in opp_moves:
                        highlights.remove(king_move)
        
        board = old_board.copy()

    return opp_moves


def king_in_check():
    pass

def king_will_be_in_check():
    pass

# Possible Moves
def highlight_moves(board, coords):
    piece = board[coords[0]][coords[1]]
    highlights = []

    # For Pawn
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
    
    #For Rook
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

    # For Bishop
    elif piece[1] == 'b':
        opponent = "w" if piece[0] == "b" else "b"

        row, col = coords[0] + 1, coords[1] + 1
        while row <= 7 and col <= 7:
            if board[row][col] == "--":
                highlights.append((row,col))
                row += 1
                col += 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break

        row, col = coords[0] + 1, coords[1] - 1
        while row <= 7 and col >= 0:
            if board[row][col] == "--":
                highlights.append((row,col))
                row += 1
                col -= 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break

        row, col = coords[0] - 1, coords[1] - 1
        while col >= 0 and row >= 0:
            if board[row][col] == "--":
                highlights.append((row,col))
                col -= 1
                row -= 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break

        row, col = coords[0] - 1, coords[1] + 1
        while col <= 7 and row >= 0:
            if board[row][col] == "--":
                highlights.append((row,col))
                col += 1
                row -= 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break
    
    #For Queen
    elif piece[1] == 'q':
        opponent = "w" if piece[0] == "b" else "b"

        row, col = coords[0] + 1, coords[1]
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

        row, col = coords[0] + 1, coords[1] + 1
        while row <= 7 and col <= 7:
            if board[row][col] == "--":
                highlights.append((row,col))
                row += 1
                col += 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break

        row, col = coords[0] + 1, coords[1] - 1
        while row <= 7 and col >= 0:
            if board[row][col] == "--":
                highlights.append((row,col))
                row += 1
                col -= 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break

        row, col = coords[0] - 1, coords[1] - 1
        while col >= 0 and row >= 0:
            if board[row][col] == "--":
                highlights.append((row,col))
                col -= 1
                row -= 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break

        row, col = coords[0] - 1, coords[1] + 1
        while col <= 7 and row >= 0:
            if board[row][col] == "--":
                highlights.append((row,col))
                col += 1
                row -= 1
            elif board[row][col][0] == opponent:
                highlights.append((row,col))
                break
            else:
                break
    
    elif piece[1] == "n":
        opponent = "w" if piece[0] == "b" else "b"
        adds = (2,1,-1,-2)
        for row_add in adds:
            for col_add in adds:
                if not ((row_add in (2,-2) and col_add in (1,-1)) or (row_add in (1,-1) and col_add in (2,-2))):
                    continue
                row = coords[0] + row_add
                col = coords[1] + col_add

                if not (0 <= row <= 7) or not (0 <= col <= 7):
                    continue

                if board[row][col] == "--":
                    highlights.append((row,col))

                elif board[row][col][0] == opponent:
                    highlights.append((row,col))

    # For King    
    elif piece[1] == 'k':
        opponent = "w" if piece[0] == "b" else "b"
        choices = (0,1,-1)
        for row_add in choices:
            for col_add in choices:
                row = coords[0] + row_add
                col = coords[1] + col_add

                if not (0 <= row <= 7) or not (0 <= col <= 7):
                    continue

                if board[row][col] == "--":
                    highlights.append((row,col))
                elif board[row][col][0] == opponent:
                    highlights.append((row,col))
        
        if piece[0] == 'b':
            empty_check_l = [(0,1),(0,2),(0,3)]
            l_castle = w_l_rook_available and w_king_available
            empty_check = [(0,5),(0,6)]
            castle = w_rook_available and w_king_available
            for ch in empty_check_l:
                if board[ch[0]][ch[1]] != "--":
                    l_castle = False
            for ch in empty_check:
                if board[ch[0]][ch[1]] != "--":
                    castle = False

            if l_castle and board[0][0] == 'br':
                highlights.append((0,2))
            if castle and board[0][7] == 'br':
                highlights.append((0,6))
            
        else:
            empty_check_l = [(7,1),(7,2),(7,3)]
            l_castle = b_l_rook_available and b_king_available
            empty_check = [(7,5),(7,6)]
            castle = b_rook_available and b_rook_available
            for ch in empty_check_l:
                if board[ch[0]][ch[1]] != "--":
                    l_castle = False
            for ch in empty_check:
                if board[ch[0]][ch[1]] != "--":
                    castle = False

            if l_castle and board[7][0] == 'wr':
                highlights.append((7,2))
            if castle and board[7][7] == 'wr':
                highlights.append((7,6))
        
        #After Everything Need to check if King is getting Checked in any Position.
        checked_here = king_can_be_captured(coords,board,highlights)
        checked_moves = set(checked_here).intersection(set(highlights))
    
        for move in checked_moves:
            highlights.remove(move)

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
                color = PIECE_PLACEMENT_COLOR

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
    turn = True

    clock = pygame.time.Clock()
    while True:
        selected, highlights,turn = handle_events(selected, board, highlights,turn)
        draw_board(window, highlights,selected)
        draw_pieces(window, board, images)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()

    