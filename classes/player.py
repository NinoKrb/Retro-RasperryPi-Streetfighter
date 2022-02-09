import os,sys,pygame

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from settings import Settings
from classes.animation_set import AnimationSet
from classes.animation import Animation
from classes.action import Action

class Player(pygame.sprite.Sprite):
    def __init__(self, id, size, fallback_image, animations):
        super().__init__()
        self.id = id
        self.fallback_image = fallback_image
        self.size = size
        self.animation_set = self.load_animation_set(animations)
        self.action_manager = Action({ 'name': 'idle', 'loop': True })
        self.animation_set.change_current_animation(self.action_manager.current_action['name'])
        self.update_sprite(os.path.join('players', 'player_1', self.fallback_image))

    def load_animation_set(self, animations):
        animation_objects = []
        for animation in animations:
            animation_objects.append(Animation(animation, os.path.join('players', 'player_1', 'animations', animation)),)

        return AnimationSet('Player', animation_objects)

    def update_sprite(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        frame = self.animation_set.play_animation()
        frame = os.path.join('players', 'player_1', 'animations', self.animation_set.current_animation['name'], frame)
        if frame:
            self.update_sprite(frame)

    def draw(self, screen):
        screen.blit(self.image, self.rect)