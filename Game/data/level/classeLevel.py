import pygame
import config
from time import time

from utility.staticLevelMouse import LevelMouse
from utility.classeTimer import Timer
from level.classePlayer import Player
from level.arrows.classePiercingArrow import PiercingArrow
from level.build_structures.classeTile import Tile
from level.build_structures.classeTile import Tile
from level.build_structures.classeSpike import Spike
from level.build_structures.classeTarget import Target
from level.build_structures.classeExitDoor import ExitDoor


class Level:
    def __init__(self, level_data: dict):
        self.__level_data = level_data # Dicionário com todas as informações do nível em questão
        
        self.__level_tile_map = level_data['tile_map']
        self.__level_texture_map = level_data['textures']
        self.__level_arrows = level_data['arrows'] # Lista de strings com o nome das flechas que o jogador terá no nível

        # Superfície onde o nível será desenhado
        level_width = len(self.__level_tile_map[0]) * config.level_tile_size
        level_height = len(self.__level_tile_map) * config.level_tile_size
        self.__display_surface = pygame.surface.Surface((level_width, level_height))

        # Jogador
        self.__player = pygame.sprite.GroupSingle()

        # Agrupa todas as superfícies do nível atual geradas por generate_level()
        self.__level_tiles = pygame.sprite.Group()
        # Agrupa as outras estruturas (com interação baseada em colisão)
        self.__level_spikes = pygame.sprite.Group()
        # Agrupa os alvos
        self.__level_targets = pygame.sprite.Group()
        self.__level_hit_targets = pygame.sprite.Group() # Alvos que foram acertados e estão na animação antes de serem eliminados
        # Porta de saída do nível
        self.__level_exit_door = pygame.sprite.GroupSingle()

        self.generate_level(self.__level_tile_map, self.__level_texture_map)

        # Flechas
        self.__moving_arrows = []
        self.__stuck_arrows = []

        self.__timer = Timer()

        # Status do nível
        self.__win_status = False
        self.__restart_status = False
        
        self.__start_hold = None
        self.__did_shoot = False

    def restart_level(self):
        self.__init__(self.__level_data)

    # Gera o mapa baseado no nível (baseado no argumento level_map recebido na construtora)
    def generate_level(self, tile_map, texture_map):
        tile_size = config.level_tile_size

        for row_index, row in enumerate(tile_map):
            for column_index, tile in enumerate(row):
                x = column_index * tile_size # Gera a posição x do tile
                y = row_index * tile_size # Gera a posição y do tile
                
                if tile == 'X':
                    texture_name = texture_map[row_index][column_index]
                    self.__level_tiles.add(Tile((x, y), tile_size, texture_name)) # Adiciona o tile criado no atributo que agrupa os tiles
                
                if tile == 'A':
                    self.__level_spikes.add(Spike((x, y), 48)) # Adiciona o spike criado no atributo que agrupa os spikes
                
                if tile == 'O':
                    self.__level_targets.add(Target((x, y))) # Adiciona o alvo criado no atributo que agrupa os alvos

                if tile == 'D':
                    self.__level_exit_door.add(ExitDoor((x, y), 48)) # Cria a porta de saída

                if tile == 'P':
                    # Os valores de posição são ajustados pois o player é gerado com base nas coordenadas em seu midbottom
                    player_origin_x = x + (tile_size/2)
                    player_origin_y = y + (tile_size)

                    # Gera o jogador usando a classe Player e enviando a posição inicial
                    player_sprite = Player((player_origin_x, player_origin_y), self.__level_arrows)
                    self.__player.add(player_sprite)

    def __update_player(self, player, actions):
        # Gera uma tupla com os valores de deslocamento calculados baseados no player
        delta_speed = player.calculate_speed(actions)
        # A parte da tupla delta_speed, calcula uma nova tupla para os valores de deslocamento transformados a partir das colisões
        collided_delta_speed = player.get_collided_position(delta_speed, self.__level_tiles) 
        # Aplica o deslocamento final no jogador
        player.update(collided_delta_speed)

    def __handle_shoot(self, player):
        self.__did_shoot = False

        # Calcula o fator de hold
        mouse_hold_time = self.__end_hold - self.__start_hold # Tempo que o mouse ficou pressionado
        if mouse_hold_time >= 1:
            hold_factor = 1
        else: hold_factor = mouse_hold_time / 1 # Vai ser um float que varia de 0 até 1

        # Tenta atirar
        try: # Tenta pegar uma flecha do arco (irá suceder se o arco tiver flechas)
            arrow = player.gun.pop_first_arrow()

        except: # Caso o jogador não tenha uma flecha no arco, ele não poderá atirar
            # Fazer efeito sonoro ou algo do gênero
            pass
            
        else: # Caso o try tenha sucedido (o jogador tenha atirado)
            target_position = LevelMouse.mouse_pos() # Pega a posição do mouse

            arrow.start_shot(player.rect.center, target_position, hold_factor) # Inicializa os atributos de posição da flecha
            self.__moving_arrows.append(arrow) # Adiciona a flecha na lista de flechas do level

            player.knockback(target_position) # Aplica o knockback no jogador

    def __update_arrows(self):
        for arrow in self.__moving_arrows:
            # Aplica o deslocamento na flecha e trata a colisão da flecha
            # Possívelmente irá alterar o atributo stuck da flecha
            arrow.update(self.__level_tiles)

            if arrow.stuck: # Se durante o update a flecha foi definida como stuck = True
                self.__stuck_arrows.append(self.__moving_arrows.pop(self.__moving_arrows.index(arrow)))
            
            # Colide a flecha com as targets
            for target in self.__level_targets:
                if arrow.rect.colliderect(target.rect):
                    self.__level_targets.remove(target)
                    self.__level_hit_targets.add(target)
                    if isinstance(arrow, PiercingArrow):
                        pass
                    else:
                        # Fix provisório de um bug "ValueError: list.remove(x): x not in list"
                        try:
                            self.__moving_arrows.remove(arrow)
                        except ValueError:
                            if arrow in self.__stuck_arrows:
                                self.__stuck_arrows.remove(arrow)

    def __handle_stuck_arrows(self, player: pygame.sprite, stuck_arrows: list):
        for arrow in stuck_arrows:
            # Se o player colidir com alguma flecha remove a flecha das flechas presas e adiciona no player
            if arrow.rect.colliderect(player.rect):
                arrow.stuck = False
                stuck_arrows.remove(arrow)
                player.gun.add_stuck_arrow(arrow)

    def __handle_spike_collisions(self, player):
        for spike in self.__level_spikes:
            if spike.collided(player):
                self.__restart_status = True

    def __check_exit_door(self, player):
        exit_door = self.__level_exit_door.sprite

        # Confere se a porta está fechada e se não há alvos restantes
        if not exit_door.is_unlocked() and len(self.__level_targets) == 0:
            exit_door.unlock()

        if exit_door.is_unlocked() and exit_door.collided(player):
            self.__win_status = True
            self.__timer.stop()
    
    def __display_gun(self, player_position):
        player_x, player_y = player_position
        gun_x = player_x
        gun_y = player_y
        
        rotated_gun_image = self.__player.sprite.gun.get_rotated_image(player_position, LevelMouse.mouse_pos())
        rotated_gun_rect = rotated_gun_image.get_rect(center = (gun_x , gun_y - 3))

        self.__display_surface.blit(rotated_gun_image, rotated_gun_rect)

    # Retorna uma surperfície com as dimensões do nível que contém o nível renderizado
    def update(self, actions):
        # Atualiza o player
        player = self.__player.sprite
        self.__update_player(player, actions)

        # Detecta o tiro
        if self.__did_shoot:
            self.__handle_shoot(player)

        # Atualiza as flechas e (possívelmente) as targets
        self.__update_arrows()
        self.__handle_stuck_arrows(player, self.__stuck_arrows) # MUDAR ##########
        self.__level_hit_targets.update() # Chama a animação para os alvos atingidos

        # Trata possíveis colisões do jogador com espinhos
        self.__handle_spike_collisions(player)

        # Trata ações da porta de saída
        self.__check_exit_door(player)

        if actions['restart']:
            self.__restart_status = True
        
    def render(self) -> pygame.Surface:
        self.__display_surface.fill((15, 15, 15)) # Limpa a surface do nível

        player = self.__player.sprite

        # Estruturas do nível
        self.__level_tiles.draw(self.__display_surface)
        self.__level_spikes.draw(self.__display_surface)
        self.__level_exit_door.draw(self.__display_surface)
        # Alvos
        self.__level_targets.draw(self.__display_surface)
        self.__level_hit_targets.draw(self.__display_surface)
        # Jogador e flecha
        self.__player.draw(self.__display_surface)
        self.__display_gun(player.rect.center)
        # Arrows
        for arrow in self.__stuck_arrows:
            self.__display_surface.blit(arrow.image, arrow.rect)
        for arrow in self.__moving_arrows:
            self.__display_surface.blit(arrow.image, arrow.rect)
            
        return self.__display_surface

    # Getters
    @property
    def display_surface(self):
        return self.__display_surface
    @property
    def width(self):
        return self.__display_surface.get_width()
    @property
    def height(self):
        return self.__display_surface.get_height()
    @property
    def win_status(self):
        return self.__win_status
    @property
    def restart_status(self):
        return self.__restart_status

    @property
    def timer(self):
        return self.__timer
    @property
    def player_arrows(self):
        return self.__player.sprite.arrows

    # Setters
    def start_hold(self):
        self.__start_hold = time()
    def end_hold(self):
        if self.__start_hold is not None:
            self.__end_hold = time()
            self.__did_shoot = True
