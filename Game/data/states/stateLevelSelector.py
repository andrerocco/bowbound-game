import pygame
from states.abstractState import State
from states.classeButton import Button
from singletonAssets import Assets
from Settings import Settings

from states.stateLevelPlaying import LevelPlaying
from utility.classeScoreController import ScoreController


class LevelSelector(State):
    def __init__(self, game):
        super().__init__(game)

        self.__scoreController = ScoreController()

        self.__assets = Assets()
        self.__background = self.__assets.images['background']

        self.__load_buttons()


    def __load_buttons(self):
        self.VOLTAR = Button(self.__assets.fonts_path['text'], 35, (255, 255, 255), '< Voltar')
        self.NIVEL = Button(self.__assets.fonts_path['text'], 50, (222, 69, 69), 'Nível')
        self.RECORDE = Button(self.__assets.fonts_path['text'], 50, (90, 107, 219), 'Recorde')
        self.SELETOR = Button(self.__assets.fonts_path['text'], 45, (222, 69, 69), '>')
        self.NIVEIS = []
        self.RECORDES = []
        scores = self.__scoreController.get_all_scores()
        
        for level in range(1, 9): # Range vai depender da classe que controla os leveis
            self.NIVEIS.append(Button(self.__assets.fonts_path['text'], 50, (255, 255, 255), str(level)))
            if level in scores:
                self.RECORDES.append(Button(self.__assets.fonts_path['text'], 50, (255, 255, 255), str(scores[level][0][1])))
            else:
                self.RECORDES.append(Button(self.__assets.fonts_path['text'], 50, (255, 255, 255), '--'))
    
    def update(self, delta_time, actions):
        if self._game.actions['mouse_left']:
            if self.VOLTAR.check_for_hover(Settings.mouse_pos()):
                self.exit_state()
            
            for i in range(0, len(self.NIVEIS)):
                if self.NIVEIS[i].check_for_hover(Settings.mouse_pos()):
                    self._game.state_stack.append(LevelPlaying(self._game))


    def render(self, display_surface):
        background = pygame.transform.smoothscale(self.__background, (self._game.screen_width, self._game.screen_height))
        display_surface.blit(background, (0, 0)) # Mostra o background

        center = display_surface.get_rect().center

        self.VOLTAR.render(display_surface, (15, 10), position_origin = 'topleft')
        self.NIVEL.render(display_surface, (130, center[1] - 200))
        self.RECORDE.render(display_surface, (center[0]-100, center[1] - 200))
        
        for i in range(0, len(self.NIVEIS)):
            self.NIVEIS[i].render(display_surface, (130, center[1] - 200 + (i + 1) * 50))
            if self.NIVEIS[i].check_for_hover(Settings.mouse_pos()):
                    self.SELETOR.render(display_surface, (100, center[1] - 200 + (i + 1) * 50))
        
        for i in range(0, len(self.RECORDES)):
            self.RECORDES[i].render(display_surface, (center[0]-100, center[1] - 200 + (i + 1) * 50))