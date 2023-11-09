import pygame

from constants import BLACK
from scenes.game import GameScene
from scenes.gameover import GameOverScene
from scenes.menu import MenuScene
from scenes.pause_menu import PauseMenuScene
from sounds.sound import SoundManager


class Game:
    size = width, height = 616, 864
    SCENE_MENU = 0
    SCENE_GAME = 1
    SCENE_GAMEOVER = 2
    SCENE_PAUSE = 3
    current_scene_index = SCENE_MENU

    def __init__(self):
        self.screen = pygame.display.set_mode(self.size)
        self.scenes = [
            MenuScene(self),
            GameScene(self),
            GameOverScene(self),
            PauseMenuScene(self)
        ]
        self.game_over = False

        self.sound_manager = SoundManager()

    @staticmethod
    def exit_button_pressed(event):
        return event.type == pygame.QUIT

    @staticmethod
    def exit_hotkey_pressed(event):
        return event.type == pygame.KEYDOWN and event.mod & pygame.KMOD_CTRL and event.key == pygame.K_q

    def process_exit_events(self, event):
        if Game.exit_button_pressed(event) or Game.exit_hotkey_pressed(event):
            self.exit_game()

    def process_all_events(self):
        for event in pygame.event.get():
            self.process_exit_events(event)
            self.scenes[self.current_scene_index].process_event(event)

    def process_all_logic(self):
        self.scenes[self.current_scene_index].process_logic()

    def set_scene(self, index):
        self.scenes[self.current_scene_index].on_deactivate()
        self.current_scene_index = index
        self.scenes[self.current_scene_index].on_activate()

    def process_all_draw(self):
        self.screen.fill(BLACK)
        self.scenes[self.current_scene_index].process_draw()
        pygame.display.flip()

    def main_loop(self):
        while not self.game_over:
            self.process_all_events()
            self.process_all_logic()
            self.process_all_draw()
            pygame.time.wait(10)

    def reset(self):
        self.scenes[1].pacman.reset()
        self.scenes[1].field.reset()
        self.scenes[1].blinky.reset(44, 113)
        self.scenes[1].pinky.reset(572, 113)
        self.scenes[1].inky.reset(44, 720)
        self.scenes[1].klyde.reset(572, 720)
        self.scenes[1].lives.reset()
        self.scenes[1].score.reset()
        self.scenes[1].cherry.reset(301, 465)

    def exit_game(self):
        print('Bye bye')
        self.game_over = True
