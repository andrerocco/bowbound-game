import pygame, sys
import config

from level.classeLevel import Level
from Settings import Settings

# Setup geral
pygame.init()
clock = pygame.time.Clock()

# Configurações da tela
MONITOR_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
SCREEN_WIDTH = int(MONITOR_SIZE[0] * 0.95)
SCREEN_HEIGHT = int(MONITOR_SIZE[1] * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Nível
current_level = config.levels[0]
level = Level(current_level) # Passa a matriz que representa o nível e a superfície onde o nível será desenhado
display_surface = level.display_surface # Superfície onde o nível será desenhado

# Informações da tela
fullscreen = False

# Define as configurações globais
Settings.set_surface_offset(int((screen.get_width() - display_surface.get_width()) / 2),
                            int((screen.get_height() - display_surface.get_height()) / 2))

while True:
    event_listener = pygame.event.get()
    for event in event_listener:
        if event.type == pygame.QUIT: # Clicar no botão de fechar a janela
            pygame.quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            Settings.set_surface_offset(int((screen.get_width() - display_surface.get_width()) / 2),
                                        int((screen.get_height() - display_surface.get_height()) / 2))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                
                if fullscreen:
                    pygame.display.quit()
                    screen = pygame.display.set_mode(MONITOR_SIZE, pygame.FULLSCREEN)
                    pygame.display.init()
                else:
                    pygame.display.quit()
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                    pygame.display.init()

                Settings.set_surface_offset(int((screen.get_width() - display_surface.get_width()) / 2),
                                            int((screen.get_height() - display_surface.get_height()) / 2))

    pygame.display.flip()

    """ Conteúdo do jogo """
    
    display_surface = level.run(event_listener) # Executa o nível atual
    
    screen.blit(display_surface, Settings.get_surface_offset()) # Desenha a superfície do nível na tela
    display_surface.fill('black') # Pinta a superfície de preto (para evitar rastros de imagem)
    
    """ Fim do conteúdo do jogo """
    
    clock.tick(60)
