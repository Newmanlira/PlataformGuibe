import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.spritesheet = pygame.image.load(CAMINHO_SPRITE).convert_alpha()
        except: 
            self.spritesheet = None

        self.animacoes = {'idle': [], 'correndo': []}
        self.frame_index = 0
        self.carregar_frames()
        
        self.image = self.animacoes['idle'][0] if self.animacoes['idle'] else pygame.Surface((72, 72))
        self.image.fill((200, 200, 200)) if not self.animacoes['idle'] else None
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direcao = pygame.math.Vector2(0, 0)
        self.velocidade_atual = VELOCIDADE_JOGADOR
        self.no_chao = False
        self.olhando_direita = True
        
        self.esta_dashing = False
        self.tempo_dash = 0
        self.cooldown_dash = 0
        
        self.tem_pulo_duplo = False
        self.pulo_botao_solto = True

    def carregar_frames(self):
        if not self.spritesheet: return
        T = 24
        E = 3
        F = T * E
        for i in range(4):
            frm = pygame.Surface((T, T), pygame.SRCALPHA)
            frm.blit(self.spritesheet, (0, 0), (i*T, 0, T, T))
            self.animacoes['idle'].append(pygame.transform.scale(frm, (F, F)))
        for i in range(6):
            frm = pygame.Surface((T, T), pygame.SRCALPHA)
            frm.blit(self.spritesheet, (0, 0), (i*T, T, T, T))
            self.animacoes['correndo'].append(pygame.transform.scale(frm, (F, F)))

    def update(self):
        teclas = pygame.key.get_pressed()
        
        if self.cooldown_dash > 0: 
            self.cooldown_dash -= 1
        
        if not self.esta_dashing:
            self.direcao.x = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT])
            if self.direcao.x > 0: self.olhando_direita = True
            elif self.direcao.x < 0: self.olhando_direita = False
            
            if teclas[pygame.K_SPACE]:
                if self.no_chao and self.pulo_botao_solto:
                    self.direcao.y = FORCA_PULO
                    self.no_chao = False
                    self.pulo_botao_solto = False
                elif not self.no_chao and self.pulo_botao_solto and self.tem_pulo_duplo:
                    self.direcao.y = FORCA_PULO
                    self.tem_pulo_duplo = False
                    self.pulo_botao_solto = False
            else: 
                self.pulo_botao_solto = True
            
            if teclas[pygame.K_LSHIFT] and self.cooldown_dash <= 0:
                self.esta_dashing = True
                self.tempo_dash = DURACAO_DASH
                self.cooldown_dash = COOLDOWN_DASH
                self.velocidade_atual = VELOCIDADE_DASH
                self.direcao.y = 0
        else:
            self.tempo_dash -= 1
            if self.tempo_dash <= 0: 
                self.esta_dashing = False
                self.velocidade_atual = VELOCIDADE_JOGADOR

        estado = 'correndo' if self.direcao.x != 0 else 'idle'
        
        if self.animacoes[estado]:
            self.frame_index = (self.frame_index + (0.4 if self.esta_dashing else 0.15)) % len(self.animacoes[estado])
            img = self.animacoes[estado][int(self.frame_index)]
            self.image = pygame.transform.flip(img, True, False) if not self.olhando_direita else img