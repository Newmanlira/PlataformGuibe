import os

# Configurações da Tela
LARGURA = 800
ALTURA = 600
FPS = 60

# Física
GRAVIDADE = 0.8
FORCA_PULO = -18         
VELOCIDADE_JOGADOR = 5

# Dash
VELOCIDADE_DASH = 15     
DURACAO_DASH = 15        
COOLDOWN_DASH = 60       

# Cores (AQUI ESTÁ A COR QUE FALTAVA)
COR_PLATAFORMA = (50, 70, 50)

# Caminhos dos Arquivos
DIRETORIO_ATUAL = os.path.dirname(__file__)
CAMINHO_FUNDO = os.path.join(DIRETORIO_ATUAL, "fundo_floresta.png")
CAMINHO_SPRITE = os.path.join(DIRETORIO_ATUAL, "AnimationSheet.png")
CAMINHO_BOSS = os.path.join(DIRETORIO_ATUAL, "boss.png")
CAMINHO_CHAO = os.path.join(DIRETORIO_ATUAL, "chao.png")