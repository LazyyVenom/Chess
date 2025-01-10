import pygame
import sys
import webbrowser
from board_utils import *
from deadfish import DeadFish
import copy

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DeadFish")

DARK_GRAY = (30, 30, 30)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
LIGHT_BLUE = (100, 149, 237)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
SHADOW_COLOR = (50, 50, 50)
SQUARE_SIZE = 75

player = "w"
opp = "b"

title_font = pygame.font.Font(None, 100)
button_font = pygame.font.Font(None, 48)

BUTTON_WIDTH, BUTTON_HEIGHT = 250, 60
HOVER_SCALE = 1.05
ANIMATION_SPEED = 0.05

current_screen = "main_menu"

button_scales = {
    "Play": 1.0,
    "Instructions": 1.0,
    "Code": 1.0,
    "Back": 1.0,
    "Start Button": 1.0,
}
code_button_clicked = False

selected_color = "white"
version_names = ["DeadFish V1", "DeadFish V2", "DeadFish V3"]
current_version_index = 0


def draw_button(text, x, y, action=None):
    global button_scales, code_button_clicked
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    is_hovered = button_rect.collidepoint(mouse)

    target_scale = HOVER_SCALE if is_hovered else 1.0
    scale = button_scales[text]
    scale += (target_scale - scale) * ANIMATION_SPEED
    button_scales[text] = scale

    width = int(BUTTON_WIDTH * scale)
    height = int(BUTTON_HEIGHT * scale)
    button_rect = pygame.Rect(
        x - (width - BUTTON_WIDTH) // 2,
        y - (height - BUTTON_HEIGHT) // 2,
        width,
        height,
    )

    shadow_rect = button_rect.move(5, 5)
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, border_radius=10)

    color = LIGHT_BLUE if is_hovered else BLUE
    pygame.draw.rect(screen, color, button_rect, border_radius=10)

    text_surface = button_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    if button_rect.collidepoint(mouse) and click[0] == 1:
        if text == "Code":
            if not code_button_clicked:
                code_button_clicked = True
                action()
        else:
            code_button_clicked = False
            action()


def open_github():
    webbrowser.open("https://github.com/LazyyVenom/Chess")


def draw_back_button():
    draw_button("Back", 20, 20, main_menu)


def main_menu():
    global current_screen
    current_screen = "main_menu"
    screen.fill(DARK_GRAY)

    title_surface = title_font.render("DeadFish", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_surface, title_rect)

    draw_button("Play", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 50, play_screen)
    draw_button(
        "Instructions",
        WIDTH // 2 - BUTTON_WIDTH // 2,
        HEIGHT // 2 + 50,
        instructions_screen,
    )
    draw_button("Code", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 150, open_github)


def instructions_screen():
    global current_screen
    current_screen = "instructions_screen"
    screen.fill(DARK_GRAY)

    title_surface = title_font.render("Instructions", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_surface, title_rect)

    draw_back_button()


def draw_color_box(x, y, color, selected):
    box_rect = pygame.Rect(x, y, 100, 100)
    border_color = GREEN if selected else BLACK
    pygame.draw.rect(screen, border_color, box_rect, border_radius=10)
    fill_color = WHITE if color == "white" else BLACK
    inner_rect = box_rect.inflate(-10, -10)
    pygame.draw.rect(screen, fill_color, inner_rect, border_radius=10)


def draw_triangle(x, y, direction):
    if direction == "left":
        points = [(x, y), (x + 20, y - 10), (x + 20, y + 10)]
    else:
        points = [(x, y), (x - 20, y - 10), (x - 20, y + 10)]
    pygame.draw.polygon(screen, WHITE, points)


