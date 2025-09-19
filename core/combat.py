import random

import pygame


class Combat:

    def __init__(
        self,
        font,
        prompt_keys=None,
        prompt_time=1500,
        rounds=6,
        on_end=None,
        return_scene=None,
    ):
        self.font = font
        self.prompt_keys = prompt_keys or [
            pygame.K_a,
            pygame.K_s,
            pygame.K_d,
            pygame.K_f,
            pygame.K_g,
        ]
        self.prompt_time = prompt_time  # milliseconds to respond
        self.active = False
        self.current_key = None
        self.prompt_start = 0
        self.result = None  # None, 'win', or 'lose'
        self.result_time = None  # When result was set
        self.result_display_duration = 1500  # ms to show result before returning
        self.manager = None  # Will be set when scene is activated

        self.rounds = rounds
        self.current_round = 0
        self.failed = False
        self.on_end = on_end
        self.return_scene = return_scene

    def start(self):
        self.result_time = None
        self.active = True
        self.result = None
        self.current_round = 0
        self.failed = False
        self._next_prompt()

    def _next_prompt(self):
        self.current_key = random.choice(self.prompt_keys)
        self.prompt_start = pygame.time.get_ticks()

    def handle_events(self, events):
        if not self.active:
            return
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == self.current_key:
                    self.current_round += 1
                    if self.current_round >= self.rounds:
                        self.result = "win"
                        self.active = False
                        if self.on_end:
                            self.on_end(self.result)
                        if self.return_scene and self.manager:
                            self.manager.set_scene(self.return_scene)
                    else:
                        self._next_prompt()
                elif e.key in self.prompt_keys:
                    self.result = "lose"
                    self.active = False
                    self.failed = True
                    if self.on_end:
                        self.on_end(self.result)
                    if self.return_scene and self.manager:
                        self.manager.set_scene(self.return_scene)

    def update(self, dt):
        now = pygame.time.get_ticks()
        if self.active:
            if now - self.prompt_start > self.prompt_time:
                self.result = "lose"
                self.active = False
                self.failed = True
                if self.on_end:
                    self.on_end(self.result)
                if self.return_scene and self.manager:
                    self.manager.set_scene(self.return_scene)

    def draw(self, screen):
        if self.active:
            key_name = pygame.key.name(self.current_key).upper()
            prompt_rect = pygame.Rect(350, 300, 300, 80)
            pygame.draw.rect(screen, (255, 200, 200), prompt_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), prompt_rect, 2, border_radius=10)
            prompt_text = self.font.render(
                f"Press {key_name}! ({self.current_round+1}/{self.rounds})",
                True,
                (0, 0, 0),
            )
            screen.blit(prompt_text, (prompt_rect.x + 30, prompt_rect.y + 20))
