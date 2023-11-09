import pygame

from constants import BLACK, YELLOW, BLUE
from objects.base import DrawableObject


class BaseCell(DrawableObject):
    color = BLACK

    def __init__(self, game, x=30, y=30, cell_width=10):
        super().__init__(game)
        self.cell_width = cell_width
        self.rect.x = x
        self.rect.y = y
        self.rect.width = cell_width
        self.rect.height = cell_width

    def process_draw(self):
        pygame.draw.rect(self.game.screen, self.color, self.rect, 0)


class EmptyCell(BaseCell):
    pass


class WallCell(BaseCell):
    color = BLUE

    def process_draw(self):
        super(WallCell, self).process_draw()
        pygame.draw.rect(self.game.screen, BLACK, self.rect, 1)   # отрисовка границы


class Grain(BaseCell):
    score = 10
    radius = 3
    color = YELLOW

    def __init__(self, game, x=30, y=30, cell_width=10):
        super().__init__(game, x, y, cell_width)
        self.is_collected = False
        self.real_grain_rect = pygame.Rect(
            self.rect.centerx - self.radius,
            self.rect.centery - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def process_draw(self):
        if self.is_collected:
            return
        pygame.draw.rect(self.game.screen, self.color, self.real_grain_rect, 0)

    def collect(self):
        # здесь делаем присвоение игроку очков за зерно
        self.is_collected = True


class BigGrain(Grain):
    score = 50
    radius = 6

    def process_draw(self):
        if self.is_collected:
            return
        super(BigGrain, self).process_draw()
        pygame.draw.circle(self.game.screen, self.color, self.rect.center, self.radius)
