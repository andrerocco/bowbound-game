import pygame
from states.abstractState import State
from utility.interface.classeTextButton import TextButton
from singletons.singletonAssets import Assets

from states.stateLevelPlaying import LevelPlaying
from utility.classeScoreController import ScoreController


class LevelSelector(State):
    def __init__(self, game, levels_list):
        ACTIONS = {'mouse_left': False, }

        super().__init__(game, ACTIONS)

        self.__score_controller = ScoreController()
        self.__assets = Assets()
        self.__background = self.__assets.images['background']

        self.__levels_list = levels_list # Lista de níveis da categoria selecionada (é decidida pela tela de início, baseada no que o jogador escolheu)
        
        # Configurações do layout da tela
        self.__margin_top = 140
        self.__list_gap = 55

        # Scroll da lista de níveis
        if len(self.__levels_list)*self.__list_gap > self._game.screen_height - self.__margin_top:
            self.__allow_scroll = True
        else:
            self.__allow_scroll = False
        
        self.__amount_per_scroll = 40
        self.__scroll = 0
        self.__max_scroll = (len(self.__levels_list)+1) * self.__list_gap - self._game.screen_height + self.__margin_top

        self.__load_buttons()

    def __load_buttons(self):
        self.VOLTAR = TextButton(self.__assets.fonts_path['text'], 35, (255, 255, 255), '< Voltar')
        self.TITULO_NIVEL = TextButton(self.__assets.fonts_path['title'], 50, (222, 142, 152), 'Nível')
        self.TITULO_RECORDE = TextButton(self.__assets.fonts_path['title'], 50, (142, 174, 222), 'Recorde')
        self.TITULO_AUTOR = TextButton(self.__assets.fonts_path['title'], 50, (142, 222, 160), 'Autor')
        self.SELETOR = TextButton(self.__assets.fonts_path['text'], 45, (222, 142, 152), '>')
        self.NIVEIS, self.RECORDES, self.AUTORES = [], [], []

        scores = self.__score_controller.get_all_best_scores()

        # Cria os botões de cada nível
        for index, level in enumerate(self.__levels_list):
            self.NIVEIS.append(TextButton(self.__assets.fonts_path['text'], 50, (255, 255, 255), str(index + 1))) # Número do nível

            # Cria o texto com o recorde do nível e seu respectivo autor
            level_name = level['level_name']
            if level_name in scores:
                name, time = scores[level_name][0], scores[level_name][1]
            else:
                name, time = "-", "-"
            self.RECORDES.append(TextButton(self.__assets.fonts_path['text'], 50, (255, 255, 255), time))
            self.AUTORES.append(TextButton(self.__assets.fonts_path['text'], 50, (255, 255, 255), name))

    def update_actions(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._actions['mouse_left'] = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._actions['mouse_left'] = False
        # Evento de scroll
        if event.type == pygame.MOUSEWHEEL and event.y > 0:
            if self.__allow_scroll and self.__scroll < 0:
                self.__scroll += self.__amount_per_scroll
        if event.type == pygame.MOUSEWHEEL and event.y < 0:
            if self.__allow_scroll and self.__scroll > -self.__max_scroll:
                self.__scroll -= self.__amount_per_scroll
    
    def update(self):
        # Atualiza o máximo de scroll caso haja mudanças no tamanho da tela
        self.__max_scroll = (len(self.__levels_list)+1) * self.__list_gap - self._game.screen_height + self.__margin_top

        if self._actions['mouse_left']:
            if self.VOLTAR.check_for_hover(pygame.mouse.get_pos()):
                self.exit_state()
            
            for i in range(0, len(self.NIVEIS)):
                if self.NIVEIS[i].check_for_hover(pygame.mouse.get_pos()):
                    LevelPlaying(self._game, self.__levels_list, i).enter_state()

    def render(self, display_surface):
        background = pygame.transform.smoothscale(self.__background, (self._game.screen_width, self._game.screen_height))
        display_surface.blit(background, (0, 0)) # Mostra o background

        # Coordenadas do centro e da direita da tela
        center = display_surface.get_rect().center
        right = display_surface.get_rect().topright

        # Títulos da lista de níveis
        self.TITULO_NIVEL.render(display_surface, (130, self.__margin_top + self.__scroll))
        self.TITULO_RECORDE.render(display_surface, (center[0]+50, self.__margin_top + self.__scroll))
        self.TITULO_AUTOR.render(display_surface, (right[0]-200, self.__margin_top + self.__scroll))

        # Lista de níveis
        for i in range(0, len(self.NIVEIS)):
            self.NIVEIS[i].render(display_surface, (130, self.__margin_top + (i+1)*self.__list_gap + self.__scroll))
            self.RECORDES[i].render(display_surface, (center[0]+50, self.__margin_top + (i+1)*self.__list_gap + self.__scroll))
            self.AUTORES[i].render(display_surface, (right[0]-200, self.__margin_top + (i+1)*self.__list_gap + self.__scroll))
            if self.NIVEIS[i].check_for_hover(pygame.mouse.get_pos()):
                self.SELETOR.render(display_surface, (100, self.__margin_top + (i+1)*self.__list_gap + self.__scroll))
        
        # Botão de voltar
        self.VOLTAR.render(display_surface, (15, 10), position_origin = 'topleft')
