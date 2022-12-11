import pygame
from states.abstractState import State
from utility.interface.classeTextButton import TextButton
from utility.interface.classeImage import Image
from singletons.singletonAssets import Assets


class ArrowHelp(State):
    def __init__(self, game):
        ACTIONS = {'mouse_left': False, 'esc': False}

        super().__init__(game, ACTIONS)

        self.__assets = Assets()
        self.__background = self.__assets.images['background']

        self.__load_buttons()

    def __load_buttons(self):
        self.VOLTAR = TextButton(self.__assets.fonts_path['text'], 35, (255, 255, 255), '< Voltar')
        self.TEXT_BOUNCE_ARROW = TextButton(self.__assets.fonts_path['text'], 40, (101, 139, 245), 'Bounce Arrow: A flecha quica 2 vezes antes de se fixar na parede')
        self.TEXT_FAST_ARROW = TextButton(self.__assets.fonts_path['text'], 40, (245, 173, 101), 'Fast Arrow: A flecha possui uma velocidade superior que as demais')
        self.TEXT_PIERCING_ARROW = TextButton(self.__assets.fonts_path['text'], 40, (245, 101, 101), 'Piercing Arrow: A flecha continua sua tragetória mesmo se atingir um alvo')
        self.TEXT_STANDARD_ARROW = TextButton(self.__assets.fonts_path['text'], 40, (200, 200, 200), 'Standard Arrow: Apenas uma flecha normal')

        self.IMAGE_BOUNCE_ARROW = Image(self.__assets.interface['arrows']['bounce'])
        self.IMAGE_FAST_ARROW = Image(self.__assets.interface['arrows']['fast'])
        self.IMAGE_PIERCING_ARROW = Image(self.__assets.interface['arrows']['piercing'])
        self.IMAGE_STANDARD_ARROW = Image(self.__assets.interface['arrows']['standard'])

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

    def update(self, delta_time):
        if self._actions['mouse_left']:
            if self.VOLTAR.check_for_hover(pygame.mouse.get_pos()):
                self.exit_state()

    def render(self, display_surface):
        background = pygame.transform.smoothscale(self.__background, (self._game.screen_width, self._game.screen_height))
        display_surface.blit(background, (0, 0)) #Background

        left = display_surface.get_rect().midleft

        self.VOLTAR.render(display_surface, (15, 10), position_origin = 'topleft')

        self.TEXT_BOUNCE_ARROW.render(display_surface, (left[0]+70, left[1]-150), position_origin = 'topleft')
        self.TEXT_FAST_ARROW.render(display_surface, (left[0]+70, left[1]-50), position_origin = 'topleft')
        self.TEXT_PIERCING_ARROW.render(display_surface, (left[0]+70, left[1]+50), position_origin = 'topleft')
        self.TEXT_STANDARD_ARROW.render(display_surface, (left[0]+70, left[1]+150), position_origin = 'topleft')
        self.IMAGE_BOUNCE_ARROW.render(display_surface, (left[0]+40, left[1]-150), position_origin = 'topleft')
        self.IMAGE_FAST_ARROW.render(display_surface, (left[0]+40, left[1]-50), position_origin = 'topleft')
        self.IMAGE_PIERCING_ARROW.render(display_surface, (left[0]+40, left[1]+50), position_origin = 'topleft')
        self.IMAGE_STANDARD_ARROW.render(display_surface, (left[0]+40, left[1]+150), position_origin = 'topleft')
        