from constants import RED
from objects.button import ButtonObject
from scenes.base import BaseScene
from sounds.sound import SoundManager


class MenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.objects.append(
            ButtonObject(
                self.game, self.game.width // 2 - 100, self.game.height // 2 - 20 - 25, 200, 50,
                RED, self.start_game, text='Запуск игры', enable_sound=False
            )
        )
        self.objects.append(
            ButtonObject(
                self.game, self.game.width // 2 - 100, self.game.height // 2 + 25, 200, 50,
                RED, self.game.exit_game, text='Выход'
            )
        )

    def start_game(self):
        self.game.set_scene(self.game.SCENE_GAME)
        self.game.sound_manager.play_sound("Intro")
        self.game.reset()
