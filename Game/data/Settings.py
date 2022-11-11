import pygame


class Settings:
    __surface_offset = (0, 0)

    @staticmethod
    def mouse_pos():
        return (pygame.mouse.get_pos()[0] - Settings.__surface_offset[0], pygame.mouse.get_pos()[1] - Settings.__surface_offset[1])

    @staticmethod
    def set_surface_offset(x, y):
        try:
            Settings.__surface_offset = (int(x), int(y))
        except:
            raise Exception('Parameters x and y must be int')

    @staticmethod
    def get_surface_offset():
        return Settings.__surface_offset
