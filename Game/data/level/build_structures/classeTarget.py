import pygame
from level.build_structures.abstractBuildStructure import BuildStructure
from singletons.singletonAssets import Assets


class Target(BuildStructure):
    def __init__(self, position):
        self.__frames = Assets().level_images['target']
        self.__frame_quantity = len(self.__frames)

        TARGET_IMAGE = self.__frames[0]
        WIDTH = TARGET_IMAGE.get_width()
        HEIGHT = TARGET_IMAGE.get_height()

        super().__init__(position, WIDTH, HEIGHT, TARGET_IMAGE)
        
        self.__frame_counter = 0 # Contador de frames (vai de zero até self.__frames_quantity - 1)
        self.__animation_speed = self.__frame_quantity/6 # 6 frames para completar a animação
    
    # Transforma o alvo em branco por alguns frames e depois exclui ele
    def update(self): 
        if self.__frame_counter >= self.__frame_quantity-1: # Se já estiver na última imagem, a animação terminou
            self.kill()
        else:
            self.__frame_counter += self.__animation_speed
            self.image = self.__frames[1]
            # Como animation_speed é um float, arredonda o valor de frame_counter para inteiro
