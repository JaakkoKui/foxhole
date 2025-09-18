import pygame

from core.game_state import SceneManager
from scenes.intro import CutsceneIntro

pygame.init()

vec = pygame.math.Vector2

SWIDTH = 1000
SHEIGHT = 800
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
pygame.display.set_caption("Foxhole")

manager = SceneManager()
manager.set_scene(CutsceneIntro(manager))

running = True

while running:
    dt = FramePerSec.tick(60)  # milliseconds since last frame
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False
    manager.handle_events(events)
    manager.update(dt)
    manager.draw(screen)
    pygame.display.flip()

pygame.quit()
