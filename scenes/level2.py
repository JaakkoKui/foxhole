import pygame

from core.segis import segis
from scenes.intro import CutsceneIntro


class Level2:
    """
    Level2 scene where the player is pictured from above and can move in all directions.
    """

    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont(None, 40)
        self.frame_width, self.frame_height = 100, 60
        self.player_image = pygame.image.load(
            "pictures/fromAbove/foxStraight.png"
        ).convert_alpha()
        self.background = pygame.image.load("pictures/backgrounds/yard.png")
        self.player_pos = pygame.Vector2(400, 300)
        self.player_speed = 5

    def handle_events(self, events):
        """
        Handle input events for the scene.
        """
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.manager.set_scene(CutsceneIntro(self.manager))

    def update(self):
        """
        Update the player position based on keyboard input.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_pos.x -= self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_pos.x += self.player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_pos.y -= self.player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_pos.y += self.player_speed

        # Clamp player position to screen bounds
        self.player_pos.x = max(
            0, min(self.player_pos.x, self.background.get_width() - self.frame_width)
        )
        self.player_pos.y = max(
            0, min(self.player_pos.y, self.background.get_height() - self.frame_height)
        )

    def draw(self, screen):
        """
        Draw the background, segis at the left corner, and player on the screen.
        """
        screen.blit(self.background, (0, 0))
        # Draw segis at the top-left corner (0, 0)
        segis_image = segis.get_image()  # Assuming segis has a get_image() method
        screen.blit(segis_image, (0, 0))
        screen.blit(self.player_image, (self.player_pos.x, self.player_pos.y))
        # Optionally draw some info text
        info_text = self.font.render(
            "Level 2: Move with arrow keys or WASD", True, (255, 255, 255)
        )
        screen.blit(info_text, (20, 20))
