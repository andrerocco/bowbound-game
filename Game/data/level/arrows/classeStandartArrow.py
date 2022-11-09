from level.arrows.abstractArrow import Arrow
from finder import find_file

class StandartArrow(Arrow):
    def __init__(self, tipo: str = 'normal'):
        IMAGE_PATH = find_file('arrow.png')
        
        super().__init__(IMAGE_PATH, 10, 15, 0.2)
 