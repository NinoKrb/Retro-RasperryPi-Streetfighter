import os,sys,pygame

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from settings import Settings

class Player(pygame.sprite.Sprite):
    def __init__(self, id, animations):
        super().__init__()
        self.id = id
        self.animations = animations

    def update_sprite(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_background, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)