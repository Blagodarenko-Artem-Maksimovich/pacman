import pygame

from objects.field import Field
from objects.lifes import Lives
from objects.pacman import Pacman
from constants import RED
from objects.button import ButtonObject
from objects.cherry import Cherry
from objects.grains import Grain, BigGrain, WallCell, EmptyCell
from scenes.base import BaseScene
from objects.score import Score
from objects.ghost import Ghost
from objects.highscore.Highscore import HighScore
from objects.timer import Timer


class GameScene(BaseScene):

    def __init__(self, game):
        super().__init__(game)
        self.field = Field(game, x=0, y=91)
        self.objects.append(self.field)

        self.pacman = Pacman(self.game, x=301, y=465)
        self.objects.append(self.pacman)

        self.blinky = Ghost(self.game, 'images/GhostRed.png', x=44, y=113)
        self.pinky = Ghost(self.game, 'images/GhostGreen.png', x=572, y=113)
        self.inky = Ghost(self.game, 'images/GhostBlue.png', x=44, y=720)
        self.klyde = Ghost(self.game, 'images/GhostOrange.png', x=572, y=720)
        self.ghosts = [
            self.blinky,
            self.pinky,
            self.inky,
            self.klyde
        ]
        self.objects += self.ghosts

        self.lives = Lives(self.game)
        self.objects.append(self.lives)

        self.cherry = Cherry(self.game, x=301, y=465)
        self.objects.append(self.cherry)

        self.time = Timer(self.game, x=290, y=22, color=RED)
        self.objects.append(self.time)

        self.text = 'Score: 0 '
        self.score = Score(self.game, x=136, y=50, text=self.text, color=RED)
        self.objects.append(self.score)

        self.highscore = HighScore(self.game, x=466, y=50, color=RED)
        self.objects.append(self.highscore)

    def spawn_cherry(self):
        self.cherry.show()
        self.cherry.sr = 170

    def process_event(self, event):
        super(GameScene, self).process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_scene(self.game.SCENE_MENU)
            if event.key == pygame.K_p:
                self.game.set_scene(self.game.SCENE_PAUSE)

    def timer(self):
        self.time.draw()

    def process_pacman_collisions(self):
        if (self.pacman.rect.x - self.field.rect.x) % self.field.CELL_SIZE == 0 and (
                self.pacman.rect.y - self.field.rect.y) % self.field.CELL_SIZE == 0:
            i, j = (self.pacman.rect.x - self.field.rect.x) // self.field.CELL_SIZE, (
                    self.pacman.rect.y - self.field.rect.y) // self.field.CELL_SIZE

            self.pacman.nearly_cells = [
                self.field.get(j - 1, i),
                self.field.get(j + 1, i),
                self.field.get(j, i - 1),
                self.field.get(j, (i + 1) % len(self.field.field[0]))
            ]
            self.pacman.forbid_directions = [list(self.pacman.directions.keys())[i]
                                             for i in range(len(list(self.pacman.directions.keys())))
                                             if type(self.pacman.nearly_cells[i]) == WallCell]
        if len(self.pacman.nearly_cells) == 0:
            return

        for ind in range(len(self.pacman.nearly_cells)):
            if self.pacman.collision(self.pacman.nearly_cells[ind]):
                if type(self.pacman.nearly_cells[ind]) in [Grain, BigGrain, Cherry]:
                    self.pacman.nearly_cells[ind].collect()
                    self.score.collect(self.pacman.nearly_cells[ind].score)

    def process_ghost_collision(self, ghost):
        if (ghost.rect.x - self.field.rect.x) % self.field.CELL_SIZE == 0 and (
                ghost.rect.y - self.field.rect.y) % self.field.CELL_SIZE == 0:
            i = (ghost.rect.x - self.field.rect.x) // self.field.CELL_SIZE
            j = (ghost.rect.y - self.field.rect.y) // self.field.CELL_SIZE

            ghost.nearly_cells = [
                self.field.get(j - 1, i),  # up
                self.field.get(j + 1, i),  # down
                self.field.get(j, i - 1),  # left
                self.field.get(j, i + 1)  # right
            ]

            if ghost.dir() == ghost.d[0]:
                if type(ghost.nearly_cells[0]) == WallCell:
                    ghost.change_direction()
            elif ghost.dir() == ghost.d[1]:
                if type(ghost.nearly_cells[1]) == WallCell:
                    ghost.change_direction()
            elif ghost.dir() == ghost.d[2]:
                if type(ghost.nearly_cells[2]) == WallCell:
                    ghost.change_direction()
            elif ghost.dir() == ghost.d[3]:
                if type(ghost.nearly_cells[3]) == WallCell:
                    ghost.change_direction()

    def on_pacman_damage(self):
        self.lives.damage()
        self.pacman.reset()
        self.game.sound_manager.play_sound('Death')

    def process_ghost_pacman_eating(self, ghost):
        if ghost.rect.colliderect(self.pacman.rect):
            self.on_pacman_damage()

    def process_all_ghosts_eating_pacman(self):
        for ghost in self.ghosts:
            self.process_ghost_pacman_eating(ghost)

    def process_gameover(self):
        if self.lives.lives_count <= 0 or self.pacman.eaten_grains == 246:
            self.game.set_scene(self.game.SCENE_GAMEOVER)

    def process_logic(self):
        if self.pacman.eaten_grains == self.cherry.sr:
            self.spawn_cherry()

        self.process_pacman_collisions()
        self.cherry.process_logic()
        self.process_ghost_collision(self.blinky)
        self.process_ghost_collision(self.pinky)
        self.process_ghost_collision(self.inky)
        self.process_ghost_collision(self.klyde)

        super(GameScene, self).process_logic()

        self.process_all_ghosts_eating_pacman()

        self.timer()
        if self.highscore.high < self.score.score:
            self.highscore.new_high(self.score)
        self.process_gameover()
