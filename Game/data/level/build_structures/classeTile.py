import pygame
from ..build_structures.abstractBuildStructure import BuildStructure

class Tile(BuildStructure):
    def __init__(self, position, size):
        super().__init__(position, size, size, 'grey')
