import pygame


class SoundManager:
    def __init__(self):
        self.sounds = {
            'Intro': pygame.mixer.Sound('sounds/intro.mp3'),
            'Death': pygame.mixer.Sound('sounds/death.mp3'),
            'Move': pygame.mixer.Sound('sounds/waka.mp3'),
        }
        self.sounds["Move"].set_volume(0.2)

    def play_sound(self, name, loops=0):
        self.sounds[name].play(loops)
