import pygame
from objects.image import ImageObject
from objects.field import Field
from random import randint
from objects.grains import WallCell


class Ghost(ImageObject):
    invincibility = False  # Уязвимость призрака к съеданию пакманом
    d = [(0, -1),
         (0, 1),
         (-1, 0),
         (1, 0)]
    direction = 0, 1
    nearly_cells = []

    FIELD_WIDTH = 616
    FIELD_HEIGHT = 864

    def reset(self, x, y):
        self.invincibility = False
        self.d = [(0, -1),
             (0, 1),
             (-1, 0),
             (1, 0)]
        self.direction = 0, 1
        self.nearly_cells = []
        self.rect.x = x
        self.rect.y = y

    def is_invincible(self):
        return self.invincibility

    def change_invincibility(self):
        if self.invincibility:
            self.invincibility = False
        else:
            self.invincibility = True

    def dir(self):
        return self.direction

    def change_direction(self):
        a = randint(0, 3)
        while type(self.nearly_cells[a]) == WallCell:
            a = randint(0, 3)
        self.direction = self.d[a]

    def process_logic(self):
        self.move(
            self.rect.x + self.direction[0],
            self.rect.y + self.direction[1]
        )
