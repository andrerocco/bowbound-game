import pygame
from singletons.singletonAssets import Assets
from level.classeCrossbow import Crossbow


class Player(pygame.sprite.Sprite):
    def __init__(self, position, arrows):
        super().__init__()

        # Carrega as imagens do jogador
        self.__images = Assets().player

        # Atributos padrões
        self.__image = self.__images["idle"][0]
        self.__rect = self.__image.get_rect(midbottom=position)

        # Mudanças de posição
        self.__precise_rect_position_x = self.__rect.x
        
        # Velocidades
        self.__delta_position = pygame.Vector2(0, 0)

        self.__knockback_speed = pygame.Vector2(0, 0)
        self.__walking_speed = 0
        self.__max_walking_speed = 5

        # Acelerações
        self.__gravity = 0.45
        self.__acceleration = pygame.Vector2(0, self.__gravity)
        self.__ground_friction = 0.75 # Desaceleração do chão em porcentagem
        self.__air_friction = 0.98 # Desaceleração do ar em porcentagem
        
        # Forças
        self.__input_strength = 0.6 # Altera a força do input do jogador
        self.__knockback_strength = 15 # Altera a força do knockback
        self.__jump_strength = 7 # Altera a força do pulo

        # Atributos de input
        self.__thrust = 0

        # Atributos de estado
        self.__jumping_status = False
        self.__on_ground_status = True
        self.__input_right_status = True # Utilizado para definir a direção da textura do jogador

        # Arco
        self.__gun = Crossbow(self.__rect.center, arrows)

        # Animação
        self.__animation_status = "idle"
        self.__animation_speed = 0.2
        self.__frame_index = 0

    def __get_animation_status(self, delta_speed, on_ground_status) -> str:
        if on_ground_status == False:
            if delta_speed[1] <= 0:
                return "jump"
            else:
                return "fall"
        if int(delta_speed[0]) != 0:
            return "run"
        else:
            return "idle"

    def __update_animation(self):
        frames = self.__images[self.__animation_status]

        self.__frame_index += self.__animation_speed # Fazer a conversão para inteiro nesse ponto ???????????
        if self.__frame_index >= len(frames):
            self.__frame_index = 0
        
        image = frames[int(self.__frame_index)]
        if self.__input_right_status == True:
            self.__image = image
        else:
            self.__image = pygame.transform.flip(image, True, False) # Flipa a imagem no eixo x

    """ MÉTODOS INTERNOS DE MOVIMENTAÇÃO """
    def __jump(self):
        self.__delta_position.y = -self.__jump_strength
        self.__jumping_status = True
        self.__on_ground_status = False

    def __movement_input(self, actions):
        # Movimento horizontal
        if (actions["right"] and actions["left"]) or (not actions["right"] and not actions["left"]):
            self.__thrust = 0
        elif actions['right']:
            self.__thrust = 1
            self.__input_right_status = True
        elif actions['left']:
            self.__thrust = -1
            self.__input_right_status = False
        
        # Se o jogador não estiver pressionando esquerda ou direita
        if not actions['right'] and not actions['left']:
            self.__thrust = 0

        self.__acceleration.x = (self.__input_strength * self.__thrust)

        # Movimento vertical
        if actions['up'] and self.__jumping_status is False:
            self.__jump()

    def __apply_accceleration(self):
        # Se a velocidade for acima se self.__max_walking_speed (ocorre pelo knockback), o uso de input não fará o jogador ganhar mais aceleração
        # Se a velocidade for abaixo de self.__max_walking_speed, o uso de input fará o jogador ganhar aceleração e essa será limitada por self.__max_walking_speed
        if self.__thrust == 1:
            if self.__delta_position.x < self.__max_walking_speed:
                self.__delta_position.x = max(self.__delta_position.x, min(self.__delta_position.x + self.__acceleration.x, self.__max_walking_speed))
        elif self.__thrust == -1:
            if self.__delta_position.x > -self.__max_walking_speed:
                self.__delta_position.x = min(self.__delta_position.x, max(self.__delta_position.x + self.__acceleration.x, -self.__max_walking_speed))

        # Aplica a aceleração da gravidade
        self.__delta_position.y += self.__acceleration.y

    def __apply_friction(self):
        if self.__on_ground_status and self.__thrust == 0:
            self.__delta_position.x = int(self.__delta_position.x * self.__ground_friction * 1000)/1000 # Arredonda para 4 pontos de precisão
        elif self.__on_ground_status and abs(self.__delta_position.x) > self.__max_walking_speed:
            self.__delta_position.x = int(self.__delta_position.x * self.__ground_friction * 1000)/1000 # Arredonda para 4 pontos de precisão

        if not self.__on_ground_status:
            self.__delta_position.x = int(self.__delta_position.x * self.__air_friction * 1000)/1000 # Arredonda para 4 pontos de precisão

    def __move_player(self, delta_speed):
        dx, dy = delta_speed

        # Movimento x
        self.__precise_rect_position_x += dx # A posição precisa será float
        self.__rect.x = int(self.__precise_rect_position_x) # A posição recebida pelo retângulo precisa ser inteira para posicionar o pixel

        # Movimento y
        self.__rect.y += dy


    """ MÉTODOS DE INTERFACE """
    def calculate_speed(self, actions):
        # Aplica a aceleração do input
        self.__movement_input(actions) # Muda os valores de aceleração
        self.__apply_accceleration() # Aplica a aceleração ao vetor de velocidade

        # Aplica a fricção na aceleração horizontal
        self.__apply_friction()

        return self.__delta_position
    
    def knockback(self, target_position, hold_factor: float = 1):
        self.__on_ground_status = False

        # Calcula a direção do knockback
        direction = pygame.Vector2(target_position) - pygame.Vector2(self.rect.center)
        direction = direction.normalize()

        # Aplica o knockback
        knockback_factor = self.__knockback_strength * hold_factor
        self.__delta_position = -(direction * knockback_factor)

    def get_collided_position(self, next_position: tuple, collide_with: pygame.sprite.Group) -> tuple:
        # Colide a próxima posição do objeto e retorna a nova posição colidida em uma tupla (collided_dx, collided_dy)

        dx, dy = next_position

        for tile in collide_with.sprites():
            # Colisão horizontal
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height): # Testa a colisão do deslocamento horizontal
                if dx > 0: # Caso o jogador colida com um superfície pela direita
                    dx = (tile.rect.left - self.rect.right)
                elif dx < 0: # Caso o jogador colida com um superfície pela esquerda
                    dx = (tile.rect.right - self.rect.left)
                else:
                    dx = 0

            # Colisão vertical
            if tile.rect.colliderect(self.__rect.x, self.__rect.y + dy, self.__rect.width, self.__rect.height): # Testa a colisão do deslocamento vertical
                if dy < 0 and (tile.rect.bottom <= self.__rect.top): # Jogador "subindo"
                    dy = (tile.rect.bottom - self.__rect.top)
                    
                    self.__delta_position.y = 0 # Reinicia a gravidade
                if dy > 0 and (tile.rect.top >= self.__rect.bottom): # Jogador "caindo"
                    dy = (tile.rect.top - self.__rect.bottom)
                    
                    self.__delta_position.y = 0 # Reinicia a gravidade
                    self.set_jumping_status(False) # Define o status de pulo como falso
                    self.set_on_ground_status(True) # Define o status de estar no chão como verdadeiro
                else:
                    dy = 0

        return (dx, dy) # Retorna as posições colididas com o sprite group passado como argumento

    def update(self, delta_speed): # Calcula o movimento baseado nos inputs
        self.__animation_status = self.__get_animation_status(delta_speed, self.__on_ground_status)
        self.__update_animation()
        self.__move_player(delta_speed) # Atualiza a posição do player
    

    # Setters
    def set_on_ground_status(self, status: bool):
        self.__on_ground_status = status
    def set_jumping_status(self, status: bool):
        self.__jumping_status = status

    # Getters
    @property
    def image(self):
        return self.__image
    @property
    def rect(self):
        return self.__rect
    @property
    def gun(self):
        return self.__gun
    @property
    def thrust(self):
        return self.__thrust
    @property
    def arrows(self):
        return self.__gun.arrows