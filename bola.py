from player import *
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

som_bola_parede = mixer.Sound('data/sons/chute_fraco.ogg')


class Bola(sprite.Sprite):

    def __init__(self, x, y, bola_img):
        sprite.Sprite.__init__(self)
        self.imgPath = 'data/balls/' + bola_img + '.png'
        self.image = image.load(self.imgPath)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.radius = self.rect.w / 2
        self.mask = mask.from_surface(self.image)
        self.vel = 0
        self.angulo = 0
        self.ang_rot = 0
        self.status = {'golo': False, 'b_left': False, 'b_right': False}

    def update(self, all_players):
        self.autoMove(all_players)
        self.atrito()
        if self.vel > 1:
            self.rodar()

    def autoMove(self, all_players):
        inc_x = self.vel * cos(self.angulo)
        inc_y = self.vel * sin(self.angulo)

        if -1 < inc_x < 1 and -1 < inc_y < 1:
            self.controlLineColision()
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
            if self.collide_player(all_players):
                break

    def collide_player(self, all_players):
        for player in all_players:
            if sprite.collide_mask(self, player):
                return True

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

    def setImage(self, num):
        self.image = image.load('data/balls/bola' + str(num) + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask = mask.from_surface(self.image)

    def rodar(self):
        # self.image = image.load(self.imgPath)
        if self.ang_rot > 360:
            self.ang_rot = 0
        else:
            if 5 < self.vel < 50:
                self.ang_rot += 90
            elif 3 < self.vel < 5:
                self.ang_rot += 45
            else:
                self.ang_rot += 30
        if self.ang_rot % 90 == 0:
            self.image = transform.rotate(self.image, self.ang_rot)

    def controlLineColision(self):
        const = 0.8
        if sprite.collide_mask(self, ballZoneEsq):
            self.status['golo'], self.status['b_left'] = True, True

        elif sprite.collide_mask(self, ballZoneDir):
            self.status['golo'], self.status['b_right'] = True, True

        if sprite.collide_mask(self, lateralCima) or sprite.collide_mask(self, lateralCimaBalizaDir) \
                or sprite.collide_mask(self, lateralCimaBalizaEsq):
            self.rect.y += 3
            self.angulo *= -1
            self.vel *= const
            som_bola_parede.play()
        elif sprite.collide_mask(self, lateralBaixo) or sprite.collide_mask(self, lateralBaixoBalizaDir) \
                or sprite.collide_mask(self, lateralBaixoBalizaEsq):
            self.rect.y -= 3
            self.angulo *= -1
            self.vel *= const
            som_bola_parede.play()

        if sprite.collide_mask(self, fundoCimaEsq) or sprite.collide_mask(self, fundoBaixoEsq) \
                or sprite.collide_mask(self, fundoBalizaEsq):
            if sprite.collide_mask(self, fundoBalizaEsq):
                self.vel *= 0.2
            self.rect.x += 3
            self.angulo = pi - self.angulo
            self.vel *= const
            som_bola_parede.play()

        elif sprite.collide_mask(self, fundoCimaDir) or sprite.collide_mask(self, fundoBaixoDir) \
                or sprite.collide_mask(self, fundoBalizaDir):
            if sprite.collide_mask(self, fundoBalizaDir):
                self.vel *= 0.2
            self.rect.x -= 3
            self.angulo = pi - self.angulo
            self.vel *= const
            som_bola_parede.play()

    def move(self, xcont, ycont):
        vel = hypot(xcont, ycont) * 0.2  # 0.15
        # print(vel)
        if vel > 50:
            self.vel = 50
        else:
            self.vel = vel
        self.angulo = atan2(ycont, xcont) - pi

    def resetStatus(self):
        self.status = {'golo': False, 'b_left': False, 'b_right': False}

    def atrito(self):
        self.vel *= 0.98

    def getAxis(self):
        return self.rect.x, self.rect.y

    def setAxis(self, axis):
        self.rect.x = axis[0]
        self.rect.y = axis[1]

    def setX(self, x):
        self.rect.x = x

    def setY(self, y):
        self.rect.y = y

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

    def getH(self):
        return self.rect.h

    def getCenterX(self):
        return self.rect.centerx

    def getCenterY(self):
        return self.rect.centery

    def getW(self):
        return self.rect.w

    def setVelocity(self, vel):
        self.vel = vel

    def setAngulo(self, vel):
        self.angulo = vel

    def setTop(self, top):
        self.rect.top = top

    def setBottom(self, bottom):
        self.rect.bottom = bottom

    def setRigth(self, right):
        self.rect.right = right

    def setLeft(self, left):
        self.rect.left = left

    def getCenter(self):
        return self.rect.center

    def draw(self, surface):
        surface.blit(self.image, self.getAxis())
