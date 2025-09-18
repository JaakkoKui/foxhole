# scenes/level1.py
import pygame


class Level1:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont(None, 40)

        # Player setup
        self.frame_width, self.frame_height = 200, 140
        self.player_image = pygame.image.load(
            "pictures/fromSide/frownFox.png"
        ).convert_alpha()
        self.background = pygame.image.load("pictures/backgrounds/kitchen.png")
        self.background = pygame.transform.scale(
            self.background, pygame.display.get_surface().get_size()
        )
        self.player_x, self.player_y = 50, 500
        self.player_speed = 5
        self.floor_start = (0, 680)  # Start of slanted floor (up left)
        self.floor_end = (1000, 770)  # End of slanted floor (down right)

        # Gravity setup
        self.gravity = 0.5  # Acceleration due to gravity
        self.velocity_y = 0  # Player's vertical velocity
        self.jump_strength = -10  # Initial velocity when jumping
        self.is_jumping = False

        self.clock = pygame.time.Clock()
        self.facing_right = True  # Track the direction the player is facing

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    # Switch to next scene
                    from scenes.intro import CutsceneIntro

                    self.manager.set_scene(CutsceneIntro(self.manager))
                elif e.key == pygame.K_UP and not self.is_jumping:
                    # Jump if not already in the air
                    self.velocity_y = self.jump_strength
                    self.is_jumping = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_x -= self.player_speed
            self.facing_right = False  # Update direction
        if keys[pygame.K_RIGHT]:
            self.player_x += self.player_speed
            self.facing_right = True  # Update direction

        # Apply gravity
        self.velocity_y += self.gravity
        self.player_y += self.velocity_y

        # Calculate y position of the slanted floor at player's x
        x0, y0 = self.floor_start
        x1, y1 = self.floor_end
        # Linear interpolation for floor y at player_x
        floor_y_at_x = y0 + (y1 - y0) * ((self.player_x - x0) / (x1 - x0))
        if self.player_y + self.frame_height >= floor_y_at_x:
            self.player_y = floor_y_at_x - self.frame_height
            self.velocity_y = 0
            self.is_jumping = False

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        if not self.facing_right:
            player_image = pygame.transform.flip(self.player_image, True, False)
        else:
            player_image = self.player_image
        # Calculate scale factor: starts at 1.0, increases to 2.0 at far right
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
