import pygame
import sys
import webbrowser

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 600 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DeadFish")

# Colors (dark theme)
DARK_GRAY = (30, 30, 30)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
LIGHT_BLUE = (100, 149, 237)
WHITE = (255, 255, 255)
SHADOW_COLOR = (50, 50, 50)

# Fonts
title_font = pygame.font.Font(None, 100)  # Increased font size for the title
button_font = pygame.font.Font(None, 48)

# Button settings
BUTTON_WIDTH, BUTTON_HEIGHT = 250, 60
HOVER_SCALE = 1.05  
ANIMATION_SPEED = 0.05

# Screen management
current_screen = "main_menu"

# Track each button's scale for smooth animation
button_scales = {"Play": 1.0, "Instructions": 1.0, "Code": 1.0, "Back": 1.0}
code_button_clicked = False

# Function to draw animated buttons with smoother hover effect
def draw_button(text, x, y, action=None):
    global button_scales, code_button_clicked
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    is_hovered = button_rect.collidepoint(mouse)

    # Smoothly animate the scale factor
    target_scale = HOVER_SCALE if is_hovered else 1.0
    scale = button_scales[text]
    scale += (target_scale - scale) * ANIMATION_SPEED
    button_scales[text] = scale

    # Calculate the new scaled button size and position
    width = int(BUTTON_WIDTH * scale)
    height = int(BUTTON_HEIGHT * scale)
    button_rect = pygame.Rect(x - (width - BUTTON_WIDTH) // 2, y - (height - BUTTON_HEIGHT) // 2, width, height)

    # Shadow
    shadow_rect = button_rect.move(5, 5)
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, border_radius=10)

    # Button color change on hover
    color = LIGHT_BLUE if is_hovered else BLUE
    pygame.draw.rect(screen, color, button_rect, border_radius=10)

    # Button text
    text_surface = button_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    # Button click action
    if button_rect.collidepoint(mouse) and click[0] == 1:
        if text == "Code":
            if not code_button_clicked:  # Only open the link if it wasn't already clicked
                code_button_clicked = True
                action()
        else:
            code_button_clicked = False  # Reset for other buttons
            action()  # Call action for other buttons

# Function to open GitHub link
def open_github():
    webbrowser.open("https://github.com/LazyyVenom/Chess")

# Draw back button
def draw_back_button():
    draw_button("Back", 20, 20, main_menu)

# Screen functions
def main_menu():
    global current_screen
    current_screen = "main_menu"
    screen.fill(DARK_GRAY)
    
    # Title
    title_surface = title_font.render("DeadFish", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_surface, title_rect)

    # Buttons
    draw_button("Play", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 50, play_screen)
    draw_button("Instructions", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 50, instructions_screen)
    draw_button("Code", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 150, open_github)

def play_screen():
    global current_screen
    current_screen = "play_screen"
    screen.fill(DARK_GRAY)
    
    # Title
    title_surface = title_font.render("Play With", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_surface, title_rect)

    draw_back_button()  # Draw back button

def instructions_screen():
    global current_screen
    current_screen = "instructions_screen"
    screen.fill(DARK_GRAY)
    
    # Title
    title_surface = title_font.render("Instructions", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_surface, title_rect)
    
    draw_back_button()  # Draw back button

# Main game loop
def main():
    global current_screen
    running = True
    while running:
        screen.fill(DARK_GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Display the current screen
        if current_screen == "main_menu":
            main_menu()
        elif current_screen == "play_screen":
            play_screen()
        elif current_screen == "instructions_screen":
            instructions_screen()
        
        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
