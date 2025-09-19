import pygame

import core.combat


class Level1:
    def __init__(self, manager):
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
        self.player_x, self.player_y = 150, 700
        self.player_speed = 5
        self.floor_start = (0, 710)
        self.floor_end = (1000, 780)
        self.block_x, self.block_y = 120, 0
        self.block_width, self.block_height = 5, 800
        self.gravity = 0.5
        self.velocity_y = 0
        self.jump_strength = -10
        self.is_jumping = False
        self.clock = pygame.time.Clock()
        self.facing_right = True
        self.show_drink_prompt = False  # Only show when at fridge
        self.did_drink = False
        self.fox_did_drink = pygame.image.load(
            "pictures/fromSide/foxDidDrink.png"
        ).convert_alpha()

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    from scenes.intro import CutsceneIntro

                    self.manager.set_scene(CutsceneIntro(self.manager))
                elif e.key == pygame.K_UP and not self.is_jumping:
                    self.velocity_y = self.jump_strength
                    self.is_jumping = True
                elif e.key == pygame.K_g and self.show_drink_prompt:

                    def combat_callback(result):
                        if result == "win":
                            self.did_drink = False
                            self.player_image = self.fox_standing
                        else:
                            self.did_drink = True
                            self.player_image = self.fox_did_drink

                    combat_scene = core.combat.Combat(
                        self.font,
                        prompt_time=2000,
                        rounds=4,
                        on_end=combat_callback,
                        return_scene=self,
                    )
                    combat_scene.start()
                    combat_scene.manager = self.manager
                    self.manager.set_scene(combat_scene)
                    self.show_drink_prompt = False

    def update(self, dt):
        # Reset drink state if moving after drinking
        if self.did_drink and (
            pygame.key.get_pressed()[pygame.K_LEFT]
            or pygame.key.get_pressed()[pygame.K_RIGHT]
        ):
            self.did_drink = False
        fridge_x_min = 450
        fridge_x_max = 550
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
        if player_rect.colliderect(block_rect):
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

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
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
            prompt_rect = pygame.Rect(350, 100, 300, 60)
            pygame.draw.rect(screen, (230, 230, 230), prompt_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), prompt_rect, 2, border_radius=10)
            prompt_text = self.font.render("Juo bisse, paina G", True, (0, 0, 0))
            screen.blit(prompt_text, (prompt_rect.x + 20, prompt_rect.y + 20))
        min_scale = 0.7
        max_scale = 2.0
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
