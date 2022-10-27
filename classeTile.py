import pygame
from abstractBuildStructure import BuildStructure

class Tile(BuildStructure):
    def __init__(self, position, size):
        super().__init__(position, size, size, 'grey')
