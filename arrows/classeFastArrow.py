from abstractArrow import Arrow
from os import path

class FastArrow(Arrow):
    def __init__(self):
        IMAGE_PATH = path.join('arrow.png')
        MINIMUN_SPEED = 20

        super().__init__(IMAGE_PATH, MINIMUN_SPEED, 5, 0.2)