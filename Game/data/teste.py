import pygame


class Settings:
    __surface_offset = (3, 5)

    @staticmethod
    def teste():
        return pygame.Vector2((3, 5))

    @staticmethod
    def mouse_pos():
        return pygame.Vector2(pygame.mouse.get_pos()[0] - Settings.__surface_offset[0], pygame.mouse.get_pos()[1] - Settings.__surface_offset[1])

    """ @staticmethod
    def set_surface_offset(x, y):
        Settings.__surface_offset = (x, y) """

    @staticmethod
    def update_screen_offset(screen: pygame.display, display_surface: pygame.Surface):
        try:
            Settings.__screen_offset = (int((screen.get_width() - display_surface.get_width()) / 2),
                                        int((screen.get_height() - display_surface.get_height()) / 2))
        except:
            raise TypeError('Parameters screen and display_surface must be pygame.display and pygame.Surface, respectively')

print(Settings.teste().x)