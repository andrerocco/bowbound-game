import pygame
from states.abstractState import State
from utility.interface.classeTextButton import TextButton
from utility.interface.classeInputBox import InputBox
from singletons.singletonAssets import Assets

from states.stateTitleScreen import TitleScreen


class InputName(State):
    def __init__(self, game):
        ACTIONS = {'enter': False}

        super().__init__(game, ACTIONS)

        self.__assets = Assets()
        self.__background = self.__assets.images['background']

        self.__load_buttons()

        self.__verificador = False

    def __load_buttons(self):
        self.NOME = TextButton(self.__assets.fonts_path['text'], 40, (255,255,255), 'Digite seu nome:')
        self.INPUT_BOX = InputBox(self.__assets.fonts_path['text'], 50, (255,255,255), 300)
        self.TEXTO_ERRO = TextButton(self.__assets.fonts_path['text'], 30, (140,140,140), '')

    def update_actions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(self.INPUT_BOX.text) < 3:
                    self.__verificador = False
                    self.TEXTO_ERRO = TextButton(self.__assets.fonts_path['text'], 30, (140,140,140), 'Seu nome precisa ter no mínimo 3 letras')
                elif len(self.INPUT_BOX.text) > 8:
                    self.__verificador = False
                    self.TEXTO_ERRO = TextButton(self.__assets.fonts_path['text'], 30, (140,140,140), 'Seu nome pode ter no máximo 8 letras')
                else:
                    self.__verificador = True 
                    self._actions['enter'] = True
        
        self.INPUT_BOX.update_actions(event)

    def update(self):
        if self._actions['enter'] and self.__verificador:
            self.__assets.user_name = str(self.INPUT_BOX.text).upper() # Salva o nome do usuário (em all caps)
            TitleScreen(self._game).enter_state()

        self.INPUT_BOX.update()
        
    def render(self, display_surface):
        display_surface.fill((0, 0, 0)) # Limpa a tela

        background = pygame.transform.smoothscale(self.__background, (self._game.screen_width, self._game.screen_height))
        display_surface.blit(background, (0, 0)) # Mostra o background

        center = display_surface.get_rect().center
        
        self.NOME.render(display_surface, (center[0], center[1]-100))
        self.INPUT_BOX.render(display_surface, (center[0], center[1]))
        if self.__verificador != True:
            self.TEXTO_ERRO.render(display_surface, (center[0], center[1] + 80))
