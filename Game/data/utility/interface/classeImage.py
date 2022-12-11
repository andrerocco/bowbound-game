import pygame
from utility.interface.abstractInterfaceElement import InterfaceElement


class Image(InterfaceElement):
    def __init__(self, image: pygame.image):
        super().__init__()

        self._image = image
        self._rect = self._image.get_rect()
    
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
        
        screen.blit(self._image, self._rect)
