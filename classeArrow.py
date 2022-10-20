from cmath import pi
import pygame
from math import atan2, sin, cos, pi

class Arrow():
    def __init__(self, tipo: str = 'normal'):
        # Importa a imagem da flecha
        self.base_image = pygame.image.load('./arrow.png').convert()

        # Atributos de características da flecha
        self.minimun_speed = 10
        self.maximun_extra_speed = 15
        self.gravity = 0.2

    # Quando for atirada, inicia os atributos usados para o seu movimento
    def start_shot(self, initial_position: tuple, target_position: tuple, hold_factor: float):
        # Velocidade da flecha depende do tempo que o jogador segurou o mouse
        self.speed = self.minimun_speed + (self.maximun_extra_speed * hold_factor)
        print(self.speed)

        # Atributos de posição
        angle_radian = atan2(target_position[1] - initial_position[1], target_position[0] - initial_position[0]) # Define o ângulo em radianos
        self.delta_position = pygame.Vector2((cos(angle_radian) * self.speed), (sin(angle_radian) * self.speed))
        angle_degrees = -(angle_radian) * 180 / pi # Converte o ângulo para graus

        # Retângulo da flecha
        rotated_image = pygame.transform.rotate(self.base_image, angle_degrees).convert()
        rotated_image.set_colorkey((255, 255, 255))
        self.image = rotated_image
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
        angle_radian = atan2(self.delta_position.y, self.delta_position.x) # Define o ângulo em radianos do vetor deslocamento
        angle_degrees = -(angle_radian) * 180 / pi # Converte o ângulo para graus

        rotated_image = pygame.transform.rotate(self.base_image, angle_degrees).convert()
        rotated_image.set_colorkey((255, 255, 255))
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.move()
        self.rotate_image()
 