import pygame
from states.abstractState import State
from utility.interface.classeTextButton import TextButton
from singletons.singletonAssets import Assets

from utility.classeScoreController import ScoreController


class HighScores(State):
    def __init__(self, game, level_name, background_surface: pygame.Surface):
        ACTIONS = {'mouse_left': False, 'esc': False}

        super().__init__(game, ACTIONS)

        self.__score_controller = ScoreController()
        self.__assets = Assets()
        self.__level_name = level_name
        self.__background_surface = background_surface

        self.__load_buttons()

    def __load_buttons(self):
        self.VOLTAR = TextButton(self.__assets.fonts_path['text'], 35, (255, 255, 255), '< Voltar')
        self.RANK = TextButton(self.__assets.fonts_path['title'], 50, (222, 142, 152), 'Rank')
        self.AUTOR = TextButton(self.__assets.fonts_path['title'], 50, (142, 222, 160), 'Autor')
        self.RECORDE = TextButton(self.__assets.fonts_path['title'], 50, (142, 174, 222), 'Recorde')
        
        self.RANKS = []
        self.RECORDES = []
        self.AUTORES = []
        scores = self.__score_controller.get_all_level_scores_sorted(self.__level_name)
        
        for rank in range(0, len(scores)): # Range vai depender da classe que controla os leveis
            if rank > 8:
                break
            self.RANKS.append(TextButton(self.__assets.fonts_path['text'], 50, (255, 255, 255), f"{rank+1}."))
            self.AUTORES.append(TextButton(self.__assets.fonts_path['text'], 50, (255, 255, 255), str(scores[rank][0])))
            self.RECORDES.append(TextButton(self.__assets.fonts_path['text'], 50, (255, 255, 255), str(scores[rank][1])))

    def update_actions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._actions['esc'] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self._actions['esc'] = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._actions['mouse_left'] = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._actions['mouse_left'] = False

    def update(self):
        if self._actions['esc']:
            self.exit_state()
        if self._actions['mouse_left']:
            if self.VOLTAR.check_for_hover(pygame.mouse.get_pos()):
                self.exit_state()

    def render(self, display_surface):
        display_surface.fill((0, 0, 0)) # Limpa a tela

        display_surface.blit(self.__background_surface, (self._game.screen_width / 2 - self.__background_surface.get_width() / 2,
                                                         self._game.screen_height / 2 - self.__background_surface.get_height() / 2))

        center = display_surface.get_rect().center
        right = display_surface.get_rect().topright

        self.VOLTAR.render(display_surface, (15, 10), position_origin = 'topleft')
        self.RANK.render(display_surface, (170, 150))
        self.AUTOR.render(display_surface, (420, 150))
        self.RECORDE.render(display_surface, (right[0]-220, 150))
        
        for i in range(0, len(self.RANKS)):
            self.RANKS[i].render(display_surface, (170, 220 + i*55))
            self.AUTORES[i].render(display_surface, (420, 220 + i*55))
            self.RECORDES[i].render(display_surface, (right[0]-220, 220 + i*55))
