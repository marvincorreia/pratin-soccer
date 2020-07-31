from math import *
from random import choice
from pygame import *
from mythreads import MyTaskThread, MyTimer, MyMusicPlayer
from balizas import BalizaLeft, BalizaRight
from bola import Bola
from campo import Campo, Linhas
from items import TextMenu, SelectorMenu, SelecaoPlayer, MouseCursor, Item, SetaDirecao, Label, ScoreBoard
from player import Player

# initializacao
init()
mixer.init()

# variaveis globais
screen_width, screen_height = 800, 600
screen = display.set_mode((screen_width, screen_height))
display.set_caption('Pratinhos Soccer')
clock = time.Clock()
estadio = None
sound, optMode, optSpeed = True, 1, 2
flag_anim, mouseOnmove, update, run, show_lines = False, False, False, True, False
flag = {'home': True, 'away': False}
campo = Campo()
seta = SetaDirecao()
bgmenu_principal = image.load('data/backgrounds/menu_bg.png')
baliza_group = sprite.Group((BalizaLeft(), BalizaRight()))
power_bar = sprite.GroupSingle(Linhas(70, 574, 200, 20, Color('black')))
selection = sprite.GroupSingle(SelecaoPlayer())
all_players, home_players, away_players = sprite.Group(), sprite.Group(), sprite.Group()
bola = sprite.GroupSingle()
cursor = sprite.GroupSingle(MouseCursor())
nomes_equipas = ['argentina', 'australia', 'belgium', 'brazil', 'cape_verde', 'colombia',
                 'costa_rica', 'croatia', 'denmark', 'egypt', 'england', 'france',
                 'germany', 'iceland', 'iran', 'japan', 'marocco', 'mexico', 'nigeria',
                 'panama', 'peru', 'poland', 'portugal', 'russia', 'saudi_arabia',
                 'senegal', 'serbia', 'south_korea', 'spain', 'sweden',
                 'switzerland', 'tunisia', 'uruguai']

nomes_bolas = ['bola1', 'bola2', 'bola3', 'bola4', 'bola5']
nomes_estadios = ['estadio1', 'estadio2', 'estadio3']
casa = choice(range(len(nomes_equipas))[1:])
fora = choice(range(len(nomes_equipas))[1:])
while casa == fora:
    fora = choice(range(len(nomes_equipas))[1:])

num_bal = choice(range(len(nomes_bolas))[1:])
num_stadium = choice(range(len(nomes_estadios))[1:])
vels_de_jogo = {1: 22, 2: 30, 3: 40}
smart_mod = {1: False, 2: True}
score = {'home': 0, 'away': 0}
score_board = sprite.GroupSingle(ScoreBoard(380, 79, font.SysFont('Arial', 20, bold=True), (0, 0), Color('white')))
pontape_de_saida, team_goal = True, None
placar_labels = sprite.Group()

# sons
som_seta = mixer.Sound('data/sons/seta.ogg')
som_enter = mixer.Sound('data/sons/go_click.ogg')
som_back = mixer.Sound('data/sons/back.ogg')
som_enter_play = mixer.Sound('data/sons/go_play.ogg')
som_intro = mixer.Sound('data/sons/intro.ogg')
som_clack = mixer.Sound('data/sons/clack.ogg')
som_move = mixer.Sound('data/sons/move.ogg')
som_golo = mixer.Sound('data/sons/golo22.ogg')
som_celebracao = mixer.Sound('data/sons/celebracao.ogg')
som_rede = mixer.Sound('data/sons/bola_rede.ogg')
world_cup_2018 = mixer.Sound('data/sons/Jason Derulo feat. Lizha James - Colours (FIFA World Cup 2018).ogg')
som_golo.set_volume(0.3)
som_celebracao.set_volume(0.4)
som_clack.set_volume(0.3)
som_intro.set_volume(0.3)
play_back = MyMusicPlayer(world_cup_2018, 8)


def saveConfig():
    """
    salvar dados de configuração de sistema
    """
    global sound, optMode, optSpeed
    file = open('config.txt', mode='w')
    file.write(str(sound) + '\n')
    file.write(str(optMode) + '\n')
    file.write(str(optSpeed) + '\n')
    file.close()


def strToBool(string):
    """
    converter uma string em boolean
    :param string:
    :return bool:
    """
    return string.lower() == 'true'


def check_som():
    """
    verificar se o som está on se sim da um volume ao playback
    """
    global play_back
    if sound:
        play_back.set_volume(0.2)
    else:
        play_back.set_volume(0)


def loadConfig():
    """
    carregar dados de configuração de sistema
    :return None:
    """
    global sound, optMode, optSpeed
    try:
        file = open('config.txt', mode='r')
    except OSError:
        sound, optMode, optSpeed = True, 1, 2
        return

    dados = file.read().splitlines()
    file.close()
    try:
        if dados[0].lower() in ('true', 'false'):
            sound = strToBool(dados[0])
        else:
            sound = True
    except:
        sound = True
    try:
        if int(dados[1]) in (1, 2):
            optMode = int(dados[1])
        else:
            optMode = 1
    except:
        optMode = 1
    try:
        if int(dados[2]) in (1, 2, 3):
            optSpeed = int(dados[2])
        else:
            optSpeed = 2
    except:
        optSpeed = 2


def menuPause():
    """
    pausar o jogo
    :return dict: 'quit' se desejar sair ou 'resume' se quizer retormar a partida
    """
    global run, mouseOnmove
    quit_rect = Rect(274, 351, 111, 36)
    resume_rect = Rect(418, 351, 111, 36)
    paused = sprite.GroupSingle(Item(0, 0, 'paused.png'))
    quit = sprite.GroupSingle(Item(251, 339, 'quit.png'))
    resume = sprite.GroupSingle(Item(406, 339, 'resume.png'))
    opcao = 2
    update = True

    while True:
        clock.tick(30)
        for evento in event.get():
            if evento.type == MOUSEMOTION:
                mouseOnmove = True
                update = True
            if evento.type == KEYDOWN:
                mouseOnmove = False
                update = True
            if evento.type == QUIT:
                run = False
                return {'quit': True, 'resume': False}
        # key events
        keys = key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            if sound:
                som_seta.play()
            time.delay(150)
            opcao = 1
        elif keys[K_RIGHT] or keys[K_d]:
            if sound:
                som_back.play()
            som_seta.play()
            time.delay(150)
            opcao = 2
        elif keys[K_RETURN]:
            if sound:
                som_back.play()
            time.delay(100)
            if opcao == 1:
                return {'quit': True, 'resume': False}
            else:
                return {'quit': False, 'resume': True}
        elif keys[K_SPACE] or keys[K_ESCAPE] or mouse.get_pressed()[2]:
            if sound:
                som_back.play()
            time.delay(300)

            return {'quit': False, 'resume': True}
        # mouse events

        if mouseOnmove:
            ms = mouse.get_pos()
            if quit_rect.collidepoint(ms[0], ms[1]):
                if sound and (opcao != 1):
                    som_seta.play()
                opcao = 1
                if mouse.get_pressed()[0]:
                    if sound:
                        som_back.play()
                    time.delay(100)
                    return {'quit': True, 'resume': False}
            elif resume_rect.collidepoint(ms[0], ms[1]):
                if sound and (opcao != 2):
                    som_seta.play()
                opcao = 2
                if mouse.get_pressed()[0]:
                    if sound:
                        som_back.play()
                    time.delay(100)
                    return {'quit': False, 'resume': True}

        if update:
            paused.clear(screen, estadio)
            quit.clear(screen, estadio)
            resume.clear(screen, estadio)
            atualizarDisplay()
            paused.draw(screen)
            if opcao == 1:
                quit.draw(screen)
            else:
                resume.draw(screen)
            cursor.draw(screen)
            display.update()

        update = False


def tutorial():
    """
    mostrar tutorial na tela
    :return dict: 'quit' se desejar sair ou 'resume' se quizer retormar a partida
    """
    global run, mouseOnmove
    update = True
    tutor = sprite.GroupSingle(Item(0, 0, 'tutorial.png'))
    tutor.draw(screen)
    screen.fill(Color('black'))

    while True:
        clock.tick(30)
        for evento in event.get():
            if evento.type == MOUSEMOTION:
                mouseOnmove = True
                update = True
            if evento.type == KEYDOWN or mouse.get_pressed()[0]:
                if sound:
                    som_back.play()
                time.delay(200)
                mouseOnmove = False
                update = True
                tutor.clear(screen, estadio)
                cursor.clear(screen, estadio)
                return {'quit': False, 'resume': True}
            if evento.type == QUIT:
                run = False
                tutor.clear(screen, estadio)
                cursor.clear(screen, estadio)
                return {'quit': True, 'resume': False}

        if update:
            tutor.clear(screen, screen)
            cursor.clear(screen, screen)
            tutor.draw(screen)
            cursor.update()
            cursor.draw(screen)
            display.update()
        update = False


def credits():
    """
    mostrar creditos na tela
    :return None:
    """
    time.delay(200)
    global run, mouseOnmove
    update = True
    creds = sprite.GroupSingle(Item(0, 0, 'credits.png'))
    creds.draw(screen)
    screen.fill(Color('black'))
    while True:
        clock.tick(30)
        for evento in event.get():
            if evento.type == MOUSEMOTION:
                mouseOnmove = True
                update = True
            if evento.type == KEYDOWN or mouse.get_pressed()[0]:
                if sound:
                    som_back.play()
                time.delay(200)
                mouseOnmove = False
                update = True
                creds.clear(screen, bgmenu_principal)
                cursor.clear(screen, bgmenu_principal)
                return
            if evento.type == QUIT:
                run = False
                creds.clear(screen, bgmenu_principal)
                cursor.clear(screen, bgmenu_principal)
                return

        if update:
            creds.clear(screen, screen)
            cursor.clear(screen, screen)
            creds.draw(screen)
            cursor.update()
            cursor.draw(screen)
            display.update()
        update = False


