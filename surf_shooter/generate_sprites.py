import pygame
import os
import math

# Initialize Pygame
pygame.init()

# Create sprites directory if it doesn't exist
os.makedirs(os.path.join('assets', 'sprites'), exist_ok=True)

def draw_limb(surface, start_pos, end_pos, color, width=6):
    """Draw a limb (arm or leg) between two points"""
    pygame.draw.line(surface, color, start_pos, end_pos, width)
    # Add a joint at the end
    pygame.draw.circle(surface, color, (int(end_pos[0]), int(end_pos[1])), width//2)

def create_surfer_sprite(color_scheme):
    # Create a surface for the surfer
    surface = pygame.Surface((100, 140), pygame.SRCALPHA)
    
    # Color scheme
    body_color = color_scheme['body']
    board_color = color_scheme['board']
    skin_color = color_scheme['skin']
    
    # Draw surfboard
    board_points = [
        (15, 100),  # Front tip
        (25, 95),
        (75, 95),
        (85, 100),  # Back tip
        (75, 105),
        (25, 105)
    ]
    pygame.draw.polygon(surface, board_color, board_points)
    # Add board details
    pygame.draw.line(surface, (min(255, board_color[0] + 30), 
                             min(255, board_color[1] + 30),
                             min(255, board_color[2] + 30)), 
                    (25, 100), (75, 100), 2)
    
    # Draw legs in surfing stance
    draw_limb(surface, (50, 60), (40, 85), skin_color)  # Left leg
    draw_limb(surface, (50, 60), (60, 85), skin_color)  # Right leg
    
    # Draw torso
    pygame.draw.ellipse(surface, body_color, (40, 30, 20, 35))
    
    # Draw arms in dynamic pose
    draw_limb(surface, (50, 35), (30, 45), skin_color)  # Left arm
    draw_limb(surface, (50, 35), (70, 45), skin_color)  # Right arm
    
    # Draw head
    pygame.draw.circle(surface, skin_color, (50, 25), 10)  # Head
    # Add simple hair
    pygame.draw.arc(surface, (50, 25, 0), (40, 15, 20, 20), 0, math.pi, 3)
    
    # Add wetsuit details
    pygame.draw.line(surface, (255, 255, 255), (45, 40), (55, 40), 1)  # Wetsuit line
    
    return surface

def create_water_balloon():
    # Create a surface for the water balloon
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    
    # Draw a more detailed water balloon
    # Main balloon body
    pygame.draw.circle(surface, (30, 144, 255), (20, 22), 12)  # Main balloon
    # Add water effect
    pygame.draw.circle(surface, (135, 206, 250), (16, 18), 4)  # Water highlight
    # Balloon tie
    pygame.draw.polygon(surface, (200, 200, 200), 
                       [(18, 10), (22, 10), (20, 15)])  # Tie
    # Add some droplet effects around
    for pos in [(15, 25), (25, 25), (20, 30)]:
        pygame.draw.circle(surface, (135, 206, 250), pos, 2)
    
    return surface

# Define color schemes
PLAYER_COLORS = {
    'body': (0, 100, 255),    # Blue wetsuit
    'board': (255, 215, 0),   # Gold board
    'skin': (255, 218, 185)   # Light skin tone
}

SURFER_COLORS = {
    'body': (50, 50, 50),     # Black wetsuit
    'board': (139, 69, 19),   # Brown board
    'skin': (210, 180, 140)   # Darker skin tone
}

# Generate and save sprites
sprites = {
    'player.png': create_surfer_sprite(PLAYER_COLORS),
    'surfer.png': create_surfer_sprite(SURFER_COLORS),
    'water_balloon.png': create_water_balloon()
}

# Save all sprites
for filename, surface in sprites.items():
    pygame.image.save(surface, os.path.join('assets', 'sprites', filename))

print("Sprites generated successfully!") 