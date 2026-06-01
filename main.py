import pygame, sys
from settings import *
from level import Level

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dark Forest: Shadow Sentinel")
clock = pygame.time.Clock()

# Fontes para o Menu
fonte_titulo = pygame.font.SysFont("Arial", 80, bold=True)
fonte_texto = pygame.font.SysFont("Arial", 35, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 20)

estado = "MENU"
level = Level(tela)
fundo_menu_x = 0

# A Lista de opções que você pediu
menu_opcoes = ["Continue", "New Game", "Load Game", "Settings", "Credits"]
# O índice da opção selecionada (Começamos no 1, que é o "New Game")
opcao_selecionada = 1 

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: 
            pygame.quit(); sys.exit()
            
        # Sistema de Controle do Teclado
        if evento.type == pygame.KEYDOWN:
            if estado == "MENU":
                # Seta para CIMA sobe no menu
                if evento.key == pygame.K_UP:
                    opcao_selecionada -= 1
                    # Se passar do limite de cima, vai para a última opção
                    if opcao_selecionada < 0:
                        opcao_selecionada = len(menu_opcoes) - 1
                        
                # Seta para BAIXO desce no menu
                elif evento.key == pygame.K_DOWN:
                    opcao_selecionada += 1
                    # Se passar do limite de baixo, volta para a primeira
                    if opcao_selecionada >= len(menu_opcoes):
                        opcao_selecionada = 0
                        
                # Apertar ENTER confirma a seleção
                elif evento.key == pygame.K_RETURN:
                    selecao = menu_opcoes[opcao_selecionada]
                    
                    if selecao == "New Game":
                        estado = "JOGANDO"
                        level = Level(tela) # Cria um mapa novo do zero
                    elif selecao == "Continue":
                        # Apenas entra no jogo sem recriar o level (se já houver progresso)
                        estado = "JOGANDO" 
                    # Os outros botões estão prontos, mas precisam das próprias telas no futuro!

            elif estado == "VITORIA":
                if evento.key == pygame.K_RETURN:
                    estado = "MENU" # Volta pro lobby após ganhar

    tela.fill((0, 0, 0))

    # ==========================
    # 1. TELA DE LOBBY (MENU)
    # ==========================
    if estado == "MENU":
        # Fundo em movimento
        fundo_menu_x -= 1
        if fundo_menu_x <= -LARGURA:
            fundo_menu_x = 0
            
        tela.blit(level.fundo, (fundo_menu_x, 0))
        tela.blit(level.fundo, (fundo_menu_x + LARGURA, 0))

        # Película escura
        pelicula = pygame.Surface((LARGURA, ALTURA))
        pelicula.set_alpha(180) 
        pelicula.fill((0, 0, 0))
        tela.blit(pelicula, (0, 0))

        # Título
        titulo_sombra = fonte_titulo.render("DARK FOREST", True, (100, 0, 100))
        titulo = fonte_titulo.render("DARK FOREST", True, (255, 105, 180)) 
        tela.blit(titulo_sombra, (LARGURA//2 - titulo.get_width()//2 + 5, 85))
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 80))

        # --- A MÁGICA DO MENU ---
        # Desenha cada item da lista na tela
        for i, opcao in enumerate(menu_opcoes):
            if i == opcao_selecionada:
                # Se for o item atual, fica rosa e ganha as setinhas
                cor = (255, 105, 180) 
                texto_final = f"> {opcao} <"
            else:
                # Os outros ficam cinza
                cor = (120, 120, 120) 
                texto_final = opcao
            
            txt_render = fonte_texto.render(texto_final, True, cor)
            # A matemática no Eixo Y (230 + i * 50) faz os botões ficarem um embaixo do outro
            tela.blit(txt_render, (LARGURA//2 - txt_render.get_width()//2, 230 + i * 50))

        # Avisozinho discreto de controles no rodapé
        aviso = fonte_pequena.render("Use as setas UP/DOWN e ENTER para selecionar", True, (100, 100, 100))
        tela.blit(aviso, (LARGURA//2 - aviso.get_width()//2, 550))

    # ==========================
    # 2. JOGO ROLANDO
    # ==========================
    elif estado == "JOGANDO":
        level.run()
        if level.vitoria:
            estado = "VITORIA"

    # ==========================
    # 3. TELA DE VITÓRIA
    # ==========================
    elif estado == "VITORIA":
        tela.blit(level.fundo, (0, 0)) 
        txt_vitoria = fonte_titulo.render("BOSS DERROTADO!", True, (255, 215, 0))
        tela.blit(txt_vitoria, (LARGURA//2 - txt_vitoria.get_width()//2, ALTURA//2 - 100))
        txt_voltar = fonte_texto.render("Pressione ENTER para Voltar ao Menu", True, (255, 255, 255))
        tela.blit(txt_voltar, (LARGURA//2 - txt_voltar.get_width()//2, ALTURA//2 + 50))

    pygame.display.flip()
    clock.tick(FPS)