import pygame


class CutsceneIntro:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont(None, 40)
        self.timer = 0
        self.text_alpha = 255
        self.text_fade_duration = 2000
        self.text_surface = self.font.render(
            "Based on a true story...", True, (255, 255, 255))
        self.fox_image = pygame.image.load(
            "pictures/fromSide/foxStanding1.png")
        self.background = pygame.image.load("pictures/backgrounds/sofa.png")
        self.fox_pos = [100, 300]
        self.fox_direction = 1
        self.fox_talk_timer = 0

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                from scenes.level1 import Level1
                self.manager.set_scene(Level1(self.manager))

    def update(self, dt):
        self.timer += dt
        # After 15 seconds go to Level1 automatically
        if self.timer > 15000:
            from scenes.level1 import Level1
            self.manager.set_scene(Level1(self.manager))

        if self.timer > 2000:
            self.text_alpha -= (255 / self.text_fade_duration) * dt
            if self.text_alpha < 0:
                self.text_alpha = 0
            self.text_surface.set_alpha(self.text_alpha)

    def draw(self, screen):
        screen.fill((50, 50, 50))
        if self.text_alpha > 0:
            text_surface = self.text_surface.copy()
            text_surface.set_alpha(self.text_alpha)
            screen.blit(text_surface, (50, 200))
        else:
            # Display sofa.png as background after text has faded
            screen.blit(self.background, (0, 0))
