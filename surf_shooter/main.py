import asyncio
import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLUE = (0, 128, 255)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (0, 100, 200)
SAND = (238, 214, 175)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Surf Shooter")
clock = pygame.time.Clock()

# Load images
def load_image(name: str, scale: float = 1.0):
    try:
        image = pygame.image.load(os.path.join('assets', 'sprites', name))
        image = pygame.transform.scale(image, 
                                    (int(image.get_width() * scale), 
                                     int(image.get_height() * scale)))
        return image
    except pygame.error:
        # If image loading fails, create a colored rectangle as fallback
        surf = pygame.Surface((40, 60))
        surf.fill(BLACK)
        return surf

# Load sprites
PLAYER_SPRITE = load_image('player.png', 0.8)
SURFER_SPRITE = load_image('surfer.png', 0.8)
WATER_BALLOON = load_image('water_balloon.png', 0.5)

class Wave:
    def __init__(self):
        self.amplitude = 20
        self.frequency = 0.02
        self.speed = 0.05
        self.time = 0
        self.wave_points = []
        self.wave_segments = 40
        self.update_wave_points()

    def update_wave_points(self):
        self.wave_points = []
        for x in range(0, WINDOW_WIDTH, self.wave_segments):
            # Create multiple overlapping sine waves for more natural look
            y = (math.sin(self.time + x * self.frequency) * self.amplitude +
                 math.sin(self.time * 0.7 + x * self.frequency * 1.2) * self.amplitude * 0.5)
            y += WINDOW_HEIGHT - 150  # Base wave height
            self.wave_points.append((x, y))

    def update(self):
        self.time += self.speed
        self.update_wave_points()

    def draw(self, surface):
        # Draw multiple waves with different colors for depth
        for offset in range(3):
            points = [(x, y + offset * 20) for x, y in self.wave_points]
            points.append((WINDOW_WIDTH, WINDOW_HEIGHT))
            points.append((0, WINDOW_HEIGHT))
            
            color = DARK_BLUE if offset == 2 else LIGHT_BLUE if offset == 1 else BLUE
            pygame.draw.polygon(surface, color, points)

    def get_height_at(self, x):
        # Get the wave height at a specific x position for surfer positioning
        segment_index = int(x // self.wave_segments)
        if segment_index >= len(self.wave_points) - 1:
            return self.wave_points[-1][1]
        
        x1, y1 = self.wave_points[segment_index]
        x2, y2 = self.wave_points[segment_index + 1]
        
        # Linear interpolation between wave points
        ratio = (x - x1) / self.wave_segments
        return y1 + (y2 - y1) * ratio

class Player:
    def __init__(self):
        self.image = PLAYER_SPRITE
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = WINDOW_HEIGHT - 120
        self.projectiles = []

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for projectile in self.projectiles:
            if WATER_BALLOON:
                balloon_rect = WATER_BALLOON.get_rect(center=(int(projectile['x']), int(projectile['y'])))
                surface.blit(WATER_BALLOON, balloon_rect)
            else:
                pygame.draw.circle(surface, RED, (int(projectile['x']), int(projectile['y'])), 5)

    def shoot(self, target_x, target_y):
        # Calculate direction vector
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        # Normalize the vector
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            dx = dx / distance
            dy = dy / distance
        
        self.projectiles.append({
            'x': self.rect.centerx,
            'y': self.rect.centery,
            'dx': dx * 10,
            'dy': dy * 10
        })

    def update_projectiles(self):
        # Update projectile positions and remove ones that are off-screen
        self.projectiles = [p for p in self.projectiles if 0 <= p['x'] <= WINDOW_WIDTH and 0 <= p['y'] <= WINDOW_HEIGHT]
        for p in self.projectiles:
            p['x'] += p['dx']
            p['y'] += p['dy']

class Surfer:
    def __init__(self, x, y):
        self.image = SURFER_SPRITE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_hit = False
        self.speed = random.uniform(3, 6)
        self.direction = 1
        self.original_y = y

    def update(self, wave):
        if not self.is_hit:
            # Horizontal movement
            self.rect.x += self.speed * self.direction
            
            # Change direction when hitting screen bounds
            if self.rect.right > WINDOW_WIDTH - 20:
                self.direction = -1
            elif self.rect.left < 400:
                self.direction = 1
            
            # Follow wave height
            wave_height = wave.get_height_at(self.rect.centerx)
            self.rect.bottom = wave_height + 10

    def draw(self, surface):
        if not self.is_hit:
            # Tilt the surfer based on direction
            if self.direction == 1:
                rotated_image = pygame.transform.rotate(self.image, -15)
            else:
                rotated_image = pygame.transform.rotate(pygame.transform.flip(self.image, True, False), 15)
            surface.blit(rotated_image, self.rect)

    def check_hit(self, projectile):
        if not self.is_hit:
            return self.rect.collidepoint(projectile['x'], projectile['y'])
        return False

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

def reset_game():
    # Reset game objects
    player.projectiles.clear()
    surfers.clear()
    surfers.extend([
        Surfer(600, 180),
        Surfer(650, 220),
        Surfer(700, 160),
    ])
    wave.time = 0
    wave.update_wave_points()

# Game objects
player = Player()
wave = Wave()
surfers = [
    Surfer(600, 180),
    Surfer(650, 220),
    Surfer(700, 160),
]

# Create restart button (centered, below win text)
restart_button = Button(
    WINDOW_WIDTH//2 - 60,
    WINDOW_HEIGHT//2 + 50,
    120, 40,
    "Restart",
    (100, 200, 100)
)

async def main():
    # Game loop
    running = True
    game_won = False
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if game_won:
                        if restart_button.handle_event(event):
                            game_won = False
                            reset_game()
                    else:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        player.shoot(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEMOTION and game_won:
                restart_button.handle_event(event)

        # Update
        player.update_projectiles()
        wave.update()
        
        # Update surfers
        for surfer in surfers:
            surfer.update(wave)
        
        # Check for hits
        for surfer in surfers:
            for projectile in player.projectiles[:]:
                if surfer.check_hit(projectile):
                    surfer.is_hit = True
                    if projectile in player.projectiles:
                        player.projectiles.remove(projectile)
                    break

        # Draw
        # Background
        screen.fill(LIGHT_BLUE)  # Sky
        wave.draw(screen)  # Draw waves
        pygame.draw.rect(screen, SAND, (0, WINDOW_HEIGHT - 80, WINDOW_WIDTH, 80))  # Beach
        
        # Game objects
        player.draw(screen)
        for surfer in surfers:
            surfer.draw(screen)

        # Check win condition
        game_won = all(surfer.is_hit for surfer in surfers)
        if game_won:
            font = pygame.font.Font(None, 74)
            text = font.render('Clear to Surf!', True, BLACK)
            screen.blit(text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2))
            restart_button.draw(screen)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)
        
        # CRITICAL: Yield control back to browser
        await asyncio.sleep(0)

asyncio.run(main()) 