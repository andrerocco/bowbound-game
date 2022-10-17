import pygame, sys
import config
from classeLevel import Level

# Setup geral
pygame.init()
clock = pygame.time.Clock()

# Configurações da tela
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Nível
current_level_map = config.levels[1]
level = Level(current_level_map, screen) # Passa a matriz que representa o nível e a superfície onde o nível será desenhado

while True:
    event_listener = pygame.event.get()
    for event in event_listener:
        if event.type == pygame.QUIT: # Clicar no botão de fechar a janela
            pygame.quit()
            exit()
    
    pygame.display.flip()
    
    # Preenchimento de tela
    screen.fill('black')

    # Conteúdo do jogo
    level.run(event_listener)

    clock.tick(60)