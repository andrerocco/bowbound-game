import pygame
from states.abstractState import State
from states.stateLevelPaused import LevelPaused


class LevelPlaying(State):
    def __init__(self, game):
        super().__init__(game)

        self.__background = None
        self.__buttons = pygame.sprite.Group()

    def update(self, delta_time, actions):
        # Se o jogador pressionar ESC, entra no estado de pausa
        if self._game.actions['esc']:
            pause_state = LevelPaused(self._game)
            pause_state.enter_state()

    def render(self, display_surface):
        pass
