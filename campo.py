from pygame import *


class Campo:
    def __init__(self):
        self.rect = Rect(60, 118, 678, 431)

    def getAxis(self):
        return self.rect.x, self.rect.y

    def getCenter(self):
        return self.rect.center

    def draw(self, surface):
        # surface.blit(self.rect, self.getAxis())
        draw.rect(surface, (255, 255, 0), self.rect)


class Linhas(sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        sprite.Sprite.__init__(self)
        self.color = color
        self.image = Surface([w, h])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        self.mask.fill()

    def getAxis(self):
        return self.rect.x, self.rect.y

    def draw(self, surface):
        surface.blit(self.image, self.getAxis())

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

    def getH(self):
        return self.rect.h

    def getW(self):
        return self.rect.w