def draw_version_selection():
    global current_version_index
    triangle_y = HEIGHT // 2 + 140
    triangle_x = WIDTH // 2 - 130

    draw_triangle(triangle_x, triangle_y, "left")

    version_surface = button_font.render(
        version_names[current_version_index], True, WHITE
    )
    version_rect = version_surface.get_rect(center=(WIDTH // 2, triangle_y))
    screen.blit(version_surface, version_rect)

    draw_triangle(triangle_x + 260, triangle_y, "right")


def play_screen():
    global current_screen
    current_screen = "play_screen"
    screen.fill(DARK_GRAY)

    title_surface = title_font.render("Play With", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_surface, title_rect)

    draw_color_box(
        WIDTH // 2 - 120, HEIGHT // 2 - 50, "white", selected_color == "white"
    )
    draw_color_box(
        WIDTH // 2 + 20, HEIGHT // 2 - 50, "black", selected_color == "black"
    )

    draw_version_selection()

    draw_back_button()

    draw_button(
        "Start Button",
        WIDTH - BUTTON_WIDTH - 20,
        HEIGHT - BUTTON_HEIGHT - 20,
        game_screen,
    )


def checkmate_screen():
    global current_screen
    current_screen = "checkmate_screen"
    screen.fill(DARK_GRAY)

    title_surface = title_font.render("Checkmate", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_surface, title_rect)

    print("Checkmate")

    draw_back_button()


def game_screen():
    global selected_piece, valid_moves, current_screen, board, players_turn
    global king_moved, left_rook_moved, right_rook_moved

    current_screen = "game"

    if "selected_piece" not in globals():
        selected_piece = None
    if "valid_moves" not in globals():
        valid_moves = []

    screen.fill(DARK_GRAY)
    draw_board(screen, valid_moves, selected_piece, player)
    draw_players_info(screen, player, version_names[current_version_index])
    draw_pieces(screen, board)

    for event in pygame.event.get():
        if not players_turn:
            if ThisDeadFish.stalemate(board[::-1]):
                if ThisDeadFish.inCheck(board[::-1]):
                    for row in board:
                        print(row)
                    checkmate_screen()
                else:
                    print("Stalemate")

                # pygame.quit()
                # sys.exit()
            
            board = ThisDeadFish.make_decision(board)
            players_turn = True

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            col = mouse_pos[0] // SQUARE_SIZE
            row = mouse_pos[1] // SQUARE_SIZE

            if col > 7 or row > 7:
                continue

            if selected_piece:
                if (row, col) in valid_moves:

                    # Checking if rook moved
                    if board[selected_piece[0]][selected_piece[1]][1] == "r":
                        if selected_piece[1] == 0 and not left_rook_moved:
                            left_rook_moved = True
                        elif selected_piece[1] == 7 and not right_rook_moved:
                            right_rook_moved = True

                    # Checking if king moved
                    if board[selected_piece[0]][selected_piece[1]][1] == "k":
                        king_moved = True

                    board = move_piece(board, selected_piece, (row, col))
                    players_turn = not players_turn
                    selected_piece = None
                    valid_moves = []
                else:
                    selected_piece = None
                    valid_moves = []
            else:
                piece = board[row][col]
                if piece != "--" and (
                    (player == "w" and piece[0] == "w")
                    or (player == "b" and piece[0] == "b")
                ):
                    selected_piece = (row, col)

                opp_color = "b" if player == "w" else "w"

                if (
                    selected_piece
                    and board[selected_piece[0]][selected_piece[1]][1] == "k"
                ):
                    valid_moves = valid_move_decider(
                        board,
                        selected_piece,
                        (not king_moved, not left_rook_moved, not right_rook_moved),
                    )

                else:
                    valid_moves = valid_move_decider(board, selected_piece)

                new_valid_moves = valid_moves.copy()

                for move in new_valid_moves:
                    temp_board = copy.deepcopy(board)
                    temp_board = move_piece(temp_board, selected_piece, move)
                    if check(temp_board[::-1], opp_color, ThisDeadFish):
                        valid_moves.remove(move)


def main():
    global current_screen, selected_color, current_version_index, player, opp, board
    global selected_piece, valid_moves

    selected_piece = None
    valid_moves = []
    running = True

    while running:
        screen.fill(DARK_GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if current_screen == "play_screen":
                    if (
                        WIDTH // 2 - 120 <= mouse_pos[0] <= WIDTH // 2 - 20
                        and HEIGHT // 2 - 50 <= mouse_pos[1] <= HEIGHT // 2 + 50
                    ):
                        selected_color = "white"
                        player = "w"
                        opp = "b"

                    elif (
                        WIDTH // 2 + 20 <= mouse_pos[0] <= WIDTH // 2 + 120
                        and HEIGHT // 2 - 50 <= mouse_pos[1] <= HEIGHT // 2 + 50
                    ):
                        selected_color = "black"
                        player = "b"
                        opp = "w"

                    if (
                        WIDTH // 2 - 125 <= mouse_pos[0] <= WIDTH // 2 - 105
                        and HEIGHT // 2 + 140 - 20
                        <= mouse_pos[1]
                        <= HEIGHT // 2 + 140 + 20
                    ):
                        current_version_index = (current_version_index - 1) % len(
                            version_names
                        )

                    elif (
                        WIDTH // 2 + 110 <= mouse_pos[0] <= WIDTH // 2 + 130
                        and HEIGHT // 2 + 140 - 20
                        <= mouse_pos[1]
                        <= HEIGHT // 2 + 140 + 20
                    ):
                        current_version_index = (current_version_index + 1) % len(
                            version_names
                        )

                    global players_turn, king_moved, left_rook_moved, right_rook_moved, ThisDeadFish
                    king_moved = False
                    left_rook_moved = False
                    right_rook_moved = False
                    players_turn = True if player == "w" else False
                    ThisDeadFish = DeadFish(current_version_index,deadfish_color=opp)

                    o = opp
                    p = player
                    board = [
                        [f"{o}r",f"{o}n",f"{o}b",f"{o}k",f"{o}q",f"{o}b",f"{o}n",f"{o}r",],
                        [f"{o}p",f"{o}p",f"{o}p",f"{o}p",f"{o}p",f"{o}p",f"{o}p",f"{o}p",],
                        ["--","--","--","--","--","--","--","--",],
                        ["--","--","--","--","--","--","--","--",],
                        ["--","--","--","--","--","--","--","--",],
                        ["--","--","--","--","--","--","--","--",],
                        [f"{p}p",f"{p}p",f"{p}p",f"{p}p",f"{p}p",f"{p}p",f"{p}p",f"{p}p",],
                        [f"{p}r",f"{p}n",f"{p}b",f"{p}k",f"{p}q",f"{p}b",f"{p}n",f"{p}r",],
                    ]

        if current_screen == "main_menu":
            main_menu()
        elif current_screen == "play_screen":
            play_screen()
        elif current_screen == "instructions_screen":
            instructions_screen()
        elif current_screen == "game":
            game_screen()
        elif current_screen == "checkmate_screen":
            checkmate_screen()

        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
