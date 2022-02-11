from operator import ne
import os,sys,pygame

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from settings import Settings
from classes.animation_set import AnimationSet
from classes.animation import Animation
from classes.action import Action

class Player(pygame.sprite.Sprite):
    def __init__(self, id, size, pos, fallback_image, animations, speed, colorkey):
        super().__init__()
        self.id = id
        self.fallback_image = fallback_image
        self.size = size
        self.colorkey = colorkey
        self.speed = speed
        self.pos = { 'x': pos[0], 'y': pos[1] }
        self.direction = None
        self.moving = False
        self.flip = False
        self.animation_set = self.load_animation_set(animations)
        self.action_manager = Action({ 'name': 'idle', 'loop': False })
        self.animation_set.change_current_animation(self.action_manager.current_action['name'])
        self.update_sprite(os.path.join('players', 'player_1', self.fallback_image))

        self.is_jumping = False
        self.jumps_left = 2

    def load_animation_set(self, animations):
        animation_objects = []
        for animation in animations:
            animation_objects.append(Animation(animation, os.path.join('players', 'player_1', 'animations', animation), 100),)

        return AnimationSet('Player', animation_objects)

    def move(self):
        if self.moving:
            if self.direction == 'right':
                self.pos['x'] += self.speed
            elif self.direction == 'left':
                self.pos['x'] -= self.speed

    def start_moving(self):
        self.moving = True

    def stop_moving(self):
        self.moving = False    

    def change_direction(self, direction):
        self.direction = direction

    def set_pos(self, x, y):
        self.rect.top = y
        self.rect.left = x

    def set_coords(self):
        self.pos['x'] = self.rect.left
        self.pos['y'] = self.rect.top

    def update_sprite(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        if self.flip:
            self.image = pygame.transform.flip(self.image, self.flip, False)
        self.image.set_colorkey(self.colorkey)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.set_pos(self.pos['x'], self.pos['y'])

    def update(self, game):
        self.game = game
        self.process_animation()
        self.gravity()
        self.move()

    def gravity(self):
        if self.is_jumping:
            self.jump_velocity += 10
            if self.jump_velocity < 300:
                self.pos['y'] -= 10
            else:
                self.is_jumping = False

        print(self.rect)
        if not pygame.sprite.collide_rect(self, self.game.arena.floor):
            self.pos['y'] += 1
        else:
            self.jumps_left = 2
            self.is_jumping = False
            self.jump_velocity = 0
            self.rect.bottom = self.game.arena.floor.rect.top
            self.set_coords()
            print(self.rect)

    def jump(self):
        if self.jumps_left > 1:
            self.jumps_left -= 1
            self.is_jumping = True
            self.jump_velocity = 0

    def process_animation(self):
        frame = self.animation_set.play_animation()
        if frame:
            frame = os.path.join('players', 'player_1', 'animations', self.animation_set.current_animation['name'], frame)
            self.update_sprite(frame)
            if self.animation_set.current_animation['current_frame'] == 0:
                next_action = self.action_manager.is_next_action_queued()
                if next_action:
                    self.action_manager.change_action(next_action)
                    self.animation_set.change_current_animation(next_action['name'])

                elif self.action_manager.current_action['loop'] == False:
                    self.action_manager.reset_action()
                    self.animation_set.change_current_animation(self.action_manager.current_action['name'])

    def draw(self, screen):
        screen.blit(self.image, self.rect)