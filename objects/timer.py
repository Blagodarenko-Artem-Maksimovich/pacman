import pygame

from objects.text import TextObject


class Timer(TextObject):
    def __init__(self, game, x=308, y=15, color=(255, 255, 255)):
        self.time = pygame.time.get_ticks()
        self.time_m = int(pygame.time.get_ticks() / 60000)
        self.time_s = int(pygame.time.get_ticks() / 1000)
        super().__init__(game, x, y, f'Time: {self.time_m} min  {self.time_s}sec', color)
        self.draw()

    def draw(self):
        self.time_m = int(pygame.time.get_ticks() / 60000)
        self.time_s = int(pygame.time.get_ticks() / 1000 % 60)
        TextObject.update_text(self, f'Time: {self.time_m} min  {self.time_s} sec')
        TextObject.process_draw(self)
