import pygame

from objects.text import TextObject


class Score(TextObject):
    score = 0

    def reset(self):
        self.score = 0
        text = "Score: " + str(self.score)
        self.update_text(text)
        Score.score = 0

    def collect(self, score):
        self.game.scenes[1].pacman.eaten_grains += 1
        Score.score += int(score)
        text = "Score: " + str(Score.score)
        self.update_text(text)
