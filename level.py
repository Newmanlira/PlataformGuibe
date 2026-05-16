import pygame
from settings import *
from player import Player

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(COR_PLATAFORMA)
        self.rect = self.image.get_rect(topleft=(x, y))

class Level:
    def __init__(self, surface):
        self.tela = surface
        self.camera_x = 0
        
        try:
            self.fundo = pygame.image.load(CAMINHO_FUNDO).convert()
            self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))
        except FileNotFoundError:
            self.fundo = pygame.Surface((LARGURA, ALTURA))
            self.fundo.fill((20, 25, 30))

        self.plataformas = pygame.sprite.Group()
        self.jogador_grupo = pygame.sprite.GroupSingle()

        self.montar_cenario()

    def montar_cenario(self):
        jogador = Player(100, 100)
        self.jogador_grupo.add(jogador)

        # Adicionei várias plataformas para criar um desafio de pulo e dash no meio
        layout = [
            # O chão inicial
            Plataforma(0, 500, 800, 40),      
            
            # As plataformas flutuantes no meio (A escadinha)
            Plataforma(850, 400, 150, 20),    # Primeiro degrau flutuante
            Plataforma(1100, 300, 300, 40),   # A plataforma que estava isolada (agora mais alta)
            Plataforma(1450, 200, 150, 20),   # Degrau mais alto ainda
            Plataforma(1250, 100, 100, 20),   # Plataforma extra voltando por cima
            
            # O chão do outro lado
            Plataforma(1600, 500, 1500, 40)   
        ]
        self.plataformas.add(*layout)

    def colisao_horizontal(self):
        jogador = self.jogador_grupo.sprite
        jogador.rect.x += jogador.direcao.x * jogador.velocidade_atual

        for plat in self.plataformas.sprites():
            if plat.rect.colliderect(jogador.rect):
                if jogador.direcao.x > 0: 
                    jogador.rect.right = plat.rect.left
                elif jogador.direcao.x < 0: 
                    jogador.rect.left = plat.rect.right

    def colisao_vertical(self):
        jogador = self.jogador_grupo.sprite
        jogador.aplicar_gravidade()

        jogador.no_chao = False
        for plat in self.plataformas.sprites():
            if plat.rect.colliderect(jogador.rect):
                if jogador.direcao.y > 0: 
                    jogador.rect.bottom = plat.rect.top
                    jogador.direcao.y = 0
                    jogador.no_chao = True
                elif jogador.direcao.y < 0: 
                    jogador.rect.top = plat.rect.bottom
                    jogador.direcao.y = 0

        # Morte por queda
        if jogador.rect.y > ALTURA + 200:
            jogador.rect.topleft = (100, 100)
            jogador.direcao.y = 0

    def desenhar_fundo(self):
        fundo_x = -(self.camera_x % LARGURA)
        self.tela.blit(self.fundo, (fundo_x, 0))
        self.tela.blit(self.fundo, (fundo_x + LARGURA, 0))

    def run(self):
        self.jogador_grupo.update()
        self.colisao_horizontal()
        self.colisao_vertical()

        jogador = self.jogador_grupo.sprite
        self.camera_x = jogador.rect.x - (LARGURA // 2)

        self.desenhar_fundo()
        
        for plat in self.plataformas.sprites():
            self.tela.blit(plat.image, (plat.rect.x - self.camera_x, plat.rect.y))
            
        self.tela.blit(jogador.image, (jogador.rect.x - self.camera_x, jogador.rect.y))