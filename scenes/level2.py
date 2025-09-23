import pygame

from core.segis import segis


class Level2:
    """
    Level2 scene with a zoomed-in yard background, mask for walkable areas,
    and a movable fox player sprite.
    """

    def __init__(self, manager):
        """
        Initialize Level2 with zoomed background, mask, and player sprite.
        """
        self.manager = manager
        self.font = pygame.font.SysFont(None, 40)
        self.zoom = 2.1  # Zoom factor for background

        # Load and zoom background image
        original_bg = pygame.image.load("pictures/backgrounds/yard2.png")
        screen_size = pygame.display.get_surface().get_size()
        zoomed_size = (int(screen_size[0] * self.zoom), int(screen_size[1] * self.zoom))
        self.background = pygame.transform.scale(original_bg, zoomed_size)

        # Load and zoom mask image (white = walkable, black = blocked)
        original_bg_mask = pygame.image.load("pictures/backgrounds/yard2_mask.png")
        self.mask_image = pygame.transform.scale(original_bg_mask, zoomed_size)

        # Load player images
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
        self.player_x, self.player_y = 250, 500  # or another value you know is walkable
        self.player_speed = 1.8
        self.frame_width, self.frame_height = 30, 50
        print("Mask at start:", self.is_walkable(self.player_x, self.player_y))

    def is_walkable(self, x, y):
        """
        Check if the given (x, y) position is walkable using the mask image.
        White pixels are walkable, black are blocked.
        Scales coordinates by zoom factor.
        """
        mask_x = int(x * self.zoom)
        mask_y = int(y * self.zoom)
        mask_x = max(0, min(mask_x, self.mask_image.get_width() - 1))
        mask_y = max(0, min(mask_y, self.mask_image.get_height() - 1))
        color = self.mask_image.get_at((mask_x, mask_y))
        return color.r > 200 and color.g > 200 and color.b > 200  # white pixel

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                from scenes.level1 import Level1

                self.manager.set_scene(Level1(self.manager))

    def update(self, dt):
<<<<<<< HEAD
        segis.update(dt)  # Decay segis over time
=======
        """
        Update fox position based on keyboard input and mask.
        """
>>>>>>> d9e1a3257a13eebc564acd1a9755e2eb9d06223e
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx -= self.player_speed
        if keys[pygame.K_RIGHT]:
            dx += self.player_speed
        if keys[pygame.K_UP]:
            dy -= self.player_speed
        if keys[pygame.K_DOWN]:
            dy += self.player_speed

        # Calculate intended new position in background coordinates
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        # Only move if mask allows (use zoomed coordinates for mask)
        if self.is_walkable(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y
        print("Mask at new position:", self.is_walkable(new_x, new_y))

        # Clamp player position to background bounds (not screen bounds)
        bg_width = self.background.get_width() / self.zoom
        bg_height = self.background.get_height() / self.zoom
        self.player_x = max(0, min(self.player_x, bg_width - self.frame_width))
        self.player_y = max(0, min(self.player_y, bg_height - self.frame_height))

        # Direction logic
        if keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.player_image = self.up_image
        elif (
            keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]
        ):
            self.player_image = self.down_image
        elif keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.player_image = self.left_image
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.player_image = self.right_image
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.player_image = pygame.transform.rotate(self.up_image, 45)
        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.player_image = pygame.transform.rotate(self.up_image, -45)
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.player_image = pygame.transform.rotate(self.down_image, -45)
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.player_image = pygame.transform.rotate(self.down_image, 45)

    def draw(self, screen, dt):
        """
        Draw the zoomed background and fox sprite centered on the screen.
        """
        screen_width, screen_height = pygame.display.get_surface().get_size()
        # Camera offset for zoom
        camera_x = int(self.player_x * self.zoom - screen_width // 2)
        camera_y = int(self.player_y * self.zoom - screen_height // 2)

        # Draw zoomed background offset by camera
        screen.blit(self.background, (-camera_x, -camera_y))

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
<<<<<<< HEAD

=======
        # Make image 1.4x larger if player_image is angled (rotated)
>>>>>>> d9e1a3257a13eebc564acd1a9755e2eb9d06223e
        base_images = [
            self.up_image,
            self.down_image,
            self.left_image,
            self.right_image,
        ]
        if self.player_image not in base_images:
            draw_width = int(draw_width * 1.4)
            draw_height = int(draw_height * 1.4)
        scaled_image = pygame.transform.scale(
            self.player_image, (int(draw_width), int(draw_height))
        )
        # Draw fox at center of screen
        fox_draw_x = screen_width // 2
        fox_draw_y = screen_height // 2
        screen.blit(scaled_image, (fox_draw_x, fox_draw_y))
