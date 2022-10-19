import pygame
from math import pi, atan2


class Bow():
    def __init__(self, initial_position):
        self.image = pygame.image.load('./gun.png').convert() # Carrega a imagem do arco (que tem fundo preto)
        self.image.set_colorkey((0,0,0)) # Define a cor preta como transparente
        self.image = pygame.transform.scale(self.image, (58, 8)) # Redimensiona a imagem do arco

        self.rect = self.image.get_rect(center=initial_position)
    
    def get_rotated_image(self, player_position):
        cursor_position = pygame.mouse.get_pos()
        
        # Calcula o ângulo entre o centro do jogador (ponto pivô de rotação da arma) e o cursor
        relative_position = pygame.Vector2(cursor_position) - pygame.Vector2(player_position)
        angle_degrees = (180 / pi) * (-atan2(relative_position[1], relative_position[0]))

        rotated_image = pygame.transform.rotate(self.image, angle_degrees) # Faz uma cópia da imagem rotacionada

        return rotated_image
