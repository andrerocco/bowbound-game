import pygame
from abc import ABC
from cmath import pi
from math import atan2, sin, cos, pi

class Arrow(ABC):
    def __init__(self, image_path: str, minimun_speed, maximun_extra_speed, gravity):
        super().__init__() # Inicia a classe ABC que define a classe como abstrata

        # Importa a imagem da flecha
        self.base_image = pygame.image.load(image_path).convert()

        # Atributos de características da flecha
        self.minimun_speed = minimun_speed
        self.maximun_extra_speed = maximun_extra_speed
        self.gravity = gravity
    
    # Quando for atirada, inicia os atributos usados para o seu movimento
    def start_shot(self, initial_position: tuple, target_position: tuple, hold_factor: float):
        # Velocidade da flecha depende do tempo que o jogador segurou o mouse
        self.speed = self.minimun_speed + (self.maximun_extra_speed * hold_factor)

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
    
    # Rotaciona a imagem baseado no vetor direção
    def rotate_image(self):
        angle_radian = atan2(self.delta_position.y, self.delta_position.x) # Define o ângulo em radianos do vetor deslocamento
        angle_degrees = -(angle_radian) * 180 / pi # Converte o ângulo para graus

        rotated_image = pygame.transform.rotate(self.base_image, angle_degrees).convert()
        rotated_image.set_colorkey((255, 255, 255))
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def calculate_speed(self):
        # Aplica a gravidade no self.dy
        self.delta_position.y += self.gravity

        return self.delta_position

    def move(self, delta_speed):
        # Acrescenta self.x_pos e self.y_pos para floats
        self.x_pos += delta_speed[0]
        self.y_pos += delta_speed[1]

        # Atualiza a posição do retângulo de fato
        self.rect.x = int(self.x_pos)
        self.rect.y = int(self.y_pos)

    def get_collided_position(self, next_position: tuple, collide_with: pygame.sprite.Group) -> tuple:
        dx, dy = next_position

        for tile in collide_with.sprites():
            # Colisão horizontal
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height): # Testa a colisão do deslocamento horizontal
                if self.delta_position.x < 0: # Caso o jogador colida com um superfície pela esquerda
                    dx = tile.rect.right - self.rect.left
                elif self.delta_position.x > 0: # Caso o jogador colida com um superfície pela direita
                    dx = tile.rect.left - self.rect.right
                else:
                    dx = 0

            # Colisão vertical
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height): # Testa a colisão do deslocamento vertical
                if self.delta_position.y < 0 and (tile.rect.bottom <= self.rect.top): # Jogador "subindo"
                    dy = (tile.rect.bottom - self.rect.top)
                if self.delta_position.y > 0 and (tile.rect.top >= self.rect.bottom): # Jogador "caindo"
                    dy = (tile.rect.top - self.rect.bottom)
                else:
                    dy = 0

        return (dx, dy) # Retorna as posições colididas com o sprite group passado como argumento

    def update(self, delta_speed):
        self.move(delta_speed)
        self.rotate_image()