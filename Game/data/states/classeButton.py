import pygame


class Button():
    def __init__(self, font_path, font_size: int, base_color: tuple, text):
        super().__init__()

        self.__font = pygame.font.Font(font_path, font_size)
        self.__base_color = base_color
        self.__text = self.__font.render(text, True, self.__base_color)

        self.__rect = self.__text.get_rect()
    
    def render(self, screen: pygame.display, position: tuple, position_origin: str = 'center'):
        if position_origin == 'topleft':
            self.__rect.topleft = position
        elif position_origin == 'topright':
            self.__rect.topright = position
        elif position_origin == 'bottomleft':
            self.__rect.bottomleft = position
        elif position_origin == 'bottomright':
            self.__rect.bottomright = position
        else: # Por padrão renderiza a partir de seu centro
            self.__rect.center = position
        
        screen.blit(self.__text, self.__rect)

    def check_for_hover(self, mouse_position):
        if self.__rect.collidepoint(mouse_position):
            return True
        return False

    #def change_color(self):
    #    ...
    
