import pygame
from states.abstractState import State


class LevelSelector(State):
    def __init__(self, game):
        super().__init__(game)

        self.__background = None
        self.__buttons = pygame.sprite.Group()
    
    def update(self):
        self.game.reset_keys()

    def render(self):
        pass
