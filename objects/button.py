import pygame

from third_party.button import Button
from constants import BLUE, GREEN, BLACK, ORANGE
from objects.base import DrawableObject


class ButtonObject(DrawableObject):
    BUTTON_STYLE = {
        "hover_color": BLUE,
        "clicked_color": GREEN,
        "clicked_font_color": BLACK,
        "hover_font_color": ORANGE,
    }

    def __init__(self, game, x, y, width, height, color, function, text, enable_sound=True):
        super().__init__(game)
        if enable_sound:
            self.BUTTON_STYLE['click_sound'] = pygame.mixer.Sound('sounds/click.wav')
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.button = Button((x, y, width, height), color, function, text=text, **self.BUTTON_STYLE)

    def process_event(self, event):
        self.button.check_event(event)

    def process_draw(self):
        self.button.update(self.game.screen)