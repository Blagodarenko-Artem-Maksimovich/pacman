from constants import RED, ORANGE
from objects.button import ButtonObject
from scenes.base import BaseScene
from objects.text import TextObject


class PauseMenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.objects.append(
            TextObject(
                self.game, self.game.width // 2 - 0, self.game.height // 2 - 175 - 25,
                text='ПАУЗА', color=ORANGE
            )
        )
        self.objects.append(
            ButtonObject(
                self.game, self.game.width // 2 - 100, self.game.height // 2 - 20 - 25, 200, 50,
                RED, self.continue_game, text='Продолжить игру'
            )
        )
        self.objects.append(
            ButtonObject(
                self.game, self.game.width // 2 - 100, self.game.height // 2 + 25, 200, 50,
                RED, self.start_game, text='Вернуться в главное меню'
            )
        )

    def start_game(self):
        self.game.set_scene(self.game.SCENE_MENU)
        # Возвращает в главное меню

    def continue_game(self):
        self.game.set_scene(self.game.SCENE_GAME)
        # Продолжает игру
