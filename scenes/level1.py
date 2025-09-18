# scenes/level1.py
import pygame


class Level1:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont(None, 40)

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                # Switch to next scene
                from scenes.cutscene_intro import CutsceneIntro
                self.manager.set_scene(CutsceneIntro(self.manager))

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((100, 150, 200))
        text = self.font.render(
            "Level 1 — Press SPACE to continue", True, (255, 255, 255))
        screen.blit(text, (50, 200))
