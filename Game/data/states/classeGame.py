import os, time, pygame

from Settings import Settings


class Game():
    def __init__(self):
        pygame.init()

        # Configurações da janela
        self.__fullscreen = False
        self.__monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.__screen_width = int(self.__monitor_size[0] * 0.95)
        self.__screen_height = int(self.__monitor_size[1] * 0.80)
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height), pygame.RESIZABLE)

        pygame.display.set_caption("Speed Archer")

        # Configurações da superfície de display
        self.__display_surface = pygame.Surface((self.__screen_width, self.__screen_height))

        # Configurações do jogo
        self.__running, self.__playing = True, True
        self.__actions = {'up': False, 'down': False, 'left': False, 'right': False, "action1": False, "action2": False, "start": False}
        self.__dt, self.__prev_time = 0, 0
        self.__state_stack = []

        # Carrega os assets
        self.__load_assets()

    def __load_assets(self):
        pass

        """ self.assets_dir = os.path.join("assets")
        self.sprite_dir = os.path.join(self.assets_dir, "sprites")
        self.font_dir = os.path.join(self.assets_dir, "fonts")
        self.font = pygame.font.Font(os.path.join(self.font_dir, "PressStart2P.ttf"), 28) """

    def run(self):
        while self.__playing:
            self.__get_events()
            self.__update()
            self.__render()
            self.__get_dt()

    def __get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                self.__playing = False
            
            if event.type == pygame.VIDEORESIZE:
                self.__screen_resize()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.__fullscreen = not self.__fullscreen
                    if self.__fullscreen:
                        pygame.display.quit()
                        self.__screen = pygame.display.set_mode(self.__monitor_size, pygame.FULLSCREEN)
                        pygame.display.init()
                    else:
                        pygame.display.quit()
                        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height), pygame.RESIZABLE)
                        pygame.display.init()
                    self.__screen_resize()

                if event.key == pygame.K_UP:
                    self.__actions['up'] = True
                if event.key == pygame.K_DOWN:
                    self.__actions['down'] = True
                if event.key == pygame.K_LEFT:
                    self.__actions['left'] = True
                if event.key == pygame.K_RIGHT:
                    self.__actions['right'] = True
                if event.key == pygame.K_SPACE:
                    self.__actions['action1'] = True
                if event.key == pygame.K_RETURN:
                    self.__actions['action2'] = True
                if event.key == pygame.K_ESCAPE:
                    self.__actions['start'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.__actions['up'] = False
                if event.key == pygame.K_DOWN:
                    self.__actions['down'] = False
                if event.key == pygame.K_LEFT:
                    self.__actions['left'] = False
                if event.key == pygame.K_RIGHT:
                    self.__actions['right'] = False
                if event.key == pygame.K_SPACE:
                    self.__actions['action1'] = False
                if event.key == pygame.K_RETURN:
                    self.__actions['action2'] = False
                if event.key == pygame.K_ESCAPE:
                    self.__actions['start'] = False

    def __update(self):
        pass

    def __render(self):
        # self.__screen.blit(pygame.transform.scale(self.__background, (self.screen_width, self.screen_height)), (0,0))
        pygame.display.flip()

    def __get_dt(self):
        now = time.time()
        self.__dt = now - self.__prev_time
        self.__prev_time = now


    def __screen_resize(self):
        Settings.set_surface_offset(int((self.__screen.get_width() - self.__display_surface.get_width()) / 2),
                                    int((self.__screen.get_height() - self.__display_surface.get_height()) / 2))


    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False


    # Métodos que alteram a state stack
    def append_state(self, state):
        self.__state_stack.append(state)

    def pop_state(self):
        self.__state_stack.pop()


    # Getters
    @property
    def state_stack(self):
        return self.__state_stack
    @property
    def screen_width(self):
        return self.__screen_width
    @property
    def screen_height(self):
        return self.__screen_height
    @property
    def display_surface(self):
        return self.__display_surface
    
    # Setters
    @display_surface.setter
    def display_surface(self, display_surface):
        self.__display_surface = display_surface

    
""" if __name__ == "__main__":
    g = Game()
while g.running:
    g.run() """
