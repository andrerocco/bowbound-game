import pygame
from level.build_structures.abstractBuildStructure import BuildStructure
from singletons.singletonAssets import Assets


class Tile(BuildStructure):
    def __init__(self, position, size, block_name):
        try:
            if block_name.upper() == 'B_BLACK':
                SURFACE = pygame.Surface((size, size))
                SURFACE.fill((5,5,8))
            else:
                SURFACE = Assets().level_images['blocks'][block_name.upper()]
        except KeyError:
            raise ValueError(f"Invalid block name '{block_name}' recieved")

        super().__init__(position, size, size, SURFACE)
