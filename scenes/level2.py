import pygame

from core.segis import segis


class Level2:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont(None, 40)
        self.background = pygame.image.load("pictures/backgrounds/yard.png")
        self.background = pygame.transform.scale(
            self.background, pygame.display.get_surface().get_size()
        )
        self.base_image = pygame.image.load(
            "pictures/fromAbove/foxStraight.png"
        ).convert_alpha()
        self.player_image = pygame.transform.flip(self.base_image, False, True)
        self.left_image = pygame.transform.rotate(self.base_image, 90)
        self.right_image = pygame.transform.rotate(self.base_image, -90)
        self.up_image = self.base_image
        self.down_image = pygame.transform.flip(self.base_image, False, True)
        self.facing_down = True
        self.facing_right = True
        self.player_x, self.player_y = 400, 400
        self.player_speed = 2
        self.frame_width, self.frame_height = 20, 40

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                # Example: go back to Level1
                from scenes.level1 import Level1

                self.manager.set_scene(Level1(self.manager))

    def update(self, dt):
        keys = pygame.key.get_pressed()
        moving_left = keys[pygame.K_LEFT]
        moving_right = keys[pygame.K_RIGHT]
        moving_up = keys[pygame.K_UP]
        moving_down = keys[pygame.K_DOWN]
        # Default speed
        self.current_speed = self.player_speed
        self.diagonal = False
        # Detect diagonal movement
        if (
            (moving_up and moving_left)
            or (moving_up and moving_right)
            or (moving_down and moving_left)
            or (moving_down and moving_right)
        ):
            self.current_speed = self.player_speed * 0.7
            self.diagonal = True
        # Movement
        if moving_left:
            self.player_x -= self.current_speed
        if moving_right:
            self.player_x += self.current_speed
        if moving_up:
            self.player_y -= self.current_speed
        if moving_down:
            self.player_y += self.current_speed

        moving_left = keys[pygame.K_LEFT]
        moving_right = keys[pygame.K_RIGHT]
        moving_up = keys[pygame.K_UP]
        moving_down = keys[pygame.K_DOWN]

        if moving_left:
            self.player_x -= self.player_speed
        if moving_right:
            self.player_x += self.player_speed
        if moving_up:
            self.player_y -= self.player_speed
        if moving_down:
            self.player_y += self.player_speed

        # Direction logic
        if moving_up and not moving_left and not moving_right:
            self.player_image = self.up_image
        elif moving_down and not moving_left and not moving_right:
            self.player_image = self.down_image
        elif moving_left and not moving_up and not moving_down:
            self.player_image = self.left_image
        elif moving_right and not moving_up and not moving_down:
            self.player_image = self.right_image
        elif moving_up and moving_left:
            self.player_image = pygame.transform.rotate(self.up_image, 45)
        elif moving_up and moving_right:
            self.player_image = pygame.transform.rotate(self.up_image, -45)
        elif moving_down and moving_left:
            self.player_image = pygame.transform.rotate(self.down_image, -45)
        elif moving_down and moving_right:
            self.player_image = pygame.transform.rotate(self.down_image, 45)
        # Clamp player position to screen bounds
        self.player_x = max(
            0, min(self.player_x, self.background.get_width() - self.frame_width)
        )
        self.player_y = max(
            0, min(self.player_y, self.background.get_height() - self.frame_height)
        )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        segis_value = segis.get()
        segis_text = self.font.render(f"Segis: {segis_value}", True, (225, 225, 30))
        screen.blit(segis_text, (15, 15))
        # Swap dimensions if facing left or right
        if (
            self.player_image == self.left_image
            or self.player_image == self.right_image
        ):
            draw_width, draw_height = self.frame_height, self.frame_width
        else:
            draw_width, draw_height = self.frame_width, self.frame_height
        # Make image 1.5x larger if player_image is angled (rotated)
        # Check if player_image is a rotated surface (diagonal movement)
        # We assume diagonal images are created by pygame.transform.rotate and are not equal to up/down/left/right images
        base_images = [
            self.up_image,
            self.down_image,
            self.left_image,
            self.right_image,
        ]
        if self.player_image not in base_images:
            draw_width = int(draw_width * 1.5)
            draw_height = int(draw_height * 1.5)
        scaled_image = pygame.transform.scale(
            self.player_image, (int(draw_width), int(draw_height))
        )
        screen.blit(scaled_image, (self.player_x, self.player_y))
