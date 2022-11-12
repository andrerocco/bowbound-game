import pygame
from states.abstractState import State


class LevelPaused(State):
    def __init__(self, game):
        super().__init__(game)

        self.__background = None
        self.__buttons = pygame.sprite.Group()

    def update(self, delta_time, actions):
        # Se o jogador pressionar ESC, sai do estado de pausa
        if actions['esc']:
            self.exit_state()

    def render(self, display_surface):
        self.__display_surface.fill('black') # Limpa a tela
