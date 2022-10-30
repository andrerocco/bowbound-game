import pygame
from abc import ABC

class BuildStructure(ABC, pygame.sprite.Sprite):
    def __init__(self, initial_position, width, height, fill):
        super(BuildStructure, self).__init__() # Inicia a classe ABC e a classe de Sprite

        self.image = pygame.Surface((width, height))
        self.image.fill(fill)
        self.rect = self.image.get_rect(topleft = initial_position)
