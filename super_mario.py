#!/usr/bin/env python3
# Super Mario Style Game with AI and User Controls
# Created using Pygame

import pygame
import random
import os
import sys
import time
from enum import Enum

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.8
SCROLL_THRESH = 200
PLAYER_SPEED = 5
JUMP_STRENGTH = -16
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)

# Game states
class GameState(Enum):
    MENU = 0
    INSTRUCTIONS = 1
    PLAYING = 2
    GAME_OVER = 3
    AI_MODE = 4

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Style Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load fonts
pygame.font.init()
font_small = pygame.font.Font(None, 30)
font_medium = pygame.font.Font(None, 40)
font_large = pygame.font.Font(None, 60)

# Create simple colored rectangles for sprites (in a real game, you'd use image assets)
def create_rect_surface(width, height, color):
    surface = pygame.Surface((width, height))
    surface.fill(color)
    return surface

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = create_rect_surface(40, 60, RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.vel_x = 0
        self.jumping = False
        self.direction = 1  # 1 for right, -1 for left
        self.on_ground = False
        self.health = 3
        self.score = 0
        self.invincible = False
        self.invincible_timer = 0
        self.ai_controlled = False
        
    def update(self, platforms, enemies, coins, scroll):
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Horizontal movement (AI or user)
        if self.ai_controlled:
            self.ai_movement(platforms, enemies)
        else:
            # Reset horizontal velocity
            self.vel_x = 0
            
            # Check for keyboard input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.vel_x = -PLAYER_SPEED
                self.direction = -1
            if keys[pygame.K_RIGHT]:
                self.vel_x = PLAYER_SPEED
                self.direction = 1
            if keys[pygame.K_SPACE] and self.on_ground:
                self.jump()
        
        # Move in the X direction
        self.rect.x += self.vel_x
        
        # Check for horizontal collisions
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if self.vel_x > 0:  # Moving right
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:  # Moving left
                    self.rect.left = platform.rect.right
        
        # Move in the Y direction
        self.rect.y += self.vel_y
        self.on_ground = False
        
        # Check for vertical collisions
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        
        # Check for enemy collisions
        if not self.invincible:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    if self.vel_y > 0 and self.rect.bottom < enemy.rect.top + 20:
                        # Jumped on enemy
                        enemy.kill()
                        self.score += 100
                        self.vel_y = -10  # Bounce
                    else:
                        # Hit by enemy
                        self.health -= 1
                        self.invincible = True
                        self.invincible_timer = pygame.time.get_ticks()
        
        # Check invincibility timer
        if self.invincible and pygame.time.get_ticks() - self.invincible_timer > 2000:
            self.invincible = False
        
        # Check for coin collisions
        for coin in coins:
            if self.rect.colliderect(coin.rect):
                self.score += 50
                coin.kill()
        
        # Prevent falling off the bottom of the screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            self.on_ground = True
        
        # Prevent going off the left side of the screen
        if self.rect.left < 0:
            self.rect.left = 0
        
        # Determine if scrolling should happen
        scroll_direction = 0
        if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH) and scroll < 3000 and self.vel_x > 0:
            scroll_direction = 1  # Scroll right
            self.rect.x -= self.vel_x  # Keep player in position
        elif (self.rect.left < SCROLL_THRESH) and scroll > 0 and self.vel_x < 0:
            scroll_direction = -1  # Scroll left
            self.rect.x -= self.vel_x  # Keep player in position
        
        return scroll_direction
    
    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            pygame.mixer.Sound.play(jump_sound)
    
    def ai_movement(self, platforms, enemies):
        # Simple AI behavior:
        # 1. Avoid enemies by jumping over them
        # 2. Jump over gaps
        # 3. Jump when approaching a wall
        # 4. Try to move right most of the time
        
        # Default: move right
        self.vel_x = PLAYER_SPEED
        self.direction = 1
        
        # Look for enemies in front
        for enemy in enemies:
            if 0 < enemy.rect.x - self.rect.x < 200 and abs(enemy.rect.y - self.rect.y) < 50:
                if self.on_ground:
                    self.jump()
                    break
        
        # Check for walls ahead
        wall_ahead = False
        for platform in platforms:
            # If there's a wall in front
            if (abs(platform.rect.left - self.rect.right) < 10 or abs(platform.rect.bottom - self.rect.top) < 20) and \
               platform.rect.top < self.rect.bottom:
                if self.on_ground:
                    self.jump()
                    break
        
        # Check for gaps
        on_edge = True
        for platform in platforms:
            if self.on_ground and self.rect.bottom == platform.rect.top:
                # Check if we have ground for the next few steps
                test_x = self.rect.right + 50
                if platform.rect.left <= test_x <= platform.rect.right:
                    on_edge = False
                    break
        
        if on_edge and self.on_ground:
            self.jump()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, move_range=100):
        super().__init__()
        self.image = create_rect_surface(40, 40, BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_speed = random.randint(1, 3)
        self.direction = 1  # 1 for right, -1 for left
        self.start_x = x
        self.move_range = move_range
    
    def update(self, scroll):
        # Move horizontally within defined range
        self.rect.x += self.move_speed * self.direction
        
        # Change direction if moved too far
        if self.rect.x > self.start_x + self.move_range:
            self.direction = -1
        elif self.rect.x < self.start_x - self.move_range:
            self.direction = 1
        
        # Update position based on screen scrolling (safely)
        if scroll != 0:
            new_x = self.rect.x - scroll
            # Ensure value stays within valid range
            self.rect.x = max(-1000, min(new_x, 10000))
            
        # Update start_x for movement range calculation
        if scroll != 0:
            self.start_x -= scroll

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, is_moving=False, move_range=0):
        super().__init__()
        self.image = create_rect_surface(width, height, BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_moving = is_moving
        self.move_speed = 2 if is_moving else 0
        self.direction = 1  # 1 for right, -1 for left
        self.start_x = x
        self.move_range = move_range
    
    def update(self, scroll=0):
        # Update for scrolling (safely)
        if scroll != 0:
            new_x = self.rect.x - scroll
            # Ensure value stays within valid range
            self.rect.x = max(-1000, min(new_x, 10000))
            
            # Update start_x for movement range calculation
            self.start_x -= scroll
        
        # Handle movement if it's a moving platform
        if self.is_moving:
            self.rect.x += self.move_speed * self.direction
            
            # Change direction if moved too far
            if self.rect.x > self.start_x + self.move_range:
                self.direction = -1
            elif self.rect.x < self.start_x - self.move_range:
                self.direction = 1

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = create_rect_surface(20, 20, (255, 215, 0))  # Gold color
        pygame.draw.circle(self.image, (255, 255, 0), (10, 10), 8)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, scroll=0):
        # Update for scrolling (safely)
        if scroll != 0:
            new_x = self.rect.x - scroll
            # Ensure value stays within valid range
            self.rect.x = max(-1000, min(new_x, 10000))

