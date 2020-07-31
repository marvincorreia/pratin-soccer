from random import choice
from pygame import *
from math import *
from campo import Linhas

mixer.init()

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

som_remate = mixer.Sound('data/sons/chute_forte.ogg')
som_passe = mixer.Sound('data/sons/chute_fraco.ogg')
som_contact = mixer.Sound('data/sons/contact.ogg')
som_mover = mixer.Sound('data/sons/move.ogg')


class Player(sprite.Sprite):
    def __init__(self, x, y, equipa, gk=False, smart=False):
        sprite.Sprite.__init__(self)
        self.isSelected = False
        self.equipa = equipa
        self.imgSel = image.load('data/items/selecaoplayer.png')
        self.imgPath = 'data/players/' + equipa + '.png'
        self.image = image.load(self.imgPath)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.radius = self.rect.w / 2
        self.mask = mask.from_surface(self.image)
        self.vel = 0
        self.angulo = 0
        self.gk = gk
        self.ang_rot = 0
        self.rodavel = False
        self.smart = smart

    def update(self, bola, all_players):
        self.autoMove(bola, all_players)
        self.atrito()
        self.rodar()

    def tratarColisao(self, obj):
        if self.getCenter()[0] > obj.getCenter()[0]:
            x = self.getCenter()[0] - obj.getCenter()[0]
        else:
            x = (obj.getCenter()[0] - self.getCenter()[0]) * (-1)
        if self.getCenter()[1] > obj.getCenter()[1]:
            y = (self.getCenter()[1] - obj.getCenter()[1]) * (-1)
        else:
            y = obj.getCenter()[1] - self.getCenter()[1]

        return x, y

    def controlBallColision(self, bola, all_players):
        if sprite.collide_mask(self, bola.sprites()[0]):
            x, y = self.tratarColisao(bola.sprites()[0])
            if self.vel > bola.sprites()[0].vel:
                bola.sprites()[0].move(x, y)
                bola.sprites()[0].setVelocity(self.vel + 1.2)
                bola.update(all_players)
            else:
                self.angulo = bola.sprites()[0].angulo
                if bola.sprites()[0].vel < 2:
                    self.setVelocity(bola.sprites()[0].vel * 0.1 + 1.5)
                else:
                    self.setVelocity(bola.sprites()[0].vel * 0.1 + 1)

                lastBallvel = bola.sprites()[0].vel
                bola.sprites()[0].move(x, y)
                if not self.smart:
                    bola.sprites()[0].vel = lastBallvel - lastBallvel * 0.6
                    bola.sprites()[0].setAngulo(bola.sprites()[0].angulo + radians(choice(range(-10, 10))))
                else:
                    bola.sprites()[0].vel = lastBallvel - lastBallvel * 0.6 + 20
                    bola.sprites()[0].setAngulo(bola.sprites()[0].angulo + radians(choice(range(-10, 10))))
                bola.update(all_players)

            if bola.sprites()[0].vel > 15:
                som_remate.play()
            else:
                som_passe.play()

            for i in range(100):
                if sprite.collide_mask(self, bola.sprites()[0]):
                    bola.sprites()[0].vel += 1
                    bola.update(all_players)
                else:
                    break

    def controlLineColision(self):
        const = 0.6

        if sprite.collide_mask(self, lateralCima) or sprite.collide_mask(self, lateralCimaBalizaDir) \
                or sprite.collide_mask(self, lateralCimaBalizaEsq):
            self.rect.y += 3
            self.angulo *= -1
            self.vel *= const
            self.rodavel = True
            som_contact.play()
        elif sprite.collide_mask(self, lateralBaixo) or sprite.collide_mask(self, lateralBaixoBalizaDir) \
                or sprite.collide_mask(self, lateralBaixoBalizaEsq):
            self.rect.y -= 3
            self.angulo *= -1
            self.vel *= const
            self.rodavel = True
            som_contact.play()

        if sprite.collide_mask(self, fundoCimaEsq) or sprite.collide_mask(self, fundoBaixoEsq) \
                or sprite.collide_mask(self, fundoBalizaEsq):
            self.rect.x += 3
            self.angulo = pi - self.angulo
            self.vel *= const
            self.rodavel = True
            som_contact.play()

        elif sprite.collide_mask(self, fundoCimaDir) or sprite.collide_mask(self, fundoBaixoDir) \
                or sprite.collide_mask(self, fundoBalizaDir):
            self.rect.x -= 3
            self.angulo = pi - self.angulo
            self.vel *= const
            self.rodavel = True
            som_contact.play()

    def control_collide_player(self, bola, all_players):
        for player in all_players:
            if player == self:
                continue
            if sprite.collide_mask(self, player):
                som_contact.play()
                x, y = self.tratarColisao(player)
                player.rodavel = True
                if self.vel > player.vel:
                    player.move(x, y)
                    player.setVelocity(self.vel * 0.8)
                    self.vel *= 0.5
                    player.update(bola, all_players)
                    self.update(bola, all_players)

            while sprite.collide_mask(self, player):
                player.vel += 1
                player.autoMove(bola, all_players)

    def move(self, xcont, ycont):
        vel = hypot(xcont, ycont) * 0.2  # 0.15
        if vel > 25:
            self.vel = 25
        else:
            self.vel = vel
        self.angulo = atan2(ycont, xcont) - pi
        # print(self.vel)

    def autoMove(self, bola, all_players):
        inc_x = self.vel * cos(self.angulo)
        inc_y = self.vel * sin(self.angulo)

        if -1 < inc_x < 1 and -1 < inc_y < 1:
            self.controlBallColision(bola, all_players)
            self.controlLineColision()
            # self.setVelocity(0)
            return

        if cos(self.angulo) >= 0:
            xrange_max = self.rect.x + self.vel * cos(self.angulo)
            xrange_min = self.rect.x - self.vel * cos(self.angulo)
        else:
            xrange_max = self.rect.x - self.vel * cos(self.angulo)
            xrange_min = self.rect.x + self.vel * cos(self.angulo)
        if sin(self.angulo) >= 0:
            yrange_max = self.rect.y + self.vel * sin(self.angulo)
            yrange_min = self.rect.y - self.vel * sin(self.angulo)
        else:
            yrange_max = self.rect.y - self.vel * sin(self.angulo)
            yrange_min = self.rect.y + self.vel * sin(self.angulo)

        while (xrange_min < self.rect.x < xrange_max) or (yrange_min < self.rect.y < yrange_max):
            inc_x = self.vel * cos(self.angulo)
            inc_y = self.vel * sin(self.angulo)
            if -1 < inc_x < 1 and -1 < inc_y < 1:
                break
            if xrange_min < self.rect.x < xrange_max:
                self.incrementX(inc_x)
            if yrange_min < self.rect.y < yrange_max:
                self.incrementY(inc_y)
            self.controlLineColision()
            self.control_collide_player(bola, all_players)
            self.controlBallColision(bola, all_players)

    def autoMoveTest(self, bola, all_players, pl_ref, screen):
        colisions = {'player': False, 'bola': False}
        if self.vel < 10:
            self.vel += 20
        if cos(self.angulo) >= 0:
            xrange_max = self.rect.x + self.vel * cos(self.angulo)
            xrange_min = self.rect.x - self.vel * cos(self.angulo)
        else:
            xrange_max = self.rect.x - self.vel * cos(self.angulo)
            xrange_min = self.rect.x + self.vel * cos(self.angulo)
        if sin(self.angulo) >= 0:
            yrange_max = self.rect.y + self.vel * sin(self.angulo)
            yrange_min = self.rect.y - self.vel * sin(self.angulo)
        else:
            yrange_max = self.rect.y - self.vel * sin(self.angulo)
            yrange_min = self.rect.y + self.vel * sin(self.angulo)

        while (xrange_min < self.rect.x < xrange_max) or (yrange_min < self.rect.y < yrange_max):
            # Demostracao de IA
            '''§time.delay(2)
            for ev in event.get():
                pass
            self.draw(screen)
            display.update()'''

            inc_x = self.vel * cos(self.angulo)
            inc_y = self.vel * sin(self.angulo)
            if xrange_min < self.rect.x < xrange_max:
                self.incrementX(inc_x)
            if yrange_min < self.rect.y < yrange_max:
                self.incrementY(inc_y)
            for player in all_players:
                if player == pl_ref:
                    continue
                if sprite.collide_mask(self, player):
                    colisions['player'] = True
            if sprite.collide_mask(self, bola.sprites()[0]):
                colisions['bola'] = True

        self.vel *= 0.9
        return colisions

    def atrito(self):
        self.vel *= 0.96

    def incrementX(self, inc_x):
        if inc_x > 0:
            self.rect.x += 1
        elif inc_x < 0:
            self.rect.x += -1

    def incrementY(self, inc_y):
        if inc_y > 0:
            self.rect.y += -1
        elif inc_y < 0:
            self.rect.y += 1

    def incrementXY(self, inc_x, inc_y):
        self.incrementX(inc_x)
        self.incrementY(inc_y)

    def rodar(self):
        self.ang_rot = 90
        if self.rodavel and self.vel > 4:
            self.image = transform.rotate(self.image, self.ang_rot)
        else:
            self.rodavel = False

    # def rodar(self):
    #     # self.image = image.load(self.imgPath)
    #     if self.rodavel and self.vel > 1:
    #         if self.ang_rot >= 360:
    #             self.ang_rot = 0
    #         else:
    #             if 5 < self.vel < 50:
    #                 self.ang_rot += 90
    #             elif 2 < self.vel < 5:
    #                 self.ang_rot += 45
    #             else:
    #                 self.ang_rot += 30
    #         if self.ang_rot % 90 == 0:
    #             self.image = transform.rotate(self.image, self.ang_rot)
    #     else:
    #         self.rodavel = False

    def getAxis(self):
        return self.rect.x, self.rect.y

    def setAxis(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def setX(self, x):
        self.rect.x = x

    def setY(self, y):
        self.rect.y = y

    def setTop(self, top):
        self.rect.top = top

    def setBottom(self, bottom):
        self.rect.bottom = bottom

    def setRigth(self, right):
        self.rect.right = right

    def setLeft(self, left):
        self.rect.left = left

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

    def getH(self):
        return self.rect.h

    def getW(self):
        return self.rect.w

    def setVelocity(self, vel):
        self.vel = vel

    def getCenterY(self):
        return self.rect.centery

    def getCenterX(self):
        return self.rect.centerx

    def setAngulo(self, vel):
        self.angulo = vel

    def getCenter(self):
        return self.rect.center

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def drawSelection(self, surface):
        if self.isSelected:
            surface.blit(self.imgSel, (self.rect.x - 2, self.rect.y - 2))
