import pygame
from abc import ABC

class BuildStructure(ABC, pygame.sprite.Sprite):
    def __init__(self, width, height, initial_position):
        super(BuildStructure, self).__init__() # Inicia a classe ABC que define essa classe como abstrata

        self.image = pygame.Surface((width, height))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = initial_position)