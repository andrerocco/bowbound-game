import pygame
from states.abstractState import State


class LevelPaused(State):
    def __init__(self, game):
        super().__init__(game)

        self.__background = None
        self.__buttons = pygame.sprite.Group()

    def update(self, delta_time, actions):
        if actions['esc']:
            self.exit_state()
        self._game.reset_keys() # Ver se é necessário

    def render(self, display_surface):
        pass