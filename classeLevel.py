import pygame
import config
from time import time
from classeTile import Tile
from classePlayer import Player
#from abstractArrow import Arrow
#from classeStandartArrow import StandartArrow
from classeTimer import Timer

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

        # Flechas
        self.moving_arrows = []
        self.stuck_arrows = []

        self.timer = Timer()

    # Gera o mapa baseado no nível (baseado no argumento level_map recebido na construtora)
    def generate_level(self, level_map_matrix):
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

    def display_bow(self, player_position):
        player_x, player_y = player_position
        bow_x = player_x
        bow_y = player_y
        
        rotated_bow_image = self.player.sprite.bow.get_rotated_image(player_position)
        rotated_bow_rect = rotated_bow_image.get_rect(center = (bow_x , bow_y))

        self.display_surface.blit(rotated_bow_image, rotated_bow_rect)

    def player_shoot(self, player: Player, hold_factor: float):
        try: # Tenta pegar uma flecha do arco (irá suceder se o arco tiver flechas)
            arrow = self.player.sprite.bow.pop_first_arrow()
        
        except: # Caso o jogador não tenha uma flecha no arco, ele não poderá atirar
            # Fazer efeito sonoro ou algo do gênero
            pass
        
        else: # Caso o try tenha sucedido
            target_position = pygame.mouse.get_pos() # Pega a posição do mouse

            arrow.start_shot(player.rect.center, target_position, hold_factor) # Inicializa os atributos de posição da flecha
            self.moving_arrows.append(arrow) # Adiciona a flecha na lista de flechas do level

            player.knockback(target_position) # Aplica o knockback no jogador

    def get_arrow_stuck(self, player_position):
        for arrow in self.stuck_arrows:
            # Se o player colidir com alguma flecha remove a flecha das flechas presas e adiciona no player
            if arrow.rect.colliderect(player_position):
                self.stuck_arrows.remove(arrow)
                self.player.sprite.bow.add_stuck_arrow(arrow)

    def display_arrow_quantity(self, surface, player):
        font = pygame.font.SysFont('arial', 30, True, False)  # Edita a fonte
        text = font.render(f'Quantidade de flechas: {len(player.bow.arrows)}', True, (0, 0, 0))  # Edita o texto
        surface.blit(text, (10, 10))  # Mostra na tela

    def display_timer(self, surface):
        font = pygame.font.SysFont('arial', 30, True, False)  # Edita a fonte

        time_seconds = self.timer.get_time_from_start()
        minutes, seconds = divmod(time_seconds, 60)
        formated_time = "{:0>2}:{:05.2f}".format(int(minutes),seconds)

        text = font.render(f'Tempo: {formated_time}', True, (0, 0, 0))  # Edita o texto
        surface.blit(text, (400, 10))  # Mostra na tela

    def run(self, event_listener):
        player = self.player.sprite

        # A variável delta_speed é uma tupla com os valores de deslocamento calculados baseados no player
        delta_speed = player.calculate_speed()
        
        # A variável collided_delta_speed é uma tupla com os valores de deslocamento transformados a partir das colisões
        collided_delta_speed = player.get_collided_position(delta_speed, self.level_tiles)
        
        # Aplica o deslocamento final no jogador
        player.update(collided_delta_speed)
        
        """ UPDATE DAS FLECHAS ------ ORGANIZAR DEPOIS """
        for event in event_listener:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Se o botão esquerdo do mouse for pressionado
                self.start_hold = time()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Quando o botão esquerdo do mouse for soltado
                end_hold = time()

                self.hold_time = end_hold - self.start_hold
                if self.hold_time >= 1:
                    hold_factor = 1
                else:
                    hold_factor = self.hold_time / 1 # Vai ser um float que varia de 0 até 1
                
                self.player_shoot(player, hold_factor)

        for arrow in self.moving_arrows:
            # A variável delta_speed é uma tupla com os valores do proximo deslocamento
            delta_speed = arrow.calculate_speed()

            # A variável collided_delta_speed é uma tupla com os valores de deslocamento transformados a partir das colisões
            collided_delta_speed = arrow.get_collided_position(delta_speed, self.level_tiles)
            
            # Atualiza a posição do arrow com o novo deslocamento colidido 
            arrow.update(collided_delta_speed)

            if delta_speed != collided_delta_speed:
                self.stuck_arrows.append(self.moving_arrows.pop(self.moving_arrows.index(arrow)))

            self.display_surface.blit(arrow.image, arrow.rect)

        for arrow in self.stuck_arrows:
            self.display_surface.blit(arrow.image, arrow.rect)

        self.get_arrow_stuck(player.rect)
        """ FIM DO UPDATE DAS FLECHAS """

        # Draw
        self.player.draw(self.display_surface)
        self.display_bow(player.rect.center)
        self.level_tiles.draw(self.display_surface)
        self.display_arrow_quantity(self.display_surface, player) # Mostra o número de flechas no arco
        self.display_timer(self.display_surface) # Mostra o tempo na tela