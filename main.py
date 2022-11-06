import pygame, sys
import config
from classeLevel import Level

# Setup geral
pygame.init()
clock = pygame.time.Clock()

# Configurações da tela
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Nível
current_level = config.levels[0]
level = Level(current_level) # Passa a matriz que representa o nível e a superfície onde o nível será desenhado

while True:
    event_listener = pygame.event.get()
    for event in event_listener:
        if event.type == pygame.QUIT: # Clicar no botão de fechar a janela
            pygame.quit()
            exit()
    
    pygame.display.flip()

    """ Conteúdo do jogo """
    
    display_surface = level.run(event_listener) # Executa o nível atual
    
    x_pos = int((SCREEN_WIDTH - display_surface.get_width()) / 2) # Centraliza a superfície do nível na tela
    y_pos = int((SCREEN_HEIGHT - display_surface.get_height()) / 2) # Centraliza a superfície do nível na tela

    screen.blit(display_surface, (x_pos, y_pos)) # Desenha a superfície do nível na tela
    display_surface.fill('black') # Pinta a superfície de preto (para evitar rastros de imagem)
    
    """ Fim do conteúdo do jogo """

    clock.tick(60)