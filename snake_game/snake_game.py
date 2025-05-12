import pygame
import random
import numpy as np
from collections import deque

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_SIZE // GRID_SIZE
GRID_HEIGHT = WINDOW_SIZE // GRID_SIZE
FPS = 15  # Higher FPS for more responsive controls

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
DARK_GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)
        self.big_font = pygame.font.SysFont('Arial', 40)
        self.ai_mode = False
        self.paused = False
        self.direction_changed = False
        self.reset_game()
    
    def reset_game(self):
        self.snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = (1, 0)  # Start moving right
        self.prev_direction = self.direction
        self.food = self.generate_food()
        self.score = 0
        self.is_alive = True
        self.direction_changed = False
    
    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if food not in self.snake:
                return food
    
    def find_path_to_food(self):
        start = self.snake[0]
        goal = self.food
        queue = deque([[start]])
        visited = set([start])
        
        while queue:
            path = queue.popleft()
            row, col = path[-1]
            
            if (row, col) == goal:
                return path
                
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                r, c = row + dr, col + dc
                if (0 <= r < GRID_WIDTH and 0 <= c < GRID_HEIGHT and 
                    (r, c) not in visited and (r, c) not in self.snake[:-1]):
                    queue.append(path + [(r, c)])
                    visited.add((r, c))
        
        return None
    
    def on_key_press(self, event):
        # Don't allow direction changes if we already changed direction in this frame
        if self.direction_changed:
            return
            
        # Handle direction changes
        if event.key == pygame.K_LEFT and self.prev_direction != (1, 0):
            self.direction = (-1, 0)
            self.direction_changed = True
        elif event.key == pygame.K_RIGHT and self.prev_direction != (-1, 0):
            self.direction = (1, 0)
            self.direction_changed = True
        elif event.key == pygame.K_UP and self.prev_direction != (0, 1):
            self.direction = (0, -1)
            self.direction_changed = True
        elif event.key == pygame.K_DOWN and self.prev_direction != (0, -1):
            self.direction = (0, 1)
            self.direction_changed = True
        
        # Toggle AI mode
        elif event.key == pygame.K_a:
            self.ai_mode = not self.ai_mode
        # Toggle pause
        elif event.key == pygame.K_p:
            self.paused = not self.paused
    
    def update(self):
        # Don't update if game is paused or over
        if not self.is_alive or self.paused:
            return
        
        # Reset direction change flag
        self.direction_changed = False
        
        # AI mode logic - only if AI is enabled
        if self.ai_mode:
            # Find path to food using AI
            path = self.find_path_to_food()
            if path and len(path) > 1:
                next_pos = path[1]
                new_direction = (next_pos[0] - self.snake[0][0], next_pos[1] - self.snake[0][1])
                # Don't move in the opposite direction
                if (new_direction[0] != -self.prev_direction[0] or 
                    new_direction[1] != -self.prev_direction[1]):
                    self.direction = new_direction
        
        # Remember the previous direction before moving
        self.prev_direction = self.direction
        
        # Move snake
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        
        # Check collision
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or 
            new_head in self.snake):
            self.is_alive = False
            return
            
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()
    
    def draw_grid(self):
        # Draw grid lines
        for x in range(0, WINDOW_SIZE, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_SIZE))
        for y in range(0, WINDOW_SIZE, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_SIZE, y))
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        self.draw_grid()
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(self.screen, color, 
                            (segment[0]*GRID_SIZE + 1, segment[1]*GRID_SIZE + 1, 
                             GRID_SIZE - 2, GRID_SIZE - 2))
            
            # Draw eyes on the head
            if i == 0:
                # Position eyes based on direction
                dx, dy = self.direction
                # Left eye
                left_eye_x = segment[0]*GRID_SIZE + 5 + dx * 3
                left_eye_y = segment[1]*GRID_SIZE + 5 + dy * 3
                # Right eye
                right_eye_x = segment[0]*GRID_SIZE + GRID_SIZE - 7 + dx * 3
                right_eye_y = segment[1]*GRID_SIZE + 5 + dy * 3
                
                if dx == 0:  # Moving vertically
                    left_eye_x = segment[0]*GRID_SIZE + 5
                    right_eye_x = segment[0]*GRID_SIZE + GRID_SIZE - 7
                if dy == 0:  # Moving horizontally
                    left_eye_y = segment[1]*GRID_SIZE + 5
                    right_eye_y = segment[1]*GRID_SIZE + GRID_SIZE - 7
                
                pygame.draw.circle(self.screen, BLACK, (int(left_eye_x), int(left_eye_y)), 2)
                pygame.draw.circle(self.screen, BLACK, (int(right_eye_x), int(right_eye_y)), 2)
        
        # Draw food
        pygame.draw.rect(self.screen, RED, 
                        (self.food[0]*GRID_SIZE + 1, self.food[1]*GRID_SIZE + 1, 
                         GRID_SIZE - 2, GRID_SIZE - 2))
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw AI mode status
        ai_mode_text = self.font.render(f'AI Mode: {"ON" if self.ai_mode else "OFF"}', True, 
                                        YELLOW if self.ai_mode else WHITE)
        self.screen.blit(ai_mode_text, (WINDOW_SIZE - 150, 10))
        
        # Draw pause indicator
        if self.paused:
            pause_text = self.font.render('PAUSED', True, YELLOW)
            self.screen.blit(pause_text, (WINDOW_SIZE // 2 - 40, 10))
        
        # Draw game over screen
        if not self.is_alive:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = self.big_font.render('GAME OVER', True, RED)
            self.screen.blit(game_over_text, 
                            (WINDOW_SIZE // 2 - game_over_text.get_width() // 2, 
                             WINDOW_SIZE // 2 - 50))
            
            # Final score
            final_score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
            self.screen.blit(final_score_text, 
                            (WINDOW_SIZE // 2 - final_score_text.get_width() // 2, 
                             WINDOW_SIZE // 2))
            
            # Restart instructions
            restart_text = self.font.render('Press R to restart', True, WHITE)
            self.screen.blit(restart_text, 
                            (WINDOW_SIZE // 2 - restart_text.get_width() // 2, 
                             WINDOW_SIZE // 2 + 40))
            
        # Draw controls help
        controls_text = [
            "Controls:",
            "Arrow Keys - Move Snake",
            "A - Toggle AI Mode",
            "P - Pause/Resume",
            "R - Restart (when game over)"
        ]
        
        for i, text in enumerate(controls_text):
            help_text = self.font.render(text, True, WHITE)
            self.screen.blit(help_text, (10, WINDOW_SIZE - 120 + i * 22))
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    # Handle restart
                    if event.key == pygame.K_r and not self.is_alive:
                        self.reset_game()
                    # Process direction and game control keys
                    elif self.is_alive:
                        self.on_key_press(event)
            
            self.update()
            self.draw()
            pygame.display.flip()  # Update the display
            self.clock.tick(FPS)  # Use the defined FPS constant

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
