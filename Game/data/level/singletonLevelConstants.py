from abstractSingleton import Singleton
import pygame


class LevelConstants(Singleton):
    def __init__(self, screen: pygame.display, display_surface: pygame.Surface):
        # Atributos usados para cálculo das constantes
        self.__screen = screen

    # Getters dos valores gerados
    @property
    def surface_displacement(self) -> tuple:
        x_displacement = int((self.__screen.get_width() - self.__display_surface.get_width()) / 2)
        y_displacement = int((self.__screen.get_height() - self.__display_surface.get_height()) / 2)
        return x_displacement, y_displacement
    @property
    def mouse_pos(self) -> tuple:
        # Retorna a posição do mouse relativa à posição da Surface na tela
        return pygame.mouse.get_pos()[0] - self.surface_displacement[0], pygame.mouse.get_pos()[1] - self.surface_displacement[1]