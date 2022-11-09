from abstractArrow import Arrow
from os import path

class BounceArrow(Arrow):
    def __init__(self):
        IMAGE_PATH = path.join('arrow.png')

        super().__init__(IMAGE_PATH, 10, 15, 0.2)

        self.__bounce_count = 0
        self.__max_bounce_count = 2

    def start_shot(self, initial_position: tuple, target_position: tuple, hold_factor: float):
        self.__bounce_count = 0
        super().start_shot(initial_position, target_position, hold_factor)

    def calculate_displacement(self, collide_with):
        # Aplica a gravidade no self.dy
        self.delta_position.y += self.gravity

        if self.__bounce_count < self.__max_bounce_count:     
            for tile in collide_with.sprites():
                # Colisão horizontal
                if tile.rect.colliderect(self.rect.x + self.delta_position.x, self.rect.y, self.rect.width, self.rect.height): # Testa a colisão do deslocamento horizontal
                    self.delta_position.x *= -1
                    self.__bounce_count += 1

                # Colisão vertical
                if tile.rect.colliderect(self.rect.x, self.rect.y + self.delta_position.y, self.rect.width, self.rect.height): # Testa a colisão do deslocamento vertical
                    self.delta_position.y *= -1
                    self.__bounce_count += 1

    def update(self, collide_with):
        self.calculate_displacement(collide_with)
        next_position = self.delta_position

        if self.__bounce_count + 1 >= self.__max_bounce_count:
            next_position = super().get_collided_position(next_position, collide_with)
        
        super().move(next_position)
        super().rotate_image()