def menuQuit():
    """
    confirmar saida do jogo
    :return dict: 'quit' se desejar sair ou 'resume' se quizer retormar a partida
    """
    time.delay(200)
    global run, mouseOnmove
    yes_rect = Rect(274, 351, 111, 36)
    no_rect = Rect(418, 351, 111, 36)
    paused = sprite.GroupSingle(Item(0, 0, 'quit_menu.png'))
    yes = sprite.GroupSingle(Item(251, 339, 'yes.png'))
    no = sprite.GroupSingle(Item(406, 339, 'no.png'))
    suicide_emoji = sprite.GroupSingle(Item(668, 511, 'suicide_emoji.png'))
    cool_emoji = sprite.GroupSingle(Item(684, 498, 'cool_emoji.png'))
    text_menu = sprite.GroupSingle(TextMenu('menuprincipal2.png'))
    opcao = 2
    update = True
    while True:
        clock.tick(30)
        for evento in event.get():
            if evento.type == MOUSEMOTION:
                mouseOnmove = True
                update = True
            if evento.type == KEYDOWN:
                mouseOnmove = False
                update = True
            if evento.type == QUIT:
                run = False
                return
        # key events
        keys = key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            if sound:
                som_seta.play()
            time.delay(150)
            opcao = 1
        elif keys[K_RIGHT] or keys[K_d]:
            if sound:
                som_seta.play()
            time.delay(150)
            opcao = 2
        elif keys[K_RETURN]:
            time.delay(100)
            if opcao == 1:
                if sound:
                    som_enter_play.play()
                time.delay(1500)
                run = False
                return
            else:
                if sound:
                    som_back.play()
                return

        # mouse events

        if mouseOnmove:
            ms = mouse.get_pos()
            if yes_rect.collidepoint(ms[0], ms[1]):
                if sound and (opcao != 1):
                    som_seta.play()
                opcao = 1
                if mouse.get_pressed()[0]:
                    if opcao == 1:
                        if sound:
                            som_enter_play.play()
                        time.delay(1500)
                        run = False
                        return
                    else:
                        if sound:
                            som_back.play()
                        return
            elif no_rect.collidepoint(ms[0], ms[1]):
                if sound and (opcao != 2):
                    som_seta.play()
                opcao = 2
                if mouse.get_pressed()[0]:
                    if sound:
                        som_back.play()
                    time.delay(100)
                    return

        if update:
            cursor.update()
            paused.clear(screen, bgmenu_principal)
            cursor.clear(screen, bgmenu_principal)
            yes.clear(screen, bgmenu_principal)
            no.clear(screen, bgmenu_principal)
            cool_emoji.clear(screen, bgmenu_principal)
            suicide_emoji.clear(screen, bgmenu_principal)
            text_menu.clear(screen, bgmenu_principal)

            text_menu.draw(screen)
            paused.draw(screen)

            if opcao == 1:
                yes.draw(screen)
                suicide_emoji.draw(screen)
            else:
                no.draw(screen)
                cool_emoji.draw(screen)
            cursor.draw(screen)
            display.update()

        update = False


def pauseControl():
    """
    verificar se for pressionados os butons de pausa
    :return dict:
    """
    keys = key.get_pressed()
    if keys[K_SPACE] or keys[K_ESCAPE] or mouse.get_pressed()[2]:
        time.delay(200)
        status = menuPause()
        screen.blit(estadio, (0, 0))
        atualizarDisplay()
        display.update()
        return status


def menuFullScore():
    """
    mostrar opcao de sair ou jogar novamente
    :return dict: 'quit' e 'replay'
    """
    global mouseOnmove, run, team_goal
    quit_rect = Rect(274, 351, 111, 36)
    resume_rect = Rect(418, 351, 111, 36)
    fullScore = sprite.GroupSingle(Item(0, 0, 'full_score.png'))
    quit = sprite.GroupSingle(Item(251, 339, 'quit.png'))
    resume = sprite.GroupSingle(Item(406, 339, 'replay.png'))
    label = Label(350, 286, font.SysFont('Arial', 25, True), team_goal.capitalize().replace('_', ' ') + ' Win !',
                  Color('white'))
    label.rect.centerx = 420
    equipa_win = sprite.GroupSingle(label)
    opcao = 2
    update = True
    while True:
        clock.tick(30)
        for evento in event.get():
            if evento.type == MOUSEMOTION:
                mouseOnmove = True
                update = True
            if evento.type == KEYDOWN:
                mouseOnmove = False
                update = True
            if evento.type == QUIT:
                run = False
                return {'quit': True, 'replay': False}

        # key events
        keys = key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            if sound:
                som_seta.play()
            time.delay(150)
            opcao = 1
        elif keys[K_RIGHT] or keys[K_d]:
            if sound:
                som_seta.play()
            time.delay(150)
            opcao = 2
        elif keys[K_RETURN]:
            if sound:
                som_back.play()
            time.delay(200)
            if opcao == 1:
                return {'quit': True, 'replay': False}
            else:
                return {'quit': False, 'replay': True}

        # mouse events

        if mouseOnmove:
            ms = mouse.get_pos()
            if quit_rect.collidepoint(ms[0], ms[1]):
                if sound and (opcao != 1):
                    som_seta.play()
                opcao = 1
                if mouse.get_pressed()[0]:
                    if sound:
                        som_back.play()
                    time.delay(100)
                    return {'quit': True, 'replay': False}
            elif resume_rect.collidepoint(ms[0], ms[1]):
                if sound and (opcao != 2):
                    som_seta.play()
                opcao = 2
                if mouse.get_pressed()[0]:
                    if sound:
                        som_back.play()
                    time.delay(100)
                    return {'quit': False, 'replay': True}
        if update:
            fullScore.clear(screen, estadio)
            quit.clear(screen, estadio)
            resume.clear(screen, estadio)
            equipa_win.clear(screen, estadio)
            atualizarDisplay()
            fullScore.draw(screen)
            equipa_win.draw(screen)

            if opcao == 1:
                quit.draw(screen)
            else:
                resume.draw(screen)
            cursor.draw(screen)
            display.update()

        update = False


def escolherMelhoresJogadasAwayTeam():
    """
    fazer escolha de jogadas possiveis da equipa fora
    :return list: lista de jogadas
    """
    dist_and_player_right = []
    dist_and_player_left = []
    dist_player_right = []
    dist_player_left = []
    gk_area = Rect(597, 228, 162, 222)
    centro_baliza = (737, 339)
    gks_dist = []
    gks = []
    best_way_players_dist = []

    # definir um guarda-redes quando o outro sair em ataque
    for player in away_players:
        player.gk = False
        if player.rect.colliderect(gk_area):
            dis_x = centro_baliza[0] - player.getCenterX()
            dis_y = player.getCenterY() - centro_baliza[1]
            gks_dist.append(hypot(dis_x, dis_y))
            gks.append((hypot(dis_x, dis_y), player))

    if len(gks_dist) != 0:
        gks_dist.sort()
        gks = dict(gks)
        gks[gks_dist[0]].gk = True

    # se bola estiver na area do guarda redes
    for player in away_players:
        if player.gk:
            if bola.sprites()[0].rect.colliderect(gk_area):
                dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
                dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
                distancia = hypot(dis_x, dis_y) + 100
                if dis_x < 0:
                    angulo = atan2(dis_y, dis_x)
                    player.gk = False
                    return [{'player': player, 'ang': angulo, 'dist': distancia}, ]
                elif atan2(dis_y, dis_x) > 0:
                    angulo = atan2(dis_y, dis_x) - radians(20)
                    player.gk = False
                    return [{'player': player, 'ang': angulo, 'dist': distancia}, ]
                elif atan2(dis_y, dis_x) < 0:
                    angulo = atan2(dis_y, dis_x) + radians(20)
                    player.gk = False
                    return [{'player': player, 'ang': angulo, 'dist': distancia}, ]

    # obter distancias de jogadores à direita e à esquerda da bola)
    for player in away_players:
        if player.gk:
            continue
        dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
        dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
        distancia = hypot(dis_x, dis_y)
        if dis_x < 0:
            dist_player_right.append(distancia)
            dist_and_player_right.append((distancia, player))
        elif dis_x > 0:
            dist_player_left.append(distancia)
            dist_and_player_left.append((distancia, player))

    # selecionar melhor jogada quando o jogador está à direita da bola
    if len(dist_player_right) != 0:
        dist_player_right.sort()
        dist_and_player_right = dict(dist_and_player_right)
        playerAux = Player(0, 0, away_players.sprites()[0].equipa)
        for distancia in dist_player_right:
            player = dist_and_player_right[distancia]
            playerAux.setAxis(player.getX(), player.getY())
            dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
            dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
            angulo = atan2(dis_y, dis_x)
            playerAux.setAngulo(angulo)
            playerAux.setVelocity(50)
            while True:
                # atualizarDisplay()
                colisions = playerAux.autoMoveTest(bola, all_players, player, screen)
                if colisions['player'] and colisions['bola']:
                    best_way_players_dist.append({'player': player, 'ang': angulo, 'dist': distancia})
                    print("Solução")
                    break
                elif colisions['bola']:
                    best_way_players_dist.append({'player': player, 'ang': angulo, 'dist': distancia})
                    print("Solução")
                    break
                elif colisions['player']:
                    print("Colisão")
                    break

    # selecionar melhor jogada quando o jogador está à esquerda da bola
    if len(dist_player_left) != 0:
        dist_player_left.sort()
        dist_and_player_left = dict(dist_and_player_left)
        playerAux = Player(0, 0, away_players.sprites()[0].equipa)
        for distancia in dist_player_left:
            player = dist_and_player_left[distancia]
            playerAux.setAxis(player.getX(), player.getY())
            dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
            dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
            angulo = atan2(dis_y, dis_x)
            playerAux.setAngulo(angulo)
            playerAux.setVelocity(50)
            while True:
                # atualizarDisplay()
                colisions = playerAux.autoMoveTest(bola, all_players, player, screen)
                if colisions['player'] and colisions['bola']:
                    if distancia < 100:
                        best_way_players_dist.append(
                            {'player': player, 'ang': angulo + radians(choice([20, -20])), 'dist': distancia - 50})
                    else:
                        best_way_players_dist.append(
                            {'player': player, 'ang': angulo + radians(choice([10, -10])), 'dist': distancia - 50})
                    print("Solução")
                    break
                elif colisions['bola']:
                    if distancia < 100:
                        best_way_players_dist.append(
                            {'player': player, 'ang': angulo + radians(choice([20, -20])), 'dist': distancia - 50})
                    else:
                        best_way_players_dist.append(
                            {'player': player, 'ang': angulo + radians(choice([10, -10])), 'dist': distancia - 50})
                    print("Solução")
                    break
                elif colisions['player']:
                    print("Colisão")
                    break

    # um players à direita da bola sem melhor solucao
    if len(dist_player_right) != 0:
        dist_player_right.sort()
        dist_and_player_right = dict(dist_and_player_right)
        distancia = dist_player_right[0]
        player = dist_and_player_right[distancia]
        dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
        dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
        angulo = atan2(dis_y, dis_x)
        best_way_players_dist.append({'player': player, 'ang': angulo, 'dist': distancia})

    # um players à esquerda da bola sem melhor solucao
    if len(dist_player_left) != 0:
        dist_player_left.sort()
        dist_and_player_left = dict(dist_and_player_left)
        distancia = dist_player_left[0]
        player = dist_and_player_left[distancia]
        dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
        dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
        angulo = atan2(dis_y, dis_x)
        if distancia < 100:
            best_way_players_dist.append(
                {'player': player, 'ang': angulo + radians(choice([20, -20])), 'dist': distancia - 50})
        else:
            best_way_players_dist.append(
                {'player': player, 'ang': angulo + radians(choice([10, -10])), 'dist': distancia - 50})
    return best_way_players_dist


