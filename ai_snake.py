import numpy as np
import random
import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Q-learning settings
ACTIONS = [UP, RIGHT, DOWN, LEFT]
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON = 1.0
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.01

# Snake class
class Snake:
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = RIGHT
        self.change_to = self.direction

    def change_direction(self, dir):
        if dir == UP and not self.direction == DOWN:
            self.direction = UP
        if dir == DOWN and not self.direction == UP:
            self.direction = DOWN
        if dir == LEFT and not self.direction == RIGHT:
            self.direction = LEFT
        if dir == RIGHT and not self.direction == LEFT:
            self.direction = RIGHT

    def move(self, food_pos):
        if self.direction == UP:
            self.position[1] -= CELL_SIZE
        if self.direction == DOWN:
            self.position[1] += CELL_SIZE
        if self.direction == LEFT:
            self.position[0] -= CELL_SIZE
        if self.direction == RIGHT:
            self.position[0] += CELL_SIZE

        self.body.insert(0, list(self.position))

        if self.position == food_pos:
            return True
        else:
            self.body.pop()
            return False

    def check_collision(self):
        if self.position[0] < 0 or self.position[0] > WIDTH - CELL_SIZE:
            return True
        if self.position[1] < 0 or self.position[1] > HEIGHT - CELL_SIZE:
            return True
        for block in self.body[1:]:
            if self.position == block:
                return True
        return False

    def get_head_position(self):
        return self.position

    def get_body(self):
        return self.body

# Game class
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food_pos = self.spawn_food()

    def spawn_food(self):
        return [random.randrange(1, (WIDTH // CELL_SIZE)) * CELL_SIZE,
                random.randrange(1, (HEIGHT // CELL_SIZE)) * CELL_SIZE]

    def render(self):
        screen.fill(BLACK)
        for pos in self.snake.get_body():
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, pygame.Rect(self.food_pos[0], self.food_pos[1], CELL_SIZE, CELL_SIZE))
        pygame.display.update()

    def reset(self):
        self.snake = Snake()
        self.food_pos = self.spawn_food()

# Q-learning agent
class QLearningAgent:
    def __init__(self):
        self.q_table = {}
        self.epsilon = EPSILON

    def get_state(self, game):
        snake_head = game.snake.get_head_position()
        food_pos = game.food_pos

        state = [
            snake_head[0] < food_pos[0],  # food is to the right
            snake_head[0] > food_pos[0],  # food is to the left
            snake_head[1] < food_pos[1],  # food is below
            snake_head[1] > food_pos[1],  # food is above
            game.snake.direction == UP,
            game.snake.direction == RIGHT,
            game.snake.direction == DOWN,
            game.snake.direction == LEFT,
        ]

        for block in game.snake.get_body()[1:]:
            if snake_head[0] + CELL_SIZE == block[0] and snake_head[1] == block[1]:
                state.append(True)  # collision on the right
            else:
                state.append(False)

            if snake_head[0] - CELL_SIZE == block[0] and snake_head[1] == block[1]:
                state.append(True)  # collision on the left
            else:
                state.append(False)

            if snake_head[1] + CELL_SIZE == block[1] and snake_head[0] == block[0]:
                state.append(True)  # collision below
            else:
                state.append(False)

            if snake_head[1] - CELL_SIZE == block[1] and snake_head[0] == block[0]:
                state.append(True)  # collision above
            else:
                state.append(False)

        return tuple(state)

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(ACTIONS)
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(ACTIONS))
        return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(ACTIONS))
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(len(ACTIONS))
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + DISCOUNT_FACTOR * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += LEARNING_RATE * td_error

    def decay_epsilon(self):
        self.epsilon = max(MIN_EPSILON, self.epsilon * EPSILON_DECAY)

# Training the agent
def train_agent(episodes):
    agent = QLearningAgent()
    game = Game()

    for episode in range(episodes):
        game.reset()
        state = agent.get_state(game)

        total_reward = 0
        step = 0

        while True:
            action = agent.choose_action(state)
            game.snake.change_direction(action)
            reward = 0
            if game.snake.move(game.food_pos):
                reward = 10
                game.food_pos = game.spawn_food()
            if game.snake.check_collision():
                reward = -10
                break
            next_state = agent.get_state(game)
            agent.update_q_table(state, action, reward, next_state)
            state = next_state
            total_reward += reward
            step += 1

            if step > 1000:
                break

        agent.decay_epsilon()
        print(f"Episode: {episode}, Total Reward: {total_reward}, Epsilon: {agent.epsilon}")

if __name__ == "__main__":
    train_agent(1000)
    pygame.quit()
    sys.exit()
