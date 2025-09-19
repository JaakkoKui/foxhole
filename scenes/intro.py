# Remove the duplicate rendering of the lower line in the talk bubble

import pygame


class CutsceneIntro:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont(None, 40)
        self.timer = 0
        self.text_alpha = 255
        self.text_fade_duration = 1000
        self.text_surface = self.font.render(
            "Perustuu tositapahtumiin...", True, (255, 255, 255)
        )
        self.fox_pos = [360, 580]
        self.fox_direction = 1
        self.fox_talk_timer = 0
        self.fox_state = "silent"  # silent, talking, flipping, walking

    def handle_events(self, events):
        self.fox = pygame.image.load("pictures/fromSide/foxStanding.png")
        width, height = self.fox.get_size()
        scale_factor = 1.7
        new_size = (int(width * scale_factor), int(height * scale_factor))
        self.l_fox = pygame.transform.scale(self.fox, new_size)
        self.tiredFox = pygame.image.load("pictures/fromSide/tiredFox.png")
        self.l_tiredFox = pygame.transform.scale(self.tiredFox, new_size)
        self.frownFox = pygame.image.load("pictures/fromSide/frownFox.png")
        self.l_frownFox = pygame.transform.scale(self.frownFox, new_size)
        self.background = pygame.image.load("pictures/backgrounds/sofa.png")
        self.background = pygame.transform.scale(
            self.background, pygame.display.get_surface().get_size()
        )

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

        if self.timer > 1000:
            self.text_alpha -= (255 / self.text_fade_duration) * dt
            if self.text_alpha < 0:
                self.text_alpha = 0
            self.text_surface.set_alpha(self.text_alpha)

        # Fox state transitions
        if self.timer < 5000:
            self.fox_state = "silent"
        elif self.timer < 8000:
            self.fox_state = "talking"
        elif self.timer < 10000:
            self.fox_state = "flipping"
        else:
            self.fox_state = "walking"

        # Fox walks forward after flipping
        if self.fox_state == "walking":
            self.fox_pos[0] += 5  # Move fox to the right

    def draw(self, screen):
        screen.fill((30, 30, 30))
        if self.text_alpha > 0:
            text_surface = self.text_surface.copy()
            text_surface.set_alpha(self.text_alpha)
            screen.blit(text_surface, (100, 250))
        else:
            # Display sofa.png as background after text has faded
            screen.blit(self.background, (0, 0))

            # Fox animation states
            if self.fox_state == "silent":
                # Fox is silent, just show the flipped fox
                flipped_fox = pygame.transform.flip(self.l_tiredFox, False, True)
                screen.blit(flipped_fox, self.fox_pos)
            elif self.fox_state == "talking":
                # Fox is flipped and talking
                flipped_fox = pygame.transform.flip(self.l_tiredFox, False, True)
                screen.blit(flipped_fox, self.fox_pos)

                # Draw talk bubble
                bubble_width = 650
                bubble_height = 80
                bubble_x = 150
                bubble_y = 150
                pygame.draw.rect(
                    screen,
                    (230, 230, 230),
                    (bubble_x, bubble_y, bubble_width, bubble_height),
                    border_radius=5,
                )
                pygame.draw.rect(
                    screen,
                    (20, 20, 20),
                    (bubble_x, bubble_y, bubble_width, bubble_height),
                    2,
                    border_radius=10,
                )
                # Render multiline text
                lines = [
                    "Kettu heräilee uuteen päivään ohimolla",
                    "vihlovaan hedariin ja lähtee etsimään kaljaa.",
                ]
                talk_surfaces = [
                    self.font.render(line, True, (0, 0, 0)) for line in lines
                ]
                for i, talk_surface in enumerate(talk_surfaces):
                    screen.blit(
                        talk_surface,
                        (
                            bubble_x + 10,
                            bubble_y + 10 + i * (talk_surface.get_height() + 5),
                        ),
                    )
                # Removed duplicate rendering of the lower line
            elif self.fox_state == "flipping":
                # Fox flips around (show normal image)
                screen.blit(self.l_tiredFox, self.fox_pos)
            elif self.fox_state == "walking":
                # Fox walks forward
                screen.blit(self.l_frownFox, self.fox_pos)

                # Draw moving talk bubble
                bubble_width = 200
                bubble_height = 40
                bubble_x = self.fox_pos[0] + 90
                bubble_y = self.fox_pos[1] - 70
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (bubble_x, bubble_y, bubble_width, bubble_height),
                    border_radius=10,
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (bubble_x, bubble_y, bubble_width, bubble_height),
                    2,
                    border_radius=10,
                )
                talk_surface = self.font.render("Bissee...", True, (20, 20, 20))
                screen.blit(
                    talk_surface,
                    (
                        bubble_x + 10,
                        bubble_y + (bubble_height - talk_surface.get_height()) // 2,
                    ),
                )
