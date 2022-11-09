import pygame
from finder import find_file
from math import pi, atan2
from level.arrows.abstractArrow import Arrow
from level.arrows.classeStandartArrow import StandartArrow
from level.arrows.classeBounceArrow import BounceArrow
from level.arrows.classeFastArrow import FastArrow


class Bow():
    def __init__(self, initial_position):
        # Atributos padrões
        self.__image = pygame.image.load(find_file('gun.png')).convert() # Carrega a imagem do arco (que tem fundo preto)
        self.__image.set_colorkey((0,0,0)) # Define a cor preta como transparente
        self.__image = pygame.transform.scale(self.__image, (58, 8)) # Redimensiona a imagem do arco
        self.__rect = self.__image.get_rect(center=initial_position)

        # Flechas
        self.__arrows = [BounceArrow(), StandartArrow(), FastArrow()]
        
    
    def get_rotated_image(self, player_position):
        cursor_position = pygame.mouse.get_pos()
        
        # Calcula o ângulo entre o centro do jogador (ponto pivô de rotação da arma) e o cursor
        relative_position = pygame.Vector2(cursor_position) - pygame.Vector2(player_position)
        angle_degrees = (180 / pi) * (-atan2(relative_position[1], relative_position[0]))

        rotated_image = pygame.transform.rotate(self.__image, angle_degrees) # Faz uma cópia da imagem rotacionada

        return rotated_image
    
    def pop_first_arrow(self) -> Arrow:
        return self.__arrows.pop(0) # Retorna a primeira flecha da lista e a remove da lista

    def add_stuck_arrow(self, arrow: Arrow):
        self.__arrows.append(arrow)

    # Getters
    @property
    def rect(self):
        return self.__rect

    @property
    def image(self):
        return self.__image

    @property
    def arrows(self):
        return self.__arrows