def escolherMelhoresJogadasHomeTeam():
    """
    fazer escolha de jogadas possiveis da equipa casa
    :return list de jogadas:
    """
    dist_and_player_right = []
    dist_and_player_left = []
    dist_player_right = []
    dist_player_left = []
    gk_area = Rect(39, 228, 162, 222)
    centro_baliza = (63, 339)
    gks_dist = []
    gks = []
    best_way_players_dist = []

    # definir um guarda-redes quando o outro sair em ataque
    for player in home_players:
        player.gk = False
        if player.rect.colliderect(gk_area):
            dis_x = centro_baliza[0] - player.getCenterX()
            dis_y = player.getCenterY() - centro_baliza[1]
            gks_dist.append(hypot(dis_x, dis_y))
            gks.append((hypot(dis_x, dis_y), player))

    if len(gks_dist) != 0:
        gks_dist.sort()
        gks = dict(gks)
        gks[gks_dist[0]].gk = True

    # se bola estiver na area do guarda redes
    for player in home_players:
        if player.gk:
            if bola.sprites()[0].rect.colliderect(gk_area):
                dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
                dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
                distancia = hypot(dis_x, dis_y) + 100
                if dis_x > 0:
                    angulo = atan2(dis_y, dis_x)
                    player.gk = False
                    return [{'player': player, 'ang': angulo, 'dist': distancia}, ]
                elif atan2(dis_y, dis_x) > 0:
                    angulo = atan2(dis_y, dis_x) - radians(20)
                    player.gk = False
                    return [{'player': player, 'ang': angulo, 'dist': distancia}, ]
                elif atan2(dis_y, dis_x) < 0:
                    angulo = atan2(dis_y, dis_x) + radians(20)
                    player.gk = False
                    return [{'player': player, 'ang': angulo, 'dist': distancia}, ]

    # obter distancias de jogadores à direita e à esquerda da bola)
    for player in home_players:
        if player.gk:
            continue
        dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
        dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
        distancia = hypot(dis_x, dis_y)
        if dis_x < 0:
            dist_player_right.append(distancia)
            dist_and_player_right.append((distancia, player))
        elif dis_x > 0:
            dist_player_left.append(distancia)
            dist_and_player_left.append((distancia, player))

    # selecionar melhor jogada quando o jogador está à esquerda da bola
    if len(dist_player_left) != 0:
        dist_player_left.sort()
        dist_and_player_left = dict(dist_and_player_left)
        playerAux = Player(0, 0, home_players.sprites()[0].equipa)
        for distancia in dist_player_left:
            player = dist_and_player_left[distancia]
            playerAux.setAxis(player.getX(), player.getY())
            dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
            dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
            angulo = atan2(dis_y, dis_x)
            playerAux.setAngulo(angulo)
            playerAux.setVelocity(50)
            while True:
                # atualizarDisplay()
                colisions = playerAux.autoMoveTest(bola, all_players, player, screen)
                if colisions['player'] and colisions['bola']:
                    best_way_players_dist.append({'player': player, 'ang': angulo, 'dist': distancia})
                    print("Solução")
                    break
                elif colisions['bola']:
                    best_way_players_dist.append({'player': player, 'ang': angulo, 'dist': distancia})
                    print("Solução")
                    break
                elif colisions['player']:
                    print("Colisão")
                    break

    # selecionar melhor jogada quando o jogador está à direita da bola
    if len(dist_player_right) != 0:
        dist_player_right.sort()
        dist_and_player_right = dict(dist_and_player_right)
        playerAux = Player(0, 0, home_players.sprites()[0].equipa)
        for distancia in dist_player_right:
            player = dist_and_player_right[distancia]
            playerAux.setAxis(player.getX(), player.getY())
            dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
            dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
            angulo = atan2(dis_y, dis_x)
            playerAux.setAngulo(angulo)
            playerAux.setVelocity(50)
            while True:
                # atualizarDisplay()
                colisions = playerAux.autoMoveTest(bola, all_players, player, screen)
                if colisions['player'] and colisions['bola']:
                    if distancia < 100:
                        best_way_players_dist.append(
                            {'player': player, 'ang': angulo + radians(choice([20, -20])), 'dist': distancia - 50})
                    else:
                        best_way_players_dist.append(
                            {'player': player, 'ang': angulo + radians(choice([10, -10])), 'dist': distancia - 50})
                    print("Solução")
                    break
                elif colisions['bola']:
                    if distancia < 100:
                        best_way_players_dist.append(
                            {'player': player, 'ang': angulo + radians(choice([20, -20])), 'dist': distancia - 50})
                    else:
                        best_way_players_dist.append(
                            {'player': player, 'ang': angulo + radians(choice([10, -10])), 'dist': distancia - 50})
                    print("Solução")
                    break
                elif colisions['player']:
                    print("Colisão")
                    break

    # um players à esquerda da bola sem melhor solucao
    if len(dist_player_left) != 0:
        dist_player_left.sort()
        dist_and_player_left = dict(dist_and_player_left)
        distancia = dist_player_left[0]
        player = dist_and_player_left[distancia]
        dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
        dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
        angulo = atan2(dis_y, dis_x)
        best_way_players_dist.append({'player': player, 'ang': angulo, 'dist': distancia})

    # um players à direita da bola sem melhor solucao
    if len(dist_player_right) != 0:
        dist_player_right.sort()
        dist_and_player_right = dict(dist_and_player_right)
        distancia = dist_player_right[0]
        player = dist_and_player_right[distancia]
        dis_x = bola.sprites()[0].getCenterX() - player.getCenterX()
        dis_y = player.getCenterY() - bola.sprites()[0].getCenterY()
        angulo = atan2(dis_y, dis_x)
        if distancia < 100:
            best_way_players_dist.append(
                {'player': player, 'ang': angulo + radians(choice([20, -20])), 'dist': distancia - 50})
        else:
            best_way_players_dist.append(
                {'player': player, 'ang': angulo + radians(choice([10, -10])), 'dist': distancia - 50})

    return best_way_players_dist


def inteligencia():
    """
    lancar jogada do computador
    :return:
    """
    global pontape_de_saida
    if flag['home']:
        best_jogadas = escolherMelhoresJogadasHomeTeam()
    else:
        best_jogadas = escolherMelhoresJogadasAwayTeam()
    jogada = choice(best_jogadas)
    player, angulo, dist_da_bola = jogada['player'], jogada['ang'], jogada['dist']
    if pontape_de_saida:
        player.setAngulo(angulo + radians(choice(range(-25, 25))))
        pontape_de_saida = False
    else:
        player.setAngulo(angulo)
    if 0 < dist_da_bola < 100:
        vel = 16
    elif 100 < dist_da_bola < 200:
        vel = 20
    elif 200 < dist_da_bola < 300:
        vel = 22
    elif 300 < dist_da_bola < 470:
        vel = 24
    else:
        vel = 25

    showPower(vel)
    atualizarDisplay(cur=False)
    seta.rodar(player.getCenterX(), player.getCenterY(), degrees(player.angulo - pi))
    seta.draw(screen)
    display.update()
    player.setVelocity(vel)
    time.delay(700)
    screen.blit(estadio, (0, 0))
    status = lancarJogadaLoop()
    return status


