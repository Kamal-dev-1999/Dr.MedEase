import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("User-Controlled Bouncy Ball Game")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Ball parameters
ball_radius = 15
ball_pos = [WIDTH // 2, HEIGHT - 50]
ball_speed = 5

# Obstacle parameters
obstacle_width = 80
obstacle_height = 20
obstacles = []
for i in range(5):
    x = random.randint(0, WIDTH - obstacle_width)
    y = random.randint(50, HEIGHT // 2)
    obstacles.append(pygame.Rect(x, y, obstacle_width, obstacle_height))

# Creatures
creature_radius = 20
creatures = []
for i in range(3):
    x = random.randint(creature_radius, WIDTH - creature_radius)
    y = random.randint(creature_radius, HEIGHT // 2)
    creatures.append([x, y])

# Score
score = 0
font = pygame.font.Font(None, 36)

def check_collision(ball, rect):
    return rect.collidepoint(ball[0], ball[1])

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current state of all keyboard buttons
    keys = pygame.key.get_pressed()

    # Update ball position based on user input
    if keys[pygame.K_LEFT]:
        ball_pos[0] -= ball_speed
    if keys[pygame.K_RIGHT]:
        ball_pos[0] += ball_speed
    if keys[pygame.K_UP]:
        ball_pos[1] -= ball_speed
    if keys[pygame.K_DOWN]:
        ball_pos[1] += ball_speed

    # Ensure the ball stays within the screen boundaries
    ball_pos[0] = max(ball_radius, min(WIDTH - ball_radius, ball_pos[0]))
    ball_pos[1] = max(ball_radius, min(HEIGHT - ball_radius, ball_pos[1]))

    # Clear screen
    screen.fill(BLACK)

    # Ball collision with obstacles
    for obstacle in obstacles:
        if check_collision(ball_pos, obstacle):
            obstacles.remove(obstacle)
            score += 10

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, GREEN, obstacle)

    # Ball collision with creatures
    for creature in creatures:
        dist = ((ball_pos[0] - creature[0])**2 + (ball_pos[1] - creature[1])**2)**0.5
        if dist <= ball_radius + creature_radius:
            creatures.remove(creature)
            score += 20

    # Draw creatures
    for creature in creatures:
        pygame.draw.circle(screen, YELLOW, (creature[0], creature[1]), creature_radius)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
