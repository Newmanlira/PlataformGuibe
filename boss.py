import pygame
from settings import *

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load(CAMINHO_BOSS).convert_alpha()
            self.image = pygame.transform.scale(self.image, (120, 120))
        except:
            self.image = pygame.Surface((120, 120))
            self.image.fill((50, 0, 50))
            
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vivo = True
        self.velocidade_y = 0

    def morrer(self):
        self.vivo = False

    def update(self):
        if not self.vivo:
            # Animação simples de cair
            self.velocidade_y += GRAVIDADE
            self.rect.y += self.velocidade_y
            # Gira o boss enquanto cai
            self.image = pygame.transform.rotate(self.image, 5)