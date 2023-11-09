import pygame

from objects.score import Score
from objects.image import ImageObject
from objects.grains import Grain, WallCell
from objects.text import TextObject
from objects.field import Field


class Pacman(ImageObject):
    eaten_grains = 0
    animCount = 0
    shift_x = 0
    shift_y = 0
    images = [pygame.image.load('images/pacman_close.png'), pygame.image.load('images/pacman.png')]
    filename = 'images/pacman.png'
    alpha = 0
    directions = {
        pygame.K_w: (0, -1, 270),
        pygame.K_s: (0, 1, 90),
        pygame.K_a: (-1, 0, 0),
        pygame.K_d: (1, 0, 180),
    }
    nearly_cells = []
    forbid_directions = [119, 115]
    next_turn = [-100000, (100000, 100000, 100000)]

    def reset(self):
        self.eaten_grains = 0
        self.animCount = 0
        self.shift_x = 0
        self.shift_y = 0
        self.images = [pygame.image.load('images/pacman_close.png'), pygame.image.load('images/pacman.png')]
        self.filename = 'images/pacman.png'
        self.alpha = 0
        self.directions = {
            pygame.K_w: (0, -1, 270),
            pygame.K_s: (0, 1, 90),
            pygame.K_a: (-1, 0, 0),
            pygame.K_d: (1, 0, 180),
        }
        self.nearly_cells = []
        self.forbid_directions = [119, 115]
        self.next_turn = [-100000, (100000, 100000, 100000)]
        self.rect.x = 301
        self.rect.y = 465

    def process_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key not in Pacman.directions.keys():
            return
        if self.is_exact_position() and event.key not in self.forbid_directions \
                or (
                self.shift_x == -Pacman.directions[event.key][0] and self.shift_y == -Pacman.directions[event.key][1]) \
                or (self.shift_x == 0 and self.shift_y == 0 and event.key not in self.forbid_directions):
            self.shift_x, self.shift_y, Pacman.alpha = Pacman.directions[event.key]
            self.next_turn = Pacman.next_turn
        else:
            self.next_turn = (pygame.time.get_ticks(), Pacman.directions[event.key])

    def process_logic(self):
        d = {(0, 0): 0,
             (0, -1): 119,  # w
             (0, 1): 115,  # s
             (-1, 0): 97,  # a
             (1, 0): 100}  # d

        delta = pygame.time.get_ticks() - self.next_turn[0]
        if (self.next_turn[1][0:2]) in d.keys():
            if delta < 1000 and d[self.next_turn[1][0:2]] not in self.forbid_directions \
                    and (self.rect.x - self.game.scenes[1].field.rect.x) % Field.CELL_SIZE == 0 and (
                    self.rect.y - self.game.scenes[1].field.rect.y) % Field.CELL_SIZE == 0:
                self.shift_x, self.shift_y, Pacman.alpha = self.next_turn[1]
                self.next_turn = Pacman.next_turn

        if self.rect.x <= -Field.CELL_SIZE + 2:
            self.rect.x = self.game.width - 2
        if self.rect.x > self.game.width - 2:
            self.rect.x = -Field.CELL_SIZE + 2

        if d[self.shift_x, self.shift_y] not in self.forbid_directions:
            self.move(
                x=self.rect.x + self.shift_x,
                y=self.rect.y + self.shift_y
            )
        else:
            self.shift_x, self.shift_y = 0, 0

    def collision(self, other):
        if hasattr(other, 'is_collected') and other.is_collected:
            return False
        return self.rect.colliderect(other.rect)

    def process_draw(self):
        if Pacman.animCount + 1 >= 30:
            Pacman.animCount = 0
        if self.shift_x == 0 and self.shift_y == 0:
            self.image = pygame.transform.rotate(Pacman.images[1], Pacman.alpha)
        else:
            self.image = pygame.transform.rotate(Pacman.images[Pacman.animCount // 15], Pacman.alpha)
            Pacman.animCount += 1
        self.game.screen.blit(self.image, self.rect)

    # print(Pacman.animCount)

    def is_exact_position(self):
        return (self.rect.x - self.game.scenes[1].field.rect.x) % Field.CELL_SIZE == 0 and \
               (self.rect.y - self.game.scenes[1].field.rect.y) % Field.CELL_SIZE == 0

    def teleport(self):
        self.rect.x = 672 / 2
        self.rect.y = 864 / 2
