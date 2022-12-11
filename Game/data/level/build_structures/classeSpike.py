import pygame
from level.build_structures.abstractBuildStructure import BuildStructure
from singletons.singletonAssets import Assets


class Spike(BuildStructure):
    def __init__(self, position, block_size):
        IMAGE = Assets().level_images['spike']
        WIDTH = IMAGE.get_width()
        HEIGHT = IMAGE.get_height()

        # Como a imagem é mais baixa que o tamanho usual do bloco, deve ser posicionada na região inferior do bloco
        POSITION = (position[0] + (block_size - WIDTH), position[1] + (block_size - HEIGHT))

        super().__init__(POSITION, WIDTH, HEIGHT, IMAGE)
    
    def collided(self, collided_with):
        return self.rect.colliderect(collided_with)
