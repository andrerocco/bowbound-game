from turtle import position, speed
import pygame
import config
from classeTile import Tile
from classePlayer import Player

class Level:
    def __init__(self, level_data: dict, surface):
        self.level_number = level_data['level_number']
        self.level_name = level_data['level_name']
        self.level_map_matrix = level_data['tile_map']

        # Superfície onde o nível será desenhado
        self.display_surface = surface

        # Jogador
        self.player = pygame.sprite.GroupSingle()

        # Agrupa todas as superfícies do nível atual geradas por generate_level()
        self.level_tiles = pygame.sprite.Group() 
        self.generate_level(self.level_map_matrix)

        
    def generate_level(self, level_map_matrix): # Gera o mapa baseado no nível (baseado no argumento level_map recebido na construtora)
        tile_size = config.level_tile_size

        for row_index, row in enumerate(level_map_matrix):
            for column_index, tile in enumerate(row):
                x = column_index * tile_size # Gera a posição x do tile
                y = row_index * tile_size # Gera a posição y do tile
                
                if tile == 'X':
                    tile = Tile((x, y), tile_size) # Invoca a classe Tile que cria o sprite daquele bloco
                    self.level_tiles.add(tile) # Adiciona o tile criado no atributo que agrupa os tiles
                
                if tile == 'P':
                    # Os valores de posição são ajustados pois o player é gerado com base nas coordenadas em seu midbottom
                    player_origin_x = x + (tile_size/2)
                    player_origin_y = y + (tile_size)

                    # Gera o jogador usando a classe Player e enviando a posição inicial
                    player_sprite = Player((player_origin_x, player_origin_y)) 
                    self.player.add(player_sprite)
    
    # Recebe o objeto que irá colidir, a próxima posição do objeto e o sprite group que irá ser colidido
    # Colide a próxima posição do objeto e retorna a nova posição colidida em uma tupla (collided_dx, collided_dy)
    def get_collided_position(self, object, next_position: tuple, collide_with: pygame.sprite.Group) -> tuple:
        dx, dy = next_position

        for tile in collide_with.sprites():
            # Colisão horizontal
            if tile.rect.colliderect(object.rect.x + dx, object.rect.y, object.rect.width, object.rect.height): # Testa a colisão do deslocamento horizontal
                if object.speed.x < 0: # Caso o jogador colida com um superfície pela esquerda
                    dx = tile.rect.right - object.rect.left
                elif object.speed.x > 0: # Caso o jogador colida com um superfície pela direita
                    dx = tile.rect.left - object.rect.right
                else:
                    dx = 0

            # Colisão vertical
            if tile.rect.colliderect(object.rect.x, object.rect.y + dy, object.rect.width, object.rect.height): # Testa a colisão do deslocamento vertical
                if object.speed.y < 0 and (tile.rect.bottom <= object.rect.top): # Jogador "subindo"
                    dy = (tile.rect.bottom - object.rect.top)
                    object.speed.y = 0 # Reinicia a gravidade
                if object.speed.y > 0 and (tile.rect.top >= object.rect.bottom): # Jogador "caindo"
                    dy = (tile.rect.top - object.rect.bottom)
                    object.speed.y = 0 # Reinicia a gravidade  
                    if isinstance(object, Player):
                        object.set_jumping_status(False)
                        object.set_on_ground_status(True)
                else:
                    dy = 0

        return (dx, dy) # Retorna as posições colididas com o sprite group passado como argumento


    def display_bow(self, player_position):
        player_x, player_y = player_position
        bow_x = player_x
        bow_y = player_y
        
        rotated_bow_image = self.player.sprite.bow.get_rotated_image(player_position)
        rotated_bow_rect = rotated_bow_image.get_rect(center = (bow_x , bow_y))

        self.display_surface.blit(rotated_bow_image, rotated_bow_rect)

    def run(self, event_listener):
        player = self.player.sprite

        # A variável delta_speed é uma tupla com os valores de deslocamento calculados baseados no player
        delta_speed = player.calculate_speed(event_listener)
        
        # A variável collided_delta_speed é uma tupla com os valores de deslocamento transformados a partir das colisões
        collided_delta_speed = self.get_collided_position(player, delta_speed, self.level_tiles)
        
        # Aplica o deslocamento final no jogador
        player.update(collided_delta_speed)

        # Draw
        self.player.draw(self.display_surface)
        self.display_bow(player.rect.center)
        self.level_tiles.draw(self.display_surface)