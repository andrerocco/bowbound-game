import pygame
from level.build_structures.abstractBuildStructure import BuildStructure

class ExitDoor(BuildStructure):
    def __init__(self, position, width, height):
        super().__init__(position, width, height, 'blue')
        self.__unlocked = False

    def is_unlocked(self) -> bool:
        return self.__unlocked
    
    def unlock(self):
        self.__unlocked = True

    def collided(self, collided_with):
        return self.rect.colliderect(collided_with)
