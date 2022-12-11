import pygame

from utility.interface.classeTextButton import TextButton


class InputBox(TextButton):
    def __init__(self, font_path, font_size: int, base_color: tuple, initial_width = 400, text=''):
        super().__init__(font_path, font_size, base_color, text)

        self.__text_string = text
        self.__text_surface = self._text

        self.__initial_box_width = initial_width
        self._rect = pygame.Rect(0, 0, initial_width, font_size + 20)
        
    def update_actions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                pass # Não espaços no nome
            elif event.key == pygame.K_BACKSPACE:
                self.__text_string = self.__text_string[:-1] # Remove o último caractere
            else:
                self.__text_string += event.unicode

            # Atualiza o texto
            self.__text_surface = self._font.render(str(self.__text_string).upper(), True, self._base_color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.__initial_box_width, self.__text_surface.get_width()+10)
        self._rect.w = width
    
    def render(self, screen: pygame.display, position: tuple, position_origin: str = 'center'):
        if position_origin == 'topleft':
            self._rect.topleft = position
        elif position_origin == 'topright':
            self._rect.topright = position
        elif position_origin == 'bottomleft':
            self._rect.bottomleft = position
        elif position_origin == 'bottomright':
            self._rect.bottomright = position
        else: # Por padrão renderiza a partir de seu centro
            self._rect.center = position
        
        # Calcula a posição que centraliza o texto no input
        text_x = self._rect.x + (self._rect.w // 2) - (self.__text_surface.get_width() // 2) 
        text_y = self._rect.y + (self._rect.h // 2) - (self.__text_surface.get_height() // 1.75) # Divide por 1.75 pois a fonte não é perfeitamente centralizada
        screen.blit(self.__text_surface, (text_x, text_y))
        # Blit the rect.
        pygame.draw.rect(screen, self._base_color, self._rect, 2)

    @property
    def text(self):
        return self.__text_string
