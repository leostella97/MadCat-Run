import pygame
import os

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da janela
largura_janela = 800
altura_janela = 600
janela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("MadCat Run")

# Carregue as imagens e dimensione-as
pasta_imagens = "img"
cat_img = pygame.transform.scale(pygame.image.load(os.path.join(pasta_imagens, "cat.png")), (50, 50))
rat_img = pygame.transform.scale(pygame.image.load(os.path.join(pasta_imagens, "rat.png")), (50, 50))

# Defina a posição inicial do gato e do rato
posicao_gato = [100, 300]
posicao_rato = [600, 300]

# Defina a velocidade de movimento do jogador e do inimigo
velocidade_jogador = 5
velocidade_inimigo = 3

# Variável para controlar qual personagem está sendo controlado
personagem_controlado = None

# Variáveis para controlar o tempo
tempo_inicial = pygame.time.get_ticks()  # Tempo em milissegundos
tempo_limite = 60000  # 1 minuto em milissegundos

# Função para desenhar os personagens na tela inicial
def desenhar_tela_inicial():
    janela.fill((255, 255, 255))
    fonte = pygame.font.SysFont(None, 40)
    texto = fonte.render("Escolha um personagem:", True, (0, 0, 0))
    janela.blit(texto, (250, 200))
    botao_rato = pygame.Rect(300, 300, 200, 50)
    botao_gato = pygame.Rect(300, 400, 200, 50)
    pygame.draw.rect(janela, (0, 255, 0), botao_rato)
    pygame.draw.rect(janela, (0, 0, 255), botao_gato)
    fonte = pygame.font.SysFont(None, 30)
    texto_rato = fonte.render("Rato", True, (0, 0, 0))
    texto_gato = fonte.render("Gato", True, (0, 0, 0))
    janela.blit(texto_rato, (365, 315))
    janela.blit(texto_gato, (365, 415))

# Função para desenhar os personagens na tela do jogo
def desenhar_personagens():
    janela.blit(cat_img, posicao_gato)
    janela.blit(rat_img, posicao_rato)

# Função para controlar o movimento do personagem
def controlar_personagem(teclas, posicao, velocidade):
    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        posicao[1] -= velocidade
    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        posicao[0] -= velocidade
    if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        posicao[1] += velocidade
    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        posicao[0] += velocidade

    # Verifique se o personagem atingiu os limites da tela
    if posicao[0] < 0:
        posicao[0] = 0
    elif posicao[0] > largura_janela - 50:  # 50 é a largura do personagem
        posicao[0] = largura_janela - 50
    if posicao[1] < 0:
        posicao[1] = 0
    elif posicao[1] > altura_janela - 50:  # 50 é a altura do personagem
        posicao[1] = altura_janela - 50

# Função para verificar colisões entre o jogador e o inimigo
def verificar_colisoes():
    global personagem_controlado

    if personagem_controlado == "rato":
        if pygame.Rect(posicao_rato, (50, 50)).colliderect(pygame.Rect(posicao_gato, (50, 50))):
            return True  # Colisão entre rato e gato
    elif personagem_controlado == "gato":
        if pygame.Rect(posicao_gato, (50, 50)).colliderect(pygame.Rect(posicao_rato, (50, 50))):
            return True  # Colisão entre gato e rato
    return False

# Função para exibir mensagens na tela
def exibir_mensagem(texto):
    fonte = pygame.font.SysFont(None, 40)
    texto_renderizado = fonte.render(texto, True, (255, 0, 0))
    janela.blit(texto_renderizado, (250, 250))

# Loop principal do jogo
tela_inicial = True
jogo_iniciado = False
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if tela_inicial:
                x, y = pygame.mouse.get_pos()
                botao_rato = pygame.Rect(300, 300, 200, 50)
                botao_gato = pygame.Rect(300, 400, 200, 50)
                if botao_rato.collidepoint(x, y):
                    personagem_controlado = "rato"
                    tela_inicial = False
                    jogo_iniciado = True
                elif botao_gato.collidepoint(x, y):
                    personagem_controlado = "gato"
                    tela_inicial = False
                    jogo_iniciado = True

    if tela_inicial:
        desenhar_tela_inicial()
    elif jogo_iniciado:
        teclas = pygame.key.get_pressed()
        if personagem_controlado == "rato":
            controlar_personagem(teclas, posicao_rato, velocidade_jogador)
            # Fazer o gato perseguir o rato
            if posicao_gato[0] < posicao_rato[0]:
                posicao_gato[0] += velocidade_inimigo
            elif posicao_gato[0] > posicao_rato[0]:
                posicao_gato[0] -= velocidade_inimigo
            if posicao_gato[1] < posicao_rato[1]:
                posicao_gato[1] += velocidade_inimigo
            elif posicao_gato[1] > posicao_rato[1]:
                posicao_gato[1] -= velocidade_inimigo
        elif personagem_controlado == "gato":
            controlar_personagem(teclas, posicao_gato, velocidade_jogador)
            # Fazer o rato fugir do gato
            if posicao_rato[0] < posicao_gato[0]:
                posicao_rato[0] += velocidade_inimigo
            elif posicao_rato[0] > posicao_gato[0]:
                posicao_rato[0] -= velocidade_inimigo
            if posicao_rato[1] < posicao_gato[1]:
                posicao_rato[1] += velocidade_inimigo
            elif posicao_rato[1] > posicao_gato[1]:
                posicao_rato[1] -= velocidade_inimigo

        # Verificar colisões
        if verificar_colisoes():
            exibir_mensagem("Você perdeu!")
        else:
            # Verificar tempo
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_inicial >= tempo_limite:
                if personagem_controlado == "rato":
                    exibir_mensagem("Você venceu!")
                else:
                    exibir_mensagem("Você perdeu!")
        # Limpe a tela
        janela.fill((255, 255, 255))

        # Desenhe os personagens
        desenhar_personagens()

    pygame.display.flip()

# Encerre o Pygame
pygame.quit()
