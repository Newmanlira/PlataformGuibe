import pygame
import sys
from settings import *
from level import Level

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dark Forest Platformer")
clock = pygame.time.Clock()

level = Level(tela)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((0, 0, 0))
    
    level.run()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()