def criarBola(bola_img):
    """
    criar a bola de jogo
    :param bola_img:  imagem da bola
    """
    bola.empty()
    bola.add(Bola(campo.rect.centerx - 5, campo.rect.centery, bola_img))
    # bola.sprites()[0].setX(700)
    # bola.sprites()[0].setY(campo.rect.centery + 30)


def menuPrincipal():
    """
    menu de escolhas
    :return:
    """
    global run, mouseOnmove
    opcao = 1
    sp = Rect(502, 162, 235, 49)
    mp = Rect(502, 211, 235, 56)
    comp = Rect(502, 267, 235, 55)
    opt = Rect(502, 322, 235, 55)
    crd = Rect(502, 377, 235, 55)
    qt = Rect(502, 432, 235, 55)
    text_menu = sprite.GroupSingle(TextMenu('menuprincipal2.png'))
    selector_menu = sprite.GroupSingle(SelectorMenu(452, sp.y - 25))
    screen.blit(bgmenu_principal, (0, 0))

    while run:
        getEvent(30)
        # key events
        keys = key.get_pressed()
        if keys[K_DOWN] or keys[K_s]:
            if sound:
                som_seta.play()
            time.delay(150)
            if opcao != 6:
                opcao += 1
            else:
                opcao = 1
        elif keys[K_UP] or keys[K_w]:
            if sound:
                som_seta.play()
            time.delay(150)
            if opcao != 1:
                opcao -= 1
            else:
                opcao = 6
        elif keys[K_RETURN] or keys[K_SPACE]:
            if sound:
                som_enter.play()
            return opcao

        # mouse events

        if mouseOnmove:
            ms = mouse.get_pos()
            if sp.collidepoint(ms[0], ms[1]):
                if (opcao != 1) and sound:
                    som_seta.play()
                opcao = 1
                if mouse.get_pressed()[0]:
                    if sound:
                        som_enter.play()
                    return opcao
            elif mp.collidepoint(ms[0], ms[1]):
                if (opcao != 2) and sound:
                    som_seta.play()
                opcao = 2
                if mouse.get_pressed()[0]:
                    if sound:
                        som_enter.play()
                    return opcao
            elif comp.collidepoint(ms[0], ms[1]):
                if (opcao != 3) and sound:
                    som_seta.play()
                opcao = 3
                if mouse.get_pressed()[0]:
                    if sound:
                        som_enter.play()
                    return opcao
            elif opt.collidepoint(ms[0], ms[1]):
                if (opcao != 4) and sound:
                    som_seta.play()
                opcao = 4
                if mouse.get_pressed()[0]:
                    if sound:
                        som_enter.play()
                    return opcao
            elif crd.collidepoint(ms[0], ms[1]):
                if (opcao != 5) and sound:
                    som_seta.play()
                opcao = 5
                if mouse.get_pressed()[0]:
                    if sound:
                        som_enter.play()
                    return opcao
            elif qt.collidepoint(ms[0], ms[1]):
                if (opcao != 6) and sound:
                    som_seta.play()
                opcao = 6
                if mouse.get_pressed()[0]:
                    som_enter.play()
                    return opcao

        if opcao == 1:
            selector_menu.update(sp.y - 25)
        elif opcao == 2:
            selector_menu.update(mp.y - 15)
        elif opcao == 3:
            selector_menu.update(comp.y - 15)
        elif opcao == 4:
            selector_menu.update(opt.y - 15)
        elif opcao == 5:
            selector_menu.update(crd.y - 15)
        elif opcao == 6:
            selector_menu.update(qt.y - 15)

        cursor.clear(screen, bgmenu_principal)
        text_menu.clear(screen, bgmenu_principal)
        selector_menu.clear(screen, bgmenu_principal)
        selector_menu.draw(screen)
        text_menu.draw(screen)
        cursor.update()
        cursor.draw(screen)
        display.update()


def menuOptions():
    """
    menu de opcoes de configuracao do jogo
    :return:
    """
    global sound, bola, estadio, optMode, optSpeed
    time.delay(100)
    posicao = 1
    sound_button = Rect(629, 98, 67, 26)
    prev_mode = Rect(506, 202, 26, 26)
    next_mode = Rect(680, 202, 26, 26)
    prev_speed = Rect(506, 349, 29, 24)
    next_speed = Rect(680, 349, 26, 26)
    okay = Rect(508, 451, 55, 33)
    seta_posicao = sprite.GroupSingle(Item(400, 98, 'seta_posicao.png'))
    seta_prev_on_mode = sprite.GroupSingle(Item(500, 199, 'setaleft.png'))
    seta_next_on_mode = sprite.GroupSingle(Item(673, 199, 'setaright.png'))
    seta_prev_on_speed = sprite.GroupSingle(Item(502, 345, 'setaleft.png'))
    seta_next_on_speed = sprite.GroupSingle(Item(675, 345, 'setaright.png'))
    okay_on = sprite.GroupSingle(Item(500, 444, 'okay.png'))
    sound_on = sprite.GroupSingle(Item(617, 91, 'on.png'))
    sound_off = sprite.GroupSingle(Item(617, 91, 'off.png'))
    text_menu = sprite.GroupSingle(TextMenu('menuopt.png'))
    pos_seta = [91, 144, 272, 446]
    mode_view = [sprite.GroupSingle(Item(555, 198, 'normal.png')),
                 sprite.GroupSingle(Item(555, 198, 'smart.png'))]
    speed_view = [sprite.GroupSingle(Item(553, 340, 'slow.png')), sprite.GroupSingle(Item(553, 340, 'normal.png')),
                  sprite.GroupSingle(Item(553, 340, 'fast.png'))]

    screen.blit(bgmenu_principal, (0, 0))

    while run:
        print(vels_de_jogo[optSpeed])
        getEvent(30)
        check_som()
        if not sound:
            som_intro.set_volume(0)
        text_menu.clear(screen, bgmenu_principal)
        cursor.clear(screen, bgmenu_principal)
        text_menu.draw(screen)
        seta_posicao.clear(screen, bgmenu_principal)

        # key events
        keys = key.get_pressed()
        if keys[K_DOWN] or keys[K_s]:
            if sound:
                som_seta.play()
            time.delay(200)
            seta_posicao.clear(screen, bgmenu_principal)
            if posicao != 4:
                posicao += 1
            else:
                posicao = 1
            seta_posicao.update(400, pos_seta[posicao - 1])
        elif keys[K_UP] or keys[K_w]:
            if sound:
                som_seta.play()
            time.delay(200)
            seta_posicao.clear(screen, bgmenu_principal)
            if posicao != 1:
                posicao -= 1
            else:
                posicao = 4
            seta_posicao.update(400, pos_seta[posicao - 1])
        elif keys[K_RIGHT] or keys[K_d]:
            if sound:
                som_seta.play()
            if posicao == 2:
                seta_next_on_mode.draw(screen)
                display.update(seta_next_on_mode.sprites()[0].rect)
                time.delay(200)
                seta_next_on_mode.clear(screen, bgmenu_principal)
                if optMode != 2:
                    optMode += 1
            elif posicao == 3:
                seta_next_on_speed.draw(screen)
                display.update(seta_next_on_speed.sprites()[0].rect)
                time.delay(200)
                seta_next_on_speed.clear(screen, bgmenu_principal)
                if optSpeed != 3:
                    optSpeed += 1
        elif keys[K_LEFT] or keys[K_a]:
            if sound:
                som_seta.play()
            if posicao == 2:
                seta_prev_on_mode.draw(screen)
                display.update(seta_prev_on_mode.sprites()[0].rect)
                time.delay(200)
                seta_prev_on_mode.clear(screen, bgmenu_principal)
                if optMode != 1:
                    optMode -= 1
            elif posicao == 3:
                seta_prev_on_speed.draw(screen)
                display.update(seta_prev_on_speed.sprites()[0].rect)
                time.delay(200)
                seta_prev_on_speed.clear(screen, bgmenu_principal)
                if optSpeed != 1:
                    optSpeed -= 1
        elif keys[K_RETURN] or keys[K_SPACE]:
            if posicao == 1:
                som_enter.play()
                time.delay(150)
                if sound:
                    sound = False
                else:
                    sound = True
            elif posicao == 4:
                if sound:
                    som_enter.play()
                okay_on.draw(screen)
                display.update(okay_on.sprites()[0].rect)
                time.delay(400)
                return
        elif keys[K_ESCAPE] or keys[K_BACKSPACE]:
            if sound:
                som_back.play()
            okay_on.draw(screen)
            display.update(okay_on.sprites()[0].rect)
            time.delay(400)
            return

        # mouse events
        ms = mouse.get_pos()
        if sound_button.collidepoint(ms[0], ms[1]):
            if mouse.get_pressed()[0]:
                if sound:
                    som_seta.play()
                time.delay(200)
                if sound:
                    sound = False
                else:
                    sound = True
        elif prev_mode.collidepoint(ms[0], ms[1]):
            seta_prev_on_mode.clear(screen, bgmenu_principal)
            seta_prev_on_mode.draw(screen)
            if mouse.get_pressed()[0]:
                if sound:
                    som_seta.play()
                time.delay(200)
                if optMode != 1:
                    optMode -= 1
        elif next_mode.collidepoint(ms[0], ms[1]):
            seta_next_on_mode.clear(screen, bgmenu_principal)
            seta_next_on_mode.draw(screen)
            if mouse.get_pressed()[0]:
                if sound:
                    som_seta.play()
                time.delay(200)
                if optMode != 2:
                    optMode += 1
        elif prev_speed.collidepoint(ms[0], ms[1]):
            seta_prev_on_speed.clear(screen, bgmenu_principal)
            seta_prev_on_speed.draw(screen)
            if mouse.get_pressed()[0]:
                if sound:
                    som_seta.play()
                time.delay(200)
                if optSpeed != 1:
                    optSpeed -= 1
        elif next_speed.collidepoint(ms[0], ms[1]):
            seta_next_on_speed.clear(screen, bgmenu_principal)
            seta_next_on_speed.draw(screen)
            if mouse.get_pressed()[0]:
                if sound:
                    som_seta.play()
                time.delay(200)
                if optSpeed != 3:
                    optSpeed += 1
        elif okay.collidepoint(ms[0], ms[1]):
            okay_on.clear(screen, bgmenu_principal)
            okay_on.draw(screen)
            if mouse.get_pressed()[0]:
                if sound:
                    som_back.play()
                time.delay(250)
                return

        if sound:
            sound_on.clear(screen, bgmenu_principal)
            sound_on.draw(screen)
        else:
            sound_off.clear(screen, bgmenu_principal)
            sound_off.draw(screen)

        for i in range(3)[1:]:
            if optMode == i:
                mode_view[i - 1].clear(screen, bgmenu_principal)
                mode_view[i - 1].draw(screen)
                break

        for i in range(4)[1:]:
            if optSpeed == i:
                speed_view[i - 1].clear(screen, bgmenu_principal)
                speed_view[i - 1].draw(screen)
                break

        seta_posicao.draw(screen)
        cursor.update()
        cursor.draw(screen)
        display.update()


