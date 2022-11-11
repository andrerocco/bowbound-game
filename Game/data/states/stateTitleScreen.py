import pygame
from states.abstractState import State


class TitleScreen(State):
    def __init__(self, game):
        super().__init__(game)

        self.__background = None
        self.__buttons = pygame.sprite.Group()
    
    def update(self, delta_time, actions):
        self._game.reset_keys()

    def render(self, display_surface):
        font = pygame.font.SysFont(None, 24)
        text = font.render('Menu', True, (255, 255, 255))
        
        center = display_surface.get_rect().center
        center = (center[0] - text.get_width() / 2, center[1] - text.get_height() / 2)

        display_surface.blit(text, center)