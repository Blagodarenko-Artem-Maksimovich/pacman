import pygame
from objects.image import ImageObject


class Lives(ImageObject):
    filename = 'images/health_point.png'

    def __init__(self, game, lives=3):
        super().__init__(game, self.filename, 0, 800)
        self.lives_count = lives

    def reset(self):
        self.__init__(self.game, 3)

    def damage(self):
        self.lives_count -= 1

    def process_draw(self):
        mini_image = pygame.transform.scale(self.image, (30, 30))
        for i in range(self.lives_count):
            self.rect.x = 30 + 35 * i
            self.game.screen.blit(mini_image, self.rect)
