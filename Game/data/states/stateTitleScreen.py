import pygame
from states.abstractState import State
from states.classeButton import Button
from singletonAssets import Assets
from Settings import Settings

from states.stateLevelSelector import LevelSelector


class TitleScreen(State):
    def __init__(self, game):
        super().__init__(game)

        self.__assets = Assets()
        self.__background = self.__assets.images['background']
        
        self.__load_buttons()

    def __load_buttons(self):
        self.TITLE = Button(self.__assets.fonts_path['title'], 96, (232, 192, 50), 'Speed Archer')
        self.SELECT_1 = Button(self.__assets.fonts_path['text'], 50, (255, 255, 255), 'Selecionar nível')
        self.SELECT_2 = Button(self.__assets.fonts_path['text'], 50, (255, 255, 255), 'Criar mapa')
        self.SELECT_3 = Button(self.__assets.fonts_path['text'], 50, (255, 255, 255), 'Ajuda')
    
    def update(self, delta_time, actions):
        if self._game.actions['mouse_left']:
            if self.SELECT_1.check_for_hover(Settings.mouse_pos()):
                self._game.state_stack.append(LevelSelector(self._game))
            if self.SELECT_2.check_for_hover(Settings.mouse_pos()):
                pass
            if self.SELECT_3.check_for_hover(Settings.mouse_pos()):
                pass

    def render(self, display_surface):
        display_surface.fill((0, 0, 0)) # Limpa a tela
        
        background = pygame.transform.smoothscale(self.__background, (self._game.screen_width, self._game.screen_height))
        display_surface.blit(background, (0, 0)) # Mostra o background

        center = display_surface.get_rect().center

        self.TITLE.render(display_surface, (center[0], center[1] - 120))
        self.SELECT_1.render(display_surface, (center[0], center[1]))
        self.SELECT_2.render(display_surface, (center[0], center[1] + 60))
        self.SELECT_3.render(display_surface, (center[0], center[1] + 120))
