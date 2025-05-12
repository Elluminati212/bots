import pygame
import random
import sys
import time
from collections import deque
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Directions
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    @staticmethod
    def opposite(dir1, dir2):
        return (dir1.value[0] + dir2.value[0] == 0 and 
                dir1.value[1] + dir2.value[1] == 0)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.length = 3
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]
        self.direction = Direction.RIGHT
        self.score = 0
        
        # Create initial snake body
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i, self.positions[0][1]))
            
    def get_head_position(self):
        return self.positions[0]
    
    def change_direction(self, direction):
        if len(self.positions) > 1 and Direction.opposite(direction, self.direction):
            return
        self.direction = direction
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction.value
        
        # Calculate new position with wrapping
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Check for collision with self
        if new_position in self.positions[1:]:
            return False  # Game over
        
        # Move snake
        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return True
    
    def grow(self):
        self.length += 1
        self.score += 10
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            color = GREEN if i == 0 else (0, 200, 0)  # Head is brighter green
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position([])
    
    def randomize_position(self, occupied_positions):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in occupied_positions:
                break
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

class AIBot:
    def __init__(self, snake, food):
        self.snake = snake
        self.food = food
    
    def find_path(self):
        """Find a path to the food using BFS (Breadth-First Search)"""
        head = self.snake.get_head_position()
        food_pos = self.food.position
        
        # If food is right next to us, just move there
        for direction in Direction:
            dx, dy = direction.value
            new_x = (head[0] + dx) % GRID_WIDTH
            new_y = (head[1] + dy) % GRID_HEIGHT
            
            if (new_x, new_y) == food_pos:
                return direction
        
        # Use BFS to find a path to the food
        queue = deque([(head, [])])
        visited = set([head])
        snake_body = set(self.snake.positions[1:])  # Exclude head to allow movement
        
        while queue:
            (x, y), path = queue.popleft()
            
            # Try each direction
            for direction in Direction:
                dx, dy = direction.value
                new_x = (x + dx) % GRID_WIDTH
                new_y = (y + dy) % GRID_HEIGHT
                next_pos = (new_x, new_y)
                
                # If we found the food
                if next_pos == food_pos:
                    if not path:  # If we're adjacent to food
                        return direction
                    return path[0]  # Return first step in path
                
                # If the position is valid (not visited and not snake body)
                if next_pos not in visited and next_pos not in snake_body:
                    visited.add(next_pos)
                    new_path = list(path)
                    if not new_path:
                        new_path.append(direction)
                    else:
                        new_path = list(path)
                    queue.append((next_pos, new_path))
        
        # If no path to food is found, try to move safely
        return self.find_safe_move()
    
    def find_safe_move(self):
        """Find a move that won't cause immediate death"""
        head = self.snake.get_head_position()
        snake_body = set(self.snake.positions[1:])
        
        safe_directions = []
        for direction in Direction:
            if Direction.opposite(direction, self.snake.direction):
                continue  # Can't go backwards
                
            dx, dy = direction.value
            new_x = (head[0] + dx) % GRID_WIDTH
            new_y = (head[1] + dy) % GRID_HEIGHT
            new_pos = (new_x, new_y)
            
            if new_pos not in snake_body:
                safe_directions.append(direction)
        
        if safe_directions:
            return random.choice(safe_directions)
            
        # If no safe moves, just continue in current direction (will likely die)
        return self.snake.direction

def draw_grid(surface):
    for y in range(0, GRID_HEIGHT):
        for x in range(0, GRID_WIDTH):
            rect = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GRAY, rect, 1)

def main():
    # Setup game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game with AI')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 20)
    
    # Create game objects
    snake = Snake()
    food = Food()
    ai_bot = AIBot(snake, food)
    
    # Game state
    running = True
    game_over = False
    ai_mode = False
    
    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        # Reset game
                        snake.reset()
                        food.randomize_position(snake.positions)
                        game_over = False
                else:
                    if event.key == pygame.K_UP:
                        snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(Direction.RIGHT)
                    elif event.key == pygame.K_a:
                        # Toggle AI mode
                        ai_mode = not ai_mode
        
        if not game_over:
            # AI control
            if ai_mode:
                best_direction = ai_bot.find_path()
                snake.change_direction(best_direction)
            
            # Move snake
            if not snake.move():
                game_over = True
            
            # Check for food collision
            if snake.get_head_position() == food.position:
                snake.grow()
                food.randomize_position(snake.positions)
        
        # Draw everything
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        
        # Draw score
        score_text = font.render(f'Score: {snake.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw AI indicator
        ai_text = font.render(f"AI: {'ON' if ai_mode else 'OFF'}", True, WHITE)
        screen.blit(ai_text, (SCREEN_WIDTH - 100, 10))
        
        # Game over text
        if game_over:
            game_over_text = font.render('Game Over! Press R to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
        
        pygame.display.update()
        clock.tick(SNAKE_SPEED)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

