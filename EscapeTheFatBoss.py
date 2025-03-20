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

# Load custom font for title and subtitle
font_path = os.path.join(script_directory, "jorolks font", "jorolks.ttf")
font_title = pygame.font.Font(font_path, 48)
font_subtitle = pygame.font.Font(font_path, 24)

# Default font for move counter and top score
font_counter = pygame.font.Font(None, 36) 

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

# Load main character image (Mainchar)
mainchar_path = os.path.join(script_directory, "Mainchar.png")
mainchar_img = pygame.image.load(mainchar_path)
mainchar_size = (50, 50)
mainchar_img = pygame.transform.scale(mainchar_img, mainchar_size)

# Load badman image
badman_path = os.path.join(script_directory, "Badman.png")
badman_img = pygame.image.load(badman_path)
badman_size = (50, 50)
badman_img = pygame.transform.scale(badman_img, badman_size)

# Border thickness
border_thickness = 20  

# Define grid size based on checkerboard pattern
grid_size = 48  
checkerboard_x = border_thickness + 40  
checkerboard_y = border_thickness       
checkerboard_width = screen_width - 2 * border_thickness
checkerboard_height = screen_height - 2 * border_thickness

# Main character's original starting position
mainchar_x, mainchar_y = 150, 105  

# Badman position resets when game starts
def reset_badman_position():
    global badman_x, badman_y
    badman_x, badman_y = 595, 445  #Bad man og position reset

# Move counter and top score
move_counter = 0
top_score = 0

# Timer for badman movement
badman_move_interval = 250  # Move every 0.25 seconds (250 millisecconds)
last_badman_move_time = 0  # Tracks the last time badman moved

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLDEN_YELLOW = (255, 215, 0)

def move_badman_toward_player():
    """Moves Badman one step toward the main character."""
    global badman_x, badman_y

    dx = mainchar_x - badman_x
    dy = mainchar_y - badman_y

    # Move horizontally if distance in X is greater, else move vertically
    if abs(dx) > abs(dy):
        badman_x += 65 if dx > 0 else -65  # Move the same amount as the main character
    else:
        badman_y += grid_size if dy > 0 else -grid_size  # Move the same amount as the main character

    # Badman stays within boundaries
    if not (checkerboard_x + grid_size <= badman_x < checkerboard_x + checkerboard_width - (grid_size + 150)):
        badman_x -= 65 if dx > 0 else -65
    if not (checkerboard_y + grid_size <= badman_y < checkerboard_y + checkerboard_height - (grid_size + 50)):
        badman_y -= grid_size if dy > 0 else -grid_size

def game_page():
    """Starts the game loop where the main character and Badman move within the grid."""
    print("Game Started")
    
    # Reset Badman position when the game starts
    reset_badman_position()

    running_game = True
    clock = pygame.time.Clock()
    
    global mainchar_x, mainchar_y, badman_x, badman_y, move_counter, top_score, last_badman_move_time

    while running_game:
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds

        # Move badman every 0.25 seconds
        if current_time - last_badman_move_time >= badman_move_interval:
            last_badman_move_time = current_time  # Update last move time
            move_badman_toward_player()  # Move badman toward mainchar

        # Redraw the entire background
        screen.blit(bkg_img, (0, 0))

        # Draw main character
        screen.blit(mainchar_img, (mainchar_x, mainchar_y))
        
        # Draw badman
        screen.blit(badman_img, (badman_x, badman_y))

        # Display move counter (centered and slightly lower)
        counter_text = font_counter.render(f"Moves: {move_counter}", True, WHITE)
        counter_x = screen_width // 2 - counter_text.get_width() // 2
        counter_y = screen_height // 2 - 225  # Adjusted vertical position to prevent overlap
        screen.blit(counter_text, (counter_x, counter_y))


        # Display top score (top-right corner)
        top_score_text = font_counter.render(f"Top Score: {top_score}", True, WHITE)
        top_score_x = screen_width - top_score_text.get_width() - 10
        top_score_y = 10
        screen.blit(top_score_text, (top_score_x, top_score_y))

        pygame.display.flip()
        clock.tick(10)

        # Check if Mainchar and Badman collide (using bounding rectangles)
        mainchar_rect = pygame.Rect(mainchar_x, mainchar_y, mainchar_size[0], mainchar_size[1])
        badman_rect = pygame.Rect(badman_x, badman_y, badman_size[0], badman_size[1])
        if mainchar_rect.colliderect(badman_rect):
            print("Game Over! Collision detected.")
            if move_counter > top_score:
                top_score = move_counter  # Update top score
            move_counter = 0  # Reset move counter
            running_game = False  # Exit the game loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                new_main_x, new_main_y = mainchar_x, mainchar_y

                # Arrow keys for main character
                if event.key == pygame.K_RIGHT:
                    new_main_x += 65
                elif event.key == pygame.K_LEFT:
                    new_main_x -= 65
                elif event.key == pygame.K_DOWN:
                    new_main_y += grid_size
                elif event.key == pygame.K_UP:
                    new_main_y -= grid_size
                
                # Ensure main character stays within the checkerboard boundaries
                if (checkerboard_x + grid_size <= new_main_x < checkerboard_x + checkerboard_width - (grid_size + 150) and
                    checkerboard_y + grid_size <= new_main_y < checkerboard_y + checkerboard_height - (grid_size + 50)):
                    mainchar_x, mainchar_y = new_main_x, new_main_y
                    move_counter += 1  # Increment the move counter

running = True
while running:
    screen.fill(BLACK)
    pygame.draw.rect(screen, GOLDEN_YELLOW, (0, 0, screen_width, screen_height), border_thickness)

    # Position Mainchar (left side above title)
    mainchar_x = 150  #  starting X position
    mainchar_y = 105  #  starting Y position
    screen.blit(mainchar_img, (mainchar_x, mainchar_y))

    # Position Badman 
    badman_x = screen_width // 2 + 50
    badman_y = 100
    screen.blit(badman_img, (badman_x, badman_y))

    # Title Text
    text = font_title.render("ESCAPE THE FATTY", True, WHITE)
    text2 = font_subtitle.render("BY: DAVID HOVSEPIAN", True, WHITE)

    text_x = screen_width // 2 - text.get_width() // 2
    text_y = screen_height // 2 - text.get_height() // 2 - 50
    screen.blit(text, (text_x, text_y))

    text2_x = screen_width // 2 - text2.get_width() // 2
    text2_y = text_y + text.get_height()
    screen.blit(text2, (text2_x, text2_y))

    # Draw Play Button
    screen.blit(play_button_img, play_button_rect.topleft)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                move_counter = 0  # Reset the move counter when starting the game
                game_page()  # game starts and resets 

pygame.quit()