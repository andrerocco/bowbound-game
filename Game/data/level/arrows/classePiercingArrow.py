from singletons.singletonAssets import Assets
from level.arrows.abstractArrow import Arrow


class PiercingArrow(Arrow):
    def __init__(self):
        IMAGE = Assets().level_images['arrows']['piercing']
        ICON_IMAGE = Assets().interface['arrows']['piercing']
        BORDERED_ICON_IMAGE = Assets().interface['bordered-arrows']['piercing']

        super().__init__(10, 15, 0.2, IMAGE, ICON_IMAGE, BORDERED_ICON_IMAGE)
