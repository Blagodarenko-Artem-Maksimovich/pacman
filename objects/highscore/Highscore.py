import pygame
import os

from objects.text import TextObject


class HighScore(TextObject):

    def __init__(self, game, x=300, y=30, color=(255, 0, 0)):
        hs = open("objects/highscore/high.txt", "r")
        self.high = int(hs.read())
        hs.close()

        super().__init__(game, x, y, f'Hi-Score: {self.high}', color)
        self.draw()

    def draw(self):
        TextObject.update_text(self, f'Hi-Score: {self.high}')
        TextObject.process_draw(self)

    # если highscore меньше чем скор, то вызвать эту функцию, как аргемент передать score
    def new_high(self, score_class):
        if score_class.score > self.high:
            self.high = score_class.score
            self.draw()
            f = open('objects/highscore/high.txt', 'w')
            f.write(str(self.high))
            f.close()
