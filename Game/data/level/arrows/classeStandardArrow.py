from singletons.singletonAssets import Assets
from level.arrows.abstractArrow import Arrow


class StandardArrow(Arrow):
    def __init__(self):
        IMAGE = Assets().level_images['arrows']['standard']
        ICON_IMAGE = Assets().interface['arrows']['standard']
        BORDERED_ICON_IMAGE = Assets().interface['bordered-arrows']['standard']

        super().__init__(10, 15, 0.2, IMAGE, ICON_IMAGE, BORDERED_ICON_IMAGE)
 