import pygame
from traitlets import Bool
from abstractBuildStructure import BuildStructure

class ExitDoor(BuildStructure):
    def __init__(self, position, width, height):
        super().__init__(position, width, height, 'blue')
        self.__locked = False

    def is_locked(self) -> bool:
        return self.__locked
    
    def unlock(self):
        self.__locked = False
