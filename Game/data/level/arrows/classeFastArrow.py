from level.arrows.abstractArrow import Arrow
from finder import find_file

class FastArrow(Arrow):
    def __init__(self):
        IMAGE_PATH = find_file('arrow.png')
        MINIMUN_SPEED = 20

        super().__init__(IMAGE_PATH, MINIMUN_SPEED, 5, 0.2)