import pygame, sys
import config
from classeLevel import Level

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

# Status de tela cheia
fullscreen = False

while True:
    event_listener = pygame.event.get()
    for event in event_listener:
        if event.type == pygame.QUIT: # Clicar no botão de fechar a janela
            pygame.quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            pygame.display.quit()
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            pygame.display.init()
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

    pygame.display.flip()

    """ Conteúdo do jogo """
    
    display_surface = level.run(event_listener) # Executa o nível atual
    
    x_pos = int((screen.get_width() - display_surface.get_width()) / 2) # Centraliza a superfície do nível na tela
    y_pos = int((screen.get_height() - display_surface.get_height()) / 2) # Centraliza a superfície do nível na tela
    
    screen.blit(display_surface, (x_pos, y_pos)) # Desenha a superfície do nível na tela
    display_surface.fill('black') # Pinta a superfície de preto (para evitar rastros de imagem)
    
    """ Fim do conteúdo do jogo """
    
    clock.tick(60)
