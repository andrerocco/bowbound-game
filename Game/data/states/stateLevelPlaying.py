import pygame
from random import randint # Usando para o screenshake
from states.abstractState import State
from singletons.singletonAssets import Assets
import config

from utility.staticLevelMouse import LevelMouse
from utility.classeScoreController import ScoreController
from utility.classeTimer import Timer
from utility.interface.classeTextButton import TextButton

from states.stateLevelPaused import LevelPaused
from level.classeLevel import Level


class LevelPlaying(State):
    def __init__(self, game, levels_list, start_index = 0):
        ACTIONS = {'esc': False, 'restart': False,
                   'up': False, 'down': False, 'left': False, 'right': False,
                   'mouse_left': False, 'mouse_right': False}

        super().__init__(game, ACTIONS)

        self.__levels_list = levels_list
        self.__current_level_index = start_index

        self.__assets = Assets()
        self.__score_controller = ScoreController()
        self.__level_surface = pygame.Surface((0,0))
        
        self.__load_interface()
        self.__load_level(self.__current_level_index)
    
    def __load_interface(self):
        self.TIMER = TextButton(self.__assets.fonts_path['text'], 40, (255,255,255), '00:00')

    def __load_level(self, index = 0):
        current_level = self.__levels_list[index]
        self.__level = Level(current_level) # Passa a matriz que representa o nível e a superfície onde o nível será desenhado
        self.__timer = Timer()
        self.__timer_paused_status = False

    def restart_actions(self):
        self._actions = {'esc': False, 'restart': False,
                         'up': False, 'down': False, 'left': False, 'right': False,
                         'mouse_left': False, 'mouse_right': False}

    def update_actions(self, event):
        if event.type == pygame.KEYDOWN: # Inputs do teclado (soltar tecla)
            if event.key == pygame.K_ESCAPE:
                self._actions['esc'] = True
            if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                self._actions['up'] = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self._actions['down'] = True
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self._actions['left'] = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self._actions['right'] = True
            if event.key == pygame.K_r:
                self._actions['restart'] = True
                
        if event.type == pygame.KEYUP: # Inputs do teclado (soltar tecla)
            if event.key == pygame.K_ESCAPE:
                self._actions['esc'] = False
            if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                self._actions['up'] = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self._actions['down'] = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self._actions['left'] = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self._actions['right'] = False
            if event.key == pygame.K_r:
                self._actions['restart'] = False

        if event.type == pygame.MOUSEBUTTONDOWN: # Inputs do mouse (pressionar botão)
            if event.button == 1:
                self._actions['mouse_left'] = True
                self.__level.start_hold()
            if event.button == 3:
                self._actions['mouse_right'] = True
                    
        if event.type == pygame.MOUSEBUTTONUP: # Inputs do mouse (soltar botão)
            if event.button == 1:
                self._actions['mouse_left'] = False
                self.__level.end_hold()
            if event.button == 3:
                self._actions['mouse_right'] = False

    def update(self):
        # Despausa o timer se estiver pausado
        if self.__timer_paused_status:
            self.__timer_paused_status = False
            self.__timer.set_time(self.__paused_on)

        # Se o jogador pressionar ESC, entra no estado de pausa
        if self._actions['esc']:
            # Pausa o cronômetro
            self.__timer_paused_status = True
            self.__paused_on = self.__timer.get_time()
            # Muda o estado
            level_name = self.__levels_list[self.__current_level_index]['level_name']
            pause_state = LevelPaused(self._game, level_name, self.__level_surface.copy())
            pause_state.enter_state()

        # Atualiza o nível, enviando os inputs detectados
        LevelMouse.set_surface_offset((self._game.screen_width, self._game.screen_height), (self.__level.width, self.__level.height))
        self.__level.update(self._actions)

        # Confere os status do nível
        if self.__level.win_status:
            self.__timer.stop()
            level_name = self.__levels_list[self.__current_level_index]['level_name']
            self.__score_controller.add_score(level_name, self.__assets.user_name, self.__timer.stopped_time)
            self.__next_level()
        if self.__level.restart_status:
            self.__timer.reset()
            self.__level.restart_level()

    def __next_level(self):
        if self.__current_level_index + 1 >= len(self.__levels_list):
            self.exit_state()
        else:
            self.__current_level_index += 1
            self.__load_level(self.__current_level_index)

    def render(self, display_surface):
        display_surface.fill((5,5,8)) # Limpa a tela

        screen_center = display_surface.get_rect().center

        self.__level_surface = self.__level.render() # Recebe a display surface do level
        display_surface.blit(self.__level_surface, LevelMouse.get_surface_offset()) # Desenha o level
        
        # Interface
        formated_time = self.__timer.get_formated_time()  # Recebe o tempo decorrido formatado
        self.TIMER.set_text(formated_time)
        self.TIMER.render(display_surface, (screen_center[0], 30)) # Desenha o tempo decorrido

        player_arrows = self.__level.player_arrows
        try:
            for index, arrow in enumerate(self.__level.player_arrows):
                if index == 0:
                    display_surface.blit(arrow.bordered_icon_image, (12 + index*25, 12))
                else:
                    display_surface.blit(arrow.icon_image, (15 + index*25, 15))
        except:
            print("Não foi possível carregar a interface das flechas.")