# Load sounds
jump_sound = pygame.mixer.Sound(os.path.join('sounds', 'jump.wav')) if os.path.exists(os.path.join('sounds', 'jump.wav')) else None
coin_sound = pygame.mixer.Sound(os.path.join('sounds', 'coin.wav')) if os.path.exists(os.path.join('sounds', 'coin.wav')) else None
game_over_sound = pygame.mixer.Sound(os.path.join('sounds', 'gameover.wav')) if os.path.exists(os.path.join('sounds', 'gameover.wav')) else None

# Fallback: Create dummy sounds if files don't exist
if jump_sound is None:
    jump_sound = pygame.mixer.Sound(pygame.sndarray.array(bytearray([0] * 1000)))
if coin_sound is None:
    coin_sound = pygame.mixer.Sound(pygame.sndarray.array(bytearray([0] * 1000)))
if game_over_sound is None:
    game_over_sound = pygame.mixer.Sound(pygame.sndarray.array(bytearray([0] * 1000)))

# Main Game class
class SuperMarioGame:
    def __init__(self):
        self.game_state = GameState.MENU
        self.scroll = 0
        self.prev_scroll = 0
        self.level_length = 5000
        self.reset_game()
    
    def reset_game(self):
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        
        # Create player
        self.player = Player(100, 100)
        self.all_sprites.add(self.player)
        
        # Create level
        self.create_level()
    
    def create_level(self):
        # Create ground
        ground_height = 50
        for x in range(0, self.level_length, 100):
            # Create gaps in the ground for challenge
            if random.random() > 0.8 and x > 500:  # No gaps in the first 500 pixels
                continue
            
            platform = Platform(x, SCREEN_HEIGHT - ground_height, 100, ground_height)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
        # Create platforms
        for i in range(30):
            x = random.randint(200, self.level_length - 200)
            y = random.randint(200, SCREEN_HEIGHT - 150)
            width = random.randint(60, 150)
            
            # Some platforms move
            is_moving = random.random() > 0.7
            move_range = random.randint(50, 150) if is_moving else 0
            
            platform = Platform(x, y, width, 20, is_moving, move_range)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
        # Create enemies
        for i in range(15):
            x = random.randint(500, self.level_length - 200)  # No enemies in the first 500 pixels
            y = random.randint(0, SCREEN_HEIGHT - 100)
            enemy = Enemy(x, y, move_range=100)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
        # Create coins
        for i in range(50):
            x = random.randint(100, self.level_length - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)
            coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state in [GameState.PLAYING, GameState.AI_MODE]:
                        self.game_state = GameState.MENU
                    else:
                        return False
                
                if self.game_state == GameState.MENU:
                    if event.key == pygame.K_1:
                        self.reset_game()
                        self.game_state = GameState.PLAYING
                        self.player.ai_controlled = False
                    elif event.key == pygame.K_2:
                        self.reset_game()
                        self.game_state = GameState.AI_MODE
                        self.player.ai_controlled = True
                    elif event.key == pygame.K_3:
                        self.game_state = GameState.INSTRUCTIONS
                    elif event.key == pygame.K_4:
                        return False
                
                elif self.game_state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.game_state = GameState.PLAYING
                        self.player.ai_controlled = False
                
                elif self.game_state == GameState.INSTRUCTIONS:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.MENU
        
        return True
    
    def update(self):
        if self.game_state in [GameState.PLAYING, GameState.AI_MODE]:
            # Get scroll direction from player update
            scroll_dir = self.player.update(self.platforms, self.enemies, self.coins, self.scroll)
            
            # Calculate actual scroll amount
            scroll_amount = 0
            if scroll_dir != 0:
                # Determine how much to scroll
                scroll_speed = PLAYER_SPEED
                scroll_amount = scroll_dir * scroll_speed
                
                # Update total scroll value (with limits)
                self.scroll = max(0, min(self.scroll + scroll_amount, 3000))
                
                # Update all sprites with the scroll amount
                for sprite in self.all_sprites:
                    if sprite != self.player:
                        sprite.update(scroll_amount)

            # Update moving platforms and enemies even if not scrolling
            if scroll_amount == 0:
                for sprite in self.all_sprites:
                    if (sprite != self.player and 
                        (isinstance(sprite, Enemy) or 
                         (isinstance(sprite, Platform) and sprite.is_moving))):
                        sprite.update(0)
            
            # Check player health
            if self.player.health <= 0:
                self.game_state = GameState.GAME_OVER
                pygame.mixer.Sound.play(game_over_sound)
            
            # Check if player reached the end
            if self.player.rect.x > self.level_length - 100:
                self.game_state = GameState.GAME_OVER
    
    def draw_text(self, text, font, color, x, y, center=True):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)
    
    def draw_hud(self):
        # Draw HUD background
        hud_height = 40
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, SCREEN_WIDTH, hud_height))
        
        # Draw score
        self.draw_text(f"Score: {self.player.score}", font_small, WHITE, 80, hud_height // 2, True)
        
        # Draw health
        self.draw_text(f"Lives: {self.player.health}", font_small, WHITE, SCREEN_WIDTH - 80, hud_height // 2, True)
        
        # Draw game mode
        mode_text = "AI Mode" if self.player.ai_controlled else "Player Mode"
        self.draw_text(mode_text, font_small, WHITE, SCREEN_WIDTH // 2, hud_height // 2, True)
    
    def draw_menu(self):
        # Draw background
        screen.fill(SKY_BLUE)
        
        # Draw title
        self.draw_text("SUPER MARIO STYLE GAME", font_large, RED, SCREEN_WIDTH // 2, 100, True)
        
        # Draw menu options
        self.draw_text("1. Start Game", font_medium, WHITE, SCREEN_WIDTH // 2, 250, True)
        self.draw_text("2. AI Mode", font_medium, WHITE, SCREEN_WIDTH // 2, 300, True)
        self.draw_text("3. Instructions", font_medium, WHITE, SCREEN_WIDTH // 2, 350, True)
        self.draw_text("4. Quit", font_medium, WHITE, SCREEN_WIDTH // 2, 400, True)
        
        # Draw footer
        self.draw_text("Use number keys to select an option", font_small, WHITE, SCREEN_WIDTH // 2, 500, True)
    
    def draw_instructions(self):
        # Draw background
        screen.fill((0, 0, 50))
        
        # Draw title
        self.draw_text("INSTRUCTIONS", font_large, WHITE, SCREEN_WIDTH // 2, 80, True)
        
        # Draw instructions
        instructions = [
            "LEFT/RIGHT ARROW KEYS: Move left/right",
            "SPACE: Jump",
            "ESCAPE: Return to menu",
            "",
            "GOAL: Collect coins and defeat enemies to score points",
            "Jump on enemies to defeat them",
            "Avoid touching enemies from the sides",
            "Watch out for gaps and moving platforms",
            "",
            "AI MODE: Watch the computer play automatically",
            "",
            "Press ENTER or ESC to return to the main menu"
        ]
        
        for i, line in enumerate(instructions):
            self.draw_text(line, font_small, WHITE, SCREEN_WIDTH // 2, 150 + i * 30, True)
    
    def draw_game_over(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha
        screen.blit(overlay, (0, 0))
        
        # Draw game over text
        self.draw_text("GAME OVER", font_large, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, True)
        
        # Draw score
        self.draw_text(f"Final Score: {self.player.score}", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, True)
        
        # Draw restart instruction
        self.draw_text("Press R to restart or ESC to return to menu", font_small, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3, True)
    
    def draw(self):
        if self.game_state == GameState.MENU:
            self.draw_menu()
        elif self.game_state == GameState.INSTRUCTIONS:
            self.draw_instructions()
        elif self.game_state in [GameState.PLAYING, GameState.AI_MODE]:
            # Draw background
            screen.fill(SKY_BLUE)
            
            # Draw all sprites
            for sprite in self.all_sprites:
                screen.blit(sprite.image, sprite.rect)
            
            # Draw HUD
            self.draw_hud()
        elif self.game_state == GameState.GAME_OVER:
            # Draw game world in background
            screen.fill(SKY_BLUE)
            for sprite in self.all_sprites:
                screen.blit(sprite.image, sprite.rect)
            
            # Draw game over screen
            self.draw_game_over()
    
    def run(self):
        running = True
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update
            self.update()
            
            # Draw
            self.draw()
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            clock.tick(FPS)

# Create directories for sounds if they don't exist
os.makedirs('sounds', exist_ok=True)

# Main game loop
def main():
    game = SuperMarioGame()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
