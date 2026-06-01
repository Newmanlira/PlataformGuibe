import pygame
from settings import *
from player import Player
from boss import Boss

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        try:
            self.tile = pygame.image.load(CAMINHO_CHAO).convert_alpha()
            self.image = pygame.Surface((largura, altura))
            for i in range(0, largura, 32):
                for j in range(0, altura, 32):
                    self.image.blit(pygame.transform.scale(self.tile, (32, 32)), (i, j))
        except:
            self.image = pygame.Surface((largura, altura))
            self.image.fill(COR_PLATAFORMA)
        self.rect = self.image.get_rect(topleft=(x, y))

class ItemPuloDuplo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 24))
        self.image.fill((255, 105, 180)) 
        self.rect = self.image.get_rect(center=(x, y))

# NOVA CLASSE: O Checkpoint (Ponto de Renascimento)
class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 215, 0)) # Amarelo/Dourado
        # Usamos bottomleft para ele ficar certinho em cima da plataforma
        self.rect = self.image.get_rect(bottomleft=(x, y))

class Level:
    def __init__(self, surface):
        self.tela = surface
        self.camera_x = 0; self.camera_y = 0
        self.vitoria = False
        
        # Variável que guarda onde o jogador deve renascer
        self.spawn_atual = (50, 450)
        
        try:
            self.fundo = pygame.image.load(CAMINHO_FUNDO).convert()
            self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))
        except:
            self.fundo = pygame.Surface((LARGURA, ALTURA)); self.fundo.fill((10, 10, 20))

        self.plataformas = pygame.sprite.Group()
        self.itens = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        self.boss_grupo = pygame.sprite.GroupSingle()
        self.jogador_grupo = pygame.sprite.GroupSingle()
        
        self.montar_cenario()
        self.gerar_itens() # Chamamos os itens separadamente agora

    def gerar_itens(self):
        """ Limpa e recria todos os itens da fase """
        self.itens.empty() 
        
        self.itens.add(ItemPuloDuplo(4450, 800))
        self.itens.add(ItemPuloDuplo(4250, 600))
        self.itens.add(ItemPuloDuplo(4550, 400))
        self.itens.add(ItemPuloDuplo(4350, 200))
        self.itens.add(ItemPuloDuplo(4650, 0))
        self.itens.add(ItemPuloDuplo(4850, -200))

        self.itens.add(ItemPuloDuplo(5950, -400))
        self.itens.add(ItemPuloDuplo(6650, -400))
        self.itens.add(ItemPuloDuplo(7250, -300))
        self.itens.add(ItemPuloDuplo(7850, -400))
        self.itens.add(ItemPuloDuplo(8450, -300))

        self.itens.add(ItemPuloDuplo(10700, -300))
        self.itens.add(ItemPuloDuplo(11150, -350))
        self.itens.add(ItemPuloDuplo(11650, -300))
        self.itens.add(ItemPuloDuplo(12150, -350))

        self.itens.add(ItemPuloDuplo(13050, 250))
        self.itens.add(ItemPuloDuplo(13350, 550))

    def montar_cenario(self):
        jogador = Player(self.spawn_atual[0], self.spawn_atual[1])
        self.jogador_grupo.add(jogador)
        
        layout = [
            Plataforma(0, 500, 1500, 50),
            Plataforma(300, 350, 150, 20),   
            Plataforma(700, 250, 150, 20),   
            Plataforma(1100, 350, 150, 20),  
            Plataforma(1700, 500, 800, 50),
            Plataforma(2700, 400, 300, 50),

            Plataforma(3000, 500, 100, 20),  
            Plataforma(3200, 600, 200, 20),
            Plataforma(3100, 700, 100, 20),  
            Plataforma(3500, 800, 200, 20),
            Plataforma(3300, 900, 150, 20),  
            Plataforma(3800, 1000, 500, 50), 

            Plataforma(4400, 900, 150, 20),
            Plataforma(4100, 800, 100, 20),  
            Plataforma(4200, 700, 150, 20),
            Plataforma(4500, 500, 150, 20),
            Plataforma(4700, 400, 100, 20),  
            Plataforma(4300, 300, 150, 20),
            Plataforma(4600, 100, 150, 20),
            Plataforma(4800, -100, 150, 20),
            Plataforma(5100, -300, 200, 20),

            Plataforma(5500, -300, 300, 50),
            Plataforma(6000, -200, 50, 20),  
            Plataforma(6200, -300, 200, 50),
            Plataforma(6700, -400, 50, 20),  
            Plataforma(6900, -200, 200, 50),
            Plataforma(7500, -300, 200, 50),
            Plataforma(7900, -250, 50, 20),  
            Plataforma(8100, -400, 300, 50),

            Plataforma(8600, -200, 400, 50),
            Plataforma(9200, 0, 400, 50),
            Plataforma(9800, -100, 400, 50), 

            Plataforma(10500, -200, 150, 20),
            Plataforma(10900, -400, 100, 20),
            Plataforma(11400, -150, 150, 20),
            Plataforma(11900, -400, 100, 20),
            Plataforma(12400, -200, 200, 50),

            Plataforma(12900, 100, 150, 20),
            Plataforma(13200, 400, 100, 20),
            Plataforma(13500, 700, 150, 20),
            Plataforma(13900, 900, 200, 50),

            Plataforma(14400, 900, 2500, 50), 
        ]
        self.plataformas.add(*layout)
        
        # --- CHECKPOINTS ESPALHADOS PELO MAPA ---
        # Posicionados no início de cada desafio grande
        self.checkpoints.add(Checkpoint(2800, 400))  # Antes de cair na Fenda Profunda
        self.checkpoints.add(Checkpoint(5200, -300)) # Antes dos Vãos Celestiais (Onde usa muito dash)
        self.checkpoints.add(Checkpoint(9900, -100)) # Antes do Caminho das Nuvens
        self.checkpoints.add(Checkpoint(14000, 900)) # No chão seguro, antes da arena do Boss
        
        self.boss_grupo.add(Boss(16000, 780))

    def renascer_jogador(self):
        """ Função executada quando o jogador morre """
        jogador = self.jogador_grupo.sprite
        # Volta para a posição salva no checkpoint
        jogador.rect.topleft = self.spawn_atual
        
        # Zera a física e habilidades para evitar bugs
        jogador.direcao.y = 0
        jogador.velocidade_atual = VELOCIDADE_JOGADOR
        jogador.esta_dashing = False
        jogador.tem_pulo_duplo = False
        
        # Recria os itens para você poder tentar o percurso novamente
        self.gerar_itens()

    def run(self):
        jogador = self.jogador_grupo.sprite
        boss = self.boss_grupo.sprite
        
        self.jogador_grupo.update()
        self.boss_grupo.update()
        
        # Física X
        jogador.rect.x += jogador.direcao.x * jogador.velocidade_atual
        if jogador.rect.left < 0: jogador.rect.left = 0
        for p in self.plataformas:
            if jogador.rect.colliderect(p.rect):
                if jogador.direcao.x > 0: jogador.rect.right = p.rect.left
                elif jogador.direcao.x < 0: jogador.rect.left = p.rect.right
        
        # Física Y
        if not jogador.esta_dashing: jogador.direcao.y += GRAVIDADE
        jogador.rect.y += jogador.direcao.y
        jogador.no_chao = False
        for p in self.plataformas:
            if jogador.rect.colliderect(p.rect):
                if jogador.direcao.y > 0: jogador.rect.bottom = p.rect.top; jogador.direcao.y = 0; jogador.no_chao = True
                elif jogador.direcao.y < 0: jogador.rect.top = p.rect.bottom; jogador.direcao.y = 0
        
        # --- ATUALIZAR CHECKPOINT ---
        # Se tocar no bloco amarelo, salva a posição dele
        for check in self.checkpoints:
            if jogador.rect.colliderect(check.rect):
                # Salva o X e Y, subindo um pouquinho para não prender no chão
                self.spawn_atual = (check.rect.x, check.rect.y - 20)
        
        # Pegar Cubos Rosas
        if pygame.sprite.spritecollide(jogador, self.itens, True): jogador.tem_pulo_duplo = True
        
        # Derrotar o Boss
        if jogador.rect.colliderect(boss.rect) and boss.vivo:
            boss.morrer()
            self.vitoria = True
            
        # --- MORTE POR QUEDA ---
        if jogador.rect.y > ALTURA + 3000: 
            self.renascer_jogador() # Agora chama a nova função!

        # Atualizar a Câmera
        self.camera_x = jogador.rect.x - LARGURA//2
        self.camera_y = jogador.rect.y - ALTURA//2

        # Desenhar o fundo infinito
        fx = -(self.camera_x % LARGURA)
        fy = -(self.camera_y * 0.1) % ALTURA 
        
        self.tela.blit(self.fundo, (fx, fy))
        self.tela.blit(self.fundo, (fx + LARGURA, fy))
        self.tela.blit(self.fundo, (fx, fy - ALTURA))
        self.tela.blit(self.fundo, (fx + LARGURA, fy - ALTURA))
        
        # Desenha os checkpoints também!
        for c in self.checkpoints: self.tela.blit(c.image, (c.rect.x - self.camera_x, c.rect.y - self.camera_y))
        for p in self.plataformas: self.tela.blit(p.image, (p.rect.x - self.camera_x, p.rect.y - self.camera_y))
        for i in self.itens: self.tela.blit(i.image, (i.rect.x - self.camera_x, i.rect.y - self.camera_y))
        self.tela.blit(boss.image, (boss.rect.x - self.camera_x, boss.rect.y - self.camera_y))
        self.tela.blit(jogador.image, (jogador.rect.x - self.camera_x, jogador.rect.y - self.camera_y))