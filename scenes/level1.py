import pygame

import core.combat
from core.segis import segis
from scenes.intro import CutsceneIntro


class Level1:

    def __init__(self, manager):
        self.segis_color_phase = 0.0
        if self.segis_color_phase > 1.0:
            self.segis_color_phase -= 1.0
        self.manager = manager
        self.font = pygame.font.SysFont(None, 40)
        self.frame_width, self.frame_height = 200, 140
        self.player_image = pygame.image.load(
            "pictures/fromSide/frownFox.png"
        ).convert_alpha()
        self.background = pygame.image.load("pictures/backgrounds/kitchen.png")
        self.jump_image = pygame.image.load(
            "pictures/fromSide/foxJump.png"
        ).convert_alpha()
        self.fox_standing = pygame.image.load(
            "pictures/fromSide/foxStanding.png"
        ).convert_alpha()
        self.background = pygame.transform.scale(
            self.background, pygame.display.get_surface().get_size()
        )
        screen = pygame.display.get_surface()
        self.screen_w = screen.get_width()
        self.screen_h = screen.get_height()
        self.player_x, self.player_y = self.screen_w - 0.75 * self.screen_w, 700
        self.player_speed = 7
        self.floor_start = (0, 710)
        self.floor_end = (1000, 780)
        self.block_x, self.block_y = self.screen_w - 0.83 * self.screen_w, 0
        self.block_width, self.block_height = 5, 800
        self.end_block_x, self.end_block_y = screen.get_width() + 100, 700
        self.end_block_width, self.end_block_height = 10, 200
        self.gravity = 0.5
        self.velocity_y = 0
        self.jump_strength = -10
        self.is_jumping = False
        self.clock = pygame.time.Clock()
        self.facing_right = True
        self.show_drink_prompt = False
        self.wins = 0
        self.did_drink = False
        self.fox_did_drink = pygame.image.load(
            "pictures/fromSide/foxDidDrink.png"
        ).convert_alpha()

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.manager.set_scene(CutsceneIntro(self.manager))
                elif e.key == pygame.K_UP and not self.is_jumping:
                    self.velocity_y = self.jump_strength
                    self.is_jumping = True
                elif e.key == pygame.K_g and self.show_drink_prompt:

                    def combat_callback(result):

                        if result == "win":
                            self.did_drink = False
                            self.player_image = self.fox_standing
                            combat_scene.return_scene = self
                            segis.add(5)
                            self.wins += 1
                            print(f"Wins: {self.wins}")
                        else:
                            self.did_drink = True
                            self.player_image = self.fox_did_drink
                            self.player_speed = 0
                            fade_surface = pygame.Surface(self.background.get_size())
                            fade_surface.fill((0, 0, 0))

                            fox_image = pygame.transform.scale(
                                self.player_image, (self.frame_width, self.frame_height)
                            )
                            screen = pygame.display.get_surface()
                            fox_x = (screen.get_width() - self.frame_width) // 2
                            fox_y = (screen.get_height() - self.frame_height) // 1.5
                            for alpha in range(0, 256, 10):
                                screen.blit(self.background, (0, 0))
                                fade_surface.set_alpha(alpha)
                                screen.blit(fade_surface, (0, 0))
                                pygame.display.flip()
                                pygame.time.delay(50)
                            screen.fill((0, 0, 0))
                            screen.blit(fox_image, (fox_x, fox_y))
                            prompt_text = self.font.render(
                                "Ei bisse maistu, huomenna uus yritys.",
                                True,
                                (200, 200, 200),
                            )
                            screen.blit(
                                prompt_text,
                                (
                                    (screen.get_width()) // 4,
                                    (screen.get_height()) // 3.5,
                                ),
                            )
                            pygame.display.flip()
                            segis.reset()
                            pygame.time.delay(3500)
                            # Transition to the intro cutscene after drinking
                            self.manager.set_scene(CutsceneIntro(self.manager))

                    combat_scene = core.combat.Combat(
                        self.font,
                        prompt_time=2000,
                        rounds=1,
                        on_end=combat_callback,
                        return_scene=None,
                    )
                    combat_scene.start()
                    combat_scene.manager = self.manager
                    self.manager.set_scene(combat_scene)
                    self.show_drink_prompt = False

    def update(self, dt):
        # ...existing code...
        # Remove early usage of player_rect, ensure it is defined before use
        # Reset drink state if moving after drinking
        segis_value = segis.get()
        speed = 0.000005 * segis_value  # much slower, tune as needed
        self.segis_color_phase += speed * dt
        segis.update(dt)  # Decay segis over time
        if self.did_drink and (
            pygame.key.get_pressed()[pygame.K_LEFT]
            or pygame.key.get_pressed()[pygame.K_RIGHT]
        ):
            self.did_drink = False
        fridge_x_min = self.screen_w - 0.5 * self.screen_w
        fridge_x_max = self.screen_w - 0.35 * self.screen_w
        if fridge_x_min <= self.player_x <= fridge_x_max and not self.did_drink:
            self.show_drink_prompt = True
        else:
            self.show_drink_prompt = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_x -= self.player_speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.player_x += self.player_speed
            self.facing_right = True
        self.velocity_y += self.gravity
        self.player_y += self.velocity_y
        x0, y0 = self.floor_start
        x1, y1 = self.floor_end
        floor_y_at_x = y0 + (y1 - y0) * ((self.player_x - x0) / (x1 - x0))
        player_rect = pygame.Rect(
            self.player_x, self.player_y, self.frame_width, self.frame_height
        )
        block_rect = pygame.Rect(
            self.block_x, self.block_y, self.block_width, self.block_height
        )
        end_block_rect = pygame.Rect(
            self.end_block_x,
            self.end_block_y,
            self.end_block_width,
            self.end_block_height,
        )
        if player_rect.colliderect(end_block_rect):
            from scenes.level2 import Level2

            self.manager.set_scene(Level2(self.manager))
        elif player_rect.colliderect(block_rect):
            # Calculate overlap on each side
            dx_right = block_rect.right - player_rect.left
            dx_left = player_rect.right - block_rect.left
            dy_bottom = block_rect.bottom - player_rect.top
            dy_top = player_rect.bottom - block_rect.top
            # Find the smallest overlap
            min_overlap = min(dx_right, dx_left, dy_bottom, dy_top)
            if min_overlap == dx_right:
                self.player_x = block_rect.right
                # Place fox on the floor after side collision
                self.player_y = floor_y_at_x - self.frame_height
                self.velocity_y = 0
                self.is_jumping = False
            elif min_overlap == dx_left:
                self.player_x = block_rect.left - self.frame_width
                self.player_y = floor_y_at_x - self.frame_height
                self.velocity_y = 0
                self.is_jumping = False
            elif min_overlap == dy_bottom:
                self.player_y = block_rect.bottom
                # Do NOT change velocity_y here (side collision)
            elif min_overlap == dy_top:
                self.player_y = block_rect.top - self.frame_height
                self.velocity_y = 0
                self.is_jumping = False
        elif self.player_y + self.frame_height >= floor_y_at_x:
            self.player_y = floor_y_at_x - self.frame_height
            self.velocity_y = 0
            self.is_jumping = False

    def draw(self, screen, dt):
        screen.blit(self.background, (0, 0))
        segis_value = segis.get()
        from core.segis import get_rainbow_color

        color = get_rainbow_color(self.segis_color_phase)
        segis_text = self.font.render(f"Segis: {segis_value}", True, color)
        screen.blit(segis_text, (15, 15))
        if self.did_drink:
            player_image = self.fox_did_drink
            self.player_speed = 3
        else:
            if not self.facing_right:
                player_image = pygame.transform.flip(self.player_image, True, False)
                if self.is_jumping:
                    reversed_jump = pygame.transform.flip(self.jump_image, True, False)
                    player_image = reversed_jump
            elif self.is_jumping:
                player_image = self.jump_image
            else:
                player_image = self.player_image
        # Draw drink prompt rectangle if needed
        if self.show_drink_prompt:
            prompt_rect = pygame.Rect(350, 150, 350, 60)
            pygame.draw.rect(screen, (230, 230, 230), prompt_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), prompt_rect, 2, border_radius=10)
            # Update prompt text based on wins
            if self.wins < 3:
                prompt_text = self.font.render(" Juo bisse. Paina G", True, (0, 0, 0))
            else:
                prompt_text = self.font.render(
                    "Pitää hakee lisää bissee", True, (0, 0, 0)
                )
                self.show_drink_prompt = False
            screen.blit(prompt_text, (prompt_rect.x + 20, prompt_rect.y + 20))
        min_scale = 0.6
        max_scale = 1.6
        screen_width = screen.get_width()
        scale_factor = min_scale + (max_scale - min_scale) * (
            self.player_x / max(screen_width, 1)
        )
        new_size = (
            int(self.frame_width * scale_factor),
            int(self.frame_height * scale_factor),
        )
        scaled_image = pygame.transform.scale(player_image, new_size)
        screen.blit(scaled_image, (self.player_x, self.player_y))
