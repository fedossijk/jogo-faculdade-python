import random
import pygame

estado_jogo = "menu"
som_game_over_tocado = False
pygame.init()
pygame.mixer.init()

fonte = pygame.font.SysFont(None, 40)
fonte_titulo = pygame.font.SysFont(None, 70)
fonte_game_over = pygame.font.SysFont(None, 80)

largura = 800
altura = 600

virus_x = 650
virus_y = 400

vidas = 5
ultimo_dano = 0

pontos = 0

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("A Desenvolvedora e os Bugs")

fundo = pygame.image.load("assets/imagens/fundo.png")
fundo = pygame.transform.scale(fundo, (largura, altura))


som_bug = pygame.mixer.Sound("assets/sons/Map.wav")
som_dano = pygame.mixer.Sound("assets/sons/Mercury.wav")
som_game_over = pygame.mixer.Sound("assets/sons/Venus.wav")

som_bug.set_volume(0.2)
som_dano.set_volume(0.2)
som_game_over.set_volume(0.3)

canal_bug = pygame.mixer.Channel(0)
canal_dano = pygame.mixer.Channel(1)
canal_game_over = pygame.mixer.Channel(2)

player = pygame.image.load("assets/imagens/player.png")
player = pygame.transform.scale(player, (80, 80))

bug = pygame.image.load("assets/imagens/bug.png")
bug = pygame.transform.scale(bug, (60, 60))

virus = pygame.image.load("assets/imagens/virus.png")
virus = pygame.transform.scale(virus, (70, 70))

# Posições
player_x = 100
player_y = 100

bug_x = 500
bug_y = 250

velocidade = 5
velocidade_virus = 1.8

mostrar_vida = False
tempo_mensagem_vida = 0

rodando = True

clock = pygame.time.Clock()

while rodando:

    # =========================
    # EVENTOS
    # =========================
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:

            if estado_jogo == "menu":
                if evento.key == pygame.K_SPACE:
                    estado_jogo = "jogando"

            if estado_jogo == "game_over":
                if evento.key == pygame.K_r:

                    pygame.mixer.stop()

                    player_x = 100
                    player_y = 100

                    bug_x = 500
                    bug_y = 250

                    virus_x = 650
                    virus_y = 400

                    pontos = 0
                    vidas = 5
                    ultimo_dano = 0

                    som_game_over_tocado = False

                    estado_jogo = "jogando"

    # =========================
    # MOVIMENTAÇÃO DA JOGADORA
    # =========================
    if estado_jogo == "jogando":

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_UP]:
            player_y -= velocidade

        if teclas[pygame.K_DOWN]:
            player_y += velocidade

        if teclas[pygame.K_LEFT]:
            player_x -= velocidade

        if teclas[pygame.K_RIGHT]:
            player_x += velocidade


    # =========================
    # MOVIMENTO DO VÍRUS
    # =========================
    if estado_jogo == "jogando":

        if virus_x < player_x:
            virus_x += velocidade_virus

        if virus_x > player_x:
            virus_x -= velocidade_virus

        if virus_y < player_y:
            virus_y += velocidade_virus

        if virus_y > player_y:
            virus_y -= velocidade_virus


    if player_x < 0:
        player_x = 0

    if player_x > 720:
        player_x = 720

    if player_y < 0:
        player_y = 0

    if player_y > 520:
        player_y = 520


    player_rect = pygame.Rect(player_x, player_y, 80, 80)
    bug_rect = pygame.Rect(bug_x, bug_y, 60, 60)

    if estado_jogo == "jogando":

        if player_rect.colliderect(bug_rect):
            canal_bug.play(som_bug)
            pontos += 1

            if pontos % 5 == 0 and vidas < 5:
                vidas += 1
                mostrar_vida = True
                tempo_mensagem_vida = pygame.time.get_ticks()

            bug_x = random.randint(0, 740)
            bug_y = random.randint(0, 540)


    virus_rect = pygame.Rect(virus_x, virus_y, 70, 70)

    if estado_jogo == "jogando":

        tempo_atual = pygame.time.get_ticks()

        if player_rect.colliderect(virus_rect):

            if tempo_atual - ultimo_dano > 2000:
                canal_dano.play(som_dano)
                vidas -= 1
                ultimo_dano = tempo_atual

                virus_x = 700
                virus_y = 500


    if vidas <= 0:
        estado_jogo = "game_over"

    if estado_jogo == "game_over":

        if not som_game_over_tocado:
             pygame.mixer.stop()
             canal_game_over.play(som_game_over)
             som_game_over_tocado = True

    # TELA INICIAL
    if estado_jogo == "menu":
        tela.fill((135, 206, 235))

        titulo = fonte_titulo.render(
            "A Desenvolvedora e os Bugs",
            True,
            (0, 0, 0)
        )

        instrucoes = fonte.render(
            "Pressione ESPAÇO para iniciar",
            True,
            (0, 0, 0)
        )
        objetivo = fonte.render(
            "Capture os bugs e evite o vírus!",
            True,
            (0, 0, 0)
        )

        controles = fonte.render(
            "Use as teclas direcionais para mover a personagem",
            True,
            (0, 0, 0)
        )

        titulo_rect = titulo.get_rect(center=(400, 80))
        objetivo_rect = objetivo.get_rect(center=(400, 170))
        controles_rect = controles.get_rect(center=(400, 280))
        instrucoes_rect = instrucoes.get_rect(center=(400, 500))

        tela.blit(titulo, titulo_rect)
        tela.blit(objetivo, objetivo_rect)
        tela.blit(controles, controles_rect)
        tela.blit(instrucoes, instrucoes_rect)


    # =========================
    # TELA DO JOGO
    # =========================
    elif estado_jogo == "jogando":

        # Fundo
        tela.blit(fundo, (0, 0))

        # Bug
        tela.blit(bug, (bug_x, bug_y))

        # Vírus
        tela.blit(virus, (virus_x, virus_y))

        # Jogadora
        tela.blit(player, (player_x, player_y))

        # Pontuação
        texto_pontos = fonte.render(
            f"Pontos: {pontos}",
            True,
            (0, 0, 0)
        )
        tela.blit(texto_pontos, (620, 20))

        # Vidas
        texto_vidas = fonte.render(
            f"Vidas: {vidas}",
            True,
            (0, 0, 0)
        )
        tela.blit(texto_vidas, (20, 20))

        if mostrar_vida:

            texto_vida = fonte.render(
                "+1 VIDA!",
                True,
                (0, 180, 0)
            )

            tela.blit(texto_vida, (330, 70))

            if pygame.time.get_ticks() - tempo_mensagem_vida > 2000:
                mostrar_vida = False



    # =========================
    # TELA GAME OVER
    # =========================
    elif estado_jogo == "game_over":

        tela.fill((255, 255, 255))

        texto_game_over = fonte_game_over.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        tela.blit(texto_game_over, (220, 220))

        texto_pontos = fonte.render(
            f"Pontuação Final: {pontos}",
            True,
            (0, 0, 0)
        )
        tela.blit(texto_pontos, (260, 300))

        texto_reiniciar = fonte.render(
            "Pressione R para reiniciar",
            True,
            (0, 0, 0)
        )
        tela.blit(texto_reiniciar, (220, 350))


    pygame.display.update()
    clock.tick(60)

pygame.quit()