def menuTeam():
    """
    menu de escolha de equipas
    :return:
    """
    time.delay(200)
    global bola, mouseOnmove, casa, fora, run
    home_team, away_team = casa, fora
    bg_menu_team = image.load('data/backgrounds/bg_menu_equipa.jpg')
    posicao = 1
    # rects
    back_zone = Rect(37, 547, 114, 40)
    next_zone = Rect(652, 547, 114, 40)
    home_zone = Rect(61, 150, 313, 363)
    away_zone = Rect(433, 150, 313, 363)
    prev_home_team_zone = Rect(200, 172, 35, 26)
    next_home_team_zone = Rect(200, 431, 35, 26)
    prev_away_team_zone = Rect(579, 172, 30, 26)
    next_away_team_zone = Rect(579, 431, 30, 26)
    # images
    selector = sprite.GroupSingle(Item(61, 150, 'selector_team.png'))
    seta_prev_home_team = sprite.GroupSingle(Item(202, 167, 'seta_up.png'))
    seta_next_home_team = sprite.GroupSingle(Item(202, 424, 'seta_down.png'))
    seta_prev_away_team = sprite.GroupSingle(Item(574, 166, 'seta_up.png'))
    seta_next_away_team = sprite.GroupSingle(Item(574, 424, 'seta_down.png'))
    next_button = sprite.GroupSingle(Item(624, 528, 'next_button.png'))
    back_button = sprite.GroupSingle(Item(8, 528, 'back_button.png'))
    pos_selector = (61, 433)

    home_team_view = []
    away_team_view = []
    for i in range(33):
        home_team_view.append(sprite.GroupSingle(Item(113, 219, nomes_equipas[i] + '.png')))
    for i in range(33):
        away_team_view.append(sprite.GroupSingle(Item(493, 219, nomes_equipas[i] + '.png')))

    screen.blit(bg_menu_team, (0, 0))
    info = sprite.GroupSingle(
        Label(235, 560, font.SysFont('Comic Sans MS', 20), 'Back: esc/backspace       Next: enter', Color('white'),
              Color('black')))

    while True:
        clock.tick(30)
        for evento in event.get():
            if evento.type == MOUSEMOTION:
                mouseOnmove = True
            if evento.type == KEYDOWN:
                mouseOnmove = False
            if evento.type == QUIT:
                run = False
                return {'next': False, 'back': True,
                        'equipas': (nomes_equipas[home_team - 1], nomes_equipas[away_team - 1])}

        cursor.clear(screen, bg_menu_team)
        info.clear(screen, bg_menu_team)

        # keys events
        keys = key.get_pressed()
        if keys[K_RIGHT] or keys[K_d]:
            if sound:
                som_seta.play()
            if posicao == 1:
                time.delay(100)
                posicao = 2
                selector.clear(screen, bg_menu_team)
                selector.update(pos_selector[posicao - 1], 150)
        elif keys[K_LEFT] or keys[K_a]:
            if sound:
                som_seta.play()
            if posicao == 2:
                time.delay(100)
                selector.clear(screen, bg_menu_team)
                posicao = 1
                selector.update(pos_selector[posicao - 1], 150)
        elif keys[K_UP] or keys[K_w]:
            if sound:
                som_seta.play()
            if posicao == 1:
                seta_prev_home_team.draw(screen)
                display.update(seta_prev_home_team.sprites()[0].rect)
                time.delay(150)
                seta_prev_home_team.clear(screen, bg_menu_team)
                if home_team != 1:
                    home_team -= 1
            elif posicao == 2:
                seta_prev_away_team.draw(screen)
                display.update(seta_prev_away_team.sprites()[0].rect)
                time.delay(150)
                seta_prev_away_team.clear(screen, bg_menu_team)
                if away_team != 1:
                    away_team -= 1
        elif keys[K_DOWN] or keys[K_s]:
            if sound:
                som_seta.play()
            if posicao == 1:
                seta_next_home_team.draw(screen)
                display.update(seta_next_home_team.sprites()[0].rect)
                time.delay(150)
                seta_next_home_team.clear(screen, bg_menu_team)
                if home_team != len(nomes_equipas):
                    home_team += 1
            elif posicao == 2:
                seta_next_away_team.draw(screen)
                display.update(seta_next_away_team.sprites()[0].rect)
                time.delay(150)
                seta_next_away_team.clear(screen, bg_menu_team)
                if away_team != len(nomes_equipas):
                    away_team += 1
        elif keys[K_RETURN] or keys[K_KP_ENTER]:
            if sound:
                som_enter.play()
            next_button.draw(screen)
            display.update(next_button.sprites()[0].rect)
            time.delay(100)
            casa, fora = home_team, away_team
            return {'next': True, 'back': False,
                    'equipas': (nomes_equipas[home_team - 1], nomes_equipas[away_team - 1])}

        elif keys[K_ESCAPE] or keys[K_BACKSPACE]:
            if sound:
                som_back.play()
            back_button.draw(screen)
            display.update(back_button.sprites()[0].rect)
            time.delay(100)
            casa, fora = home_team, away_team
            return {'next': False, 'back': True,
                    'equipas': (nomes_equipas[home_team - 1], nomes_equipas[away_team - 1])}

        for i in range(len(nomes_equipas) + 1)[1:]:
            if home_team == i:
                home_team_view[i - 1].clear(screen, bg_menu_team)
                break
        for i in range(len(nomes_equipas) + 1)[1:]:
            if away_team == i:
                away_team_view[i - 1].clear(screen, bg_menu_team)
                break

        selector.clear(screen, bg_menu_team)
        selector.draw(screen)

        # mouse events
        if mouseOnmove:
            ms = mouse.get_pos()
            if home_zone.collidepoint(ms[0], ms[1]):
                if sound and (posicao != 1):
                    som_seta.play()
                if posicao == 2:
                    posicao = 1
                    selector.clear(screen, bg_menu_team)
                    selector.update(pos_selector[posicao - 1], 150)
            elif away_zone.collidepoint(ms[0], ms[1]):
                if sound and (posicao != 2):
                    som_seta.play()
                if posicao == 1:
                    posicao = 2
                    selector.clear(screen, bg_menu_team)
                    selector.update(pos_selector[posicao - 1], 150)
            if prev_home_team_zone.collidepoint(ms[0], ms[1]):
                seta_prev_home_team.clear(screen, bg_menu_team)
                seta_prev_home_team.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_seta.play()
                    seta_prev_home_team.draw(screen)
                    cursor.draw(screen)
                    display.update(seta_prev_home_team.sprites()[0].rect)
                    time.delay(150)
                    seta_prev_home_team.clear(screen, bg_menu_team)
                    if home_team != 1:
                        home_team -= 1
            elif prev_away_team_zone.collidepoint(ms[0], ms[1]):
                seta_prev_away_team.clear(screen, bg_menu_team)
                seta_prev_away_team.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_seta.play()
                    seta_prev_away_team.draw(screen)
                    cursor.draw(screen)
                    display.update(seta_prev_away_team.sprites()[0].rect)
                    time.delay(150)
                    seta_prev_away_team.clear(screen, bg_menu_team)
                    if away_team != 1:
                        away_team -= 1
            elif next_home_team_zone.collidepoint(ms[0], ms[1]):
                seta_next_home_team.clear(screen, bg_menu_team)
                seta_next_home_team.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_seta.play()
                    seta_next_home_team.draw(screen)
                    cursor.draw(screen)
                    display.update(seta_next_home_team.sprites()[0].rect)
                    time.delay(150)
                    seta_next_home_team.clear(screen, bg_menu_team)
                    if home_team != len(nomes_equipas):
                        home_team += 1
            elif next_away_team_zone.collidepoint(ms[0], ms[1]):
                seta_next_away_team.clear(screen, bg_menu_team)
                seta_next_away_team.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_seta.play()
                    seta_next_away_team.draw(screen)
                    cursor.draw(screen)
                    display.update(seta_next_away_team.sprites()[0].rect)
                    time.delay(150)
                    seta_next_away_team.clear(screen, bg_menu_team)
                    if away_team != len(nomes_equipas):
                        away_team += 1
            elif next_zone.collidepoint(ms[0], ms[1]):
                next_button.clear(screen, bg_menu_team)
                next_button.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_enter.play()
                    time.delay(10)
                    casa, fora = home_team, away_team
                    return {'next': True, 'back': False,
                            'equipas': (nomes_equipas[home_team - 1], nomes_equipas[away_team - 1])}
            elif back_zone.collidepoint(ms[0], ms[1]):
                back_button.clear(screen, bg_menu_team)
                back_button.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_back.play()
                    time.delay(100)
                    casa, fora = home_team, away_team
                    return {'next': False, 'back': True,
                            'equipas': (nomes_equipas[home_team - 1], nomes_equipas[away_team - 1])}
            else:
                next_button.clear(screen, bg_menu_team)
                back_button.clear(screen, bg_menu_team)

        for i in range(len(nomes_equipas) + 1)[1:]:
            if home_team == i:
                home_team_view[i - 1].draw(screen)
                break
        for i in range(len(nomes_equipas) + 1)[1:]:
            if away_team == i:
                away_team_view[i - 1].draw(screen)
                break

        info.draw(screen)
        cursor.update()
        cursor.draw(screen)
        display.update()


