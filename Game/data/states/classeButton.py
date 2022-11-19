import pygame


class Button():
    def __init__(self, font_path, font_size: int, base_color: tuple, text):
        super().__init__()

        self.__font = pygame.font.Font(font_path, font_size)
        self.__base_color = base_color
        self.__text = self.__font.render(text, True, self.__base_color)

        self.__rect = self.__text.get_rect()
    
    def render(self, screen: pygame.display, center_position: tuple):
        self.__rect.center = center_position
        screen.blit(self.__text, self.__rect)

    def check_for_input(self, mouse_position):
        if self.__rect.collidepoint(mouse_position):
            return True
        return False

    #def change_color(self):
    #    ...
    
