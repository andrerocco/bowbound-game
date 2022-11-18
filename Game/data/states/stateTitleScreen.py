import pygame
from states.abstractState import State
from states.stateLevelPlaying import LevelPlaying


class TitleScreen(State):
    def __init__(self, game):
        super().__init__(game)

        self.__background = None
        self.__buttons = pygame.sprite.Group()
    
    def update(self, delta_time, actions):
        pass
        #if self._game.actions['reset']:
        #    level_playing_state = LevelPlaying(self._game)
        #    level_playing_state.enter_state()

    def render(self, display_surface):
        display_surface.fill('black') # Limpa a tela

        font = pygame.font.SysFont(None, 24)
        text = font.render('Menu', True, (255, 255, 255))
        
        center = display_surface.get_rect().center
        center = (center[0] - text.get_width() / 2, center[1] - text.get_height() / 2)

        display_surface.blit(text, center)