def menuBallStadium():
    """
    menu de escolha de bola e estadio
    :return:
    """
    time.delay(200)
    global bola, mouseOnmove, num_bal, num_stadium, run
    balls, stadiums = num_bal, num_stadium
    bg_menu_b_s = image.load('data/backgrounds/bg_menu_ball_stadium.jpg')
    posicao = 1
    # rects
    back_zone = Rect(37, 547, 114, 32)
    next_zone = Rect(652, 547, 114, 32)
    ball_zone = Rect(61, 150, 313, 363)
    stadium_zone = Rect(433, 150, 313, 363)
    prev_ball_zone = Rect(200, 172, 24, 26)
    next_ball_zone = Rect(200, 431, 24, 26)
    prev_stadium_zone = Rect(579, 172, 24, 26)
    next_stadium_zone = Rect(579, 431, 24, 26)
    # images
    selector = sprite.GroupSingle(Item(61, 150, 'selector_team.png'))
    seta_prev_ball = sprite.GroupSingle(Item(202, 167, 'seta_up.png'))
    seta_next_ball = sprite.GroupSingle(Item(202, 424, 'seta_down.png'))
    seta_prev_stadium = sprite.GroupSingle(Item(574, 166, 'seta_up.png'))
    seta_next_stadium = sprite.GroupSingle(Item(574, 424, 'seta_down.png'))
    next_button = sprite.GroupSingle(Item(624, 528, 'next_button.png'))
    back_button = sprite.GroupSingle(Item(8, 528, 'back_button.png'))
    pos_selector = (61, 433)

    ball_view = []
    stadium_view = []
    for i in range(len(nomes_bolas)):
        ball_view.append(sprite.GroupSingle(Item(137, 231, nomes_bolas[i] + '.png')))
    for i in range(len(nomes_estadios)):
        stadium_view.append(sprite.GroupSingle(Item(462, 218, nomes_estadios[i] + '.png')))

    screen.blit(bg_menu_b_s, (0, 0))
    info = sprite.GroupSingle(
        Label(235, 560, font.SysFont('Comic Sans MS', 20), 'Back: esc/backspace       Next: enter', Color('white'),
              Color('black')))

    while True:
        clock.tick(30)
        for evento in event.get():
            if evento.type == MOUSEMOTION:
                mouseOnmove = True
            if evento.type == KEYDOWN:
                mouseOnmove = False
            if evento.type == QUIT:
                run = False
                return {'next': False, 'back': True, 'bola': nomes_bolas[balls - 1],
                        'estadio': nomes_estadios[stadiums - 1]}

        cursor.clear(screen, bg_menu_b_s)
        info.clear(screen, bg_menu_b_s)

        # keys events
        keys = key.get_pressed()
        if keys[K_RIGHT] or keys[K_d]:
            if sound:
                som_seta.play()
            if posicao == 1:
                time.delay(100)
                posicao = 2
                selector.clear(screen, bg_menu_b_s)
                selector.update(pos_selector[posicao - 1], 150)
        elif keys[K_LEFT] or keys[K_a]:
            if sound:
                som_seta.play()
            if posicao == 2:
                time.delay(100)
                selector.clear(screen, bg_menu_b_s)
                posicao = 1
                selector.update(pos_selector[posicao - 1], 150)
        elif keys[K_UP] or keys[K_w]:
            if sound:
                som_seta.play()
            if posicao == 1:
                seta_prev_ball.draw(screen)
                display.update(seta_prev_ball.sprites()[0].rect)
                time.delay(150)
                seta_prev_ball.clear(screen, bg_menu_b_s)
                if balls != 1:
                    balls -= 1
            elif posicao == 2:
                seta_prev_stadium.draw(screen)
                display.update(seta_prev_stadium.sprites()[0].rect)
                time.delay(150)
                seta_prev_stadium.clear(screen, bg_menu_b_s)
                if stadiums != 1:
                    stadiums -= 1
        elif keys[K_DOWN] or keys[K_s]:
            if sound:
                som_seta.play()
            if posicao == 1:
                seta_next_ball.draw(screen)
                display.update(seta_next_ball.sprites()[0].rect)
                time.delay(150)
                seta_next_ball.clear(screen, bg_menu_b_s)
                if balls != len(nomes_bolas):
                    balls += 1
            elif posicao == 2:
                seta_next_stadium.draw(screen)
                display.update(seta_next_stadium.sprites()[0].rect)
                time.delay(150)
                seta_next_stadium.clear(screen, bg_menu_b_s)
                if stadiums != len(nomes_estadios):
                    stadiums += 1
        elif keys[K_RETURN]:
            if sound:
                som_enter_play.play()
            next_button.draw(screen)
            display.update(next_button.sprites()[0].rect)
            time.delay(100)
            num_bal, num_stadium = balls, stadiums
            return {'next': True, 'back': False, 'bola': nomes_bolas[balls - 1],
                    'estadio': nomes_estadios[stadiums - 1]}

        elif keys[K_ESCAPE] or keys[K_BACKSPACE]:
            if sound:
                som_back.play()
            back_button.draw(screen)
            display.update(back_button.sprites()[0].rect)
            time.delay(0)
            num_bal, num_stadium = balls, stadiums
            return {'next': False, 'back': True, 'bola': nomes_bolas[balls - 1],
                    'estadio': nomes_estadios[stadiums - 1]}

        for i in range(len(nomes_bolas) + 1)[1:]:
            if balls == i:
                ball_view[i - 1].clear(screen, bg_menu_b_s)
                break
        for i in range(len(nomes_estadios) + 1)[1:]:
            if stadiums == i:
                stadium_view[i - 1].clear(screen, bg_menu_b_s)
                break

        selector.clear(screen, bg_menu_b_s)
        selector.draw(screen)

        # mouse events
        if mouseOnmove:
            ms = mouse.get_pos()
            if ball_zone.collidepoint(ms[0], ms[1]):
                if sound and (posicao == 2):
                    som_seta.play()
                if posicao == 2:
                    posicao = 1
                    selector.clear(screen, bg_menu_b_s)
                    selector.update(pos_selector[posicao - 1], 150)
            elif stadium_zone.collidepoint(ms[0], ms[1]):
                if sound and (posicao == 1):
                    som_seta.play()
                if posicao == 1:
                    posicao = 2
                    selector.clear(screen, bg_menu_b_s)
                    selector.update(pos_selector[posicao - 1], 150)
            if prev_ball_zone.collidepoint(ms[0], ms[1]):
                seta_prev_ball.clear(screen, bg_menu_b_s)
                seta_prev_ball.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_seta.play()
                    seta_prev_ball.draw(screen)
                    cursor.draw(screen)
                    display.update(seta_prev_ball.sprites()[0].rect)
                    time.delay(150)
                    seta_prev_ball.clear(screen, bg_menu_b_s)
                    if balls != 1:
                        balls -= 1
            elif prev_stadium_zone.collidepoint(ms[0], ms[1]):
                seta_prev_stadium.clear(screen, bg_menu_b_s)
                seta_prev_stadium.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_seta.play()
                    seta_prev_stadium.draw(screen)
                    cursor.draw(screen)
                    display.update(seta_prev_stadium.sprites()[0].rect)
                    time.delay(150)
                    seta_prev_stadium.clear(screen, bg_menu_b_s)
                    if stadiums != 1:
                        stadiums -= 1
            elif next_ball_zone.collidepoint(ms[0], ms[1]):
                seta_next_ball.clear(screen, bg_menu_b_s)
                seta_next_ball.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_seta.play()
                    seta_next_ball.draw(screen)
                    cursor.draw(screen)
                    display.update(seta_next_ball.sprites()[0].rect)
                    time.delay(150)
                    seta_next_ball.clear(screen, bg_menu_b_s)
                    if balls != len(nomes_bolas):
                        balls += 1
            elif next_stadium_zone.collidepoint(ms[0], ms[1]):
                seta_next_stadium.clear(screen, bg_menu_b_s)
                seta_next_stadium.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_seta.play()
                    seta_next_stadium.draw(screen)
                    cursor.draw(screen)
                    display.update(seta_next_stadium.sprites()[0].rect)
                    time.delay(150)
                    seta_next_stadium.clear(screen, bg_menu_b_s)
                    if stadiums != len(nomes_estadios):
                        stadiums += 1
            elif next_zone.collidepoint(ms[0], ms[1]):
                next_button.clear(screen, bg_menu_b_s)
                next_button.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_enter_play.play()
                    time.delay(200)
                    num_bal, num_stadium = balls, stadiums
                    return {'next': True, 'back': False, 'bola': nomes_bolas[balls - 1],
                            'estadio': nomes_estadios[stadiums - 1]}
            elif back_zone.collidepoint(ms[0], ms[1]):
                back_button.clear(screen, bg_menu_b_s)
                back_button.draw(screen)
                if mouse.get_pressed()[0]:
                    if sound:
                        som_back.play()
                    time.delay(0)
                    num_bal, num_stadium = balls, stadiums
                    return {'next': False, 'back': True, 'bola': nomes_bolas[balls - 1],
                            'estadio': nomes_estadios[stadiums - 1]}
            else:
                next_button.clear(screen, bg_menu_b_s)
                back_button.clear(screen, bg_menu_b_s)

        for i in range(len(nomes_bolas) + 1)[1:]:
            if balls == i:
                ball_view[i - 1].draw(screen)
                break
        for i in range(len(nomes_estadios) + 1)[1:]:
            if stadiums == i:
                stadium_view[i - 1].draw(screen)
                break

        info.draw(screen)
        cursor.update()
        cursor.draw(screen)
        display.update()


