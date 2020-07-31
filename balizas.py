from pygame import *
from campo import Campo

campo = Campo()


class BalizaLeft(sprite.Sprite):

    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = image.load('data/balizas/balizaleft.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 266

    def getAxis(self):
        return self.rect.x, self.rect.y

    def draw(self, surface):
        surface.blit(self.image, self.getAxis())

    def drawRect(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)

    def update(self, *args):
        pass


class BalizaRight(BalizaLeft):

    def __init__(self):
        super().__init__()
        self.image = image.load('data/balizas/balizaright.png')
        self.rect = self.image.get_rect()
        self.rect.x = 725
        self.rect.y = 265
