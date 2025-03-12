import pygame
import os

pygame.init()

# Ensure the script is running in the correct directory
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Escape the Fatty")

# Load custom font
font_path = os.path.join(script_directory, "jorolks font", "jorolks.ttf")
font_title = pygame.font.Font(font_path, 48)
font_subtitle = pygame.font.Font(font_path, 24)

# Load Play button image
play_button_path = os.path.join(script_directory, "PlayButton.png")
play_button_img = pygame.image.load(play_button_path)
new_width, new_height = play_button_img.get_width() // 3, play_button_img.get_height() // 3
play_button_img = pygame.transform.scale(play_button_img, (new_width, new_height))
play_button_rect = play_button_img.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

# Load background image (checkerboard)
bkg_path = os.path.join(script_directory, "bkg.png")
bkg_img = pygame.image.load(bkg_path)
bkg_img = pygame.transform.scale(bkg_img, (screen_width, screen_height))
bkg_rect = bkg_img.get_rect()

# Load main character image
main_char_path = os.path.join(script_directory, "Mainchar.png")
main_char_img = pygame.image.load(main_char_path)
main_char_size = (50, 50)
main_char_img = pygame.transform.scale(main_char_img, main_char_size)

# Load badman image
badman_path = os.path.join(script_directory, "Badman.png")
badman_img = pygame.image.load(badman_path)
badman_size = (50, 50)  # Adjust size if needed
badman_img = pygame.transform.scale(badman_img, badman_size)

# Border thickness
border_thickness = 20  

# Define grid size based on checkerboard pattern
grid_size = 48 
checkerboard_x = border_thickness + 40  
checkerboard_y = border_thickness       
checkerboard_width = screen_width - 2 * border_thickness
checkerboard_height = screen_height - 2 * border_thickness

# Calculate rows and columns inside the checkerboard area
rows = checkerboard_height // grid_size
cols = checkerboard_width // grid_size

# Main character initial position: Top-left of checkerboard
main_char_x, main_char_y = 150, 105

# Badman position: Bottom-right of the checkerboard
badman_x, badman_y = 250, 250

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLDEN_YELLOW = (255, 215, 0)

def game_page():
    """Starts the game loop where the main character and Badman move within the grid."""
    print("Game Started!")
    running_game = True
    clock = pygame.time.Clock()
    
    global main_char_x, main_char_y, badman_x, badman_y

    while running_game:
        screen.blit(bkg_img, (0, 0))

        # Draw main character
        screen.blit(main_char_img, (main_char_x, main_char_y))
        
        # Draw badman
        screen.blit(badman_img, (badman_x, badman_y))

        pygame.display.flip()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                new_main_x, new_main_y = main_char_x, main_char_y
                new_badman_x, new_badman_y = badman_x, badman_y

                # Arrow keys for main character
                if event.key == pygame.K_RIGHT:
                    new_main_x += 65
                elif event.key == pygame.K_LEFT:
                    new_main_x -= 65
                elif event.key == pygame.K_DOWN:
                    new_main_y += grid_size
                elif event.key == pygame.K_UP:
                    new_main_y -= grid_size

                # WASD for badman
                if event.key == pygame.K_d:
                    new_badman_x += 65
                elif event.key == pygame.K_a:
                    new_badman_x -= 65
                elif event.key == pygame.K_s:
                    new_badman_y += grid_size
                elif event.key == pygame.K_w:
                    new_badman_y -= grid_size
                
                # Ensure main character stays within the checkerboard boundaries
                if (checkerboard_x + grid_size <= new_main_x < checkerboard_x + checkerboard_width - (grid_size + 150) and
                    checkerboard_y + grid_size <= new_main_y < checkerboard_y + checkerboard_height - (grid_size + 50)):
                    main_char_x, main_char_y = new_main_x, new_main_y
                
                # Ensure badman stays within the checkerboard boundaries
                if (checkerboard_x + grid_size <= new_badman_x < checkerboard_x + checkerboard_width - (grid_size + 150) and
                    checkerboard_y + grid_size <= new_badman_y < checkerboard_y + checkerboard_height - (grid_size + 50)):
                    badman_x, badman_y = new_badman_x, new_badman_y

running = True
while running:
    screen.fill(BLACK)
    pygame.draw.rect(screen, GOLDEN_YELLOW, (0, 0, screen_width, screen_height), border_thickness)
    
    text = font_title.render("ESCAPE THE FATTY", True, WHITE)
    text2 = font_subtitle.render("BY: DAVID HOVSEPIAN", True, WHITE)
    
    text_x = screen_width // 2 - text.get_width() // 2
    text_y = screen_height // 2 - text.get_height() // 2 - 50
    screen.blit(text, (text_x, text_y))
    
    text2_x = screen_width // 2 - text2.get_width() // 2
    text2_y = text_y + text.get_height()
    screen.blit(text2, (text2_x, text2_y))
    
    screen.blit(play_button_img, play_button_rect.topleft)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game_page()

pygame.quit()
