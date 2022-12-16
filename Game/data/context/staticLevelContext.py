import pygame


class LevelMouse:
    __display_surface_offset = (0, 0)
    __screen_dimensions = (0, 0)
    __level_dimensions = (0, 0)

    @staticmethod
    def mouse_pos():
        return (pygame.mouse.get_pos()[0] - LevelMouse.__display_surface_offset[0],
                pygame.mouse.get_pos()[1] - LevelMouse.__display_surface_offset[1])

    @staticmethod
    def get_surface_offset():
        return LevelMouse.__display_surface_offset

    @staticmethod
    def set_surface_offset(screen_dimensions: tuple, level_dimensions: tuple):
        if screen_dimensions != LevelMouse.__screen_dimensions or level_dimensions != LevelMouse.__level_dimensions:
            LevelMouse.__screen_dimensions = screen_dimensions
            LevelMouse.__level_dimensions = level_dimensions
            LevelMouse.__display_surface_offset = (
                (screen_dimensions[0] - level_dimensions[0]) // 2,
                (screen_dimensions[1] - level_dimensions[1]) // 2
            )

class Framerate:
    __delta_time: 0

    @staticmethod
    def get_dt():
        return Framerate.__delta_time

    @staticmethod
    def set_dt(dt):
        Framerate.__delta_time = dt
