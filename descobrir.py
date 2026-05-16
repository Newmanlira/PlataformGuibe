import pygame
import sys
import os

pygame.init()

diretorio_atual = os.path.dirname(__file__)
caminho_imagem = os.path.join(diretorio_atual, "AnimationSheet.png")

try:
    imagem = pygame.image.load(caminho_imagem)
except FileNotFoundError:
    print("Erro: Não encontrei o arquivo AnimationSheet.png na pasta.")
    sys.exit()

largura_img, altura_img = imagem.get_size()
tela = pygame.display.set_mode((max(largura_img, 500), max(altura_img + 60, 300)))
pygame.display.set_caption("Descobridor de Frames")

tamanho_frame = 32 
fonte = pygame.font.SysFont(None, 24)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                tamanho_frame += 2
            if evento.key == pygame.K_DOWN:
                tamanho_frame -= 2
            if evento.key == pygame.K_RIGHT:
                tamanho_frame += 10
            if evento.key == pygame.K_LEFT:
                tamanho_frame -= 10
                
            if tamanho_frame < 8: 
                tamanho_frame = 8

    tela.fill((40, 40, 40))
    
    deslocamento_y = 50
    tela.blit(imagem, (0, deslocamento_y))

    for x in range(0, largura_img + 1, tamanho_frame):
        pygame.draw.line(tela, (255, 0, 0), (x, deslocamento_y), (x, deslocamento_y + altura_img), 1)
    for y in range(0, altura_img + 1, tamanho_frame):
        pygame.draw.line(tela, (255, 0, 0), (0, deslocamento_y + y), (largura_img, deslocamento_y + y), 1)

    texto1 = fonte.render(f"Tamanho Atual do Frame: {tamanho_frame}x{tamanho_frame} pixels", True, (255, 255, 255))
    texto2 = fonte.render("Use as SETAS do teclado para aumentar/diminuir o quadrado vermelho", True, (200, 200, 200))
    tela.blit(texto1, (10, 10))
    tela.blit(texto2, (10, 30))

    pygame.display.flip()

pygame.quit()