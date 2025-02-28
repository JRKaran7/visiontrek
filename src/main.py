import cv2
import pygame
import random
from pose_tracking import detect_leg_movement
from game_logic import VirtualTrekGame
from database import init_db, save_score, get_high_score

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Trek")
clock = pygame.time.Clock()

# Initialize game & database
init_db()
game = VirtualTrekGame()
max_score = get_high_score()

# Load assets safely
try:
    print("Loading assets...")
    backgrounds = [
        pygame.image.load("assets/background.jpeg").convert(),
        pygame.image.load("assets/background2.jpeg").convert()
    ]
    players = [
        pygame.image.load("assets/player1.png").convert_alpha(),
        pygame.image.load("assets/player2.png").convert_alpha()
    ]
    coin_img = pygame.image.load("assets/coin.png").convert_alpha()
    ground_img = pygame.image.load("assets/ground.png").convert()
    print("Assets loaded successfully!")
except pygame.error as e:
    print(f"Error loading assets: {e}")
    pygame.quit()
    exit()

# Scale assets properly
backgrounds = [pygame.transform.scale(bg, (WIDTH, HEIGHT)) for bg in backgrounds]
players = [pygame.transform.scale(pl, (120, 120)) for pl in players]
coin_img = pygame.transform.scale(coin_img, (30, 30))
ground_img = pygame.transform.scale(ground_img, (WIDTH, 50))

# Camera Setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not detected.")
    pygame.quit()
    exit()

# Home Screen Selection Variables
selected_bg = 0
selected_player = 0
in_home_screen = True

def draw_home_screen():
    """Displays the selection screen for backgrounds and characters."""
    screen.fill((0, 0, 0))  # Clear screen
    
    font = pygame.font.Font(None, 40)
    
    # Show current selections
    screen.blit(backgrounds[selected_bg], (0, 0))
    screen.blit(players[selected_player], (WIDTH//2 - 60, HEIGHT//2 - 60))
    
    # Text instructions
    instructions = font.render("Use Left/Right to Change Background", True, (255, 255, 255))
    instructions2 = font.render("Use Up/Down to Change Character", True, (255, 255, 255))
    start_text = font.render("Press ENTER to Start", True, (255, 255, 0))

    screen.blit(instructions, (WIDTH//2 - 180, 50))
    screen.blit(instructions2, (WIDTH//2 - 160, 90))
    screen.blit(start_text, (WIDTH//2 - 100, 140))

    pygame.display.flip()

# Background Scrolling Variables
bg_x1, bg_x2 = 0, WIDTH
scroll_speed = 3  # Speed of scrolling

# Player & Coin Positions
player_x = 100
player_y = HEIGHT - 50 - players[selected_player].get_height()
coin_x = random.randint(WIDTH - 50, WIDTH + 50)
coin_y = HEIGHT - 50 - 35

score = 0
font = pygame.font.Font(None, 36)

# ---------- HOME SCREEN LOOP ----------
while in_home_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                selected_bg = (selected_bg - 1) % len(backgrounds)
            elif event.key == pygame.K_RIGHT:
                selected_bg = (selected_bg + 1) % len(backgrounds)
            elif event.key == pygame.K_UP:
                selected_player = (selected_player - 1) % len(players)
            elif event.key == pygame.K_DOWN:
                selected_player = (selected_player + 1) % len(players)
            elif event.key == pygame.K_RETURN:
                in_home_screen = False  # Exit home screen

    draw_home_screen()

# Start Game with Selected Assets
background = backgrounds[selected_bg]
player = players[selected_player]

running = True
print("Game loop starting...")

# ---------- GAME LOOP ----------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()
    if not ret:
        print("Error: Camera feed failed.")
        break

    # Detect leg movement
    if detect_leg_movement(frame):
        coin_x -= 20  # Move coin left
        bg_x1 -= scroll_speed
        bg_x2 -= scroll_speed

    # Reset background when it moves out of frame
    if bg_x1 <= -WIDTH:
        bg_x1 = WIDTH
    if bg_x2 <= -WIDTH:
        bg_x2 = WIDTH

    # Check for coin collection
    if abs(coin_x - player_x) < 40:
        score += 10
        if score > max_score:
            max_score = score
        coin_x = random.randint(WIDTH - 20, WIDTH + 20)  # Respawn coin closer

    # If coin moves out of frame, spawn a new one
    if coin_x < -30:
        coin_x = random.randint(WIDTH - 20, WIDTH + 20)

    # Draw everything
    screen.blit(background, (bg_x1, 0))
    screen.blit(background, (bg_x2, 0))

    screen.blit(ground_img, (0, HEIGHT - 50))  # Draw ground
    screen.blit(player, (player_x, player_y))  # Draw player
    screen.blit(coin_img, (coin_x, coin_y))  # Draw coin

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    max_score_text = font.render(f"Max Score: {max_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(max_score_text, (10, 40))

    pygame.display.flip()
    clock.tick(30)

# Save score and cleanup
save_score(score)
cap.release()
cv2.destroyAllWindows()
pygame.quit()
