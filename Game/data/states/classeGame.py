import os, time, pygame

from singletons.singletonAssets import Assets
from states.abstractState import State

from utility.staticLevelMouse import Framerate
from states.stateInputName import InputName


class Game():
    def __init__(self):
        pygame.init()

        # Configurações da janela
        self.__fullscreen = False
        self.__monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.__initial_screen_width = int(self.__monitor_size[0] * 0.95)
        self.__initial_screen_height = int(self.__monitor_size[1] * 0.80)
        self.__screen = pygame.display.set_mode((self.__initial_screen_width, self.__initial_screen_height), pygame.RESIZABLE)

        pygame.display.set_caption("Bowbound")

        # Configurações da superfície de display
        self.__display_surface = pygame.Surface((self.__initial_screen_width, self.__initial_screen_height))

        # Configurações do jogo
        self.__running, self.__playing = True, True
        self.__prev_time = 0
        self.__clock = pygame.time.Clock()
        self.__state_stack = []

        # Carrega o jogo
        self.__load_assets() # Carrega os assets
        self.__load_states()

    def __load_assets(self):
        Assets().load_assets() # Inicializa o singleton de assets
        try:
            pygame.display.set_icon(Assets().interface['game-icon'])
        except:
            print("O ícone do jogo não pode ser carregado")
    
    def __load_states(self):
        self.__input_name = InputName(self)
        self.__state_stack.append(self.__input_name)

    def run(self):
        while self.__playing:
            self.__get_events()
            self.__update()
            self.__render()
            self.__set_dt()
            
            self.__clock.tick(60) # Limita o FPS

    def __get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                self.__playing = False
            
            if event.type == pygame.VIDEORESIZE:
                self.__screen_resize()

            if event.type == pygame.KEYDOWN: # Inputs do teclado (pressionar tecla)
                if event.key == pygame.K_F11:
                    self.__fullscreen = not self.__fullscreen
                    if self.__fullscreen:
                        pygame.display.quit()
                        self.__screen = pygame.display.set_mode(self.__monitor_size, pygame.FULLSCREEN)
                        pygame.display.init()
                    else:
                        pygame.display.quit()
                        self.__screen = pygame.display.set_mode((self.__initial_screen_width, self.__initial_screen_height), pygame.RESIZABLE)
                        pygame.display.init()
                    self.__screen_resize()

            self.__update_state_actions(event)

    def __update_state_actions(self, event):
        self.__state_stack[-1].update_actions(event)

    def __update(self):
        self.__state_stack[-1].update()

    def __render(self):
        self.__state_stack[-1].render(self.__display_surface) # Renderiza a state atual
        self.__screen.blit(self.__display_surface, (0, 0))
        pygame.display.flip()

    def __set_dt(self):
        now = time.time()
        Framerate.set_dt(now - self.__prev_time) # Define o dt para ser usado globalmente
        self.__prev_time = now

    def __screen_resize(self):
        # Muda o tamanho da superfície de display
        self.__display_surface = pygame.Surface((self.__screen.get_width(), self.__screen.get_height()))

    # Métodos que alteram a state stack
    def append_state(self, state: State):
        self.__reset_state_actions()
        self.__state_stack.append(state)

    def pop_state(self):
        self.__state_stack.pop()

    def __reset_state_actions(self):
        self.__state_stack[-1].restart_actions()

    # Getters
    @property
    def state_stack(self):
        return self.__state_stack
    @property
    def screen_width(self):
        return self.__screen.get_width()
    @property
    def screen_height(self):
        return self.__screen.get_height()
    @property
    def display_surface(self):
        return self.__display_surface
    @property
    def state_stack(self):
        return self.__state_stack
    
    # Setters
    @display_surface.setter
    def display_surface(self, display_surface):
        self.__display_surface = display_surface