def resetVel():
    global bola, all_players
    bola.sprites()[0].setVelocity(0)
    for player in all_players:
        player.setVelocity(0)


def goal():
    global bola, pontape_de_saida, team_goal, sound
    status = bola.sprites()[0].status
    if status['golo']:
        if status['b_left']:
            team_goal = away_players.sprites()[0].equipa
            score['away'] += 1
            flag['home'], flag['away'] = True, False
        elif status['b_right']:
            team_goal = home_players.sprites()[0].equipa
            score['home'] += 1
            flag['home'], flag['away'] = False, True
        bola.sprites()[0].resetStatus()
        pontape_de_saida = True

        return True


def flagControlSelAnimation():
    global flag_anim, animthread
    if flag_anim:
        flag_anim = False
    else:
        flag_anim = True


def atualizarAnimacao():
    selectAux = sprite.Group()
    if flag_anim:
        if flag['home']:
            for player in home_players:
                sel = SelecaoPlayer()
                sel.update(player.getAxis())
                selectAux.add(sel)
        elif flag['away']:
            for player in away_players:
                sel = SelecaoPlayer()
                sel.update(player.getAxis())
                selectAux.add(sel)

    clearAll()
    selectAux.draw(screen)
    drawAll()
    showLines()
    display.update()
    selectAux.clear(screen, estadio)


def showLines():
    """
    mostrar linhas do campo na tela
    """
    global show_lines
    if show_lines:
        lateralCima = Linhas(48, 122, 700, 9, Color('red'))
        lateralBaixo = Linhas(48, 539, 700, 9, Color('red'))
        fundoCimaEsq = Linhas(66, 113, 3, 166, Color('blue'))
        fundoBaixoEsq = Linhas(66, 397, 3, 166, Color('blue'))
        fundoCimaDir = Linhas(730, 113, 3, 166, Color('blue'))
        fundoBaixoDir = Linhas(730, 397, 3, 166, Color('blue'))
        fundoBalizaDir = Linhas(758, 244, 9, 185, Color('blue'))
        fundoBalizaEsq = Linhas(27, 244, 9, 185, Color('blue'))
        lateralCimaBalizaEsq = Linhas(20, 277, 45, 3, Color('blue'))
        lateralBaixoBalizaEsq = Linhas(20, 397, 45, 3, Color('blue'))
        lateralCimaBalizaDir = Linhas(733, 277, 45, 3, Color('blue'))
        lateralBaixoBalizaDir = Linhas(733, 397, 45, 3, Color('blue'))
        ballZoneEsq = Linhas(27, 268, 27, 140, Color('yellow'))
        ballZoneDir = Linhas(744, 268, 27, 140, Color('yellow'))
        lateralCima.draw(screen)
        lateralBaixo.draw(screen)
        fundoCimaEsq.draw(screen)
        fundoBaixoEsq.draw(screen)
        fundoCimaDir.draw(screen)
        fundoBaixoDir.draw(screen)
        ballZoneEsq.draw(screen)
        ballZoneDir.draw(screen)
        fundoBalizaDir.draw(screen)
        fundoBalizaEsq.draw(screen)
        lateralCimaBalizaEsq.draw(screen)
        lateralBaixoBalizaEsq.draw(screen)
        lateralCimaBalizaDir.draw(screen)
        lateralBaixoBalizaDir.draw(screen)


def criarPlayers(equipas):
    """
    criar os jogadores das duas equipas
    :param equipas: tuple de strings
    """
    placar_labels.empty()
    placar_labels.add(
        Label(173, 60, font.SysFont('Arial', 18, True), equipas[0].capitalize().replace('_', ' '), Color('white')))
    placar_labels.add(
        Label(526, 60, font.SysFont('Arial', 18, True), equipas[1].capitalize().replace('_', ' '), Color('white')))

    home_ofensive = [(322, 319), (241, 220), (241, 422), (190, 319), (71, 319)]
    home_defensive = [(283, 321), (190, 253), (190, 390), (190, 319), (71, 319)]
    away_defensive = [(475, 321), (570, 253), (570, 390), (570, 319), (687, 319)]
    away_ofensive = [(436, 319), (517, 220), (517, 422), (570, 319), (687, 319)]

    all_players.empty()
    home_players.empty()
    away_players.empty()

    if flag['home']:
        positions = (home_ofensive, away_defensive)
    else:
        positions = (home_defensive, away_ofensive)

    for pos in positions[0]:
        home_players.add(Player(pos[0], pos[1], equipas[0], smart=smart_mod[optMode]))
    for pos in positions[1]:
        away_players.add(Player(pos[0], pos[1], equipas[1], smart=smart_mod[optMode]))

    home_players.sprites()[-1].gk = True
    away_players.sprites()[-1].gk = True

    for player in home_players:
        all_players.add(player)
    for player in away_players:
        all_players.add(player)


def getSelectedPlayer():
    """
    retorna o jogador selecionado pelo mouse
    :return Class Player:
    """
    if flag['home']:
        for player in home_players:
            if player.isSelected:
                return player
    elif flag['away']:
        for player in away_players:
            if player.isSelected:
                return player


def disselectAllPlayer():
    """
    descelecionar todos os jogadores
    """
    for player in all_players:
        player.isSelected = False


def atualizarDisplay(cur=True):
    """
    atualizar a tela
    :param cur: refere ao cursor
    """
    clearAll()
    drawAll(cur=cur)
    showLines()
    for p in all_players:
        if p.vel > 1:
            draw.rect(screen, Color('gold'), p.rect, 1)


def getEvent(fps):
    """
    obter eventos basicos do pygame
    :param fps: velocidade de execucao do trexo de codigo
    """
    global run, mouseOnmove, update
    clock.tick(fps)
    for evento in event.get():
        if evento.type == QUIT:
            run = False
            # update = True
        if evento.type == MOUSEMOTION:
            mouseOnmove = True
            # update = True
        if evento.type == KEYDOWN:
            mouseOnmove = False
            # update = True


def mouseOverPlayer():
    """
    verificar se o mouse está a colidir com um jogador
    :return: bool
    """
    for player in all_players:
        if player.rect.collidepoint(mouse.get_pos()):
            player.isSelected = True
            return True


def emMovimento():
    """
    verifica se o jogo ainda está a decorrer
    :return: bool
    """
    for player in all_players:
        if player.vel > 1 or bola.sprites()[0].vel > 1:
            return True
    return False


def changeFlag():
    """
    trocar a flag (casa e fora)
    """
    global flag
    if flag['home']:
        flag['home'], flag['away'] = False, True
    elif flag['away']:
        flag['home'], flag['away'] = True, False


def multiPlayer():
    """
    jogo de jogador contra jogador
    """
    global estadio, play_back
    while run:
        getEvent(30)
        info_menu_team = menuTeam()
        if not info_menu_team['back']:
            info_menu_b_s = menuBallStadium()
            if info_menu_b_s['back']:
                continue
        else:
            break
        criarPlayers((info_menu_team['equipas']))
        criarBola(info_menu_b_s['bola'])
        estadio = image.load('data/backgrounds/' + info_menu_b_s['estadio'] + '.jpg')
        som_intro.set_volume(0)
        play_back.pause(sound)
        if sound:
            som_clack.play(-1)
        status = tutorial()
        try:
            if status['quit']:
                break
        except:
            pass
        screen.blit(estadio, (0, 0))
        animthread.resume()
        while run:
            getEvent(30)
            atualizarAnimacao()
            status = pauseControl()
            try:
                if status['quit']:
                    break
            except:
                pass
            status = jogar()
            try:
                if status['quit']:
                    break
            except:
                pass

            if status['golo']:
                if score['home'] == 2 or score['away'] == 2:
                    status = menuFullScore()
                    if status['quit']:
                        break
                    else:
                        resetGameStatus()
                        screen.blit(estadio, (0, 0))
                        atualizarDisplay()

                criarPlayers((info_menu_team['equipas']))
                criarBola(info_menu_b_s['bola'])

        animthread.pause()
        resetGameStatus()
        som_clack.stop()
        play_back.play(sound)
        break


