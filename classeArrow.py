import pygame
from math import atan2, sin, cos

class Arrow():
    def __init__(self, tipo: str = 'normal'):
        # Atributos padrões
        self.image = pygame.image.load('./arrow.png').convert()
        
        # Atributos de características da flecha
        self.speed = 16
        self.gravity = 0.5

    # Quando for atirada, inicia os atributos usados para o seu movimento
    def start_shot(self, initial_position: tuple, target_position: tuple):
        # Atributos de posição
        angle_radian = atan2(target_position[1] - initial_position[1], target_position[0] - initial_position[0]) # Define o ângulo em radianos
        self.delta_position = pygame.Vector2((cos(angle_radian) * self.speed), (sin(angle_radian) * self.speed))

        # Retângulo da flecha
        self.rect = self.image.get_rect(center=initial_position)
        
        # Posição x e y da flecha (quer será atualizada para float apartir de dx e dy)
        self.x_pos = self.rect.x
        self.y_pos = self.rect.y

    def move(self):
        # Aplica a gravidade no self.dy
        self.delta_position.y += self.gravity

        # Acrescenta self.x_pos e self.y_pos para floats
        self.x_pos += self.delta_position.x
        self.y_pos += self.delta_position.y

        # Atualiza a posição do retângulo de fato
        self.rect.x = int(self.x_pos)
        self.rect.y = int(self.y_pos)

    def rotate_image(self):
        pass

    def update(self):
        self.move()
 