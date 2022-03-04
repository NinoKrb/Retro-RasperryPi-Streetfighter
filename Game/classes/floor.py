import os,sys,pygame

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from settings import Settings

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos, size=[50,50]):
        super().__init__()
        self.pos = pos
        self.size = size
        self.update_surface(self.size)
        self.set_pos(*self.pos)

    def update_surface(self, size):
        #self.image = pygame.Surface(size, pygame.SRCALPHA, 32) #32
        self.image = pygame.Surface(size)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.top = y
        self.rect.left = x

    def draw(self, screen):
        screen.blit(self.image, self.rect)
