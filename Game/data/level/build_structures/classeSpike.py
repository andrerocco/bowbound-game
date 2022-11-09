import pygame
from ..build_structures.abstractBuildStructure import BuildStructure

class Spike(BuildStructure):
    def __init__(self, position, width, height):
        super().__init__(position, width, height, 'green')
    
    def collided(self, collided_with):
        return self.rect.colliderect(collided_with)
