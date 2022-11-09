import pygame
from classeBow import Bow

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        # Atributos padrões
        self.__image = pygame.Surface((27,54))
        self.__image.fill('red')
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
        self.__jump_strength = 6 # Altera a força do pulo

        # Atributos de input
        self.__thrust = 0

        # Atributos de estado
        self.__jumping_status = False
        self.__on_ground_status = True
        self.__facing_right_status = True # Utilizado para definir a direção da textura do jogador

        # Arco
        self.__bow = Bow(self.__rect.center)

    """ MOVIMENTAÇÃO """

    def jump(self):
        self.__delta_position.y = -self.__jump_strength
        self.__jumping_status = True
        self.__on_ground_status = False

    def movement_input(self):
        keys = pygame.key.get_pressed()

        # Movimento horizontal
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.__thrust = 1
            self.__facing_right_status = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.__thrust = -1
            self.__facing_right_status = False
        
        # Se o jogador não estiver pressionando esquerda ou direita
        if not (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.__thrust = 0

        self.__acceleration.x = (self.__input_strength * self.__thrust)

        # Movimento vertical
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.__jumping_status is False:
            self.jump()

    def apply_accceleration(self):
        temp_speed_result = self.__delta_position.x + self.__acceleration.x

        # Se a velocidade for maior que a máxima de caminhada e o jogador estiver pressionando a tecla de movimento na mesma direção, não entra na condição
        if not (temp_speed_result > self.__max_walking_speed and self.__thrust == 1) and not (temp_speed_result < -self.__max_walking_speed and self.thrust == -1):
            self.__delta_position.x += self.__acceleration.x
        
        # Aplica a aceleração da gravidade
        self.__delta_position.y += self.__acceleration.y

    def apply_friction(self):
        if self.__on_ground_status and self.__thrust == 0:
            self.__delta_position.x = int(self.__delta_position.x * self.__ground_friction * 1000)/1000 # Arredonda para 4 pontos de precisão
        elif self.__on_ground_status and abs(self.__delta_position.x) > self.__max_walking_speed:
            self.__delta_position.x = int(self.__delta_position.x * self.__ground_friction * 1000)/1000 # Arredonda para 4 pontos de precisão

        if not self.__on_ground_status:
            self.__delta_position.x = int(self.__delta_position.x * self.__air_friction * 1000)/1000 # Arredonda para 4 pontos de precisão

    def knockback(self, target_position, hold_factor: float = 1):
        self.__on_ground_status = False

        # Calcula a direção do knockback
        direction = pygame.Vector2(target_position) - pygame.Vector2(self.rect.center)
        direction = direction.normalize()

        # Aplica o knockback
        knockback_factor = self.__knockback_strength * hold_factor
        self.__delta_position = -(direction * knockback_factor)

    def calculate_speed(self):
        # Aplica a aceleração do input
        self.movement_input() # Muda os valores de aceleração
        self.apply_accceleration() # Aplica a aceleração ao vetor de velocidade

        # Aplica a fricção na aceleração horizontal
        self.apply_friction()

        return self.__delta_position

    def move(self, delta_speed):
        dx, dy = delta_speed

        # Movimento x
        self.__precise_rect_position_x += dx # A posição precisa será float
        self.__rect.x = int(self.__precise_rect_position_x) # A posição recebida pelo retângulo precisa ser inteira para posicionar o pixel

        # Movimento y
        self.__rect.y += dy

    """ COLISÃO """
    # Colide a próxima posição do objeto e retorna a nova posição colidida em uma tupla (collided_dx, collided_dy)
    def get_collided_position(self, next_position: tuple, collide_with: pygame.sprite.Group) -> tuple:
        dx, dy = next_position

        for tile in collide_with.sprites():
            # Colisão horizontal
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height): # Testa a colisão do deslocamento horizontal
                if self.__delta_position.x < 0: # Caso o jogador colida com um superfície pela esquerda
                    dx = tile.rect.right - self.rect.left
                elif self.__delta_position.x > 0: # Caso o jogador colida com um superfície pela direita
                    dx = tile.rect.left - self.rect.right
                else:
                    dx = 0

            # Colisão vertical
            if tile.rect.colliderect(self.__rect.x, self.__rect.y + dy, self.__rect.width, self.__rect.height): # Testa a colisão do deslocamento vertical
                if self.__delta_position.y < 0 and (tile.rect.bottom <= self.__rect.top): # Jogador "subindo"
                    dy = (tile.rect.bottom - self.__rect.top)
                    
                    self.__delta_position.y = 0 # Reinicia a gravidade
                if self.__delta_position.y > 0 and (tile.rect.top >= self.__rect.bottom): # Jogador "caindo"
                    dy = (tile.rect.top - self.__rect.bottom)
                    
                    self.__delta_position.y = 0 # Reinicia a gravidade
                    self.set_jumping_status(False) # Define o status de pulo como falso
                    self.set_on_ground_status(True) # Define o status de estar no chão como verdadeiro
                else:
                    dy = 0

        return (dx, dy) # Retorna as posições colididas com o sprite group passado como argumento

    """ ATUALIZAÇÃO """

    def update(self, delta_speed): # Calcula o movimento baseado nos inputs
        self.move(delta_speed) # Atualiza a posição do player
    

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
    def bow(self):
        return self.__bow
    @property
    def thrust(self):
        return self.__thrust