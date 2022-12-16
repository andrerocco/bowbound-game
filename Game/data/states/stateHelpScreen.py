import pygame
from states.abstractState import State
from utility.interface.classeTextButton import TextButton
from utility.interface.classeImage import Image
from singletons.singletonAssets import Assets

from states.stateArrowHelpScreen import ArrowHelp


class HelpScreen(State):
    def __init__(self, game):
        ACTIONS = {'mouse_left': False, 'esc': False}

        super().__init__(game, ACTIONS)

        self.__assets = Assets()
        self.__background = self.__assets.images['background']

        self.__load_buttons()

    def __load_buttons(self):
        self.VOLTAR = TextButton(self.__assets.fonts_path['text'], 35, (255, 255, 255), '< Voltar')
        self.TEXT_RESET_LEVEL = TextButton(self.__assets.fonts_path['text'], 40, (255, 255, 255), 'Reset Level')
        self.TEXT_PAUSE = TextButton(self.__assets.fonts_path['text'], 40, (255, 255, 255), 'Pause')
        self.TEXT_SHOOT = TextButton(self.__assets.fonts_path['text'], 40, (255, 255, 255), 'Shoot')
        self.TEXT_MOVE = TextButton(self.__assets.fonts_path['text'], 40, (255, 255, 255), 'Move')
        self.NEXT_PAGE = TextButton(self.__assets.fonts_path['text'], 35, (255, 255, 255), 'Proxíma Página >')

        self.IMAGE_R = Image(self.__assets.interface['keys']['r'])
        self.IMAGE_ESC = Image(self.__assets.interface['keys']['esc'])
        self.IMAGE_LMB = Image(self.__assets.interface['keys']['lmb'])
        self.IMAGE_WASD = Image(self.__assets.interface['keys']['wasd'])
        self.IMAGE_KEYS = Image(self.__assets.interface['keys']['directions'])

    def update_actions(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._actions['mouse_left'] = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._actions['mouse_left'] = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._actions['esc'] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self._actions['esc'] = False

    def update(self):
        if self._actions['mouse_left']:
            if self.VOLTAR.check_for_hover(pygame.mouse.get_pos()):
                self.exit_state()
            if self.NEXT_PAGE.check_for_hover(pygame.mouse.get_pos()):
                ArrowHelp(self._game).enter_state()

    def render(self, display_surface):
        background = pygame.transform.smoothscale(self.__background, (self._game.screen_width, self._game.screen_height))
        display_surface.blit(background, (0, 0)) #Background

        left_half_center = (self._game.screen_width//4, self._game.screen_height//2)
        right_half_center = ((self._game.screen_width//4)*3, self._game.screen_height//2)
        right = display_surface.get_rect().topright

        self.VOLTAR.render(display_surface, (15, 10), position_origin = 'topleft')
        self.NEXT_PAGE.render(display_surface, (right[0]-15, right[1]+10), position_origin = 'topright')

        self.IMAGE_R.render(display_surface, (left_half_center[0]-70, left_half_center[1]-100), position_origin = 'center')
        self.IMAGE_ESC.render(display_surface, (left_half_center[0]-70, left_half_center[1]+0), position_origin = 'center')
        self.IMAGE_LMB.render(display_surface, (left_half_center[0]-70, left_half_center[1]+100), position_origin = 'center')
        
        self.TEXT_RESET_LEVEL.render(display_surface, (left_half_center[0]+20, left_half_center[1]-100-25), position_origin = 'topleft')
        self.TEXT_PAUSE.render(display_surface, (left_half_center[0]+20, left_half_center[1]+0-25), position_origin = 'topleft')
        self.TEXT_SHOOT.render(display_surface, (left_half_center[0]+20, left_half_center[1]+100-25), position_origin = 'topleft')

        self.TEXT_MOVE.render(display_surface, (right_half_center[0]-50, right_half_center[1]+90), position_origin = 'center')
        self.IMAGE_WASD.render(display_surface, (right_half_center[0]-100-50, right_half_center[1]-10), position_origin = 'center')
        self.IMAGE_KEYS.render(display_surface, (right_half_center[0]+100-50, right_half_center[1]-10), position_origin = 'center')
