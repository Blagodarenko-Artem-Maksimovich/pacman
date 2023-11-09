'''
0 - пустое поле
1 - стена
2 - зерно
3 - большое зерно
'''

import pygame

from constants import BLACK, BLUE, YELLOW, ORANGE
from objects.grains import Grain, BigGrain, EmptyCell, WallCell
from objects.base import DrawableObject


class Field(DrawableObject):
    CELL_SIZE = 22
    CELL_TYPES = [
        EmptyCell,
        WallCell,
        Grain,
        BigGrain
    ]

    def __init__(self, game, x=10, y=10, field_filename='maps/map.txt'):
        super().__init__(game)
        self.rect.x = x
        self.rect.y = y
        self.field_filename = field_filename
        self.field = self.get_field()
        self.rect.w = len(self.field[0]) * self.CELL_SIZE
        self.rect.h = len(self.field) * self.CELL_SIZE

    def reset(self):
        self.__init__(self.game, x=0, y=91)

    def get_field(self):
        field = []
        with open(self.field_filename, 'r') as f:
            data = f.readlines()
            for row_index in range(len(data)):
                row = []
                data[row_index] = data[row_index].split()
                for col_index in range(len(data[row_index])):
                    try:
                        cell_value = int(data[row_index][col_index])
                    except ValueError:
                        cell_value = 0
                    if 0 <= cell_value <= 3:
                        cell = self.CELL_TYPES[cell_value](
                            game=self.game,
                            x=self.rect.x + col_index * self.CELL_SIZE,
                            y=self.rect.y + row_index * self.CELL_SIZE,
                            cell_width=self.CELL_SIZE
                        )
                        row.append(cell)
                field.append(row)
        return field

    def get(self, x, y):
        return self.field[x][y]

    def set(self, x, y, value):
        self.field[x][y] = int(value)

    def process_draw(self):  # sc это pg.display.set_mode
        cell_colors = [
            BLACK,
            BLUE,
            YELLOW,
            ORANGE
        ]
        for row_index in range(len(self.field)):
            for col_index in range(len(self.field[0])):
                cell_value = self.field[row_index][col_index]
                if cell_value in [0, 1, 2, 3]:
                    pygame.draw.rect(
                        self.game.screen,
                        cell_colors[cell_value],
                        (
                            self.rect.x + col_index * self.CELL_SIZE,
                            self.rect.y + row_index * self.CELL_SIZE,
                            self.CELL_SIZE,
                            self.CELL_SIZE
                        )
                    )
                else:
                    self.field[row_index][col_index].process_draw()
