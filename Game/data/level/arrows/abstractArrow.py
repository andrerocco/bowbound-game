import pygame
from abc import ABC
from cmath import pi
from math import atan2, sin, cos, pi


class Arrow(ABC):
    def __init__(self, minimun_speed, maximun_extra_speed, gravity, image: pygame.image, icon_image: pygame.image, bordered_icon_image: pygame.image= None):
        super().__init__() # Inicia a classe ABC que define a classe como abstrata

        # Importa a imagem da flecha
        self.__base_image = image
        self.__base_image.set_colorkey((255,255,255)) # Faz com que a flecha não tenha fundo quando for rotacionada
        self.__icon_image = icon_image
        if bordered_icon_image == None:
            self.__bordered_icon_image = icon_image
        else:
            self.__bordered_icon_image = bordered_icon_image

        # Atributos de características da flecha
        self.__minimun_speed = minimun_speed
        self.__maximun_extra_speed = maximun_extra_speed
        self.__gravity = gravity

        # Atributos de status
        self.__stuck = False
    
    # Quando for atirada, inicia os atributos usados para o seu movimento
    def start_shot(self, initial_position: tuple, target_position: tuple, hold_factor: float):
        self.__stuck = False

        # Velocidade da flecha depende do tempo que o jogador segurou o mouse
        speed = self.__minimun_speed + (self.__maximun_extra_speed * hold_factor)

        # Atributos de posição
        angle_radian = atan2(target_position[1] - initial_position[1], target_position[0] - initial_position[0]) # Define o ângulo em radianos
        self.__delta_position = pygame.Vector2((cos(angle_radian) * speed), (sin(angle_radian) * speed))
        angle_degrees = -(angle_radian) * 180 / pi # Converte o ângulo para graus

        # Retângulo da flecha
        rotated_image = pygame.transform.rotate(self.__base_image, angle_degrees).convert()
        #rotated_image.set_colorkey((0,0,0))
        self.__image = rotated_image
        self.__rect = self.__image.get_rect(center=initial_position)
        
        # Posição x e y da flecha (quer será atualizada para float apartir de dx e dy)
        self.__x_pos = self.__rect.x
        self.__y_pos = self.__rect.y
    
    # Rotaciona a imagem baseado no vetor direção
    def rotate_image(self):
        angle_radian = atan2(self.__delta_position.y, self.__delta_position.x) # Define o ângulo em radianos do vetor deslocamento
        angle_degrees = -(angle_radian) * 180 / pi # Converte o ângulo para graus

        rotated_image = pygame.transform.rotate(self.__base_image, angle_degrees).convert()
        #rotated_image.set_colorkey((0,0,0))
        self.__image = rotated_image
        self.__rect = self.__image.get_rect(center=self.__rect.center)

    # Calcula o deslocamento da flecha
    def calculate_displacement(self):
        # Aplica a gravidade no self.dy
        self.__delta_position.y += self.__gravity

    # Retorna a variação de posição próprimamente colidida
    def get_collided_position(self, next_position: tuple, collide_with: pygame.sprite.Group) -> tuple: 
        dx, dy = next_position

        for tile in collide_with.sprites():
            # Colisão horizontal
            if tile.rect.colliderect(self.__rect.x + dx, self.__rect.y, self.__rect.width, self.__rect.height): # Testa a colisão do deslocamento horizontal
                self.__stuck = True

                if dx < 0: # Caso o jogador colida com um superfície pela esquerda
                    dx = tile.rect.right - self.__rect.left
                elif dx > 0: # Caso o jogador colida com um superfície pela direita
                    dx = tile.rect.left - self.__rect.right
                else:
                    dx = 0

            # Colisão vertical
            if tile.rect.colliderect(self.__rect.x, self.__rect.y + dy, self.__rect.width, self.__rect.height): # Testa a colisão do deslocamento vertical
                self.__stuck = True

                if dy < 0 and (tile.rect.bottom <= self.__rect.top): # Jogador "subindo"
                    dy = (tile.rect.bottom - self.__rect.top)
                if dy > 0 and (tile.rect.top >= self.__rect.bottom): # Jogador "caindo"
                    dy = (tile.rect.top - self.__rect.bottom)
                else:
                    dy = 0

        return (dx, dy) # Retorna as posições colididas com o sprite group passado como argumento

    # Muda a posição do retângulo da flecha
    def move(self, delta_speed):
        # Acrescenta self.x_pos e self.y_pos para floats
        self.__x_pos += delta_speed[0]
        self.__y_pos += delta_speed[1]

        # Atualiza a posição do retângulo de fato
        self.__rect.x = int(self.__x_pos)
        self.__rect.y = int(self.__y_pos)

    # Getters
    @property
    def stuck(self):
        return self.__stuck
    @property
    def gravity(self):
        return self.__gravity
    @property
    def delta_position(self):
        return self.__delta_position
    @property
    def rect(self):
        return self.__rect
    @property
    def image(self):
        return self.__image
    @property
    def icon_image(self):
        return self.__icon_image
    @property
    def bordered_icon_image(self):
        return self.__bordered_icon_image
    
    # Setters
    @stuck.setter
    def stuck(self, value: bool):
        if isinstance(value, bool):
            self.__stuck = value
        else:
            self.__stuck = True
       
    # Updater
    def update(self, collide_with):
        self.calculate_displacement()
        next_position = self.__delta_position

        next_position = self.get_collided_position(next_position, collide_with)

        self.move(next_position)
        self.rotate_image()
