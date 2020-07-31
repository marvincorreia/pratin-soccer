from pygame import *


class SelecaoPlayer(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = image.load('data/items/selecao_player.png')
        self.rect = self.image.get_rect()

    def setAxis(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, axis):
        self.setAxis(axis[0] - 4, axis[1] - 2)


class TextMenu(sprite.Sprite):
    def __init__(self, imagem):
        sprite.Sprite.__init__(self)
        self.image = image.load('data/items/' + imagem)
        self.rect = self.image.get_rect()
        self.rect.x = 437
        self.rect.y = 4


class SelectorMenu(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load('data/items/selectormenu.png')
        self.rect = self.image.get_rect()
        # self.rect.x = 452
        self.rect.x = x
        self.rect.y = y

    def update(self, y):
        self.rect.y = y


class Item(sprite.Sprite):
    def __init__(self, x, y, imagem):
        sprite.Sprite.__init__(self)
        self.image = image.load('data/items/' + imagem)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def setX(self, x):
        self.rect.x = x

    def axis(self):
        return self.rect.x, self.rect.y

    def setY(self, y):
        self.rect.y = y

    def setXY(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def setAxis(self, axis):
        self.rect.x = axis[0]
        self.rect.y = axis[1]

    def update(self, x, y):
        self.setX(x)
        self.setY(y)

    def draw(self, surface):
        surface.blit(self.image, self.axis())


class MouseCursor(sprite.Sprite):

    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = image.load('data/cursors/mouse_cursor.png')
        self.rect = self.image.get_rect()

    def update(self, *args):
        ms = mouse.get_pos()
        self.rect.x = ms[0] - 12
        self.rect.y = ms[1] - 5


class SetaDirecao:

    def __init__(self):
        self.imgPath = 'data/items/seta_de_rodagem.png'
        self.image = image.load(self.imgPath)
        self.rect = self.image.get_rect()

    def centrar(self, centerx, centery):
        self.rect.centerx = centerx
        self.rect.centery = centery

    def getXY(self):
        return self.rect.x, self.rect.y

    def rodar(self, x, y, angle):
        self.image = image.load(self.imgPath)
        self.centrar(x, y)
        self.image = transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.centrar(x, y)

    def draw(self, surface):
        surface.blit(self.image, self.getXY())


class Botao(sprite.Sprite):

    def __init__(self, x, y, fonte, text, fcolors, bgcolors):
        sprite.Sprite.__init__(self)
        self.fonte = fonte
        self.text = text
        self.fcolors = fcolors
        self.bgcolors = bgcolors
        self.isSelected = False
        self.rect = Rect(x, y, fonte.size(text)[0] + 20, fonte.size(text)[1] + 10)
        self.image = self.fonte.render(self.text, 1, self.fcolors['dissel'])

    def update(self, *args):
        if self.rect.collidepoint(mouse.get_pos()[0], mouse.get_pos()[1]):
            self.isSelected = True
        else:
            self.isSelected = False

        print(self.isSelected)

    def draw(self, surface):
        if self.isSelected:
            draw.rect(surface, self.bgcolors['sel'], self.rect)
            self.image = self.fonte.render(self.text, 12, self.fcolors['sel'])
        else:
            draw.rect(surface, self.bgcolors['dissel'], self.rect)
            self.image = self.fonte.render(self.text, 12, self.fcolors['dissel'])

        surface.blit(self.image, (self.rect.x + 10, self.rect.y + 5))

    def setX(self, x):
        self.rect.x = x

    def setY(self, y):
        self.rect.y = y

    def setXY(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Label(sprite.Sprite):
    def __init__(self, x, y, fonte, text, f_color, bg_color=None):
        sprite.Sprite.__init__(self)
        self.fonte = fonte
        self.f_color = f_color
        self.bg_color = bg_color
        self.text = text
        self.rect = Rect(x, y, fonte.size(text)[0] + 30, fonte.size(text)[1] + 20)
        self.image = self.fonte.render(self.text, 1, self.f_color, self.bg_color)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x + 15, self.rect.y + 10))


class ScoreBoard(sprite.Sprite):
    def __init__(self, x, y, fonte, score, f_color, bg_color=None):
        sprite.Sprite.__init__(self)
        self.fonte = fonte
        self.x = x
        self.y = y
        self.f_color = f_color
        self.bg_color = bg_color
        self.text = str(score[0]) + ' - ' + str(score[1])
        self.rect = Rect(self.x, self.y, self.fonte.size(self.text)[0] + 30, self.fonte.size(self.text)[1] + 20)
        self.image = self.fonte.render(self.text, 1, self.f_color, self.bg_color)

    def update(self, score):
        self.text = str(score[0]) + ' - ' + str(score[1])
        self.rect = Rect(self.x, self.y, self.fonte.size(self.text)[0] + 30, self.fonte.size(self.text)[1] + 20)
        self.image = self.fonte.render(self.text, 1, self.f_color, self.bg_color)
