import pygame
from utility.finder import find_file
from math import pi, atan2

from singletons.singletonAssets import Assets

from level.arrows.abstractArrow import Arrow
from level.arrows.classeStandardArrow import StandardArrow
from level.arrows.classeBounceArrow import BounceArrow
from level.arrows.classeFastArrow import FastArrow
from level.arrows.classePiercingArrow import PiercingArrow


class Crossbow():
    def __init__(self, initial_position, initial_arrows):
        # Atributos padrões
        self.__image = Assets().level_images['gun'] # Carrega a imagem do arco (que tem fundo preto)
        self.__rect = self.__image.get_rect(center=initial_position)

        # Flechas
        self.__arrows = []
        for arrow in initial_arrows:
            if str(arrow).lower() == 'standard':
                self.__arrows.append(StandardArrow())
            elif str(arrow).lower() == 'bounce':
                self.__arrows.append(BounceArrow())
            elif str(arrow).lower() == 'fast':
                self.__arrows.append(FastArrow())
            elif str(arrow).lower() == 'piercing':
                self.__arrows.append(PiercingArrow())
            else:
                print(f"Flecha não reconhecida iniciada: {arrow}. Adicionando flecha padrão.")
                self.__arrows.append(StandardArrow())

    def get_rotated_image(self, player_position, cursor_position):
        # Calcula o ângulo entre o centro do jogador (ponto pivô de rotação da arma) e o cursor
        relative_position = pygame.Vector2(cursor_position) - pygame.Vector2(player_position)
        angle_degrees = (180 / pi) * (-atan2(relative_position[1], relative_position[0]))

        if angle_degrees <= 90 and angle_degrees >= -90: # Quadrantes da direita
            image = self.__image
        else: # Quadrantes da esquerda
            image = pygame.transform.flip(self.__image, False, True) # Faz uma cópia da imagem espelhada verticalmente
            
        rotated_image = pygame.transform.rotate(image, angle_degrees) # Faz uma cópia da imagem rotacionada

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
