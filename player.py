import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        try:
            self.spritesheet = pygame.image.load(CAMINHO_SPRITE).convert_alpha()
        except FileNotFoundError:
            self.spritesheet = None

        self.animacoes = {'idle': [], 'correndo': []}
        self.frame_index = 0
        self.velocidade_animacao = 0.15
        
        self.carregar_frames()

        if self.animacoes['idle']:
            self.image = self.animacoes['idle'][0]
        else:
            self.image = pygame.Surface((72, 72))
            self.image.fill((200, 200, 200))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.direcao = pygame.math.Vector2(0, 0)
        self.velocidade_atual = VELOCIDADE_JOGADOR
        self.no_chao = False
        self.olhando_direita = True

        self.esta_dashing = False
        self.tempo_dash = 0
        self.cooldown_dash = 0

    def carregar_frames(self):
        if not self.spritesheet: return
        
        TAMANHO_ORIGINAL = 24
        ESCALA = 3 
        TAMANHO_FINAL = TAMANHO_ORIGINAL * ESCALA

        for coluna in range(4): 
            frame = pygame.Surface((TAMANHO_ORIGINAL, TAMANHO_ORIGINAL), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (coluna * TAMANHO_ORIGINAL, 0 * TAMANHO_ORIGINAL, TAMANHO_ORIGINAL, TAMANHO_ORIGINAL))
            frame = pygame.transform.scale(frame, (TAMANHO_FINAL, TAMANHO_FINAL))
            self.animacoes['idle'].append(frame)

        for coluna in range(6): 
            frame = pygame.Surface((TAMANHO_ORIGINAL, TAMANHO_ORIGINAL), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (coluna * TAMANHO_ORIGINAL, 1 * TAMANHO_ORIGINAL, TAMANHO_ORIGINAL, TAMANHO_ORIGINAL))
            frame = pygame.transform.scale(frame, (TAMANHO_FINAL, TAMANHO_FINAL))
            self.animacoes['correndo'].append(frame)

    def obter_input(self):
        teclas = pygame.key.get_pressed()
        
        if self.cooldown_dash > 0:
            self.cooldown_dash -= 1

        if not self.esta_dashing:
            if teclas[pygame.K_LEFT]:
                self.direcao.x = -1
                self.olhando_direita = False
            elif teclas[pygame.K_RIGHT]:
                self.direcao.x = 1
                self.olhando_direita = True
            else:
                self.direcao.x = 0

            if teclas[pygame.K_SPACE] and self.no_chao:
                self.pular()

            if teclas[pygame.K_LSHIFT] and self.cooldown_dash <= 0:
                self.iniciar_dash()

    def iniciar_dash(self):
        self.esta_dashing = True
        self.tempo_dash = DURACAO_DASH
        self.cooldown_dash = COOLDOWN_DASH
        self.velocidade_atual = VELOCIDADE_DASH
        self.direcao.x = 1 if self.olhando_direita else -1
        self.direcao.y = 0 

    def gerenciar_dash(self):
        if self.esta_dashing:
            self.tempo_dash -= 1
            if self.tempo_dash <= 0:
                self.esta_dashing = False
                self.velocidade_atual = VELOCIDADE_JOGADOR

    def aplicar_gravidade(self):
        if not self.esta_dashing:
            self.direcao.y += GRAVIDADE
        self.rect.y += self.direcao.y

    def pular(self):
        self.direcao.y = FORCA_PULO
        self.no_chao = False

    def animar(self):
        if not self.animacoes['idle']: return

        if self.esta_dashing:
            estado = 'correndo'
            self.velocidade_animacao = 0.4
        else:
            estado = 'correndo' if self.direcao.x != 0 else 'idle'
            self.velocidade_animacao = 0.15
        
        self.frame_index += self.velocidade_animacao
        if self.frame_index >= len(self.animacoes[estado]):
            self.frame_index = 0
            
        imagem_atual = self.animacoes[estado][int(self.frame_index)]
        
        if not self.olhando_direita:
            self.image = pygame.transform.flip(imagem_atual, True, False)
        else:
            self.image = imagem_atual

    def update(self):
        self.obter_input()
        self.gerenciar_dash()
        self.animar()