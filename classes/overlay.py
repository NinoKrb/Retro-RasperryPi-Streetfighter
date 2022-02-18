import pygame, os
from settings import Settings

class Overlay():
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

        self.elements = []
        self.elements.append(Avatar('player_1', self.player_1.avatar_image, Settings.avatar_size, (50,50)))
        self.elements.append(Avatar('player_2', self.player_2.avatar_image, Settings.avatar_size, (Settings.window_width - 50 - Settings.avatar_size[0],50), True))

    def draw(self, screen):
        for element in self.elements:
            element.draw(screen)

class OverlayElement(pygame.sprite.Sprite):
    def __init__(self, filename, size, pos, flip=False):
        super().__init__()
        self.filename = filename
        self.size = size
        self.flip = flip
        self.pos = { 'x': pos[0], 'y': pos[1] }

    def update_sprite(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename))
        self.image = pygame.transform.scale(self.image, self.size)
        if self.flip:
            self.image = pygame.transform.flip(self.image, self.flip, False)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.set_pos(self.pos['x'], self.pos['y'])

    def set_pos(self, x, y):
        self.rect.top = y
        self.rect.left = x

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Avatar(OverlayElement):
    def __init__(self, player_name, filename, size, pos, flip=False):
        super().__init__(filename, size, pos, flip)
        self.update_sprite(player_name, self.filename)

    def update_sprite(self, player_name, filename):
        joined_path = os.path.join('players', player_name, filename)
        print(joined_path)
        print(os.path.join(Settings.path_image, joined_path))
        super().update_sprite(joined_path)