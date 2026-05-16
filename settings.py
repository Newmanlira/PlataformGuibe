import os

# Configurações da Tela
LARGURA = 800
ALTURA = 600
FPS = 60

# Física e Movimento
GRAVIDADE = 0.8
FORCA_PULO = -15
VELOCIDADE_JOGADOR = 5

# Configurações do Dash
VELOCIDADE_DASH = 15     
DURACAO_DASH = 15        
COOLDOWN_DASH = 60       

# Cores
COR_PLATAFORMA = (50, 70, 50)

# Caminhos dos Arquivos
DIRETORIO_ATUAL = os.path.dirname(__file__)
CAMINHO_FUNDO = os.path.join(DIRETORIO_ATUAL, "fundo_floresta.png")
CAMINHO_SPRITE = os.path.join(DIRETORIO_ATUAL, "AnimationSheet.png")