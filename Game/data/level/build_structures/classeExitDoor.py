import pygame
from level.build_structures.abstractBuildStructure import BuildStructure
from singletons.singletonAssets import Assets


class ExitDoor(BuildStructure):
    def __init__(self, position, block_size):
        self.__frames = Assets().level_images['door']
        self.__frame_quantity = len(self.__frames)

        CLOSED_IMAGE = self.__frames[0]
        WIDTH = CLOSED_IMAGE.get_width()
        HEIGHT = CLOSED_IMAGE.get_height()
        
        # Como a imagem é mais alta que o tamanho usual do bloco, deve ser posicionada na região inferior do bloco
        POSITION = (position[0] + (block_size - WIDTH), position[1] + (block_size - HEIGHT))
        
        super().__init__(POSITION, WIDTH, HEIGHT, CLOSED_IMAGE)
        
        self.__frame_counter = 0 # Contador de frames (vai de zero até self.__frames_quantity - 1)
        self.__animation_speed = self.__frame_quantity/90 # 90 frames para completar a animação
        self.__unlocked = False

    def is_unlocked(self) -> bool:
        return self.__unlocked
    
    def unlock(self):
        if self.__frame_counter >= self.__frame_quantity - 1: # Se já estiver na última imagem, a animação terminou
            self.__unlocked = True
        else:
            self.__frame_counter += self.__animation_speed # Incrementa o contador de frames
            self.image = self.__frames[int(self.__frame_counter)] # Como animation_speed é um float, arredonda o valor de frame_counter para inteiro

    def collided(self, collided_with):
        return self.rect.colliderect(collided_with)
