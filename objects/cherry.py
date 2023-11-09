import pygame
from random import randint

from objects.image import ImageObject


class Cherry(ImageObject):
    sr = 4
    score = 100
    radius = 10
    display_seconds = 9
    filename = 'images/cherry.png'

    def __init__(self, game, filename=None, x=80, y=80):
        super().__init__(game, filename, x, y)
        self.image = pygame.transform.scale(self.image, [22, 22])
        self.is_collected = False
        self.time_start_display = None
        self.is_visible = False

    def reset(self, x, y):
        self.__init__(self.game, None, x, y)

    def show(self):
        self.is_visible = True
        self.time_start_display = pygame.time.get_ticks()

    def hide(self):
        self.is_visible = False

    def process_logic(self):
        if not self.is_visible:
            return
        delta = pygame.time.get_ticks() - self.time_start_display
        if delta >= self.display_seconds * 1000:
            self.hide()

    def collect(self, player):
        self.is_collected = True
