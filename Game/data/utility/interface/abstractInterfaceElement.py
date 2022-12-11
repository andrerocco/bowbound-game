import pygame
from abc import ABC, abstractmethod


class InterfaceElement(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def render(self, screen: pygame.display, position: tuple, position_origin: str = 'center'):
        pass
