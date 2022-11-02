from abstractArrow import Arrow

class FastArrow(Arrow):
    def __init__(self):
        IMAGE_PATH = './arrow.png'
        MINIMUN_SPEED = 20

        super().__init__(IMAGE_PATH, MINIMUN_SPEED, 5, 0.2)