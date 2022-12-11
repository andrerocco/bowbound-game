import pygame
from utility.interface.abstractInterfaceElement import InterfaceElement


class TextButton(InterfaceElement):
    def __init__(self, font_path, font_size: int, base_color: tuple, text):
        super().__init__()

        self._font = pygame.font.Font(font_path, font_size)
        self._base_color = base_color
        self._text = self._font.render(text, True, self._base_color)

        self._rect = self._text.get_rect()
    
    def render(self, screen: pygame.display, position: tuple, position_origin: str = 'center'):
        if position_origin == 'center':
            self._rect.center = position
        elif position_origin == 'topleft':
            self._rect.topleft = position
        elif position_origin == 'topright':
            self._rect.topright = position
        elif position_origin == 'bottomleft':
            self._rect.bottomleft = position
        elif position_origin == 'bottomright':
            self._rect.bottomright = position
        else: # Por padrão renderiza a partir de seu centro
            self._rect.center = position
        
        screen.blit(self._text, self._rect)

    def check_for_hover(self, mouse_position):
        if self._rect.collidepoint(mouse_position):
            return True
        return False

    def set_text(self, text):
        self._text = self._font.render(text, True, self._base_color)
        self._rect = self._text.get_rect()