def singlePlayer():
    """
    jogo de jogador contra computador
    """
    global estadio
    while run:
        getEvent(30)
        info_menu_team = menuTeam()
        if not info_menu_team['back']:
            info_menu_b_s = menuBallStadium()
            if info_menu_b_s['back']:
                continue
        else:
            break
        criarPlayers((info_menu_team['equipas']))
        criarBola(info_menu_b_s['bola'])
        estadio = image.load('data/backgrounds/' + info_menu_b_s['estadio'] + '.jpg')
        som_intro.set_volume(0)
        play_back.pause(sound)
        if sound:
            som_clack.play(-1)
        status = tutorial()
        try:
            if status['quit']:
                break
        except:
            pass
        screen.blit(estadio, (0, 0))
        animthread.resume()

        while run:
            getEvent(30)
            atualizarAnimacao()
            status = pauseControl()
            try:
                if status['quit']:
                    break
            except:
                pass
            if flag['away']:
                clearAll()
                drawAll(cur=False)
                display.update()
                time.delay(1000)
                status = inteligencia()
                try:
                    if status['quit']:
                        break
                except:
                    pass
            else:
                status = jogar()
                try:
                    if status['quit']:
                        break
                except:
                    pass
            if status['golo']:
                if score['home'] == 2 or score['away'] == 2:
                    status = menuFullScore()
                    if status['quit']:
                        break
                    else:
                        resetGameStatus()
                        screen.blit(estadio, (0, 0))
                        atualizarDisplay()

                criarPlayers((info_menu_team['equipas']))
                criarBola(info_menu_b_s['bola'])

        animthread.pause()
        resetGameStatus()
        som_clack.stop()
        play_back.play(sound)
        break


def computerVScomputer():
    """
    jogo de computador contra computador
    """
    global estadio, flag
    while run:
        getEvent(30)
        info_menu_team = menuTeam()
        if not info_menu_team['back']:
            info_menu_b_s = menuBallStadium()
            if info_menu_b_s['back']:
                continue
        else:
            break
        criarPlayers((info_menu_team['equipas']))
        criarBola(info_menu_b_s['bola'])
        estadio = image.load('data/backgrounds/' + info_menu_b_s['estadio'] + '.jpg')
        som_intro.set_volume(0)
        play_back.pause(sound)
        if sound:
            som_clack.play(-1)
        status = tutorial()
        try:
            if status['quit']:
                break
        except:
            pass
        screen.blit(estadio, (0, 0))
        sprite.GroupSingle(Item(263, 549, 'powerby.png')).draw(screen)
        animthread.resume()
        while run:
            sprite.GroupSingle(Item(263, 549, 'powerby.png')).clear(screen, estadio)
            sprite.GroupSingle(Item(263, 549, 'powerby.png')).draw(screen)
            getEvent(30)
            atualizarAnimacao()
            status = pauseControl()
            try:
                if status['quit']:
                    break
            except:
                pass
            time.delay(1500)
            status = inteligencia()
            try:
                if status['quit']:
                    break
            except:
                pass
            if status['golo']:
                if score['home'] == 2 or score['away'] == 2:
                    status = menuFullScore()
                    if status['quit']:
                        break
                    else:
                        resetGameStatus()
                        screen.blit(estadio, (0, 0))
                        atualizarDisplay()

                criarPlayers((info_menu_team['equipas']))
                criarBola(info_menu_b_s['bola'])

        animthread.pause()
        resetGameStatus()
        som_clack.stop()
        play_back.play(sound)
        break


def resetGameStatus():
    """
    resetar dados do jogo anterior
    """
    global score, score_board, flag, pontape_de_saida
    score = {'home': 0, 'away': 0}
    score_board = sprite.GroupSingle(ScoreBoard(380, 79, font.SysFont('Arial', 20, bold=True), (0, 0), Color('white')))
    flag = {'home': True, 'away': False}
    pontape_de_saida = True


def lancarJogadaLoop():
    """
    loop que controla se a jogada esta a decorrer
    :return:
    """
    global sound
    atualizarDisplay()
    display.update()
    som_move.play()
    while emMovimento():
        getEvent(vels_de_jogo[optSpeed])
        all_players.update(bola, all_players)
        bola.update(all_players)
        atualizarDisplay()
        display.update()
        if goal():
            som_rede.play()
            if sound:
                som_golo.play()
                som_celebracao.play()
            time.delay(20)
            equipa = team_goal.capitalize().replace('_', ' ')
            info_golo = sprite.GroupSingle(
                Label(300, 126, font.SysFont('Arial', 40, True), equipa + ' Scored !', Color('white')))
            info_golo.sprites()[0].rect.centerx = 440
            goal_anim = sprite.GroupSingle(Item(0, 0, 'goal.png'))
            timer = MyTimer(4)
            timer.start()
            while not timer.done:
                getEvent(vels_de_jogo[optSpeed])
                all_players.update(bola, all_players)
                bola.update(all_players)
                goal_anim.clear(screen, estadio)
                info_golo.clear(screen, estadio)
                atualizarDisplay()
                goal_anim.draw(screen)
                info_golo.draw(screen)
                display.update()
            screen.blit(estadio, (0, 0))
            return {'golo': True}
        status = pauseControl()
        try:
            if status['quit']:
                return {'golo': False, 'quit': True}
        except:
            pass
    changeFlag()
    disselectAllPlayer()
    resetVel()
    atualizarDisplay()
    display.update()
    return {'golo': False}


def clearAll():
    """
    apagar todos os sprites da tela
    """
    cursor.clear(screen, estadio)
    score_board.clear(screen, estadio)
    placar_labels.clear(screen, estadio)
    selection.clear(screen, estadio)
    all_players.clear(screen, estadio)
    power_bar.clear(screen, estadio)
    bola.clear(screen, estadio)
    baliza_group.clear(screen, estadio)


def drawAll(cur=True):
    """
    desenhar todos os sprites na tela
    :param cur: refere ao cursor
    """
    all_players.draw(screen)
    bola.draw(screen)
    baliza_group.draw(screen)
    score_board.update((score['home'], score['away']))
    score_board.draw(screen)
    placar_labels.draw(screen)

    if cur:
        cursor.update()
        cursor.draw(screen)

    # showLines()


def showPower(vel):
    """
    mostrar a barra de força do remate
    :param vel:
    """
    if vel <= 2:
        power = 1
    elif vel > 25:
        power = 200
    else:
        power = (vel / 25) * 200

    if flag['home']:
        pos_x = (60, 70)
    else:
        pos_x = (530, 540)

    Label(pos_x[0], 545, font.SysFont(None, 25), 'Power : ' + str(power // 2) + '%', Color('white')).draw(screen)

    if 0 < power < 50:
        draw.rect(screen, Color('green'), Rect(pos_x[1], 574, power, 20))
    elif 50 < power < 100:
        draw.rect(screen, Color('yellow'), Rect(pos_x[1], 574, power, 20))
    elif 100 < power < 150:
        draw.rect(screen, Color('orange'), Rect(pos_x[1], 574, power, 20))
    else:
        draw.rect(screen, Color('red'), Rect(pos_x[1], 574, power, 20))

    draw.rect(screen, Color('black'), Rect(pos_x[1], 574, 200, 20), 3)


def jogar():
    """
    controlar a jogada do jogador
    :return:
    """
    global xmouse, ymouse, pontape_de_saida
    if mouseOverPlayer():
        while mouseOverPlayer():
            getEvent(30)
            player_sel = getSelectedPlayer()
            if not player_sel:
                break
            clearAll()
            selection.update(player_sel.getAxis())
            selection.draw(screen)
            drawAll()
            display.update()

            vel = 0
            if mouse.get_pressed()[0]:
                while mouse.get_pressed()[0]:
                    getEvent(30)

                    if mouse.get_pos()[0] > player_sel.getCenter()[0]:
                        xmouse = mouse.get_pos()[0] - player_sel.getCenter()[0]
                    else:
                        xmouse = (player_sel.getCenter()[0] - mouse.get_pos()[0]) * (-1)
                    if mouse.get_pos()[1] > player_sel.getCenter()[1]:
                        ymouse = (mouse.get_pos()[1] - player_sel.getCenter()[1]) * (-1)
                    else:
                        ymouse = player_sel.getCenter()[1] - mouse.get_pos()[1]

                    vel = hypot(xmouse, ymouse) * 0.2
                    seta.rodar(player_sel.getCenterX(), player_sel.getCenterY(), degrees(atan2(ymouse, xmouse)))
                    showPower(vel)
                    clearAll()
                    draw.line(screen, (0, 0, 0), player_sel.getCenter(), mouse.get_pos(), 2)
                    drawAll()
                    seta.draw(screen)
                    display.update()
                    screen.blit(estadio, (0, 0))

                if vel > 2:
                    player_sel.move(xmouse, ymouse)
                    disselectAllPlayer()
                    status = lancarJogadaLoop()
                    try:
                        if status['quit']:
                            return {'golo': False, 'quit': True}
                    except:
                        pass
                    if pontape_de_saida:
                        pontape_de_saida = False
                    return status

            status = pauseControl()
            try:
                if status['quit']:
                    return {'golo': False, 'quit': True}
            except:
                pass

        disselectAllPlayer()
    return {'golo': False}


animthread = MyTaskThread(flagControlSelAnimation, 1.5)


def main():
    """
    programa pricipal
    """
    global run, sound
    loadConfig()
    if sound:
        som_intro.play()
    mouse.set_visible(False)
    # threads init
    animthread.start()
    animthread.pause()
    play_back.start()
    # Main Loop
    while run:
        getEvent(30)
        check_som()
        opt_menu = menuPrincipal()
        if opt_menu == 1:
            singlePlayer()
        elif opt_menu == 2:
            multiPlayer()
        elif opt_menu == 3:
            computerVScomputer()
        elif opt_menu == 4:
            menuOptions()
            saveConfig()
        elif opt_menu == 5:
            credits()
        elif opt_menu == 6:
            menuQuit()
        cursor.update()

    saveConfig()
    animthread.destroy()
    play_back.destroy()
    quit()


if __name__ == '__main__':
    main()
