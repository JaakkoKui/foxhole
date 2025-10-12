import pygame

from core.game_state import SceneManager
from scenes.intro import CutsceneIntro

pygame.init()
S_WIDTH = 1200
S_HEIGHT = 800
FPS = 60
FramePerSec = pygame.time.Clock()
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption("Ketunkolo")
manager = SceneManager()
manager.set_scene(CutsceneIntro(manager))

running = True
while running:
    dt = FramePerSec.tick(FPS)
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False
    manager.handle_events(events)
    manager.update(dt)
    manager.draw(screen, dt)
    pygame.display.flip()

pygame.quit()
