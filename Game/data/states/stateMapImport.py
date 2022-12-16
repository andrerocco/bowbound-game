import pygame
from states.abstractState import State
from utility.interface.classeTextButton import TextButton
from singletons.singletonAssets import Assets


from utility.classeLevelImportController import LevelImportController


class MapImport(State):
    def __init__(self, game):
        ACTIONS = {'mouse_left': False}
        
        super().__init__(game, ACTIONS)
        
        self.__assets = Assets()
        self.__background = self.__assets.images['background']

        self.__level_import_controller = LevelImportController('created-levels.json')
        
        self.__load_buttons()
    
    def __load_buttons(self):
        self.VOLTAR = TextButton(self.__assets.fonts_path['text'], 35, (255, 255, 255), '< Voltar')
        self.IMPORTAR = TextButton(self.__assets.fonts_path['text'], 35, (255, 255, 255), 'Clique para abrir o explorador de arquivos...')
        self.TEXTO_ERRO = TextButton(self.__assets.fonts_path['text'], 30, (140,140,140), '')
    
    def update_actions(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._actions['mouse_left'] = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._actions['mouse_left'] = False
    
    def update(self, delta_time):
        if self._actions['mouse_left']:
            if self.VOLTAR.check_for_hover(pygame.mouse.get_pos()):
                self.exit_state()
            if self.IMPORTAR.check_for_hover(pygame.mouse.get_pos()):
                super().restart_actions() # Reinicia as ações para que não fique abrindo varias vezes o file picker
                try:
                    status = self.__level_import_controller.import_from_file_picker()
                    if status:
                        self.TEXTO_ERRO.set_text('Mapa importado com sucesso! Reinicie o jogo para carregar.')
                    else:
                        self.TEXTO_ERRO.set_text('')
                except Exception as e:
                    self.TEXTO_ERRO.set_text('Erro ao importar mapa!')
                    print(e)

    def render(self, display_surface):
        display_surface.fill((0, 0, 0)) # Limpa a tela
        background = pygame.transform.smoothscale(self.__background, (self._game.screen_width, self._game.screen_height))
        display_surface.blit(background, (0, 0)) # Mostra o background

        center = display_surface.get_rect().center

        self.VOLTAR.render(display_surface, (15, 10), position_origin = 'topleft')
        self.IMPORTAR.render(display_surface, (center[0], center[1]), position_origin = 'center')
        self.TEXTO_ERRO.render(display_surface, (center[0], center[1] + 80), position_origin = 'center')
