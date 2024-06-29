import pygame
import random

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake initial position and size
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Food position
food_pos = [random.randrange(1, (WIDTH//CELL_SIZE)) * CELL_SIZE,
            random.randrange(1, (HEIGHT//CELL_SIZE)) * CELL_SIZE]
food_spawn = True

# Initial direction
direction = 'RIGHT'
change_to = direction

# Speed
speed = 15
clock = pygame.time.Clock()

# Main function
def game_loop():
    global change_to, direction, snake_pos, snake_body, food_pos, food_spawn

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Validate direction
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Move snake
        if direction == 'UP':
            snake_pos[1] -= CELL_SIZE
        if direction == 'DOWN':
            snake_pos[1] += CELL_SIZE
        if direction == 'LEFT':
            snake_pos[0] -= CELL_SIZE
        if direction == 'RIGHT':
            snake_pos[0] += CELL_SIZE

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH//CELL_SIZE)) * CELL_SIZE,
                        random.randrange(1, (HEIGHT//CELL_SIZE)) * CELL_SIZE]
        food_spawn = True

        # Background
        screen.fill(BLACK)

        # Draw snake
        for pos in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

        # Draw food
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

        # Check for game over
        if snake_pos[0] < 0 or snake_pos[0] > WIDTH-CELL_SIZE:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > HEIGHT-CELL_SIZE:
            game_over()
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()

        pygame.display.update()
        clock.tick(speed)

def game_over():
    pygame.quit()
    quit()

if __name__ == "__main__":
    game_loop()
