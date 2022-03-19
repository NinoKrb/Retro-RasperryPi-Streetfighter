import pygame, os
from settings import Settings

class Overlay():
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

        self.header_text = Text(os.path.join(Settings.path_font, 'pixelart.ttf'), 50, 'Streetfighter', (255,255,255), 50, Settings.window_width // 2)

        self.elements = []
        self.elements.append(Avatar('player_1', self.player_1.avatar_image, Settings.avatar_size, (50,50)))
        self.elements.append(Avatar('player_2', self.player_2.avatar_image, Settings.avatar_size, (Settings.window_width - 50 - Settings.avatar_size[0],50)))

        self.elements.append(self.header_text)

        self.healthbar_player_1 = Healthbar(self, self.player_1, self.player_1.health, self.player_1.max_health, (50 + Settings.avatar_size[0], 50))
        self.healthbar_player_2 = Healthbar(self, self.player_2, self.player_2.health, self.player_2.max_health, (Settings.window_width - 50 - Settings.avatar_size[0], 50), 'right')

    def draw(self, screen):
        for element in self.elements:
            element.draw(screen)
        
        self.healthbar_player_1.draw(screen)
        self.healthbar_player_2.draw(screen)

    def update_healthbars(self, player_1, player_2):
        self.healthbar_player_1.update_bar(player_1.health)
        self.healthbar_player_2.update_bar(player_2.health)

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
        super().update_sprite(joined_path)

class Healthbar(pygame.sprite.Sprite):
    def __init__(self, overlay, player, health, max, pos, direction='left'):
        self.player = player
        self.health = health
        self.max = max
        self.pos = pos
        self.direction = direction
        self.overlay = overlay
        self.build_surface(self.health, self.max, self.pos, self.direction)

    def build_surface(self, health, max, pos, direction):
        health_surface = pygame.Surface((health // Settings.healthbar_width_factor, Settings.healthbar_height))
        health_surface.fill(Settings.healthbar_health_color)
        self.health_surface = { "surface": health_surface, "rect": health_surface.get_rect() }
        self.set_pos(self.health_surface['rect'], *pos, direction)
        
        max_surface = pygame.Surface((max // Settings.healthbar_width_factor, Settings.healthbar_height))
        max_surface.fill(Settings.healthbar_blank_color)
        self.max_surface = { "surface": max_surface, "rect": max_surface.get_rect() }
        self.set_pos(self.max_surface['rect'], *pos, direction)

    def update_bar(self, health):
        try:
            self.health_surface['surface'] = pygame.transform.scale(self.health_surface['surface'], (health // Settings.healthbar_width_factor, self.health_surface['rect'].height))
        except:
            self.overlay.header_text.update('Game Over', (255,255,255), 50, Settings.window_width // 2)

    def draw(self, screen):
        screen.blit(self.max_surface['surface'], self.max_surface['rect'])
        screen.blit(self.health_surface['surface'], self.health_surface['rect'])

    def set_pos(self, rect, x, y, direction='left'):
        rect.top = y
        if direction == 'left':
            rect.left = x
        else:
            rect.right = x

class Text(pygame.sprite.Sprite):
    def __init__(self, font, size, text, color, y_offset, x_offset, is_visible=True):
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.top = y_offset
        self.rect.centerx = x_offset

        self.is_visible = is_visible

    def update(self, text, color, y_offset=False, x_offset=False):
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        if y_offset:
            self.rect.top = y_offset

        if x_offset:
            self.rect.centerx = x_offset

    def draw(self, screen):
        if self.is_visible:
            screen.blit(self.image, self.rect)