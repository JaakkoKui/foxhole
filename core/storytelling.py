import pygame


class StoryTeller:
    def __init__(
        self,
        text,
        font_size=36,
        letter_delay=30,
        pause_delay=30,
        fade_delay=1000,
        fade_duration=1000,
    ):
        self.story_text = text
        self.story_words = self.story_text.split()
        self.story_displayed = ""
        self.story_word_index = 0
        self.story_letter_index = 0
        self.story_timer = 0
        self.state = "letter"  # 'letter', 'pause', 'fade'
        self.letter_delay = letter_delay  # ms between letters
        self.pause_delay = pause_delay  # ms pause after word
        self.font = pygame.font.SysFont(None, font_size)
        self.fade_delay = fade_delay  # ms to wait before fading
        self.fade_duration = fade_duration  # ms fade duration
        self.fade_timer = 0
        self.alpha = 255

    def update(self, dt):
        self.story_timer += dt
        if self.state in ("letter", "pause"):
            if self.story_word_index < len(self.story_words):
                word = self.story_words[self.story_word_index]
                if self.state == "letter":
                    if self.story_letter_index < len(word):
                        if self.story_timer > self.letter_delay:
                            self.story_displayed += word[self.story_letter_index]
                            self.story_letter_index += 1
                            self.story_timer = 0
                    else:
                        self.state = "pause"
                        self.story_timer = 0
                elif self.state == "pause":
                    if self.story_timer > self.pause_delay:
                        self.story_word_index += 1
                        self.story_letter_index = 0
                        if self.story_word_index < len(self.story_words):
                            self.story_displayed += " "
                        self.state = "letter"
                        self.story_timer = 0
            else:
                # All text displayed, start fade timer
                self.state = "fade"
                self.fade_timer = 0
                self.alpha = 255
        elif self.state == "fade":
            self.fade_timer += dt
            if self.fade_timer > self.fade_delay:
                fade_progress = min(
                    1.0, (self.fade_timer - self.fade_delay) / self.fade_duration
                )
                self.alpha = int(255 * (1.0 - fade_progress))
                if self.alpha <= 0:
                    self.alpha = 0
                    self.story_displayed = ""

    def draw(self, screen):
        # Measure text size
        text = self.story_displayed if self.story_displayed else " "
        text_width, text_height = self.font.size(text)
        padding_x, padding_y = 40, 28
        box_width = text_width + padding_x
        box_height = text_height + padding_y
        screen_width, screen_height = screen.get_size()
        box_x = (screen_width - box_width) // 2
        box_y = (screen_height - box_height) // 8
        # Create surfaces for fade effect
        box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        shadow_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        # Draw drop shadow
        shadow_color = (80, 80, 80, int(self.alpha * 0.5))
        pygame.draw.rect(
            shadow_surf, shadow_color, (0, 0, box_width, box_height), border_radius=18
        )
        screen.blit(shadow_surf, (box_x + 6, box_y + 6))
        # Draw main box
        box_color = (255, 255, 245, self.alpha)
        pygame.draw.rect(
            box_surf, box_color, (0, 0, box_width, box_height), border_radius=18
        )
        # Draw border
        border_color = (40, 40, 40, self.alpha)
        pygame.draw.rect(
            box_surf, border_color, (0, 0, box_width, box_height), 3, border_radius=18
        )
        # Draw text centered in box
        text_color = (30, 30, 30, self.alpha)
        story_render = self.font.render(text, True, text_color)
        text_x = (box_width - text_width) // 2
        text_y = (box_height - text_height) // 2
        box_surf.blit(story_render, (text_x, text_y))
        screen.blit(box_surf, (box_x, box_y))
