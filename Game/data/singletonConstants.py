from abstractSingleton import Singleton
import pygame


class Constants(Singleton):
    def update_screen_offset(self, screen: pygame.display, display_surface: pygame.Surface):
        try:
            x_pos = int((screen.get_width() - display_surface.get_width()) / 2)
            y_pos = int((screen.get_height() - display_surface.get_height()) / 2)
            self.__screen_offset = (x_pos, y_pos)
        except:
            raise TypeError('Parameters screen and display_surface must be pygame.display and pygame.Surface, respectively')

    @property
    def mouse_pos(self) -> tuple:
        return pygame.mouse.get_pos()[0] - self.__screen_offset[0], pygame.mouse.get_pos()[1] - self.__screen_offset[1]
    
    @property
    def surface_offset(self) -> tuple:
        return self.__screen_offset
