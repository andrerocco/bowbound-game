import pygame
from abstractBuildStructure import BuildStructure

class Target(BuildStructure):
    def __init__(self, position, width, height):
        super().__init__(position, width, height, 'orange')