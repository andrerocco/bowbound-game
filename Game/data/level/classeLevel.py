import pygame
import config
from time import time

from singletonConstants import Constants
from classeTimer import Timer
from level.classePlayer import Player
from level.build_structures.classeTile import Tile
from level.build_structures.classeTile import Tile
from level.build_structures.classeSpike import Spike
from level.build_structures.classeTarget import Target
from level.build_structures.classeExitDoor import ExitDoor


class Level:
    def __init__(self, level_data: dict):
        self.__level_data = level_data
        self.__level_map_matrix = level_data['tile_map']
        self.__constants = Constants()

        # Superfície onde o nível será desenhado
        level_width = len(self.__level_map_matrix[0]) * config.level_tile_size
        level_height = len(self.__level_map_matrix) * config.level_tile_size
        self.__display_surface = pygame.surface.Surface((level_width, level_height))

        # Jogador
        self.__player = pygame.sprite.GroupSingle()

        # Agrupa todas as superfícies do nível atual geradas por generate_level()
        self.__level_tiles = pygame.sprite.Group()
        # Agrupa as outras estruturas (com interação baseada em colisão)
        self.__level_spikes = pygame.sprite.Group()
        # Agrupa os alvos
        self.__level_targets = pygame.sprite.Group()
        # Porta de saída do nível
        self.__level_exit_door = pygame.sprite.GroupSingle()

        self.generate_level(self.__level_map_matrix)

        # Flechas
        self.__moving_arrows = []
        self.__stuck_arrows = []

        self.__timer = Timer()

        # Status do nível
        self.__win_status = False

    def restart_level(self):
        self.__init__(self.__level_data)

    # Gera o mapa baseado no nível (baseado no argumento level_map recebido na construtora)
    def generate_level(self, level_map_matrix):
        tile_size = config.level_tile_size

        for row_index, row in enumerate(level_map_matrix):
            for column_index, tile in enumerate(row):
                x = column_index * tile_size # Gera a posição x do tile
                y = row_index * tile_size # Gera a posição y do tile
                
                if tile == 'X':
                    self.__level_tiles.add(Tile((x, y), tile_size)) # Adiciona o tile criado no atributo que agrupa os tiles
                
                if tile == 'A':
                    self.__level_spikes.add(Spike((x, y), 48, 48)) # Adiciona o spike criado no atributo que agrupa os spikes
                
                if tile == 'O':
                    self.__level_targets.add(Target((x + (48-30)/2, y + (48-30)/2), 30, 30)) # Adiciona o alvo criado no atributo que agrupa os alvos

                if tile == 'D':
                    self.__level_exit_door.add(ExitDoor((x, y), 48, 48)) # Cria a porta de saída

                if tile == 'P':
                    # Os valores de posição são ajustados pois o player é gerado com base nas coordenadas em seu midbottom
                    player_origin_x = x + (tile_size/2)
                    player_origin_y = y + (tile_size)

                    # Gera o jogador usando a classe Player e enviando a posição inicial
                    player_sprite = Player((player_origin_x, player_origin_y)) 
                    self.__player.add(player_sprite)

    def display_bow(self, player_position):
        player_x, player_y = player_position
        bow_x = player_x
        bow_y = player_y
        
        rotated_bow_image = self.__player.sprite.bow.get_rotated_image(player_position, self.constants.mouse_pos)
        rotated_bow_rect = rotated_bow_image.get_rect(center = (bow_x , bow_y))

        self.__display_surface.blit(rotated_bow_image, rotated_bow_rect)

    def player_shoot(self, player: Player, hold_factor: float):
        try: # Tenta pegar uma flecha do arco (irá suceder se o arco tiver flechas)
            arrow = self.__player.sprite.bow.pop_first_arrow()
        
        except: # Caso o jogador não tenha uma flecha no arco, ele não poderá atirar
            # Fazer efeito sonoro ou algo do gênero
            pass
        
        else: # Caso o try tenha sucedido
            target_position = self.constants.mouse_pos # Pega a posição do mouse

            arrow.start_shot(player.rect.center, target_position, hold_factor) # Inicializa os atributos de posição da flecha
            self.__moving_arrows.append(arrow) # Adiciona a flecha na lista de flechas do level

            player.knockback(target_position) # Aplica o knockback no jogador

    def get_arrow_stuck(self, player_position):
        for arrow in self.__stuck_arrows:
            # Se o player colidir com alguma flecha remove a flecha das flechas presas e adiciona no player
            if arrow.rect.colliderect(player_position):
                arrow.stuck = False
                self.__stuck_arrows.remove(arrow)
                self.__player.sprite.bow.add_stuck_arrow(arrow)

    def display_arrow_quantity(self, surface, player):
        font = pygame.font.SysFont('arial', 30, True, False)  # Edita a fonte
        text = font.render(f'Quantidade de flechas: {len(player.bow.arrows)}', True, (0, 0, 0))  # Edita o texto
        surface.blit(text, (10, 10))  # Mostra na tela

    def display_timer(self, surface):
        font = pygame.font.SysFont('arial', 30, True, False)  # Edita a fonte

        time_seconds = self.__timer.get_time_from_start()
        minutes, seconds = divmod(time_seconds, 60)
        formated_time = "{:0>2}:{:05.2f}".format(int(minutes),seconds)

        text = font.render(f'Tempo: {formated_time}', True, (0, 0, 0))  # Edita o texto
        surface.blit(text, (400, 10))  # Mostra na tela


    def run(self, event_listener):

        """ DETECÇÃO DE INPUT PARA O NÍVEL (atualizar quando for feito a organização dos inputs) """
        if pygame.key.get_pressed()[pygame.K_r]:
            self.restart_level()
        """ FIM DA DETECÇÃO DE INPUT PARA O NÍVEL """

        player = self.__player.sprite

        delta_speed = player.calculate_speed() # É uma tupla com os valores de deslocamento calculados baseados no player
        collided_delta_speed = player.get_collided_position(delta_speed, self.__level_tiles) # É uma tupla com os valores de deslocamento transformados a partir das colisões
        
        player.update(collided_delta_speed) # Aplica o deslocamento final no jogador


        """ UPDATE DAS FLECHAS ------ ORGANIZAR DEPOIS """
        for event in event_listener:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Se o botão esquerdo do mouse for pressionado
                self.__start_hold = time()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Quando o botão esquerdo do mouse for soltado
                end_hold = time()

                self.__hold_time = end_hold - self.__start_hold
                if self.__hold_time >= 1:
                    hold_factor = 1
                else:
                    hold_factor = self.__hold_time / 1 # Vai ser um float que varia de 0 até 1
                
                self.player_shoot(player, hold_factor)

        for arrow in self.__moving_arrows:
            arrow.update(self.__level_tiles) # Aplica o deslocamento na flecha

            if arrow.stuck:
                self.__stuck_arrows.append(self.__moving_arrows.pop(self.__moving_arrows.index(arrow)))

            self.__display_surface.blit(arrow.image, arrow.rect)

            """ TAGET """
            for target in self.__level_targets:
                if arrow.rect.colliderect(target.rect):
                    target.kill()
                    self.__moving_arrows.remove(arrow)

                    if len(self.__level_targets) == 0:
                        self.__level_exit_door.sprite.unlock()
                        print(self.__level_exit_door.sprite.is_unlocked())

                        print("PORTA ABERTA")

        for arrow in self.__stuck_arrows:
            self.__display_surface.blit(arrow.image, arrow.rect)

        self.get_arrow_stuck(player.rect)
        """ FIM DO UPDATE DAS FLECHAS """



        """ SPIKES - ORGANIZAR DEPOIS """
        for spike in self.__level_spikes:
            if spike.collided(player):
                print("MORREU")
                self.restart_level()
        """ FIM DOS SPIKES """

        
        """ PORTA DE SAIDA - ORGANIZAR DEPOIS """
        if self.__level_exit_door.sprite.is_unlocked() and self.__level_exit_door.sprite.collided(player):
            print("SAIU DO LEVEL")
            self.__win_status = True
        """ FIM DA PORTA DE SAIDA """
        

        # Draw
        self.__player.draw(self.__display_surface)
        self.display_bow(player.rect.center)
        self.__level_tiles.draw(self.__display_surface)
        self.__level_spikes.draw(self.__display_surface)
        self.__level_targets.draw(self.__display_surface)
        self.__level_exit_door.draw(self.__display_surface)
        self.display_arrow_quantity(self.__display_surface, player) # Mostra o número de flechas no arco
        self.display_timer(self.__display_surface) # Mostra o tempo na tela

        # Retorna a superfície onde com os gráficos desenhados
        return self.__display_surface

    
    # Getters
    @property
    def constants(self):
        return self.__constants
    @property
    def display_surface(self):
        return self.__display_surface