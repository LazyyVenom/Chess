import pygame
import sys
import webbrowser

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

title_font = pygame.font.Font(None, 100)  
button_font = pygame.font.Font(None, 48)

BUTTON_WIDTH, BUTTON_HEIGHT = 250, 60
HOVER_SCALE = 1.05  
ANIMATION_SPEED = 0.05

current_screen = "main_menu"

button_scales = {"Play": 1.0, "Instructions": 1.0, "Code": 1.0, "Back": 1.0, "Start Button": 1.0}
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
    button_rect = pygame.Rect(x - (width - BUTTON_WIDTH) // 2, y - (height - BUTTON_HEIGHT) // 2, width, height)

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
    draw_button("Instructions", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 50, instructions_screen)
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
    
    version_surface = button_font.render(version_names[current_version_index], True, WHITE)
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

    draw_color_box(WIDTH // 2 - 120, HEIGHT // 2 - 50, "white", selected_color == "white")
    draw_color_box(WIDTH // 2 + 20, HEIGHT // 2 - 50, "black", selected_color == "black")

    draw_version_selection()
    
    draw_back_button()

    draw_button("Start Button", WIDTH - BUTTON_WIDTH - 20, HEIGHT - BUTTON_HEIGHT - 20, game_screen)

def game_screen():
    global current_screen
    current_screen = "game"
    screen.fill(BLACK)
    

def main():
    global current_screen, selected_color, current_version_index
    running = True
    while running:
        screen.fill(DARK_GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                if (WIDTH // 2 - 120 <= mouse_pos[0] <= WIDTH // 2 - 20 and 
                        HEIGHT // 2 - 50 <= mouse_pos[1] <= HEIGHT // 2 + 50):
                    selected_color = "white"
                elif (WIDTH // 2 + 20 <= mouse_pos[0] <= WIDTH // 2 + 120 and 
                        HEIGHT // 2 - 50 <= mouse_pos[1] <= HEIGHT // 2 + 50):
                    selected_color = "black"

                if (WIDTH // 2 - 125 <= mouse_pos[0] <= WIDTH // 2 - 105 and 
                        HEIGHT // 2 + 140 - 20 <= mouse_pos[1] <= HEIGHT // 2 + 140 + 20):
                    current_version_index = (current_version_index - 1) % len(version_names)
                elif (WIDTH // 2 + 110 <= mouse_pos[0] <= WIDTH // 2 + 130 and 
                        HEIGHT // 2 + 140 - 20 <= mouse_pos[1] <= HEIGHT // 2 + 140 + 20):
                    current_version_index = (current_version_index + 1) % len(version_names)

        if current_screen == "main_menu":
            main_menu()
        elif current_screen == "play_screen":
            play_screen()
        elif current_screen == "instructions_screen":
            instructions_screen()
        elif current_screen == "game":
            game_screen()
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
    