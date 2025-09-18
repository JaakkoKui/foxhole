import pygame

# Initialize pygame
pygame.init()

# Set up the display
vec = pygame.math.Vector2

SWIDTH = 800
SHEIGHT = 600
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
pygame.display.set_caption("Fox Hole") 

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., black)
    screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()